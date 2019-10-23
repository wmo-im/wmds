import requests
import time
import re
import sys
import string
import datetime
import logging
import urllib.request

from os import listdir
from os.path import isfile, join
from os.path import splitext
from os.path import basename

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger()

    
def authenticate(session, base, userid, pss):
    auth = session.post('{}/system/security/apilogin'.format(base),
                        verify=False,
                        data={'userid':userid,
                                'password':pss})
    if not auth.status_code == 200:
        raise ValueError('auth failed')

    return session

def post_file(session, registry_url, postfile, container, status, bulk=False):
    with open(postfile, 'r') as pf:
        pdata = pf.read().encode('utf-8')
        
    params = {'status':status}
    
    if container == '.':
        container = ''
    else:
        container = '/' + container
    if not container:
        container = '/'

    if bulk:
        params = 'batch-managed&' + urllib.parse.urlencode(params)
        
    url = "{u}{c}".format(u=registry_url,c=container)
    logger.debug(url)
    res = session.post(url,
                      headers={'Content-type':'text/turtle; charset=UTF-8'}, 
                      data=pdata,
                      params=params)
    
    if res.status_code > 299:
        if res.status_code == 403:
            exists = session.get(url)
            if exists.status_code != 200:
                raise ValueError('Http response code indicates failure\n{}'.format(res.status_code))
        else:
            raise ValueError('Http response code indicates failure: {} - {}'.format(res.status_code,res.text))
 
    return session    
    
    
            
            
def publish(registry_url,token,dir):
            
    ## authenticate with registry
    data = {
      'userid': 'https://api.github.com/users/kurt-hectic',
      'password': token
    }

    session = requests.Session()
    session = authenticate(session, registry_url, data['userid'], data['password'])

    ## deploy

    for file in [ f for f in listdir(dir) if f.endswith(".ttl") ]:
        logger.debug("uploading {}".format(file))
        try: 
            post_file(session, registry_url, join(dir, file) , "wmdr", "experimental", True)
            logger.info("posted {} to registry {}".format(file,registry_url))
        except ValueError as ve:
            print("issue with {} : {}".format(file,ve))
