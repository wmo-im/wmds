import argparse
import json
import os

import requests

"""
This script uploads content to the defined register
  ./prodRegister

This reqires an authentication token and userID and structured
content.

The structured content is taken from the command line argument which
shall consist of a dictionary with the keys:
  'PUT', 'POST'
and each key shall provide a list of .ttl files to upload to prodRegister
based on the relative path of the .ttl file.

"""

def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')

    return session

def parse_uploads(uploads):
    result = json.loads(uploads)
    if set(result.keys()) != set(('PUT', 'POST')):
        raise ValueError("Uploads inputs should have keys"
                         " set(('PUT', 'POST')) only, not:\n"
                         "{}".format(result.keys()))
    return result

def post(session, url, payload):
    headers={'Content-type':'text/turtle; charset=UTF-8'}
    response = session.get(url, headers=headers)
    #if response.status_code != 200:
        #raise ValueError('Cannot POST to {}, it does not exist.'.format(url))
    params = {'status':'experimental'}
    res = session.post(url, headers=headers, data=payload.encode("utf-8"),
                       params=params)
    if res.status_code != 201:
        print('POST failed with {}\n{}'.format(res.status_code, res.reason))

def put(session, url, payload):
    headers={'Content-type':'text/turtle; charset=UTF-8'}
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError('Cannot PUT to {}, it does not exist.'.format(url))
    params = {'status':'experimental'}
    res = session.put(url, headers=headers, data=payload.encode("utf-8"),
                      params=params)

def post_uploads(session, rootURL, uploads):
    for postfile in uploads:
        with open('.{}'.format(postfile), 'r', encoding="utf-8") as pf:
            pdata = pf.read()
        # post, so remove last part of identity, this is in the payload
        relID = postfile.replace('.ttl', '')
        relID = '/'.join(postfile.split('/')[:-1])
        url = '{}{}'.format(rootURL, relID)
        print(url)
        post(session, url, pdata)

def put_uploads(session, rootURL, uploads):
    for putfile in uploads:
        with open('.{}'.format(putfile), 'r', encoding="utf-8") as pf:
            pdata = pf.read()
        relID = putfile.replace('.ttl', '')
        url = '{}{}'.format(rootURL, relID)
        print(url)
        put(session, url, pdata)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument("passcode")
    parser.add_argument("tmode")
    parser.add_argument('uploads')
    args = parser.parse_args()

    if os.path.exists(args.uploads):
        with open(args.uploads, 'r') as ups:
            uploads = ups.read()
    else:
        uploads = args.uploads
    uploads = parse_uploads(uploads)
    print(uploads)
    if args.tmode not in ['test', 'prod']:
        raise ValueError('test mode must be either "test" or "prod"')
    if args.tmode == 'prod':
        with open('prodRegister', 'r', encoding='utf-8') as fh:
            rooturl = fh.read().split('\n')[0]
            print('Running upload with respect to {}'.format(rooturl))
    elif args.tmode == 'test':
        with open('testRegister', 'r', encoding='utf-8') as fh:
            rooturl = fh.read().split('\n')[0]
            print('Running upload with respect to {}'.format(rooturl))

    session = requests.Session()
    session = authenticate(session, rooturl, args.user_id, args.passcode)
    print(uploads)
    post_uploads(session, rooturl, uploads['POST'])
    put_uploads(session, rooturl, uploads['PUT'])

