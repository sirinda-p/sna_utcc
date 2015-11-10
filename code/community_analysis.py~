import os
from igraph import *
import numpy as np
import scipy.stats
import stat_myutil as mystat 
import randomizationGraphUtil as randomutil
import myutil as myutil
import communityUtil as commutil


def getNodeInCommunity(g, group_arr):
	node_set = set()
	for   group in group_arr:
		gsize = len(group)
		 
		if gsize>1:
			for n in group:
				node_set.add(g.vs[n]['id'])
	return node_set 
	
def calAvgStdGPAwithinCommunity(g, group_arr):
	avggpa_comm_arr = []
	stdgpa_comm_arr = []
	for group in group_arr:
		gsize = len(group)
			 
		if gsize>1:
	 			
			subg = g.subgraph(group) 
			avg_gpa, std_gpa = getNodeAttribute(subg)
			#print (gsize, avg_gpa, std_gpa)
			avggpa_comm_arr.append(avg_gpa)
			stdgpa_comm_arr.append(std_gpa)
			
	return avggpa_comm_arr, stdgpa_comm_arr 

def calAvgStdGPAwithinCommunity_4rndCommunity(newg, gpa_intID_hash, group_arr):
	avggpa_comm_arr = []
	stdgpa_comm_arr = []
	
	for group in group_arr:
		gsize = len(group)
			 
		if gsize>1:
	 			
			subg = newg.subgraph(group) 
			avg_gpa, std_gpa = getNodeAttribute_4rndCommunity(subg, gpa_intID_hash)
			#print (gsize, avg_gpa, std_gpa)
			avggpa_comm_arr.append(avg_gpa)
			stdgpa_comm_arr.append(std_gpa)
			
	return avggpa_comm_arr, stdgpa_comm_arr 
	
def getNodeAttribute_4rndCommunity(subg, gpa_intID_hash):
	 
	#get avg gpa
	sum_gpa = 0
	gpa_arr = []
	for v in subg.vs():
		
		gpa =  gpa_intID_hash[v.index]
		gpa_arr.append(gpa)
 		 
	gpa_numarr = np.array(gpa_arr)
	
	std_gpa = np.std(gpa_arr)
	avg_gpa = np.mean(gpa_arr)
	
 	return avg_gpa, std_gpa
 		
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
 	
## Cal p-value to measure a change that random communities will have std of gpa lower than actual communities
def calPvalue4Std(g, ftype, stdgpa_comm_arr, comm_technique,  nrandom):
	
	## cal actual std and stat score (a ratio of communities that have std of gpa of nodes in its communitylower than the the std of  gpas of all nodes) 
	
	avg_all, std_all = getNodeAttribute(g)
	c = 0.
	comm_count = len( stdgpa_comm_arr)
	for std in stdgpa_comm_arr:
		if std < std_all:
			c += 1
			
	gpa_intID_hash  = myutil.getGPAHash_intID(g)
	
	actual_ratio = c/comm_count
	pval_nom = 0.
	for i in range(0, nrandom):
		#Randomize a graph 
		if comm_technique == "fastgreedy":
			rndg = randomutil.swapedges(ftype, g).as_undirected()
		else:
			rndg = randomutil.swapedges(ftype, g)
			
		#Get random communities
		comm_arr = commutil.findCommunity(rndg, comm_technique)
		
		#Get random ratio
	 
		avggpa_comm_arr_rnd, stdgpa_comm_arr_rnd = calAvgStdGPAwithinCommunity_4rndCommunity(rndg, gpa_intID_hash, comm_arr)
		
		rc = 0.
		for std in stdgpa_comm_arr_rnd:
		
			if std < std_all:
				rc += 1
	
		rnd_ratio = rc/len(stdgpa_comm_arr_rnd)
		if rnd_ratio >= actual_ratio:
			pval_nom += 1.
	
	pval = pval_nom/nrandom
	print pval
	
		
				 
