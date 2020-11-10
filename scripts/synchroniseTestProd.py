import argparse
import json
import requests


def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')

    return session

def post_batch(session, url, payload):
    headers={'Accept':'text/turtle'}
    response = session.get(url, headers=headers)
    print('{} returns {}'.format(url, response.status_code))
    # if response.status_code != 200:
    #     raise ValueError('Cannot POST to {}, it does not exist.'.format(url))
    headers={'Content-type':'text/turtle; charset=UTF-8'}

    params = {'status':'experimental'}
    url = url + '?batch-managed'
    res = session.post(url, headers=headers, data=payload.encode("utf-8"), params=params)

    if res.status_code != 201:
        raise ValueError('POST failed with {}\n{}'.format(res.status_code, res.reason))


def entities(reguri, baseurl):
    qstr = ("prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> " 
                  "prefix reg: <http://purl.org/linked-data/registry#> "
                  "prefix version: <http://purl.org/linked-data/version#> "
                  "select ?regdef ?label where {{ "
                  "?item reg:register <{reguri}> ;"
                  "      version:currentVersion/reg:definition/reg:entity ?regdef  . }}" ).format(reguri=reguri)

    qparams={'query': qstr, 'output': 'json'}
    baseurl = baseurl + '/system/query'
    results = requests.get(baseurl, params=qparams)
    if results.status_code != 200:
        raise ValueError('query failed to run with {}'.format(results.text))
    jdata = json.loads(results.text)
    return jdata['results']['bindings']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument("passcode")
    args = parser.parse_args()

    prod_uri = 'http://codes.wmo.int'
    test_uri = 'http://testwmocodes.metarelate.net'
    wmdr_test_uri = test_uri + '/wmdr'

    wmdr_prod_registers = [r['regdef']['value'] for r in entities(prod_uri + '/wmdr', prod_uri)]
    wmdr_test_registers = [r['regdef']['value'] for r in entities(prod_uri + '/wmdr', test_uri)]
    session = requests.Session()
    session = authenticate(session, test_uri, args.user_id, args.passcode)

    

    missing_test_regs = []
    for areg in wmdr_test_registers:
        headers = {'Accept':'text/turtle; charset=UTF-8'}
        
        treg = areg.replace('codes.wmo.int', 'testwmocodes.metarelate.net')

        test_reg_content = requests.get(treg, headers=headers)
        if test_reg_content.status_code == 200:
            real_delete_uri = treg + '?real_delete'

            print('deleting {}\n'.format(treg))
            delete_request = session.post(real_delete_uri)
            print('delete status code: {}'.format(delete_request.status_code))
            # if delete_request != 200:
            #     raise ValueError('failed to delete {} :\n{}'.format(treg, delete_request.reason))
        if areg in wmdr_prod_registers:
            prod_reg_content = requests.get(areg, headers=headers)
            assert(prod_reg_content.status_code == 200)
            if prod_reg_content.text.count('reg:Register') > 1:
                raise ValueError('{} contains sub-registers'.format(areg))

            payload = prod_reg_content.text
            payload = payload.replace('http://codes.wmo.int/wmdr/', '')
            payload = payload.replace('ldp:Container , reg:Register , ', '')
            payload = payload.replace('ldp:Container , skos:Collection , reg:Register', 'skos:Collection')
            payload = payload.replace('reg:Register , ldp:Container , skos:Collection', 'skos:Collection')
            payload = payload.replace('reg:Register , skos:Collection , ldp:Container', 'skos:Collection')
            payload = payload.replace('skos:Collection , ldp:Container , reg:Register', 'skos:Collection')
            payload = payload.replace('skos:Collection , reg:Register , ldp:Container', 'skos:Collection')


            try:
                post_batch(session, wmdr_test_uri, payload)
                print('replaced {}\n'.format(treg))

            except ValueError as e:
                missing_test_regs.append(treg)
                print(e)
            finally:
                if treg.split('/')[-1] in ['QualityFlagCIMO', 'QualityFlagOGC']:
                    invalid_identifier = wmdr_test_uri + '/_' + treg.split('/')[-1] + '?update&status=invalid'
                    session.post(invalid_identifier)
                    print('{} set to invalid'.format(invalid_identifier)) 

print(missing_test_regs)
print(len(missing_test_regs))


