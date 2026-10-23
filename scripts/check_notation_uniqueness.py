#!/usr/bin/env python3
"""
Check uniqueness of WMDR code-table notations.

Checks:
1. Every CSV code table under tables_en that has a "notation" column:
   notation values must be unique within the file.
2. Every published WMDR register listed in tables_en/wmdr-tables.csv:
   notation values must be unique within the register.
3. Observed-variable notations must be unique across tables 1-01-01..1-01-05.
4. Observing-method notations must be unique across tables
   5-02-01, 5-02-03 and 5-02-05.

The script exits with status 1 if a duplicate, missing notation, malformed mapped
table, or registry retrieval/parsing error is found. It has no third-party
dependencies.

Examples:
    python scripts/check_notation_uniqueness.py
    python scripts/check_notation_uniqueness.py --tables-dir tables_en
    python scripts/check_notation_uniqueness.py --skip-registry
    python scripts/check_notation_uniqueness.py --verbose
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_TABLES_DIR = Path("tables_en")
MAPPING_FILENAME = "wmdr-tables.csv"

CROSS_TABLE_GROUPS: dict[str, tuple[str, ...]] = {
    "observed variables": (
        "1-01-01",
        "1-01-02",
        "1-01-03",
        "1-01-04",
        "1-01-05",
    ),
    "observing methods": (
        "5-02-01",
        "5-02-03",
        "5-02-05",
    ),
}

USER_AGENT = "wmds-notation-quality-gate/1.0 (+https://github.com/wmo-im/wmds)"


@dataclass(frozen=True)
class Occurrence:
    table_id: str
    source_name: str
    row_number: int
    notation: str


@dataclass(frozen=True)
class Register:
    table_id: str
    title: str
    url: str


@dataclass
class SourceResult:
    table_id: str
    source_name: str
    occurrences: list[Occurrence]
    errors: list[str]

    @property
    def notations(self) -> list[str]:
        return [item.notation for item in self.occurrences]


def normalize_notation(value: str) -> str:
    """Normalize only insignificant CSV/Unicode representation differences.

    Notation comparison remains case-sensitive because WMDR notation forms URI
    path components and URI paths are case-sensitive.
    """
    return unicodedata.normalize("NFC", value.strip())


def read_csv_occurrences(
    text: str,
    *,
    table_id: str,
    source_name: str,
    require_notation_column: bool,
) -> SourceResult | None:
    """Parse a CSV document and return notation occurrences.

    Returns None when a non-code-table CSV has no notation column and
    require_notation_column is False.
    """
    errors: list[str] = []
    stream = io.StringIO(text.lstrip("\ufeff"))
    reader = csv.reader(stream)

    try:
        header = next(reader)
    except StopIteration:
        if require_notation_column:
            return SourceResult(
                table_id=table_id,
                source_name=source_name,
                occurrences=[],
                errors=[f"{source_name}: empty CSV"],
            )
        return None

    normalized_headers = [cell.strip().lower() for cell in header]
    if "notation" not in normalized_headers:
        if require_notation_column:
            return SourceResult(
                table_id=table_id,
                source_name=source_name,
                occurrences=[],
                errors=[f"{source_name}: required 'notation' column is missing"],
            )
        return None

    notation_index = normalized_headers.index("notation")
    occurrences: list[Occurrence] = []

    for row_number, row in enumerate(reader, start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if notation_index >= len(row):
            errors.append(
                f"{source_name}:{row_number}: row has no value in the notation column"
            )
            continue

        notation = normalize_notation(row[notation_index])
        if not notation:
            errors.append(f"{source_name}:{row_number}: notation is empty")
            continue

        occurrences.append(
            Occurrence(
                table_id=table_id,
                source_name=source_name,
                row_number=row_number,
                notation=notation,
            )
        )

    return SourceResult(
        table_id=table_id,
        source_name=source_name,
        occurrences=occurrences,
        errors=errors,
    )


def duplicate_occurrences(
    occurrences: Iterable[Occurrence],
) -> dict[str, list[Occurrence]]:
    grouped: dict[str, list[Occurrence]] = defaultdict(list)
    for occurrence in occurrences:
        grouped[occurrence.notation].append(occurrence)
    return {
        notation: items
        for notation, items in grouped.items()
        if len(items) > 1
    }


def load_register_mapping(tables_dir: Path) -> list[Register]:
    """Load table-id -> WMDR register mappings from wmdr-tables.csv.

    That repository file intentionally has no header and contains:
        table-id, title, register-url
    """
    path = tables_dir / MAPPING_FILENAME
    if not path.is_file():
        raise FileNotFoundError(f"mapping file not found: {path}")

    registers: list[Register] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        for row_number, row in enumerate(reader, start=1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) < 3:
                raise ValueError(
                    f"{path}:{row_number}: expected at least 3 columns "
                    "(table id, title, register URL)"
                )
            table_id, title, url = (cell.strip() for cell in row[:3])
            if not table_id or not url:
                raise ValueError(
                    f"{path}:{row_number}: table id and register URL are required"
                )
            registers.append(Register(table_id=table_id, title=title, url=url))
    return registers


def check_local_tables(
    tables_dir: Path,
    registers: Sequence[Register],
) -> tuple[dict[str, SourceResult], list[str], int]:
    """Check all local CSV code tables and mapped table integrity."""
    results: dict[str, SourceResult] = {}
    errors: list[str] = []
    skipped = 0

    mapped_ids = {register.table_id for register in registers}

    # First ensure every mapped register has a corresponding local code-table CSV.
    for table_id in sorted(mapped_ids):
        path = tables_dir / f"{table_id}.csv"
        if not path.is_file():
            errors.append(
                f"{path}: mapped in {MAPPING_FILENAME} but local CSV is missing"
            )

    # Then inspect every CSV. Administrative CSV files without notation are skipped.
    for path in sorted(tables_dir.glob("*.csv")):
        if path.name == MAPPING_FILENAME:
            skipped += 1
            continue

        table_id = path.stem
        require_notation = table_id in mapped_ids
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            errors.append(f"{path}: cannot read file: {exc}")
            continue

        result = read_csv_occurrences(
            text,
            table_id=table_id,
            source_name=str(path),
            require_notation_column=require_notation,
        )
        if result is None:
            skipped += 1
            continue

        results[table_id] = result
        errors.extend(result.errors)

    return results, errors, skipped


def registry_csv_url(register_url: str) -> str:
    """Return the registry's plain CSV endpoint for valid entries."""
    parsed = urllib.parse.urlsplit(register_url)
    scheme = "https" if parsed.scheme in {"http", "https"} else parsed.scheme
    query = urllib.parse.urlencode({"_format": "csv", "status": "valid"})
    return urllib.parse.urlunsplit(
        (scheme, parsed.netloc, parsed.path.rstrip("/"), query, "")
    )


