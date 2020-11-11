import copy
import glob
import json
import os
import sys
import unittest

import rdflib
import rdflib.compare
import requests
import testtools

import scripts.makeWMDREntities as makeWMDR

"""
This test script evaluates all folder which contain a file of name
'regurl'
that contains a single URL for a registry.
Test will succeed if the registry exists, and all contents is the same as
in the repository commit.
All entities must exist, evaluate to the same content, and no entities may be
remote that are not in the source tree.
"""

uploads = {'PUT': [],
           'POST': []}

with open('prodRegister', 'r') as fh:
    rooturl = fh.read().split('\n')[0]

if os.environ.get('tmode') == 'test':
    with open('testRegister', 'r') as fh:
        downloadurl = fh.read().split('\n')[0]

elif os.environ.get('tmode') == 'prod':
    downloadurl = rooturl

else:
    raise ValueError('Environment option "tmode" required to be "prod|test", but missing.')
print('Running test with respect to {}'.format(downloadurl))


class TestContentsExistance(unittest.TestCase):
    def test_register(self):
        headers={'Accept':'text/turtle'}
        pr = requests.get(downloadurl, headers=headers)
        self.assertEqual(pr.status_code, 200)

class TestContentsConsistency(unittest.TestCase):

    def check_result(self, result, expected, uploads, identityURI, resourceURL):
        lbb = ('\n####### inBothinputs #######\n')
        lbr = ('\n####### inTestResultOnly #######\n')
        lbe = ('\n####### inExpectedOnly #######\n')

        inboth, inres, inexp = rdflib.compare.graph_diff(result, expected)
        try:
            assert(rdflib.compare.isomorphic(result, expected))
        except AssertionError:
            ufile = '{}.ttl'.format(identityURI.split(rooturl)[1])
            if (list(inres.triples((None, rdflib.namespace.SKOS.member, None))) or
                list(inexp.triples((None, rdflib.namespace.SKOS.member, None)))):
                lbb = ('\n####### Containment Error, '
                       'check validity of list of contained entities '
                       '#######\n{}').format(lbb)
            
            else:
                uploads['PUT'].append(ufile)

        self.assertTrue(rdflib.compare.isomorphic(result, expected),
                        (resourceURL + '\n' +
                         lbb + inboth.serialize(format='n3').decode("utf-8") +
                         lbr + inres.serialize(format='n3').decode("utf-8") +
                         lbe + inexp.serialize(format='n3').decode("utf-8")))


# Clean all .ttl files from the source tree

for f in glob.glob('wmdr/**/*.ttl', recursive=True):
    os.remove(f)

# Ensure that all TTL content is built from the input tables.

makeWMDR.main()

print('made ttl')
# Build test cases based on the TTL files within the repository,
# one test case per file.
for f in glob.glob('wmdr/**/*.ttl', recursive=True):
    relf = f.replace('.ttl', '')
    identity = '{}/{}'.format(rooturl, relf)
    resource = '{}/{}'.format(downloadurl, relf)

    def make_a_test(infile):
        # Ensure URIs are fixed, as these are dynamic test generators
        resourceURI = copy.copy(resource)
        identityURI = copy.copy(identity)
        def entity_exists(self):
            headers={'Accept':'text/turtle', 'Cache-Control': 'private, no-store, max-age=0'}
            regr = requests.get(resourceURI, headers=headers)
            try:
                assert(regr.status_code == 200)
            except AssertionError:
                ufile = '{}.ttl'.format(identityURI.split(rooturl)[1])
                uploads['POST'].append(ufile)
            msg = ('{} expected to return 200 but returned {}'
                   ''.format(resourceURI, regr.status_code))
            self.assertEqual(regr.status_code, 200, msg)
        return entity_exists
    tname = 'test_exists_{}'.format(relf.replace('/', '_'))
    setattr(TestContentsExistance, tname, make_a_test(f))

    def make_another_test(infile):
        # Ensure URIs are fixed, as these are dynamic test generators
        resourceURI = copy.copy(resource)
        identityURI = copy.copy(identity)
        def entity_consistent(self):
            headers={'Accept':'text/turtle', 'Cache-Control': 'private, no-store, max-age=0'}
            ufile = '{}.ttl'.format(identityURI.split(rooturl)[1].lstrip('/'))
            expected = requests.get(resourceURI, headers=headers)
            assert(expected.status_code == 200)
            expected_rdfgraph = rdflib.Graph()
            expected_rdfgraph.parse(data=expected.text, format='n3')
            # print(expected)
            result_rdfgraph = rdflib.Graph()
            # print(identityURI)
            result_rdfgraph.parse(ufile, publicID=identityURI, format='n3')
            # if ldp:container with contained entities
            if os.path.exists(identityURI.split(rooturl)[1].lstrip('/')):
                # add in member relations from tree
                col_id, = result_rdfgraph.subjects(rdflib.RDF.type, rdflib.namespace.SKOS.Collection)
                for fname in glob.glob('{}/*.ttl'.format(identityURI.split(rooturl)[1].lstrip('/'))):
                    member_id = rdflib.term.URIRef(u'{}/{}'.format(identityURI, fname.split('/')[-1].split('.ttl')[0]))
                    result_rdfgraph.add((col_id, rdflib.namespace.SKOS.member, member_id))
                    expected_rdfgraph.remove((member_id, None, None))
                # do not check version info or date modified (owned by registry)
                expected_rdfgraph.remove((None, rdflib.namespace.DCTERMS.modified, None))
                expected_rdfgraph.remove((None, rdflib.namespace.OWL.versionInfo, None))
            self.check_result(result_rdfgraph, expected_rdfgraph, uploads, identityURI, resourceURI)
        return entity_consistent

    tname = 'test_consistent_{}'.format(relf.replace('/', '_'))
    setattr(TestContentsConsistency, tname, make_another_test(f))

if __name__ == '__main__':
    try:
        unittest.main()

    except Exception as e:
        raise e
    finally:
        print("uploads:\n'{}'".format(json.dumps(uploads)), flush=True)
