import os
import igraph as ig
import numpy
import stat_myutil as mystat 
import math
import mycfinder as cfinder
import collections, itertools
from itertools import combinations, product
from sklearn.metrics import jaccard_similarity_score, pairwise
 
def getSigSubgNumber(outfile, fanmod_path, size):
	f = open(fanmod_path+outfile, "r")
	lines = f.readlines()
	lenlines = len(lines)
	f.close()
	i = 0
	sigNo_arr = []
	while i<lenlines:
		line = lines[i]
		if line.startswith("Result"):
			i+=5
			line = lines[i]
			#no, x1,x2, x3,x4, x5, pvalue = line.split()
 			no, x1, x2, x3, x4, x5, pvalue = line.split(",")
			if float(pvalue) <0.05:
				#bin_no = '{0:09b}'.format(int(no))
				sigNo_arr.append((int(no)))
			i+=size+1
			while 1:
				if i>=lenlines: break
				line = lines[i]
  				 
				no, x1, x2, x3, x4, x5, pvalue = line.split(",")
				
				if float(pvalue) <0.05:
					#bin_no = '{0:09b}'.format(int(no))
					
					sigNo_arr.append(int(no))
				i+=size+1
				
			break
		else:
			i+=1
 
	return sigNo_arr


def getGPAhash(dumpfile,gml_path):
	
	#gname = dumpfile.replace(".txt.OUT.dump",".gml")
	gname = dumpfile.replace(".txt.csv.dump",".gml")
	g = ig.read(gml_path+gname, format="gml").simplify()
	id_gpa_hash = dict()
	for v in g.vs():
		nid = v['id']
		gpa = v['gpa']
		id_gpa_hash[int(nid)] = gpa
	
	return id_gpa_hash

def calAvgGPA(node_arr, id_gpa_hash):
	
	n = len(node_arr)
	gpa_arr = []
	for i in range(1, n):
		gpa_arr.append( id_gpa_hash[int(node_arr[i])])
	
	gpa_numarr = numpy.array(gpa_arr)
	
	std = numpy.std(gpa_arr)
	mean = numpy.mean(gpa_arr)
 
	return  (mean, std)
	
def getAvgGPAall(gml_path, fanmod_path, dumpfile, sigNo_arr, f_sig, f_nonsig):
	
	id_gpa_hash = getGPAhash(dumpfile,gml_path)	
	
	f = open(fanmod_path+dumpfile, "r")
	lines = f.readlines()
	f.close()
	
	motif_meanGPA_hash = dict()
	motif_stdGPA_hash = dict()
	 
	for i in range(2,len(lines)):
	 
		line = lines[i]
		node_arr = line.split(",")
		motifID = int(node_arr[0],2) 
		mean, std = calAvgGPA(node_arr, id_gpa_hash)
		
		if motifID in motif_meanGPA_hash:
			motif_meanGPA_hash[motifID].append(mean)
			motif_stdGPA_hash[motifID].append(std)
		else:
			motif_meanGPA_hash[motifID] = [mean]
			motif_stdGPA_hash[motifID] = [std]
	
	numarr = numpy.array(id_gpa_hash.values())

	tow = "All: %5.4f %5.4f\n" %(numpy.mean(numarr),numpy.std(numarr))
	f_sig.write(tow)
	f_nonsig.write(tow)
	
	## get mean gpa of all subgraphs with the same motif id 
	## separate significant and non-significant motifs
	sig_arr = []
	nonsig_arr = [] 
	for motifId in motif_meanGPA_hash.keys():
		
		mean_of_mean = sum(motif_meanGPA_hash[motifId])/len(motif_meanGPA_hash[motifId])
		mean_of_std = sum(motif_stdGPA_hash[motifId])/len(motif_stdGPA_hash[motifId])
		
		
		if  motifId in sigNo_arr:
			sig_arr.append((motifId, mean_of_mean, mean_of_std))
		else:
			nonsig_arr.append((motifId, mean_of_mean, mean_of_std))
	
	 
	for data in sig_arr:
		tow = "%3d, %5.4f %5.4f\n" %(data[0],data[1],data[2])
		f_sig.write(tow )
	
	
	for data in nonsig_arr:
		tow = "%3d, %5.4f %5.4f\n" %(data[0],data[1],data[2])
		f_nonsig.write(tow )			
	f_sig.write("\n")
	f_nonsig.write("\n")
		

			