def fetch_text(url: str, *, timeout: float, retries: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "text/csv",
            "User-Agent": USER_AGENT,
        },
    )
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, errors="strict")
        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
            UnicodeError,
        ) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.5 * (2**attempt))

    assert last_error is not None
    raise last_error


def fetch_registry(
    register: Register,
    *,
    timeout: float,
    retries: int,
) -> SourceResult:
    url = registry_csv_url(register.url)
    source_name = f"registry:{register.table_id} ({url})"

    try:
        text = fetch_text(url, timeout=timeout, retries=retries)
    except Exception as exc:  # network boundary: report cleanly to CI
        return SourceResult(
            table_id=register.table_id,
            source_name=source_name,
            occurrences=[],
            errors=[f"{source_name}: retrieval failed: {exc}"],
        )

    result = read_csv_occurrences(
        text,
        table_id=register.table_id,
        source_name=source_name,
        require_notation_column=True,
    )
    assert result is not None
    return result


def check_registry_tables(
    registers: Sequence[Register],
    *,
    timeout: float,
    retries: int,
    workers: int,
) -> tuple[dict[str, SourceResult], list[str]]:
    results: dict[str, SourceResult] = {}
    errors: list[str] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_register = {
            executor.submit(
                fetch_registry,
                register,
                timeout=timeout,
                retries=retries,
            ): register
            for register in registers
        }

        for future in as_completed(future_to_register):
            register = future_to_register[future]
            result = future.result()
            results[register.table_id] = result
            errors.extend(result.errors)

    return results, errors


def collect_within_table_duplicates(
    results: dict[str, SourceResult],
) -> list[tuple[str, str, list[Occurrence]]]:
    findings: list[tuple[str, str, list[Occurrence]]] = []
    for table_id in sorted(results):
        result = results[table_id]
        for notation, occurrences in sorted(
            duplicate_occurrences(result.occurrences).items()
        ):
            findings.append((table_id, notation, occurrences))
    return findings


def collect_cross_table_duplicates(
    results: dict[str, SourceResult],
) -> tuple[list[tuple[str, str, list[Occurrence]]], list[str]]:
    findings: list[tuple[str, str, list[Occurrence]]] = []
    errors: list[str] = []

    for group_name, table_ids in CROSS_TABLE_GROUPS.items():
        missing = [table_id for table_id in table_ids if table_id not in results]
        if missing:
            errors.append(
                f"cross-table group '{group_name}' cannot be checked; "
                f"missing table(s): {', '.join(missing)}"
            )
            continue

        grouped: dict[str, list[Occurrence]] = defaultdict(list)
        for table_id in table_ids:
            for occurrence in results[table_id].occurrences:
                grouped[occurrence.notation].append(occurrence)

        for notation, occurrences in sorted(grouped.items()):
            distinct_tables = {item.table_id for item in occurrences}
            if len(distinct_tables) > 1:
                findings.append((group_name, notation, occurrences))

    return findings, errors


