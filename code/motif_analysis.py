import os
import igraph as ig
import numpy

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
		
	
def main(): 
	'''
	fanmod_path = "/home/ubuntu/Desktop/sna_utcc/result/motif/fanmod/"
	result_path = "/home/ubuntu/Desktop/sna_utcc/result/motif/analysis/"
	gml_path = "/home/ubuntu/Desktop/sna_utcc/data/gml/notempnode/"
	'''
	fanmod_basepath = "/home/amm/Desktop/sna-project/sna-git/result/motif/fanmod/"
	result_path = "/home/amm/Desktop/sna-project/sna-git/result/motif/analysis/"
	gml_path = "/home/amm/Desktop/sna-project/sna-git/data/gml/notempnode/"
	
	
	for size in (3,4): ## need to find motifs in ICT57 -->change node id to  digits
		flist = ["Niti56","Ac57", "Biz55", "EC55","Eng55","HM Act57","HM Korea57","HM Thai57","ICT55","ICT56","Nited56","Niti55"]
		type_arr = ["bf", "friend", "study"]
		fanmod_path = fanmod_basepath+str(size)+"nodes/"
		for t in type_arr:
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
				print outfile
				sigNo_arr = getSigSubgNumber(outfile, fanmod_path, size)
				 
				getAvgGPAall(gml_path, fanmod_path, dumpfile, sigNo_arr, f_sig, f_nonsig)
					
				
			f_sig.close()
			f_nonsig.close()
		
			 
			 
			 
			 
			 
			 
			 
			
main()
