# wmds
WIGOS Metadata Standard: Semantic standard and code tables

The _tables_en_ folder contains the up-to-date versions that the TT-WIGOSMD is working on.
View mapping of CSV file identifiers to table names and Codes Registry URLs: https://github.com/wmo-im/wmds/blob/master/tables_en/wmdr-tables.csv.

Published code tables can be found at WMO Codes Registry for WIGOS Metadata Representation: https://codes.wmo.int/wmdr.

## Related Publications
[WIGOS Metadata Standard](https://library.wmo.int/index.php?lvl=notice_display&id=19925#.X7J1UtNKi3I)

[Manual on Codes, Volume I.3](https://library.wmo.int/index.php?lvl=notice_display&id=19508#.X7J48NNKi3J)
  Part D – Representations derived from data models
  See chapter FM 241: WMDR

## Testing and management

./scripts provides tools written in Python to check content consistency with the published test and prod registers and to upload changes.

example usage:

consistency check

```
tmode=test outfile=</path/to/writeable/file> python3 -m scripts.check_urls
```

upload change

```
python3 -m scripts.uploadChanges <uname> <temporaryKey> test </path/to/a/readable/file>
```