def main_std_test(): 
	 
	machine = "ubuntu"
	comm_technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
	print 	comm_technique
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/community/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	
	flist = ["Niti56","Ac57", "Biz55", "EC55","Eng55","HM Act57","HM Korea57","HM Thai57","ICT55","ICT56","ICT57-All","Nited56","Niti55"]
	type_arr = ["bf", "friend", "study"]
	
	#f_w = open(result_path+"one-tailed_2sampleTest_gpa_Community"+str(technique)+"VSall.txt", "w")
	for t in type_arr:
		#f_w.write(t+" (Name, t-stat, one-tailed pvalue (nan = all nodes are a group member))\n") 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			print fullname
			if t == "friend":
			
				g = read(gml_path+fullname, format="gml").as_undirected().simplify()
			else:
				if comm_technique == "fastgreedy":
					g = read(gml_path+fullname, format="gml").as_undirected().simplify() 	
				else:
					g = read(gml_path+fullname, format="gml").simplify() 	
			
			comm_arr = commutil.findCommunity(g, comm_technique)
			avggpa_comm_arr, stdgpa_comm_arr  = calAvgStdGPAwithinCommunity(g, comm_arr)
 			calPvalue4Std(g, t, stdgpa_comm_arr, comm_technique,  nrandom=10)
 			 
 		print ""

def main_diversity():

	machine = "ubuntu"
	comm_technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
	print comm_technique
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/community/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	
	flist = ["Niti56","Ac57", "Biz55", "EC55","Eng55","HM Act57","HM Korea57","HM Thai57","ICT55","ICT56","ICT57-All","Nited56","Niti55"]
	type_arr = ["bf", "friend", "study"]
	##two arrays to keep percentage of male and female in each community
	male_arr = []
	female_arr = []
	for t in type_arr:
		print 
 		## get percentage of male and female in each community and perform 2-mean test 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			#print fullname
			if t == "friend":
			
				g = read(gml_path+fullname, format="gml").as_undirected().simplify()
			else:
				if comm_technique == "fastgreedy":
					g = read(gml_path+fullname, format="gml").as_undirected().simplify() 	
				else:
					g = read(gml_path+fullname, format="gml").simplify() 	
			
			comm_arr = commutil.findCommunity(g, comm_technique)
			gender_freq_list = myutil.countGender(comm_arr, g)
			
			for gender_freq in gender_freq_list:
				m = gender_freq['M']*1.0
				f = gender_freq['F']
				male_arr.append(m/(f+m))
				female_arr.append(f/(f+m))
			 
			
		
		 
		print len(female_arr)
		## Perform paired t test 
		tval, pval = scipy.stats.ttest_rel(male_arr, female_arr)
		print (tval, pval)
		 
		
	
		
 							 
def main_commdectection(): 
	 
	machine = "ubuntu"
	comm_technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
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
		f_w.write(t+" (Name, t-stat, one-tailed pvalue (nan = all nodes are a group member))\n") 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			print fullname
			if t == "friend":
			
				g = read(gml_path+fullname, format="gml").as_undirected().simplify()
			else:
				if comm_technique == "fastgreedy":
					g = read(gml_path+fullname, format="gml").as_undirected().simplify() 	
				else:
					g = read(gml_path+fullname, format="gml").simplify() 	
			
			comm_arr = findCommunity(g, comm_technique)
			avggpa_comm_arr, stdgpa_comm_arr  = calAvgStdGPAwithinCommunity(g, comm_arr)
 			calPvalue4Std(g, t, stdgpa_comm_arr, comm_technique,  nrandom=1000)
 			
			#member_set = getNodeInCommunity(g,comm_arr)
			nonmember_set = set ([n['id'] for n in g.vs() ]).difference(member_set)
			print (len(member_set), len(nonmember_set))
			tval, pval = mystat.test2Means(member_set,nonmember_set  , g)  
			tow = "%15s, %5.4f, %5.4f\n" %(fname, tval.item(), pval)
			f_w.write(tow)
			
 			
		f_w.write	("\n")
 		
			 
			
main_diversity()
