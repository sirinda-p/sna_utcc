import os
from igraph import *
import numpy as np
import stat_myutil as mystat 

def findCommunity(g, technique):
	 
	if technique == "fastgreedy":
		group_arr = g.community_fastgreedy().as_clustering()
	else:
		group_arr = g.community_edge_betweenness().as_clustering()
		
	return  group_arr ## each group contains internal node ids (not my id)

def getNodeInCommunity(g, group_arr):
	node_set = set()
	for   group in group_arr:
		gsize = len(group)
		 
		if gsize>1:
			for n in group:
				node_set.add(g.vs[n]['id'])
	return node_set 
	
def calCommunityProperty(g, group_arr):
	avggpa_all, stdgpa_all = getNodeAttribute(g)
	print ("All", avggpa_all, stdgpa_all )
	for group in group_arr:
		gsize = len(group)
			 
		if gsize>1:
	 			
			subg = g.subgraph(group) 
			avg_gpa, std_gpa = getNodeAttribute(subg)
			print (gsize, avg_gpa, std_gpa)
	

def getNodeAttribute(g):
	 
	#get avg gpa
	sum_gpa = 0
	gpa_arr = []
	for n in g.vs():
		gpa =  n['gpa']
		gpa_arr.append(gpa)
 		 
	gpa_numarr = np.array(gpa_arr)
	
	std_gpa = np.std(gpa_arr)
	avg_gpa = np.mean(gpa_arr)
	
 	return avg_gpa, std_gpa
	  
							 
 
def main(): 
	 
	machine = "ubuntu"
	technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
	print technique
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/community/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	
	flist = ["Niti56","Ac57", "Biz55", "EC55","Eng55","HM Act57","HM Korea57","HM Thai57","ICT55","ICT56","ICT57-All","Nited56","Niti55"]
	type_arr = ["bf", "friend", "study"]
	
	f_w = open(result_path+"one-tailed_2sampleTest_gpa_Community"+str(technique)+"VSall.txt", "w")
	for t in type_arr:
		f_w.write(t+" (Name, t-stat, one-tailed pvalue)\n") 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			print fullname
			if t == "friend":
			
				g = read(gml_path+fullname, format="gml").as_undirected().simplify()
			else:
				if technique == "fastgreedy":
					g = read(gml_path+fullname, format="gml").as_undirected().simplify() 	
				else:
					g = read(gml_path+fullname, format="gml").simplify() 	
			
			comm_arr = findCommunity(g, technique)
			node_set = getNodeInCommunity(g,comm_arr)
			 
			tval, pval = mystat.test2Means([n['id'] for n in g.vs() ],node_set  , g)  
			tow = "%15s, %5.4f, %5.4f\n" %(fname, tval.item(), pval)
			f_w.write(tow)
			#calCommunityProperty(g, comm_arr)
 
		f_w.write	("\n")
			
			
		
			 
			 
			 
			 
			 
			 
			 
			
main()
