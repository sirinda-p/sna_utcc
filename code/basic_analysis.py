
import os
from igraph import *
import numpy as np

## calculate properties of a given network
def property_network(g,directed):
		
	den = g.density()
 	dia = g.diameter()
 	
	if directed:
		max_indeg = g.maxdegree(mode="IN")  
		max_outdeg = g.maxdegree(mode="OUT")  
		#print "Density = "+str(den)+", Diameter = "+str(dia)+", Max in-degree = "+str(max_indeg)+", Max out-degree = "+str(max_outdeg)
		max_deg = (max_indeg,max_outdeg)
	else:
		
		max_deg = (g.maxdegree(), g.maxdegree()) 
		#print "Density = "+str(den)+", Diameter = "+str(dia)+", Max degree = "+str(max_deg)
	 
	eb = g.edge_betweenness() #directed=True/False for directed graphs
	avg_edge_btw = sum(eb)/len(eb)
 	edge_conn = g.edge_connectivity()
	
	## global cc
	gcc = g.transitivity_undirected()
	
	## avg local cc  
	lcc = g.transitivity_avglocal_undirected()
	#print (avg_edge_btw,edge_conn)
	
	return den, dia, max_deg, edge_conn, gcc, lcc
 

## Compute basic properties of a connected component
def computeProperty(g,directed ):
 
	den, dia, max_deg, edge_conn, gcc, lcc = property_network(g,directed)
	
	if directed:
		 
		indegree_arr =  g.indegree()
		avg_indegree = sum(indegree_arr)/len(indegree_arr) 
		outdegree_arr = g.outdegree()
		avg_outdegree = sum(outdegree_arr)/len(outdegree_arr)
		avg_deg = (avg_indegree,avg_outdegree )
	else:
		deg_arr = g.degree()
		avg = sum(deg_arr)/len(deg_arr)
		avg_deg = (avg,avg)
		
	gsize = len(g.vs())   
	return gsize, den, dia, max_deg, edge_conn,avg_deg, gcc, lcc 
 	
def main_basic():
	path = "/home/amm/Desktop/sna-git/data/"
	result_path = "/home/amm/Desktop/sna-git/result/analysis/"
		
	for ftype in [ "bf.gml","friend.gml", "study.gml"]:
		
		f_w = open(result_path+"BasicProperty_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		if ftype == "friend.gml":
			directed = False
			f_w.write("DeptName, gsize, den, dia, max_deg, avg_deg, edge_conn, gcc, lcc\n")
		else:
			directed = True
			f_w.write("DeptName, gsize, den, dia, max_indeg, max_outdeg, avg_indeg, avg_outdeg, edge_conn, gcc, lcc\n")
		
		
 		err_list = []
		for fname in os.listdir(path):
		#for fname in fname_list:
  			try:
				ftype2 = fname.split("_")[1]
				if ftype2 != ftype:
					continue
 				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected()
				else:
					g = read(path+fname, format="gml") 
			except:
				err_list.append(fname)
				continue
				
			fshort = fname.split("_")[0]		
			gsize, den, dia, max_deg, edge_conn,avg_deg, gcc, lcc  = computeProperty(g,directed)
 			if directed:
				tow = "%10s, %3d, %5.2f, %5.2f, %3d,%d, %5.2f, %5.2f, %5.2f, %5.2f, %5.2f\n " %(fshort, gsize, den, dia, max_deg[0], max_deg[1], avg_deg[0], avg_deg[1], edge_conn, gcc, lcc )
			else:
				tow = "%10s, %3d, %5.2f, %5.2f, %3d, %5.2f, %5.2f, %5.2f, %5.2f\n " %(fshort, gsize, den, dia, max_deg[0], avg_deg[0], edge_conn, gcc, lcc )

			f_w.write(tow) 								
			
'''
Basic properties:
- Size
- Avg degree
- Density
- Diameter
- Clustering coefficient (local and global)
- Connectivity
''' 
	
