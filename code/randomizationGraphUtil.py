import os
import igraph as ig 

def swapedges(ftype, g):
	if ftype== "friend":
 
		out_seq = [v.degree() for v in g.vs()]
		newg = ig.Graph.Degree_Sequence(out_seq, method="no_multiple")
			
	else:
		isDirected = True
		out_seq = [v.outdegree() for v in g.vs()]
		in_seq = [v.indegree() for v in g.vs()]
		## nodes in newg have the same internal ids as nodes in g
		newg = ig.Graph.Degree_Sequence(out_seq, in_seq, method="no_multiple")
		
	return newg

 
