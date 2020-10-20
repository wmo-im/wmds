import csv
import os
import re
import warnings
import shutil

collectionTemplate = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                      '@prefix dct: <http://purl.org/dc/terms/> . \n'
                      '@prefix ldp:   <http://www.w3.org/ns/ldp#> .\n'
                      '@prefix reg:   <http://purl.org/linked-data/registry#> .\n'
                      '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\n'
                      '<{identity}> a reg:Register , skos:Collection , ldp:Container  ;\n'
                      '\tldp:hasMemberRelation skos:member ;\n'
                      '\trdfs:label "{label}" ;\n'
                      '\tdct:description "{description}" .\n')

conceptTemplate = ('@prefix skos:  <http://www.w3.org/2004/02/skos/core#> . \n'
                   '@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n'
                   '@prefix dct: <http://purl.org/dc/terms/> . \n\n'
                   '<{identity}> a skos:Concept ;\n'
                   '\trdfs:label "{label}" ;\n'
                   '\tskos:notation "{notation}" ;\n'
                   '\tdct:description "{description}"@en'
                   '\t.\n')

def clean(astr):
    if '"' in astr:
        astr = astr.replace('"', "'")
    astr = astr.strip()
    return astr

def main():
    print('Make WMDR TTL contents')
    root_path = os.path.split(os.path.dirname(__file__))[0]
    if os.path.exists(os.path.join(root_path, 'wmdr')):
        shutil.rmtree(os.path.join(root_path, 'wmdr'))
    os.mkdir(os.path.join(root_path, 'wmdr'))

    with open(os.path.join(root_path, 'tables_en', 'wmdr-tables.csv'), encoding='utf-8') as wmdrtables:
        reader = csv.reader(wmdrtables, delimiter=',', quotechar='"')
        for wmdrtable in reader:
            identifier = wmdrtable[2].split('/')[-1]
            if not os.path.exists(os.path.join(root_path, 'tables_en', '{}.csv'.format(wmdrtable[0]))):
                raise ValueError('WMDR Table {} missing from path'.format(wmdrtable[0]))

            with open(os.path.join(root_path, 'wmdr', '{}.ttl'.format(identifier)), 'w', encoding='utf-8') as ttlf:
                ttlf.write(collectionTemplate.format(identity=identifier, label=clean(wmdrtable[1]),
                                                  description=clean(wmdrtable[1])))
            if not os.path.exists(os.path.join(root_path, 'wmdr', identifier)):

                os.mkdir(os.path.join(root_path, 'wmdr', identifier))
            with open(os.path.join(root_path, 'tables_en', '{}.csv'.format(wmdrtable[0])), encoding='utf-8') as wmdrentries:
                wmdr_reader = csv.DictReader(wmdrentries)
                for entry in wmdr_reader:
                    with open(os.path.join(root_path, 'wmdr', identifier, '{}.ttl'.format(entry['notation'])), 'w', encoding='utf-8') as entryfile:
                        entryfile.write(conceptTemplate.format(identity=entry['notation'], notation=entry['notation'],
                                                               label=clean(entry['name']),
                                                               description=clean(entry['description'])))


if __name__ == '__main__':
    main()
