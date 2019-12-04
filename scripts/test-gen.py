from registry_deployment import generate, publish
import logging
import os
import sys
import argparse


parser = argparse.ArgumentParser(description='Command line arguments of TTL file generator and uploader')
parser.add_argument("-g", "--generate", action='store_true', default=True, help="generate files only")
parser.add_argument("-d", "--directory", default=None, help="directory for generated files")
parser.add_argument("-p", "--production", action='store_true',default=False, help="upload to production (otherwise to test)")
parser.add_argument("-t", "--token", default=False, help="token for upload")
parser.add_argument("-v", "--verbose", action='store_true', default=False, help="verbose")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
else:
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger()


dir = args.directory
token = args.token
prod = args.production
gen = args.generate


if gen :
    if dir and ( not os.path.isdir(dir) or len(os.listdir(dir) ) > 0):
        raise ValueError("{} does not exist or not empty".format(dir))

if not gen and not token:
    raise ValueError("upload specified but no token")


try:
    logger.info("generating files")
    generate(dir) #of None is passed temporary files will be used
    logger.info("generated files ok")

    registry = 'https://codes.wmo.int' if prod else 'http://test.wmocodes.info'

    if not gen:
        logger.info("uploading files to {}".format(registry))
        #publish(registry,token,dir)
        logger.info("finished upload")
    
except Exception as e:
    logging.error(e)
    logger.warning("ERROR: {}".format(e))
    sys.exit(1)