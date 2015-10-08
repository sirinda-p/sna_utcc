import os
from igraph import *
import numpy as np

''' old code '''
def findGroups(g, gtype):
	
	if gtype == "component":
		#print "\nStrongly connected components"
		group_arr = g.components(mode='STRONG')
 		
 	elif gtype == "edge":
 		#print "\nCommunity: edge betweenness"
		group_arr = g.community_edge_betweenness().as_clustering()
 		
 	
	group_size_hash = dict()
	for group in group_arr:
		l = len(group)
		if l not in group_size_hash:
			group_size_hash[l] = 1
		else:
			group_size_hash[l] += 1
			
	#for pair in group_size_hash.items():
		#print 	pair
		
	return  group_arr

def getNodeAttribute(g,gsize):
	 
	#get avg gpa
	sum_gpa = 0
	for n in g.vs():
		gpa =  n['gpa']
 		sum_gpa += gpa
	avg_gpa = sum_gpa/gsize
 	return avg_gpa
	  

def computeProperty_groups(group_arr, g, directed):
	#make a subgraph
	property_list = []
	 
	for group in group_arr:
		gsize = len(group)
		 
		if gsize>1:
 			
			subg = g.subgraph(group) 
  			den, dia, max_deg, avg_edge_btw, edge_conn,avg_deg, gcc, lcc, avg_gpa = computeProperty(subg,directed)
  			property_list.append([gsize, den, dia, max_deg[0], max_deg[1], avg_edge_btw, edge_conn,avg_deg[0],avg_deg[1], gcc, lcc, avg_gpa])
  	 	
	return property_list
	
## main function to compute properties of for each connected component
def computeProperty(subg,directed,gsize):
 	
	den, dia, max_deg, avg_edge_btw, edge_conn, gcc, lcc = property_network(subg,directed)
	
	if directed:
		 
		indegree_arr =  subg.indegree()
		avg_indegree = sum(indegree_arr)/len(indegree_arr) 
		outdegree_arr = subg.outdegree()
		avg_outdegree = sum(outdegree_arr)/len(outdegree_arr)
		avg_deg = (avg_indegree,avg_outdegree )
	
	else:
		deg_arr = subg.degree()
		avg = sum(deg_arr)/len(deg_arr)
		avg_deg = (avg,avg)
		
	avg_gpa = getNodeAttribute(subg,gsize)
	
	return den, dia, max_deg, avg_edge_btw, edge_conn,avg_deg, gcc, lcc, avg_gpa
 
		
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
 
	return den, dia, max_deg, avg_edge_btw, edge_conn, gcc, lcc
	 

	 
	
	
## calculate properties of each node and return nodes with 5 highest scores
def property_node(g, isdirected, k):
	 
	v_arr = g.vs["id"]
 	ev_arr = g.evcent(isdirected) # set directed=True/ False for directed graph
	topK_ev = getTopK(ev_arr, v_arr, k)
	print "Top "+str(k)+" eigenvector :"+str(topK_ev)
	
	if isdirected: 
		indeg_arr = g.indegree()
		topK_indeg = getTopK(indeg_arr, v_arr, k)
		print "Top "+str(k)+" indegree :"+str(topK_indeg)
		outdeg_arr = g.outdegree()
		topK_outdeg = getTopK(outdeg_arr, v_arr, k)
		print "Top "+str(k)+" outdegree :"+str(topK_outdeg)
	else:
		deg_arr = g.degree()
		topK_deg = getTopK(deg_arr, v_arr, k)
		print "Top "+str(k)+" degree :"+str(topK_deg)
	 
	hub_arr = g.hub_score()
	topK_hub = getTopK(hub_arr, v_arr, k)
	print "Top "+str(k)+" hub_score :"+str(topK_hub)
	
	closeness_arr = g.closeness()
	topK_closeness = getTopK(closeness_arr, v_arr, k)
	print "Top "+str(k)+" closeness :"+str(topK_closeness)

	tran_arr = g.transitivity_local_undirected() 
	topK_tran = getTopK(tran_arr, v_arr, k)
	print "Top "+str(k)+" local cc :"+str(topK_tran)
	
