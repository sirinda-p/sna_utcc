import os
from igraph import *
import numpy as np
import scipy.stats
import stat_myutil as mystat 
import randomizationGraphUtil as randomutil
import myutil as myutil
import communityUtil as commutil
import mycfinder as cfinder
import collections, itertools


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
	gml_path = prefix+"data/gml/gml_moreAtt/"	 	
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
				#clique_arr = g.cliques(min=csize, max=csize)
				
				att_freq_hash = dict()
				vall = [ v.index for v in g.vs()]
				for att in ["gender", "minor_programname"]:
 					att_arr_all = [g.vs[v][att] for v in vall]
  					att_freq_hash[att] = [collections.Counter(att_arr_all)]
 				
				att_arr_all = [g.vs[v]["father_income"]+g.vs[v]["mother_income"]for v in vall]
 				att_freq_hash["income"] = [collections.Counter(att_arr_all)]
					
				for comm in comm_hash.values():
				#for comm in clique_arr: 
					## get a list of feature values 
					## gender 
					for att in ["gender", "minor_programname"]:
 						
						att_arr_clique = [g.vs[c][att] for c in comm]
  						att_freq_hash[att].append(collections.Counter(att_arr_clique))
					
					
					#freq_list.append(letter_freqs)
					
					## income 
					income_arr = [g.vs[c]["father_income"]+g.vs[c]["mother_income"]for c in comm]
					att_freq_hash["income"].append(collections.Counter(income_arr))	
						
 				for att, freq_arr in att_freq_hash.items():
					print att 
					for freq in freq_arr:
						print freq
					
					print ""
					
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
 				
			  