def getNodesInMotif(size, g, mfile, directed, sig_motifID_arr, vall):
	## Analyze only a complete motif (complete graph) 
	cmotif = 0
	if directed: 
		nedge = size*(size-1)
	else:
		nedge =  size*(size-1)/2
		
	
	## get node number for each node id 
	number_hash = dict()
	
	for v, i in zip(vall, range(0,len(vall))):
		number_hash[v] = i
	
	selected_node = set()	
	motif_hash = dict()
	## extract subgraphs and get nodes in those significant subgraphs
	for line in mfile.readlines()[2::]:
		
		if size == 2:
			motif_id, n1, n2  = 	line.strip().split(",")
			temp = [float(n1), float(n2) ] 
		if size == 3:
			motif_id, n1, n2, n3 = 	line.strip().split(",")
			temp = [float(n1), float(n2), float(n3)] 
			
 		elif size == 4:
			motif_id, n1, n2, n3, n4 = line.strip().split(",")
			temp = [float(n1), float(n2), float(n3), float(n4)]
		
		
		motif_id = 	int(motif_id,2) 
 	
		if motif_id in sig_motifID_arr:
			node_arr = set(number_hash[key] for key in temp)
			
			subg = g.subgraph(node_arr)
			if len(subg.es()) == nedge:
				motif_hash[cmotif] = node_arr
				cmotif += 1
				selected_node = selected_node.union(set(temp))
			
			elif len(subg.es()) > nedge:
				print "Something is wrong. Number of edges in the graph exceeds the maximum number of edges" 
	
	#print (len(selected_node), len(vall))
 
	return selected_node, cmotif, motif_hash
		
def main_correlation(): 
	machine = "ubuntu"
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
 
	fanmod_basepath = prefix+"/result/motif/fanmod/"
	result_path = prefix+"result/motif/analysis/"
	gml_path = prefix+"data/gml/notempnode/"
	
	
	for size in ([ 4]): ## need to change node ids in motifs of ICT57  
 		flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55","Niti56","HM Act57","HM Korea57","HM Thai57","Nited56", "Biz55", "EC55"]

 		type_arr = ["friend","bf", "study"] # 
		fanmod_path = fanmod_basepath+str(size)+"nodes/"
		print "size "+str(size)
		f_w = open(result_path+"one-tailed_2sampleTest_gpa_motifSize"+str(size)+"VSall2.txt", "w")
		for t in type_arr:
			print t
			f_w.write(t+" (Name, t-stat, one-tailed pvalue (nan = no motif found)\n")
			for fname in flist:
				
				if t == "friend":
					directed = False
					g = ig.read(gml_path+fname+"_"+t+".gml", format="gml").as_undirected().simplify()
				else:
					directed = True
					g = ig.read(gml_path+fname+"_"+t+".gml", format="gml").simplify()
				 
				node_all = [n['id'] for n in g.vs() ]
				outfile = fname + "_"+t+".txt.csv" 
				dumpfilename= fname + "_"+t+ ".txt.csv.dump"
 				dfile = open(fanmod_path+dumpfilename, "r")
				## Get significant subgraphs numbers in outfile
				if size == 2:
					sigNo_arr = [1] 
				else:
					sigNo_arr = getSigSubgNumber(outfile, fanmod_path, size)	
							 
				motif_nodes, cmotif = getNodesInMotif(size, g, dfile, directed, sigNo_arr,node_all)
				print cmotif
				nonmotif_nodes = set(node_all).difference(set(motif_nodes))
				tval, pval = mystat.test2Means(motif_nodes, nonmotif_nodes, g)
				'''
				if math.isnan(pval):
					print fname
					print (len(motif_nodes),len(nonmotif_nodes))
				tow = "%15s, %5.4f, %5.4f\n" %(fname, tval.item(), pval)
				f_w.write(tow)
				 '''
			f_w.write("\n") 
			 
	 	f_w.close()

