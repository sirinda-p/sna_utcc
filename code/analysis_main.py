import os
from igraph import *


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
	  


## main function to compute properties of subgraphs
def computeProperty(group_arr, g, directed):
	#make a subgraph
	property_list = []
	 
	for group in group_arr:
		gsize = len(group)
		 
		if gsize>1:
 			
			subg = g.subgraph(group) 
 			den, dia, max_deg, avg_edge_btw, edge_conn = property_network(subg,directed)
 			
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
  			
 			property_list.append([gsize, den, dia, max_deg[0], max_deg[1], avg_edge_btw, edge_conn,avg_deg[0],avg_deg[1], avg_gpa])
		 
 	 	
	return property_list
		
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
	
	#print (avg_edge_btw,edge_conn)
	
	return den, dia, max_deg, avg_edge_btw, edge_conn
	 

	
## calculate properties of each node
def property_node(subg):
	
	eigenvector_centrality() # set directed=True/ False for directed graph
	degree()
	hub_score()
	g.closeness()
	
	
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
	path = "/home/amm/Desktop/sna-git/data/"
	result_path = "/home/amm/Desktop/sna-git/result/analysis/"
	
	for ftype in [ "bf.gml","friend.gml", "study.gml"]:
		if ftype == "friend.gml":
			directed = False
		else:
			directed = True
		
		f_w = open(result_path+"property_alldept_"+ftype.replace(".gml",""),"w")
		f_w.write("gsize, den, dia, max_indeg, max_outdeg, avg_edge_btw, edge_conn,avg_indeg,avg_outdeg, avg_gpa\n")
		
		
		for fname in os.listdir(path):
			#if fname != "Niti55_bf.gml": continue
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
					
				print "#nodes = "+str(len(g.vs()))
				
				## get connected subgraphs" 
				for gtype in ["component"]:#, "edge"
					group_arr = findGroups(g, gtype)
					#colorNodes(group_arr, g, fname, gtype)
					property_list = computeProperty(group_arr, g, directed)
					for l in property_list:
						print l
						f_w.write(str(l).lstrip("[").rstrip("]"))
						f_w.write("\n")
			except:
				print "\n"
				continue
				
		f_w.close() 
		
		
''' 
	TO DO
	1. Plot subgraphs - done 
	2. Detect overlapping community
	3. Try other community detection algorithm
	4. Compute graph properties - done
		- Centrality 
		- Density
		- Degree distribution
		- Diameter 
	5. Mark unsurveyed nodes - done
	6. Get GPA - done
	6.1 Write the properties and GPA to a file - done
	7. Compute correlation between graph properties and GPA
	8. Take unsurveyed nodes into account when analyzing data
	9. Find a way to measure interaction patterns in communities
	
	TO CROSS-CHECK with raw data
	1. Edge links 
	2. Unsurveyed students
	
'''	

main()  
