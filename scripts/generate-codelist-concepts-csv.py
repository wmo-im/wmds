##############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import csv
import sys

ROOT_CSV = 'wmdr-tables.csv'
URI_ROOT = 'https://codes.wmo.int/wmdr'
FIELDNAMES = ['id', 'title', 'description', 'url']

if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <input-dir> <output-dir>')
    sys.exit(1)

input_dir = sys.argv[1]
output_dir = sys.argv[2]

with open(f'{input_dir}/{ROOT_CSV}') as fh:
    reader = csv.reader(fh)

    for row in reader:
        codelist = f'{input_dir}/{row[0]}.csv'
        codelist_basename = row[-1].split('/')[-1]
        concept_csv = f'{output_dir}/{codelist_basename}.csv'
        with open(codelist) as fh2, open(concept_csv, 'w') as fh3:
            reader2 = csv.DictReader(fh2)
            writer = csv.DictWriter(fh3, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row2 in reader2:
                writerow = {
                    'id': row2['notation'],
                    'title': row2['name'],
                    'description': row2['description'],
                    'url': f'{URI_ROOT}/{codelist_basename}'
                }
                writer.writerow(writerow)
