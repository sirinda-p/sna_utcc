import os
from igraph import *
import numpy as np
import scipy.stats
import stat_myutil as mystat 
import randomizationGraphUtil as randomutil
import myutil as myutil
import communityUtil as commutil
import mycfinder as cfinder
 

def readMotif(fanmod_path, fname, t, size, g, directed):
	
	node_all = [n['id'] for n in g.vs() ]
	outfile = fname + "_"+t+".txt.csv" 
	dumpfilename= fname + "_"+t+ ".txt.csv.dump"
	dfile = open(fanmod_path+dumpfilename, "r")
 	## Get significant subgraphs numbers in outfile
	if size == 2:
		sigNo_arr = [1] 
	else:
		sig_motifID_arr = getSigSubgNumber(outfile, fanmod_path, size)	
	
	node_all = [n['id'] for n in g.vs() ]
	## set of nodes in each clique			 
	motif_hash = getNodesInMotif(size, g,  directed, sig_motifID_arr, node_all, dfile)
	 
	print len(motif_hash.keys())
	
def main_diversity():

	machine = "ubuntu"
 	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/motif/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	fanmod_basepath = prefix+"/result/motif/fanmod/"
	
	for csize in ([4]): 
		flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55","Niti56","HM Act57","HM Korea57","HM Thai57","Nited56", "Biz55", "EC55"]
		type_arr = ["bf", "friend", "study"]

		for t in type_arr:
			 
			## get percentage of male and female in each community and perform 2-mean test 
			for fname in flist:
				print fname+"_"+t
 				
 				if t == "friend":
					directed = False
 					g = read(gml_path+fname+"_"+t+".gml", format="gml").as_undirected().simplify()
				else:
					directed = True
					g = read(gml_path+fname+"_"+t+".gml", format="gml").simplify() 	
				
				comm_hash = cfinder.cfinder(g, csize)
				
				for comm in comm_hash.values():
				 
					## get a list of feature values 
					## gender 
					gender_arr = [g.vs[c]["gender"] for c in comm]
					
					## income 
					income_arr = [g.vs[c]["gender"] for c in comm]
					mather_arr = [g.vs[c]["gender"] for c in comm]
					
					# minor
				
				'''
				clique_arr = g.cliques(min=csize, max=csize)
				##get attribute values of members in each clique
				cid = 0 
				clique_hash = dict()
				gender_hash = dict()
				print len(clique_arr)
				#for clique in clique_arr:
				'''	
				

main_diversity()
 				
			  
