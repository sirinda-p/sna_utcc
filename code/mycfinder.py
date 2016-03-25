from itertools import combinations

import igraph
import optparse

def cfinder(g, k):

  	cls = map(set, g.maximal_cliques(min=k))

	edgelist = []
	for i, j in combinations(range(len(cls)), 2):
		if len(cls[i].intersection(cls[j])) >= k-1:
			edgelist.append((i, j))
	selected_nodes = set()
	cg = igraph.Graph(edgelist, directed=False)
	clusters = cg.clusters()
 	comm_hash = dict()
	i = 0
	for cluster in clusters:
		members = set()
		for i in cluster:
			selected_nodes.add(i)
			members.update(cls[i])
		comm_hash[i] = members
		i+=1
	
	return comm_hash, selected_nodes 