def calSim(comm_hash, g, att, att_type, all_keys):
	##Within group 
	within_sim_arr = []
	for key, comm in comm_hash.items():
		tt = 0.
		count = 0
		for (x,y) in combinations(comm, 2):
			if att_type =="nom":
				if g.vs[x][att] == g.vs[y][att]: 
					count += 1.
			elif att_type == "ord":
				count += pairwise.euclidean_distances(g.vs[x][att],g.vs[y][att])[0][0]
				#print count
			tt += 1
		 
		within_sim_arr.append( count/tt)
	within_sim = sum(within_sim_arr)/len(within_sim_arr)
	
	##Btw group
	btw_sim_arr = []
	for (g1, g2) in combinations(all_keys, 2):
		pair_node_arr = list(itertools.product(comm_hash[g1], comm_hash[g2]))
		tt = 0.
		count = 0
		for (x,y) in pair_node_arr:
			if att_type =="nom":
				if g.vs[x][att] == g.vs[y][att]: 
					count += 1.
			elif att_type == "ord":
				count += pairwise.euclidean_distances(g.vs[x][att],g.vs[y][att])[0][0]
				
			tt += 1
		btw_sim_arr.append(count/tt)
	btw_sim = sum(btw_sim_arr)/len(btw_sim_arr)
	
	return within_sim, btw_sim	
		
def main_variation(): 
	machine = "ubuntu"
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
 
	fanmod_basepath = prefix+"/result/motif/fanmod/"
	result_path = prefix+"result/motif/analysis/"
	gml_path = prefix+"data/gml/gml_moreAtt/ver2/"
	
	comm_type = "motif" #or "motif"
	
	for csize in ([ 4]): ## need to change node ids in motifs of ICT57  
 		flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55","Niti56","HM Act57","HM Korea57","HM Thai57","Nited56", "Biz55", "EC55"]
		if comm_type == "motif":
			type_arr = [ "bf", "friend", "study" ] 
		else:
			type_arr = [ "friend", "study" ,"bf"] 
			
		fanmod_path = fanmod_basepath+str(csize)+"nodes/"
		
		## Cal correlation between a pair of nodes: single variable
		ord_arr_arr = [ "total_income", "father_income", "mother_income" ] ## use cosine similarity
		nom_att_arr = ["entry_degree",  "gender"] ## use jaccard similarity 
			
  		for t in type_arr:
			f_w = open("/home/ubuntu/Desktop/sna_utcc/result/motif/analysis/variance_analysis_"+comm_type+"_"+t+".csv", "w")
			f_w.write("fname, entry_degree_within_sim, entry_degree_btw_sim, gender_within_sim, gender_btw_sim, total_income_within_sim, total_income_btw_sim, father_income_within_sim, father_income_btw_sim, mother_income_within_sim, mother_income_btw_sim\n")
  			
  			for fname in flist:
				print fname
				if t == "friend":
					directed = False
					g = ig.read(gml_path+fname+"_"+t+".gml", format="gml").as_undirected().simplify()
				else:
					directed = True
					g = ig.read(gml_path+fname+"_"+t+".gml", format="gml").simplify()
				 
				node_all = [n['id'] for n in g.vs() ]
				outfile = fname + "_"+t+".txt.csv" 
				dumpfilename= fname + "_"+t+ ".txt.csv.dump"
 				dfile = open(fanmod_path+dumpfilename, "r")
				## Get significant subgraphs numbers in outfile
				if csize == 2:
					sigNo_arr = [1] 
				else:
					sigNo_arr = getSigSubgNumber(outfile, fanmod_path, csize)	
				
				if comm_type == "motif":
								 
					motif_nodes, cmoti, comm_hash = getNodesInMotif(csize, g, dfile, directed, sigNo_arr,node_all)
 				else: # use clique percolation
					###
					comm_hash = cfinder.cfinder(g, csize)
					#clique_arr = g.cliques(min=csize, max=csize)
				
				## Add total_income = father_income + mother_incomoe 
				g.vs["total_income"] = [v["father_income"]+v["mother_income"] for v in g.vs]
 
				all_keys = comm_hash.keys()
 				if len(comm_hash.keys())<2: continue
 				att_sim_all_arr = []
 				
 				att_type = "nom"
				for att in nom_att_arr:
					#print att
 					within_sim, btw_sim	 = calSim(comm_hash, g, att, att_type, all_keys)
					att_sim_all_arr.append((within_sim, btw_sim	))
					
				att_type = "ord"	
 				for att in ord_arr_arr:	 
					 
 					within_sim, btw_sim	 = calSim(comm_hash, g, att, att_type, all_keys)
					att_sim_all_arr.append((within_sim, btw_sim	))
				
				
				val = str(att_sim_all_arr).replace("[","").replace("(","").replace(")","").replace("]","")
				print val
				to_w = fname+","+val+"\n"
				f_w.write(to_w)
			f_w.close()
					
