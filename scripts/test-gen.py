from registry_deployment import generate, publish, createReadme

import logging
import os
import sys

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

dir = "C:/TEMP/registry"

try:

    # first check if filesystem and readme are synced
    with open(r"tables_en/readme.md","r",encoding="utf8") as f:
        readme_content = f.read()
        
        virtual_readme = createReadme()
        
        if readme_content != virtual_readme:
            logging.error("readme not in sync with wmrd-tables.csv")
            sys.exit(1)

    generate(dir)

    registry = 'https://codes.wmo.int'
    #registry = 'http://test.wmocodes.info'
    token = '0039e8fb71d0d798b7766d97549a170c'

    #publish(registry,token,dir)
    
except Exception as e:
    logging.error(e)
    print("ERROR: {}".format(e))
    sys.exit(1)