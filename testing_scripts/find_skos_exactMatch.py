# this is the class where SameAsEqSolver is defined
import networkx as nx
from pyvis.network import Network
import community
import collections
import matplotlib.pyplot as plt
from random import randint
import pandas as pd
import requests
from collections import Counter
from rfc3987 import  parse
import urllib.parse
from hdt import HDTDocument, IdentifierPosition



def get_authority (w):
	try:
		return parse(w)['authority']
	except Exception as e:
		# print (e)
		if 'id.ndl.go.jp' in w:
			return 'id.ndl.go.jp'
		elif 'id.loc.gov' in w:
			return 'id.loc.gov'
		elif 'lod.ac/' in w:
			return 'lod.ac'
		else:
			return ''


def get_simp_IRI(e):
	# simplify this uri by introducing the namespace abbreviation
	ext = tldextract.extract(e)

	if 'dbpedia' == ext.domain and ext.subdomain != '' and ext.subdomain != None:
		namespace = ext.subdomain +'.'+ext.domain
	else :
		namespace = ext.domain

	short_IRI = ''

	if e.split('/') == [e] :
		if e.split('#') != [e]:
			name = e.split('#')[-1]
	else:
		name = e.split('/')[-1]

	if len (name) < 10:
		short_IRI  = namespace + ':' + name
	else:
		short_IRI = namespace + ':' + name[:10] + '...'

	return short_IRI

def get_prefix (e):
	prefix, name, sign = get_name(e)
	return prefix


def get_name (e):
	name = ''
	prefix = ''
	sign = ''
	if e.rfind('/') == -1 : # the char '/' is not in the iri
		if e.split('#') != [e]: # but the char '#' is in the iri
			name = e.split('#')[-1]
			prefix = '#'.join(e.split('#')[:-1]) + '#'
			sign = '#'
		else:
			name = None
			sign = None
			prefix =  None
	else:
		name = e.split('/')[-1]
		prefix = '/'.join(e.split('/')[:-1]) + '/'
		sign = '/'

	return prefix, sign, name




rdfs_label = "http://www.w3.org/2000/01/rdf-schema#label"
skos_preflabel = "http://www.w3.org/2004/02/skos/core#prefLabel"

owl_sameas = "http://www.w3.org/2002/07/owl#sameAs"
skos_exactMatch = "http://www.w3.org/2004/02/skos/core#exactMatch"
skos_broadMatch = "http://www.w3.org/2004/02/skos/core#broadMatch"
skos_broader = "http://www.w3.org/2004/02/skos/core#broader"
skos_narrowMatch = "http://www.w3.org/2004/02/skos/core#narrowMatch"
skos_narrower = "http://www.w3.org/2004/02/skos/core#narrower"
skos_relatedMatch = "http://www.w3.org/2004/02/skos/core#relatedMatch"
skos_closeMatch = "http://www.w3.org/2004/02/skos/core#closeMatch"
subPropertyOf = 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'
inv = 'http://www.w3.org/2002/07/owl#inverseOf'

type = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

subClassOf = 'http://www.w3.org/2000/01/rdf-schema#subClassOf'
subPropertyOf = 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'

broader = 'http://www.w3.org/2004/02/skos/core#broader'
narrower = 'http://www.w3.org/2004/02/skos/core#narrower'

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt = HDTDocument(PATH_LOD)

triples, cardinality = hdt.search_triples("", skos_exactMatch, "")
print ('There are ', cardinality, ' triples about skos:exactMatch')

g = nx.DiGraph()
entities = set()

for s, p, o in triples:
	entities.add(s)
	entities.add(o)
	g.add_edge(s, o)


print ('\t with ', len (entities), ' entities')
try:
	print ('\t diameter = ', dm.diameter(g))
except Exception as e:
	print ('\t diameter = infinite')


# sccs = list(nx.strongly_connected_components(g))
# sccs_size = [len(s) for s in sccs]
# ct_sccs = Counter(sccs_size)
# print ('sccs counter = ', ct_sccs)
# largest_cc = max(sccs, key=len)
# print ('the biggest scc has ', len(largest_cc), 'nodes')
# print ('\t{:06.2f}'.format(len(largest_cc)/ g.number_of_nodes()*100))

wccs = list(nx.weakly_connected_components(g))
wccs_size = [len(s) for s in wccs]
ct_wccs = Counter(wccs_size)
for c in ct_wccs.keys():
	if c > 50:
		print (c, ' has ', ct_wccs[c])

print ('wccs counter = ', ct_wccs)
largest_cc = max(wccs, key=len)
print ('the biggest wcc has ', len(largest_cc), 'nodes')
print ('\t{:06.2f}'.format(len(largest_cc)/ g.number_of_nodes()*100))


# print information about this biggest WCC
# wccs = list(nx.weakly_connected_components(g))
# for wcc in wccs:
# 	if len(wcc) > 500:
# 		for w in wcc:
# 			print ('entity = ', w)
# 			triples_l, cardinality_l = hdt.search_triples(w, rdfs_label, "")
# 			for (s_l, p_l, o_l) in triples_l:
# 				print ('\thas rdfs_label ', o_l)
#
# 			triples_l, cardinality_l = hdt.search_triples(w, skos_preflabel, "")
# 			for (s_l, p_l, o_l) in triples_l:
# 				print ('\thas skos:preflabel ', o_l)


print ('For the biggest one:')
ct_prefix = Counter()
wccs = list(nx.weakly_connected_components(g))
for wcc in wccs:
	if len(wcc) > 500:
		for w in wcc:
			p = get_prefix(w)
			ct_prefix[p] += 1

for p in ct_prefix.keys():
	print(p, ' has ', ct_prefix[p])

print ('Overall:')
ct_prefix = Counter()
ct_authority = Counter()
wccs = list(nx.weakly_connected_components(g))
for wcc in wccs:
	# if len(wcc) > 100 and len(wcc) < 200:
	for w in wcc:
		p = get_prefix(w)
		ct_prefix[p] += 1
		a = get_authority(w)
		ct_authority[a] += 1

print ('\n Namespace')
for (p, ct) in ct_prefix.most_common(20):
	print('\t',p, ' has ', ct)

print ('\n Authority')
for (p, ct) in ct_authority.most_common(20):
	print('\t',p, ' has ', ct)
