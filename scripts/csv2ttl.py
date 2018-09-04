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
           '    rdfs:label "%s" ;',
           '    dct:description  "%s"@en .']
item = ['WMO306_CD', 'WMO306_CD', 'Name', 'Definition']
memberStr = '<' + codelist + '/%s>'

ttlfile = open(outfilename,'w')
with open(infilename) as csvfile:
    r = csv.reader(csvfile, delimiter=',', quotechar='"')
    members = []
    first = 1
    print(header,file=ttlfile)
    count = 0
    for row in r:
        count += 1
        if first:
            keys = row
            first = 0
        else:
            row = [rr.replace("\"","\'") for rr in row]
            d = dict(zip(keys, row))
            notation = d['WMO306_CD']
            if not notation or notation == 'NA':
                print("ERROR notation not defined in line %d" % (count))
                #sys.exit(1)
                continue
            member = memberStr % (d['WMO306_CD'])
            if member in members:
                print("Two registers with the same notation: "+notation)
                sys.exit(1)
            if not all(c in string.printable  for c in d['Definition']):
                print("ERROR unprintable character in Definition in line %d" % (count))
                print(d['Definition'])
                continue
            if not all(c in string.printable for c in d['Name']):
                print("ERROR unprintable character in label in line %d" % (count))
                continue
            if not all(c not in suspectCharacters for c in d['Definition']):
                print("ERROR suspect character in Definition in line %d" % (count))
                #print(d['Definition'])
                continue
            if not all(c not in suspectCharactersNotation for c in d['WMO306_CD']):
                print("ERROR suspect character in Notation in line %d" % (count))
                continue

            members.append(member)
            for i in range(len(item)):
                print(itemStr[i] % (d[item[i]]), file=ttlfile)
            print("", file=ttlfile)

    print(codelistStr, file=ttlfile)
    print(",\n".join(members) + '.',file=ttlfile)
csvfile.close()
ttlfile.close()




