import os
from igraph import *
import numpy  as np
import myutil as myutil

''' old code ''' 
## Measure structure properties of a network 
def measureProperty(g, directed, k):
	
	'''
	Structure properties:
	- Centrality
		- Degree  x
		- Hub (directed only) x
		- Authority (directed only) x
		- Betweenness  x

	'''
	v_arr = g.vs()
 
	if directed:
		## Degree centrality

		indegree_arr =  g.indegree()
 		outdegree_arr = g.outdegree()
 		
 		topk_indegree_node_arr, topk_indegree_score_arr = myutil.getTopK(indegree_arr, v_arr, k)
 		topk_outdegree_node_arr, topk_outdegree_score_arr  = myutil.getTopK(outdegree_arr, v_arr, k)

		hub_arr = g.hub_score() 
		topk_hub_node_arr, topk_hub_score = myutil.getTopK(hub_arr, v_arr, k)
	 
		authority_arr = g.authority_score() 
		topk_authority_node_arr, topk_authority_score = myutil.getTopK(authority_arr, v_arr, k)
	
 		betweenness_arr = g.betweenness(directed=True)
		topk_di_betweenness_node_arr, topk_di_betweenness_score = myutil.getTopK(betweenness_arr, v_arr, k)
		
		assort_di = g.assortativity(types1="gpa", directed=True)
		
		
	deg_arr = g.degree()
	pvalue = power_law_fit(deg_arr,return_alpha_only=False).p
	
	# Assortativity is a preference for a network's nodes to attach to others that are similar in some way	
	# When r = 1, the network is said to have perfect assortative mixing patterns
 	# when r = 0 the network is non-assortative
	# while at r = −1 the network is completely disassortative
	
	assort_gpa = g.assortativity(types1="gpa", directed=False)
	for v in g.vs():
		if v["gender"] == "M":
			v["sex"] = 1
		else:
			v["sex"] = 0
			
	assort_gender = g.assortativity(types="sex", directed=False)
	print (assort_gpa,assort_gender)
	 
	# assortativity degree - measure if nodes tend to be connected with other nodes with similar degree values.
	# r=1: high degree nodes tend to attach to high degree nodes
	# r=0: low degree nodes tend to attach to low degree nodes
	assort_degree = g.assortativity_degree(directed=True)
	
	topk_degree_node_arr, topk_degree_score_arr  = myutil.getTopK(deg_arr, v_arr, k)
	betweenness_arr = g.betweenness(directed=False)
	topk_betweenness_node_arr, topk_betweenness_score = myutil.getTopK(betweenness_arr, v_arr, k)
	

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
 

		
def main_basic():
	path = "/home/amm/Desktop/sna-git/data/"
	result_path = "/home/amm/Desktop/sna-git/result/analysis/"
		
	for ftype in [ "bf.gml","friend.gml", "study.gml"]:
		
		f_w = open(result_path+"BasicProperty_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		if ftype == "friend.gml":
			directed = False
			f_w.write("DeptName, gsize, den, dia, max_deg, avg_deg, edge_conn, gcc, lcc, avg_gpa\n")
		else:
			directed = True
			f_w.write("DeptName, gsize, den, dia, max_indeg, max_outdeg, avg_indeg, avg_outdeg, edge_conn, gcc, lcc, avg_gpa\n")
		
		
		#fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
		err_list = []
		for fname in os.listdir(path):
		#for fname in fname_list:
  			try:
				ftype2 = fname.split("_")[1]
				if ftype2 != ftype:
					continue
 				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected().simplify()
				else:
					g = read(path+fname, format="gml").simplify()
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
			
			
		 
			

		
def main_structure():
	path = "/home/ubuntu/sna-utcc-research/data/gml/"
	result_path = "/home/ubuntu/sna-utcc-research/result/analysis/"
		
	for ftype in [ "study.gml", "bf.gml","friend.gml"]:
		
		#f_w = open(result_path+"BasicProperty_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		if ftype == "friend.gml":
			directed = False
			#f_w.write("DeptName, gsize, den, dia, max_deg, avg_deg, edge_conn, gcc, lcc, avg_gpa\n")
		else:
			directed = True
			#f_w.write("DeptName, gsize, den, dia, max_indeg, max_outdeg, avg_indeg, avg_outdeg, edge_conn, gcc, lcc, avg_gpa\n")
		
		
		fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
		err_list = []
		for fname in os.listdir(path):
		#for fname in fname_list:
			if os.path.isdir(path+fname): continue
 			
			ftype2 = fname.split("_")[1]
			if ftype2 != ftype:
				continue
			print fname
  			try:
				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected().simplify()
				else:
					g = read(path+fname, format="gml").simplify() 
			except:
				
				err_list.append(fname)
				
				continue
			k =5	
			v_arr = g.vs()
			fshort = fname.split("_")[0]		
			
			measureProperty(g, directed, k)
			
			
			 
 			if directed:
				tow = "%10s, %3d, %5.2f, %5.2f, %3d,%d, %5.2f, %5.2f, %5.2f, %5.2f, %5.2f\n " %(fshort, gsize, den, dia, max_deg[0], max_deg[1], avg_deg[0], avg_deg[1], edge_conn, gcc, lcc )
			else:
				tow = "%10s, %3d, %5.2f, %5.2f, %3d, %5.2f, %5.2f, %5.2f, %5.2f\n " %(fshort, gsize, den, dia, max_deg[0], avg_deg[0], edge_conn, gcc, lcc )
			f_w.write(tow) 								
			 
			
		#f_w.close
		print "Error list"
		for f in err_list:
			print f
				
'''
Basic properties:
- Avg degree
- Density
- Diameter
- Clustering coefficient (local and global)
- Connectivity

Structure properties:
- Centrality 
	- Degree x
	- Hub (directed only) x
	- Authority (directed only) x
	- Betweenness x
- Homophily  x
- Small world (friend) -> may be unnecessary since each network is quite small
- Power law distribution (study) x

Useful code examples - awesome visualization! http://cneurocvs.rmki.kfki.hu/igraph/screenshots2.html
'''

main()  
