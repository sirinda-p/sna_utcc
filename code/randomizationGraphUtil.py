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

def swapedges_withAttributes(ftype, g, gpa_intID_hash, gender_intID_hash ):
 	
	if ftype== "friend":
		print "get out seq"
		out_seq = [v.degree() for v in g.vs()]
		print "create random graph" ## taking too long. need to change this function
		newg = ig.Graph.Degree_Sequence(out_seq, method="no_multiple")
			
	else:
		isDirected = True
		out_seq = [v.outdegree() for v in g.vs()]
		in_seq = [v.indegree() for v in g.vs()]
		## nodes in newg have the same internal ids as nodes in g
		#print out_seq
		#print in_seq
		try:
			print "create random graph" 
			newg = ig.Graph.Degree_Sequence(out_seq, in_seq, method="no_multiple")
		except Exception as e :
			print e
			
			raise e
	print "get attributes"
	for v in newg.vs():
		v['gpa'] = gpa_intID_hash[v.index]
		v['gender'] = gender_intID_hash[v.index]

	return newg


def ER_withAttributes(ftype, gpa_intID_hash,  n,m ):
	
	if ftype== "friend":
  		
		newg = ig.Graph.Erdos_Renyi(n=n,  m=m, directed=False, loops=False)
			
	else:
		newg = ig.Graph.Erdos_Renyi(n=n,  m=m, directed=True, loops=False)
		
	for v in newg.vs():
		v['gpa'] = gpa_intID_hash[v.index]
 
	return newg
		
		
