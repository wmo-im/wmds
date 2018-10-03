#!/usr/bin/env python

import sys
import string
import csv
from os.path import basename
from os.path import splitext


codelistLabel = 'Measurement or observing method'
codelistDescription = 'The method of measurement or observation used'

infilename = sys.argv[1]
outfilename = splitext(infilename)[0]+'.ttl'
header = '@prefix dct:   <http://purl.org/dc/terms/> .\n\
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n\
@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .\n'

suspectCharacters = "?!\n"
suspectCharactersNotation = " ,:!?="
parent = splitext(basename(infilename))[0].replace("-","/")
parentURI = parent
registers = parentURI.split("/")
codelist = registers[-1]

codelistStr = '<' + codelist + '> a skos:Collection ;\n\
        rdfs:label "' + codelistLabel + '" ;\n\
        dct:description  "' + codelistDescription + '"@en ;\n\
        skos:member \n'

type = 'skos:Concept'

itemStr = ['<' + codelist + '/%s> a ' + type + ' ;',
           '    skos:notation "%s" ;',
           '    rdfs:label "%s"@en ,',
           '    "%s"@fr ,',
           '    "%s"@es ,',
           '    "%s"@ru ;',
           '    dct:description  "%s"@en ,',
           '    "%s"@fr ,',
           '    "%s"@es ,',
           '    "%s"@ru .' ]
item = ['WMO306CD_efrs', 'WMO306CD_efrs', 'Name_e', 'Name_f', 'Name_s', 'Name_r', 'Definition_e', 'Definition_f',
        'Definition_s', 'Definition_r']
memberStr = '<' + codelist + '/%s>'

ttlfile = open(outfilename, 'w', encoding='utf-8')
with open(infilename, encoding='utf-8') as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='"')
    members = []
    first = 1
    print(header, file=ttlfile)
    count = 0
    for row in r:
        count += 1
        if first:
            keys = row
            first = 0
        else:
            row = [rr.replace("\"", "\'") for rr in row]
            d = dict(zip(keys, row))
            notation = d['WMO306CD_efrs']
            if not notation or notation == 'NA':
                print("ERROR notation not defined in line %d" % (count))
                sys.exit(1)
                continue
            member = memberStr % notation
            if member in members:
                print("Two registers with the same notation: "+notation)
                sys.exit(1)
            if not all(c in string.printable for c in d['Definition_e']):
                for c in d['Definition_e']:
                    print(c)
                    if c not in string.printable:
                        break
                print("ERROR unprintable character in Definition_e in line %d" % (count))
                print(d['Definition_e'])
                continue
            if not all(c in string.printable for c in d['Name_e']):
                print("ERROR unprintable character in label in line %d" % (count))
                continue
            if not all(c not in suspectCharacters for c in d['Definition_e']):
                print("ERROR suspect character in Definition_e in line %d" % (count))
                #print(d['Definition_e'])
                continue
            if not all(c not in suspectCharactersNotation for c in d['WMO306CD_efrs']):
                print("ERROR suspect character in Notation in line %d" % (count))
                continue

            members.append(member)
            for i in range(len(item)):
                print(itemStr[i] % (d[item[i]]), file=ttlfile)
            print("", file=ttlfile)

    print(codelistStr, file=ttlfile)
    print(",\n".join(members) + '.', file=ttlfile)
csvfile.close()
ttlfile.close()




