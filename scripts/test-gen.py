from registry_deployment import generate, publish
import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

dir = "./files"

try:
    generate(None)

    #registry = 'https://codes.wmo.int'
    registry = 'http://test.wmocodes.info'
    token = '78ba0667505b855f8c990f09ade68931'

    #publish(registry,token,dir)
    
except Exception as e:
    logging.error(e)
    print("ERROR: {}".format(e))
    sys.exit(1)