def colorNodes(group_arr, g, fname, gtype ):
	
	
	num_group = len(group_arr)
	color_dict = {0:"blue", 1:"green", 2:"red", 3:"cyan", 4:"magenta", 5:"yellow", 6:"black" }
	i = 0
	print "num groups = "+str(num_group)
	for group in group_arr:
		
		if len(group) == 1:
			for node in group:
				g.vs[node]["color"] = "white"
 		else:
			print "group "+str(i)
			for node in group:
				
				g.vs[node]["color"] = color_dict[i]
			i+=1
	gname = "/home/amm/Desktop/sna-git/result/"+fname.replace(".gml","")+"_"+gtype+".png"
	plot(g,gname)  

		
def main():
	path = "/home/ubuntu/sna-utcc-research/data/gml/"
	result_path = "/home/ubuntu/sna-utcc-research/result/analysis/"
	
	analysis = "whole" # whole graph or community
	
	for ftype in [ "bf.gml","friend.gml", "study.gml"]:
		
		if analysis == "community":
			f_w = open(result_path+"property_community_alldept_"+ftype.replace(".gml",""),"w")
			f_w.write("gsize, den, dia, avg_indeg, max_outdeg, avg_edge_btw, edge_conn,avg_indeg,avg_outdeg, gcc, lcc, avg_gpa\n")
		else:
			f_w = open(result_path+"property_wholegraph_alldept_"+ftype.replace(".gml",""),"w")
			
		
		if ftype == "friend.gml":
			directed = False
			f_w.write("Name, Den, Dia, Avg_deg, Max_deg, Avg_edge_btw, Edge_conn, GCC, LCC\n")
		else:
			directed = True
			f_w.write("Name, Den, Dia, Avg_indeg, Avg_outdeg, Max_indeg, Max_outdeg, Avg_edge_btw,Edge_conn, GCC, LCC\n")
		
		
		#fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
		for fname in os.listdir(path):
			fshort = fname.split("_")[0]	
  			try:
				ftype2 = fname.split("_")[1]
				if ftype2 != ftype:
					continue
				print "\n"
				print fname
				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected()
				else:
					g = read(path+fname, format="gml") 
				
				gsize = len(g.vs())
				 
				
				if analysis == "community":
					## get connected subgraphs" 
					for gtype in ["component"]:#, "edge"
						group_arr = findGroups(g, gtype)
						colorNodes(group_arr, g, fname, gtype)
						 
						property_list = computeProperty(group_arr, g, directed)
						
						for l in property_list:
							print l
							f_w.write(str(l).lstrip("[").rstrip("]"))
							f_w.write("\n")
			 
				else:
					k=3
					
 					#property_node(g,directed, k)
 					gsize = len(g.vs())
				 	
					den, dia, max_deg, avg_edge_btw, edge_conn,avg_deg, gcc, lcc, avg_gpa = computeProperty(g, directed,gsize)
				 	

					#f_w.write("gsize, den, dia,avg_indeg,avg_outdeg, max_indeg, max_outdeg, avg_edge_btw, edge_conn, gcc, lcc, avg_gpa\n")
					if directed:
						 
						str2write = "%s, %3.2f, %3.2f, %3d, %3d, %3d, %3d, %3d, %3.2f,%3.2f, %3.2f " %(fshort, den, dia,avg_deg[0],avg_deg[1], max_deg[0], max_deg[1], avg_edge_btw, edge_conn, gcc, lcc)
 					
					else:
						 
						str2write = "%s, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f, %3.2f,%3.2f, %3.2f " %(fshort, den, dia,avg_deg[0], max_deg[0], avg_edge_btw, edge_conn, gcc, lcc)
					 	#"Den, Dia, Max_deg, Avg_deg, Avg_edge_btw, Edge_conn, GCC, LCC
					print  str2write
					f_w.write(str2write+"\n")
						
 
						
			except:
				print "\n"
				continue
				
		f_w.close() 
		
		
''' 
	TO DO
	x	1. Plot subgraphs  
		2. Detect overlapping community
		3. Try other community detection algorithm
	x	4. Compute graph properties 
			- Density
			- Degree distribution
			- Diameter 
			- Global clustering coefficient
	x	5. Compute node properties  
			- Centrality: degree, hub, closeness
			- Local clustering coefficient
			
	x	6. Mark unsurveyed nodes  
	x	7. Get GPA  
			- Write the properties and GPA to a file 
	x	8. Compute correlation between graph properties and GPA
	 	9. Take unsurveyed nodes into account when analyzing data
		10. Find a way to measure interaction patterns in communities 
			- Use motifs
		11. Analyze motifs detected by fanmod
		
		TO CROSS-CHECK with raw data (paper survey)
		1. Edge links 
		2. Unsurveyed students (check with the unsurveyed nodes)
	
'''	

main()  
