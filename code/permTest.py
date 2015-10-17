import os
from igraph import *
import random 
import edgeswap   
import networkx as nx

## permute edges while fixing node degree and direction
def permute(g, isDirected):
	all_nodes = g.vs()
	idlist = [v.index for v in all_nodes]
	
	nodes2add = set()
	
	newg = g.copy()
	## delete all edges
	newg.delete_edges(None)
	
	for v in all_nodes:
		vid = v.index
		
		if isDirected:
 
			inDeg = v.indegree()
			outDeg = v.outdegree()
			
			random.shuffle(idlist)
			in_nbs = set(idlist[0:inDeg])
			nodes2add.union(in_nbs)
			for u in in_nbs:
				newg.add_edges((u,vid))
			
			random.shuffle(idlist) 
			out_nbs = set(idlist[0:outDeg])
			nodes2add.union(out_nbs)
			for u in in_nbs:
				newg.add_edges((vid,u))
 
		else:
			 
			Deg = v.degree()
			
	for v, newv in zip(g.vs(), newg.vs()):
		print ( v.indegree(), newv.indegree())	
 	
	
	

def main():
	path = "/home/ubuntu/sna-utcc-research/data/gml/"
	for fname in os.listdir(path):
		print fname
		g = read(path+fname, format="gml").simplify()
		ftype  = fname.split("_")[1]
		
		if ftype== "friend.gml":
			isDirected = False
		else:
			isDirected = True
		
		
		permuter = EdgeSwapGraph(g)
		newg = permuter.randomize_by_edge_swaps(5)
		
		break
		
main()
