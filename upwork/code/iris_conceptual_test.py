from pprint import pprint
from random import shuffle
from concept_formation.cobweb3 import Cobweb3Tree
from concept_formation.cluster import cluster
from concept_formation.datasets import load_iris


def cobweb():
	
	irises = load_iris()
	shuffle(irises)

	tree = Cobweb3Tree()
	irises_no_class = [{a: iris[a] for a in iris if a != 'class'} for iris in irises]
	tree.fit(irises_no_class)
	
	print len(irises )
	print "nodes in tree"
	i = 0
	
	rootnode = tree.root 
	print rootnode
	print "" 
	for k, v in rootnode.items():
		print (k,v)
	clusters = k_cluster(tree, irises_no_class, 3)[0]
	 
	 
main()
