
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
from collections import Counter
from hdt import HDTDocument, IdentifierPosition
import glob
from urllib.parse import urlparse
import gzip
# from extend_metalink import *
import requests
from requests.exceptions import Timeout

rdfs_label = "http://www.w3.org/2000/01/rdf-schema#label"

PATH_LOD = "/scratch/wbeek/data/LOD-a-lot/data.hdt"
hdt = HDTDocument(PATH_LOD)

name = '""'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", "",  name+xml_string)
print ('there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"person"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", "",  name+xml_string)
print ('[anything] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"person"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", rdfs_label,  name+xml_string)
print ('[rdfs:label] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"Person"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", "",  name+xml_string)
print ('[anything] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"Person"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(triples, cardinality) = hdt.search_triples("", rdfs_label,  name+xml_string)
print ('[rdfs:label] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')
for (s,p,o) in triples:
	print ('subject  : ', s)
	# print ('predicate: ', p)

name = '"people"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", "",  name+xml_string)
print ('[anything] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"people"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", rdfs_label,  name+xml_string)
print ('[rdfs:label] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')

name = '"People"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", "",  name+xml_string)
print ('[anything] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


name = '"People"'
xml_string = '^^<http://www.w3.org/2001/XMLSchema#string>'
(_, cardinality) = hdt.search_triples("", rdfs_label,  name+xml_string)
print ('[rdfs:label] there are ', cardinality, ' about ', name, ' in the LOD-a-lot')


#eq_class
eq_class = "http://www.w3.org/2002/07/owl#equivalentClass"
foaf_person = "http://xmlns.com/foaf/0.1/Person"


eq_collect = set()
foaf_person = ''
eq_collect.add(foaf_person)


triples, direct_eq_relations = hdt.search_triples("", eq_class, foaf_person)
for (s,p ,o) in triples:
	eq_collect.add(str(s))

triples, direct_eq_relations = hdt.search_triples(foaf_person, eq_class, "")
for (s,p ,o) in triples:
	eq_collect.add(str(o))

#
record = 0
closure_coll = eq_collect.copy()
# while len(closure_coll) != record : # untill the size does not expand anymore.
# 	record = len(closure_coll)
# 	newly_found = set()
# 	for t in closure_coll:
#
# 		triples, cardinality = hdt.search_triples("", eq_class, t)
# 		for (s,p,o) in triples:
# 			newly_found.add(str(s))
#
# 		triples, cardinality = hdt.search_triples(t, eq_class, "")
# 		for (s,p,o) in triples:
# 			newly_found.add(str(o))
#
# 	closure_coll = closure_coll.union (newly_found)


count_eq_rel_triples = 0
ct_eq = Counter()
for eq_rel in closure_coll:
	triples, cardinality = hdt.search_triples("", eq_rel, "")
	ct_eq[eq_rel] =  cardinality
	count_eq_rel_triples += cardinality


count = 0
for p in closure_coll:
	if ct_eq[p] > 0:
		print(p, 'has ', ct_eq[p])
