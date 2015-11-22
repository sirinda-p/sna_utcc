from pprint import pprint
from random import shuffle
from concept_formation.cobweb3 import Cobweb3Tree
from concept_formation.cluster import cluster
from concept_formation.datasets import load_iris


def cobweb(data, attname_arr):
	
 	shuffle(irises)

	tree = Cobweb3Tree()
	cobweb_data = []
	for row in data:
		 
		cobweb_data.append({att_name: att_val for att_val, att_name in zip(row, attname_arr) })
			
	#cobweb_data = [{a: iris[a] for a in iris } for row in data]
	
	tree.fit(cobweb_data)
	
	print len( cobweb_data)
	print "nodes in tree"
	pprint(tree.root.output_json())
	
	 
