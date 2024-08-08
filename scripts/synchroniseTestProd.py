"""
Synchronises the WMDR register content on the target Codes Registry instance (Test/CI) with the
source Codes Registry instance (Prod).

1. Authenticate the user against the target registry instance.
2. Get the WMDR sub-registers from both the source and target instances.
3. Delete all sub-registers from the target register.
4. Create a copy of each sub-register from the source instance to the target instance.
"""

import argparse
import json
import time
import requests
from requests.exceptions import HTTPError

BASE_URI_PROD = "https://codes.wmo.int"
BASE_URI_TEST = "https://ci.codes.wmo.int"

DATA_PREFIX = "http://codes.wmo.int"  # Registry entities are not prefixed with HTTPS
WMDR_REGISTER = "/wmdr"
COLLECTION = "skos:Collection"

REQUESTS_TIMEOUT_SECONDS = 60
HTTP_OK_RESPONSE_CODE = 200
HTTP_CREATED_RESPONSE_CODE = 201


def authenticate(session: requests.Session, base_uri: str, userid: str, pss: str) -> requests.Session:
    """
    Authenticate the user against the target registry instance.

    :param session: The session object to use.
    :param base_uri: The base URI for the target registry instance.
    :param userid: The GitHub username e.g. https://api.github.com/users/my-username.
    :param pss: The API key to use (32 character string).
    :return: The authenticated session object.
    """
    auth_response = session.post(
        f"{base_uri}/system/security/apilogin",
        data={"userid": userid, "password": pss}
    )

    if auth_response.status_code != HTTP_OK_RESPONSE_CODE:
        raise ValueError("Auth failed")

    return session


def get_registers(register_data_uri: str, register_api_uri: str) -> list:
    """
    Return a list of registers from the target register API.

    :param register_data_uri: The register to query against.
    :param register_api_uri: The register API URI to query.
    :return: A JSON list of entities in the register.
    """
    querystring = (
        "prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        "prefix reg: <http://purl.org/linked-data/registry#> "
        "prefix version: <http://purl.org/linked-data/version#> "
        "select ?regdef ?label where {{ "
        f"?item reg:register <{register_data_uri}> ; "
        "version:currentVersion/reg:definition/reg:entity ?regdef . }}"
    )

    get_response = requests.get(
        f"{register_api_uri}/system/query",
        params={"query": querystring, "output": "json"},
        timeout=REQUESTS_TIMEOUT_SECONDS
    )

    if get_response.status_code != HTTP_OK_RESPONSE_CODE:
        raise HTTPError(f"query failed to run with {get_response.text}")

    json_data = json.loads(get_response.text)
    return [item["regdef"]["value"] for item in json_data["results"]["bindings"]]


def delete_registers(session: requests.Session, registers: list) -> None:
    """
    Delete the test sub registers contained within the target register.

    :param session: The session object to use.
    :param registers: The list of sub registers to delete.
    :return: None.
    """
    for register in registers:
        print(f"\nDeleting {register}")

        # Convert entity URI to the API equivalent
        register_api_uri = register.replace(DATA_PREFIX, BASE_URI_TEST)

        # Delete the existing entity from the Test instance
        delete_response = session.post(f"{register_api_uri}?real_delete", timeout=REQUESTS_TIMEOUT_SECONDS)
        print(f"Delete status code: {delete_response.status_code}")

        if delete_response.status_code != HTTP_OK_RESPONSE_CODE:
            raise HTTPError(f"Failed to delete {register_api_uri} :\n{delete_response.reason}")


