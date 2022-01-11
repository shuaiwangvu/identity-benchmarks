# http://www.w3.org/2002/07/owl#TransitiveProperty


from hdt import HDTDocument, IdentifierPosition
import pandas as pd
import numpy as np
import datetime
import pickle
import time
import networkx as nx
import sys
import csv
from z3 import *
from bidict import bidict
import matplotlib.pyplot as plt
import tldextract
import json
import random
from tarjan import tarjan
from collections import Counter

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt = HDTDocument(PATH_LOD)


t = "http://www.w3.org/2002/07/owl#TransitiveProperty"
s = "http://www.w3.org/2002/07/owl#SymmetricProperty"
antiS = "http://www.w3.org/2002/07/owl#AntisymmetricProperty" # not sure about this one
aS = "http://www.w3.org/2002/07/owl#AsymmetricProperty"
r = "http://www.w3.org/2002/07/owl#ReflexiveProperty"
iR = "http://www.w3.org/2002/07/owl#IrreflexiveProperty"

owl_sameas = "http://www.w3.org/2002/07/owl#sameAs"
owl_equivalent_property = "http://www.w3.org/2002/07/owl#equivalentProperty"

skos_exactMatch = "http://www.w3.org/2004/02/skos/core#exactMatch"
skos_broadMatch = "http://www.w3.org/2004/02/skos/core#broadMatch"
skos_broader = "http://www.w3.org/2004/02/skos/core#broader"
skos_narrowMatch = "http://www.w3.org/2004/02/skos/core#narrowMatch"
skos_narrower = "http://www.w3.org/2004/02/skos/core#narrower"
skos_relatedMatch = "http://www.w3.org/2004/02/skos/core#relatedMatch"
skos_closeMatch = "http://www.w3.org/2004/02/skos/core#closeMatch"

type = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

subClassOf = 'http://www.w3.org/2000/01/rdf-schema#subClassOf'
subPropertyOf = 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf'

broader = 'http://www.w3.org/2004/02/skos/core#broader'
narrower = 'http://www.w3.org/2004/02/skos/core#narrower'

inv = 'http://www.w3.org/2002/07/owl#inverseOf'


eq_collect = set()

eq_collect.add(owl_sameas)
eq_collect.add(skos_exactMatch)
eq_collect.add(skos_closeMatch)

triples, direct_eq_relations = hdt.search_triples("", owl_equivalent_property, owl_sameas)
for (s,p ,o) in triples:
	eq_collect.add(str(s))

triples, direct_eq_relations = hdt.search_triples(owl_sameas, owl_equivalent_property, "")
for (s,p ,o) in triples:
	eq_collect.add(str(o))

triples, direct_eq_relations = hdt.search_triples("", owl_equivalent_property, skos_exactMatch)
for (s,p ,o) in triples:
	eq_collect.add(str(s))

triples, direct_eq_relations = hdt.search_triples(skos_exactMatch, owl_equivalent_property, "")
for (s,p ,o) in triples:
	eq_collect.add(str(o))

count_eq_rel_triples = 0
ct_eq = Counter()
for eq_rel in eq_collect:
	triples, cardinality = hdt.search_triples("", eq_rel, "")
	ct_eq[eq_rel] =  cardinality
	count_eq_rel_triples += cardinality

print ('there are in total ', count_eq_rel_triples, ' triples among these relations')


triples, total_triples = hdt.search_triples("", "", "")
print ('that gives ', count_eq_rel_triples/ total_triples , ' overall (of all triples in LOD-a-lot)')




record = 0
closure_coll = eq_collect.copy()
while len(closure_coll) != record : # untill the size does not expand anymore.
	record = len(closure_coll)
	newly_found = set()
	for t in closure_coll:
		triples, cardinality = hdt.search_triples("", subPropertyOf, t)
		for (s,p,o) in triples:
			# print('new:',s,p,o)
			newly_found.add(str(s))

		triples, cardinality = hdt.search_triples("", owl_equivalent_property, t)
		for (s,p,o) in triples:
			# print('new:',s,p,o)
			newly_found.add(str(s))

		triples, cardinality = hdt.search_triples(t, owl_equivalent_property, "")
		for (s,p,o) in triples:
			# print('new:',s,p,o)
			newly_found.add(str(o))

		triples1, cardinality1 = hdt.search_triples("" ,inv, t)
		for (s,p,o) in triples1:
			# print('new:',s,p,o)
			newly_found.add(str(s))

		triples1, cardinality1 = hdt.search_triples(t ,inv, '')
		for (s,p,o) in triples1:
			# print('new:',s,p,o)
			newly_found.add(str(o))
	closure_coll = closure_coll.union (newly_found)

print ('After computing the closure, there are in total', len (closure_coll), ' relations in the set')


# count how many triples are there in total
count_triples_trans = 0
for p in closure_coll:
	triples, cardinality = hdt.search_triples("", p, "")
	ct_eq[p] = cardinality
	count_triples_trans += cardinality
print ('under closure = ', count_triples_trans)
print ('that gives ', count_triples_trans/ total_triples , ' overall')

print ('=========================================================================')



ct = {}

count = 0
for p in closure_coll:
	if ct_eq[p] > 0:
		print(p, 'has ', ct_eq[p])

#
# print ('Now the extended part: ')
# eq_collect_large = []
#
# ct = {}
#
# count = 0
# for p in closure_coll:
# 	t_triples, t_cardinality = hdt.search_triples("", p, "")
# 	if t_cardinality > 100000: # over 100,000
# 		eq_collect_large.append(p)
# 		print ('trans: ', p, ' : ', t_cardinality)
# 		ct[p] = t_cardinality
# 		count += 1
#
# print ('# trans: count over million: ', count)