def print_source_summary(
    label: str,
    results: dict[str, SourceResult],
    *,
    verbose: bool,
) -> None:
    notation_count = sum(len(result.occurrences) for result in results.values())
    print(f"{label}: {len(results)} table(s), {notation_count} notation(s)")
    if verbose:
        for table_id in sorted(results):
            result = results[table_id]
            print(f"  {table_id}: {len(result.occurrences)} notation(s)")


def print_within_findings(
    label: str,
    findings: Sequence[tuple[str, str, list[Occurrence]]],
) -> None:
    if not findings:
        print(f"{label}: OK - all notations are unique within each table")
        return

    print(f"{label}: FAIL - duplicate notation(s) within table(s)")
    for table_id, notation, occurrences in findings:
        locations = ", ".join(
            f"{item.source_name}:{item.row_number}" for item in occurrences
        )
        print(f"  [{table_id}] {notation!r}: {locations}")


def print_cross_findings(
    label: str,
    findings: Sequence[tuple[str, str, list[Occurrence]]],
) -> None:
    if not findings:
        print(
            f"{label}: OK - observed-variable and observing-method "
            "notations are unique across their related tables"
        )
        return

    print(f"{label}: FAIL - duplicate notation(s) across related tables")
    for group_name, notation, occurrences in findings:
        tables = sorted({item.table_id for item in occurrences})
        details = ", ".join(
            f"{item.table_id}@row{item.row_number}" for item in occurrences
        )
        print(
            f"  [{group_name}] {notation!r} occurs in "
            f"{', '.join(tables)} ({details})"
        )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check WMDR code-table notation uniqueness."
    )
    parser.add_argument(
        "--tables-dir",
        type=Path,
        default=DEFAULT_TABLES_DIR,
        help=f"directory containing WMDS CSV tables (default: {DEFAULT_TABLES_DIR})",
    )
    parser.add_argument(
        "--skip-registry",
        action="store_true",
        help="check repository CSVs only; do not query codes.wmo.int",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="per-request registry timeout in seconds (default: 20)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="registry request retries after the first attempt (default: 2)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="maximum concurrent registry requests (default: 6)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="list notation counts for every checked table",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    tables_dir: Path = args.tables_dir

    if not tables_dir.is_dir():
        print(f"ERROR: tables directory not found: {tables_dir}", file=sys.stderr)
        return 2
    if args.retries < 0:
        print("ERROR: --retries must be >= 0", file=sys.stderr)
        return 2
    if args.workers < 1:
        print("ERROR: --workers must be >= 1", file=sys.stderr)
        return 2

    try:
        registers = load_register_mapping(tables_dir)
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot load registry mapping: {exc}", file=sys.stderr)
        return 2

    print("WMDR notation uniqueness report")
    print("=" * 31)

    local_results, local_errors, skipped = check_local_tables(
        tables_dir, registers
    )
    print_source_summary("Repository CSVs", local_results, verbose=args.verbose)
    if skipped:
        print(
            f"Repository CSVs: skipped {skipped} administrative/non-code CSV file(s)"
        )

    local_within = collect_within_table_duplicates(local_results)
    local_cross, local_cross_errors = collect_cross_table_duplicates(local_results)
    local_errors.extend(local_cross_errors)

    print_within_findings("Repository CSVs / within-table", local_within)
    print_cross_findings("Repository CSVs / cross-table", local_cross)

    registry_results: dict[str, SourceResult] = {}
    registry_errors: list[str] = []
    registry_within: list[tuple[str, str, list[Occurrence]]] = []
    registry_cross: list[tuple[str, str, list[Occurrence]]] = []

    if args.skip_registry:
        print("Published registry: SKIPPED (--skip-registry)")
    else:
        print(
            f"Published registry: checking {len(registers)} register(s) "
            "at codes.wmo.int ..."
        )
        registry_results, registry_errors = check_registry_tables(
            registers,
            timeout=args.timeout,
            retries=args.retries,
            workers=args.workers,
        )
        print_source_summary(
            "Published registry", registry_results, verbose=args.verbose
        )
        registry_within = collect_within_table_duplicates(registry_results)
        registry_cross, registry_cross_errors = collect_cross_table_duplicates(
            registry_results
        )
        registry_errors.extend(registry_cross_errors)

        print_within_findings(
            "Published registry / within-table", registry_within
        )
        print_cross_findings(
            "Published registry / cross-table", registry_cross
        )

    all_errors = local_errors + registry_errors
    duplicate_count = (
        len(local_within)
        + len(local_cross)
        + len(registry_within)
        + len(registry_cross)
    )

    if all_errors:
        print("\nErrors:")
        for error in all_errors:
            print(f"  - {error}")

    print()
    if duplicate_count or all_errors:
        print(
            f"RESULT: FAIL - {duplicate_count} duplicate finding(s), "
            f"{len(all_errors)} error(s)"
        )
        return 1

    print("RESULT: PASS - all checked notations are unique")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