def main(): 
	
	fanmod_path = "/home/ubuntu/Desktop/sna_utcc/result/motif/fanmod/"
	result_path = "/home/ubuntu/Desktop/sna_utcc/result/motif/analysis/"
	gml_path = "/home/ubuntu/Desktop/sna_utcc/data/gml/notempnode/"
	'''
	fanmod_basepath = "/home/amm/Desktop/sna-project/sna-git/result/motif/fanmod/"
	result_path = "/home/amm/Desktop/sna-project/sna-git/result/motif/analysis/"
	gml_path = "/home/amm/Desktop/sna-project/sna-git/data/gml/notempnode/"
	'''
	
	for size in range(3,5):  
		flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55","Niti56","HM Act57","HM Korea57","HM Thai57","Nited56", "Biz55", "EC55"]
		type_arr = [ "friend", "study", "bf"]
		fanmod_path = fanmod_basepath+str(size)+"nodes/"
		print size
		for t in type_arr:
			print t
			f_sig = open(result_path+t+"_sigMotif_"+str(size)+"nodes_gpa.txt", "w")
			f_nonsig = open(result_path+t+"_nonsigMotif_"+str(size)+"nodes_gpa.txt", "w")
			for fname in flist:
				f_sig.write(fname+"\n")
				f_nonsig.write(fname+"\n")
				
				#outfile = fname + "_"+t+".txt.OUT"
				outfile = fname + "_"+t+".txt.csv"
				#dumpfile= fname + "_"+t+ ".txt.OUT.dump"
				dumpfile= fname + "_"+t+ ".txt.csv.dump"
				
				## Get significant subgraphs numbers in outfile
				#print outfile
				sigNo_arr = getSigSubgNumber(outfile, fanmod_path, size)
				 
				getAvgGPAall(gml_path, fanmod_path, dumpfile, sigNo_arr, f_sig, f_nonsig)
					
				
			f_sig.close()
			f_nonsig.close()
		
			 
main_variation()











'''

				att_freq_hash = dict()
				vall = [ v.index for v in g.vs()]
				for att in ["gender", "minor_programname"]:
 					att_arr_all = [g.vs[v][att] for v in vall]
  					att_freq_hash[att] = [collections.Counter(att_arr_all)]
 				
				att_arr_all = [g.vs[v]["father_income"]+g.vs[v]["mother_income"]for v in vall]
 				att_freq_hash["income"] = [collections.Counter(att_arr_all)]
				
				if len(	comm_hash.keys())== 0: continue
				print len(comm_hash.keys())
				continue
				for comm in comm_hash.values():
  					## get a list of feature values 
					## gender 
					print comm
					for att in ["gender", "minor_programname"]:
 						
						att_arr_clique = [g.vs[c][att] for c in comm]
  						att_freq_hash[att].append(collections.Counter(att_arr_clique))
					
					
					#freq_list.append(letter_freqs)
					
					## income 
					income_arr = [g.vs[c]["father_income"]+g.vs[c]["mother_income"]for c in comm]
					att_freq_hash["income"].append(collections.Counter(income_arr))	
			 
				print ""		
 				for att, freq_arr in att_freq_hash.items():
					print att 
					for freq in freq_arr:
						print freq
					
					print ""
'''
