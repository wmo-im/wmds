"""
Synchronises the WMDR register content on the target Codes Registry instance (Test/CI) with the
source Codes Registry instance (Prod).

1. Authenticates the user against the target registry instance.
2. Gets the target register content.
3. Gets the source register content.
4. For each entity in the target register:
    a. Delete it from the target register
    b. If it exists in the source register, create it in the target register from the source version.
"""

import argparse
import json
import requests

BASE_URI_PROD = "https://codes.wmo.int"
BASE_URI_TEST = "https://ci.codes.wmo.int"

DATA_PREFIX = "http://codes.wmo.int"  # Registry entities are not prefixed with HTTPS
WMDR_REGISTER = "/wmdr"
COLLECTION = "skos:Collection"


def authenticate(session: requests.Session(), base: str, userid: str, pss: str):
    """
    Authenticates the user against the target registry instance.

    :param session: The session object to use.
    :param base: The base URL for the target registry instance.
    :param userid: The GitHub username e.g. https://api.github.com/users/my-username.
    :param pss: The API key to use (32 character string).
    :return: The authenticated session object.
    """
    auth = session.post(
        f'{base}/system/security/apilogin',
        data={'userid': userid, 'password': pss}
    )

    if auth.status_code != 200:
        raise ValueError('auth failed')

    return session


def entities(register_data_uri: str, base_uri: str):
    """
    Returns a list of register entities contained within the target registry instance.

    :param register_data_uri: The register to query against.
    :param base_uri: The base URI for the target registry instance.
    :return: A JSON list of entities in the register.
    """
    querystring = (
        "prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> "
        "prefix reg: <http://purl.org/linked-data/registry#> "
        "prefix version: <http://purl.org/linked-data/version#> "
        "select ?regdef ?label where {{ "
        f"?item reg:register <{register_data_uri}> ;"
        "      version:currentVersion/reg:definition/reg:entity ?regdef . }}"
    )

    query_params = {'query': querystring, 'output': 'json'}
    base_uri = base_uri + '/system/query'
    results = requests.get(base_uri, params=query_params, timeout=5)
    if results.status_code != 200:
        raise ValueError(f'query failed to run with {results.text}')
    jdata = json.loads(results.text)
    return jdata['results']['bindings']


def post_batch(session: requests.Session, register_uri: str, post_data: str):
    """
    Submits bulk updates to the target registry instance register.

    :param session: The session object to use.
    :param register_uri: The target registry instance register.
    :param post_data: The POST data payload to submit.
    :return: None.
    """
    get_headers = {'Accept': 'text/turtle'}
    response = session.get(register_uri, headers=get_headers)
    print(f'{register_uri} returns {response.status_code}')

    post_headers = {'Content-type': 'text/turtle; charset=UTF-8'}
    params = {'status': 'stable'}

    # next, configure status to match prod status
    register_uri = register_uri + '?batch-managed'
    print("post batch: ", register_uri)
    res = session.post(
        register_uri,
        headers=post_headers, data=post_data.encode("utf-8"), params=params, timeout=5)

    if res.status_code != 201:
        raise ValueError(f'POST failed with {res.status_code}\n{res.reason}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument("passcode")
    args = parser.parse_args()

    # Authenticate against Test instance
    test_session = requests.Session()
    test_session = authenticate(test_session, BASE_URI_TEST, args.user_id, args.passcode)

    # Get a list of entities in the WMDR register for prod and test instances
    wmdr_prod_registers = [r['regdef']['value'] for r in
                           entities(DATA_PREFIX + WMDR_REGISTER, BASE_URI_PROD)]
    wmdr_test_registers = [r['regdef']['value'] for r in
                           entities(DATA_PREFIX + WMDR_REGISTER, BASE_URI_TEST)]

    print("Prod register initial count: ", len(wmdr_prod_registers))
    print("Test register initial count: ", len(wmdr_test_registers))

    missing_test_regs = []

    for register in wmdr_test_registers:
        print("---\nProcessing", register)

        # Convert entity URI to the API equivalent and verify entity exists in Test instance
        test_register_uri = register.replace(DATA_PREFIX, BASE_URI_TEST)
        headers = {'Accept': 'text/turtle; charset=UTF-8'}
        test_reg_content = requests.get(test_register_uri, headers=headers, timeout=5)

        # Delete the existing entity from the Test instance
        if test_reg_content.status_code == 200:
            print(f'Deleting {test_register_uri}')
            delete_request = test_session.post(test_register_uri + '?real_delete')

            print(f'Delete status code: {delete_request.status_code}')
            if delete_request.status_code != 200:
                raise ValueError(
                    f'Failed to delete {test_register_uri} :\n{delete_request.reason}')

        # If the entity exists on the Prod instance, replace it on the Test instance.
        if register in wmdr_prod_registers:
            prod_register_uri = register.replace(DATA_PREFIX, BASE_URI_PROD)
            prod_reg_content = requests.get(prod_register_uri, headers=headers, timeout=5)
            print(f'prod_reg_content status code: {prod_reg_content.status_code}')

            assert prod_reg_content.status_code == 200

            if prod_reg_content.text.count('reg:Register') > 1:
                raise ValueError(f'{register} contains sub-registers')

            payload = prod_reg_content.text
            payload = payload.replace(DATA_PREFIX + WMDR_REGISTER + "/", '')
            payload = payload.replace('ldp:Container , reg:Register , ', '')
            payload = payload.replace('ldp:Container , skos:Collection , reg:Register', COLLECTION)
            payload = payload.replace('reg:Register , ldp:Container , skos:Collection', COLLECTION)
            payload = payload.replace('reg:Register , skos:Collection , ldp:Container', COLLECTION)
            payload = payload.replace('skos:Collection , ldp:Container , reg:Register', COLLECTION)
            payload = payload.replace('skos:Collection , reg:Register , ldp:Container', COLLECTION)

            try:
                post_batch(test_session, BASE_URI_TEST + WMDR_REGISTER, payload)
                print(f'Replaced {test_register_uri}\n')
            except ValueError as e:
                missing_test_regs.append(test_register_uri)
                print(e)
            finally:
                if test_register_uri.split('/')[-1] in ['QualityFlagCIMO', 'QualityFlagOGC']:
                    invalid_identifier = (
                            BASE_URI_TEST + WMDR_REGISTER + '/_' +
                            test_register_uri.split('/')[-1] + '?update&status=invalid'
                    )
                    test_session.post(invalid_identifier)
                    print(f'{invalid_identifier} set to invalid')

    print("Missing registers: ", missing_test_regs)
    print("Missing register count: ", len(missing_test_regs))