def create_register(session: requests.Session, register_api_uri: str, post_data: str) -> None:
    """
    Create a register on the target registry instance register.

    :param session: The session object to use.
    :param register_api_uri: The register API URI to POST against.
    :param post_data: The POST data payload to submit.
    :return: None.
    """
    create_response = session.post(
        f"{register_api_uri}?batch-managed",
        headers={"Content-type": "text/turtle; charset=UTF-8"},
        data=post_data.encode("utf-8"),
        params={"status": "stable"},
        timeout=REQUESTS_TIMEOUT_SECONDS
    )
    print(f"Create status code: {create_response.status_code}")

    if create_response.status_code != HTTP_CREATED_RESPONSE_CODE:
        raise HTTPError(f"POST failed with {create_response.status_code}\n{create_response.reason}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_id")
    parser.add_argument("passcode")
    args = parser.parse_args()

    # Authenticate against Test instance
    test_session = requests.Session()
    test_session = authenticate(test_session, BASE_URI_TEST, args.user_id, args.passcode)

    # Get a list of sub-registers in the WMDR register for Prod and Test registry instances
    wmdr_prod_registers = get_registers(f"{DATA_PREFIX}{WMDR_REGISTER}", BASE_URI_PROD)
    wmdr_test_registers = get_registers(f"{DATA_PREFIX}{WMDR_REGISTER}", BASE_URI_TEST)

    print("Prod register initial count: ", len(wmdr_prod_registers))
    print("Test register initial count: ", len(wmdr_test_registers))

    # Compare differences between Prod and Test
    prod_diff = [register.replace(DATA_PREFIX, "") for register in wmdr_prod_registers if
                 register not in wmdr_test_registers]
    print(f"Prod contains {len(prod_diff)} unique register(s):", prod_diff)

    test_diff = [register.replace(DATA_PREFIX, "") for register in wmdr_test_registers if
                 register not in wmdr_prod_registers]
    print(f"\nTest contains {len(test_diff)} unique register(s):", test_diff)

    # Delete existing sub-registers in Test
    print("\n---\nDeleting existing sub-registers in Test")
    delete_registers(test_session, wmdr_test_registers)

    # Copy Prod sub-registers to Test
    print("\n---\nCopying sub-registers from Prod")

    missing_test_regs = []

    for prod_register in wmdr_prod_registers:
        print(f"\nCreating copy of {prod_register}")

        # Convert entity URI to the API equivalent
        prod_register_uri = prod_register.replace(DATA_PREFIX, BASE_URI_PROD)

        # Add sleep as the Codes Registry is struggling to deal with multiple requests at once
        time.sleep(2)

        print(f"Getting prod register content for {prod_register}")
        prod_reg_content = requests.get(
            prod_register_uri,
            headers={"Accept": "text/turtle; charset=UTF-8"},
            timeout=REQUESTS_TIMEOUT_SECONDS
        )
        print(f"prod_reg_content status code: {prod_reg_content.status_code}")

        if prod_reg_content.status_code != HTTP_OK_RESPONSE_CODE:
            raise HTTPError(f"prod_reg_content failed with {prod_reg_content.text}")

        if prod_reg_content.text.count("reg:Register") > 1:
            raise ValueError(f"{prod_register} contains sub-registers")

        payload = prod_reg_content.text
        payload = payload.replace(f"{DATA_PREFIX}{WMDR_REGISTER}/", "")
        payload = payload.replace("ldp:Container , reg:Register , ", "")
        payload = payload.replace("ldp:Container , skos:Collection , reg:Register", COLLECTION)
        payload = payload.replace("reg:Register , ldp:Container , skos:Collection", COLLECTION)
        payload = payload.replace("reg:Register , skos:Collection , ldp:Container", COLLECTION)
        payload = payload.replace("skos:Collection , ldp:Container , reg:Register", COLLECTION)
        payload = payload.replace("skos:Collection , reg:Register , ldp:Container", COLLECTION)

        try:
            create_register(test_session, f"{BASE_URI_TEST}{WMDR_REGISTER}", payload)
        except ValueError as e:
            missing_test_regs.append(prod_register)
            print(e)
        finally:
            name = prod_register_uri.split("/")[-1]
            if name in ["QualityFlagCIMO", "QualityFlagOGC"]:
                invalid_identifier = f"{BASE_URI_TEST}{WMDR_REGISTER}/_{name}?update&status=invalid"
                test_session.post(invalid_identifier, timeout=REQUESTS_TIMEOUT_SECONDS)
                print(f"{invalid_identifier} set to invalid")

    print("\nMissing registers: ", missing_test_regs)
    print("Missing register count: ", len(missing_test_regs))
