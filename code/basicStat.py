import os
from igraph import *

def count():
 	newpath = "/home/amm/Desktop/sna-git/data/mark_unsurveyed/"
	error_list = []
	fname_list = ["ICT55_bf.gml","ICT55_friend.gml","ICT55_study.gml"]
	for fname in fname_list:
	for fname in os.listdir(oldpath):
		 
 		src_set = set()
		f_r = open(oldpath+fname,"r")
		hash_reverse_pair = {}
		for line in f_r.readlines():
			if len(line.split())>1:
				fst, snd = line.split()
 				if fst.strip() == "source":
					sid = snd.strip() 
					src_set.add(float(sid))
					
 		#try:
 		print "\n"
		print  oldpath+fname
		g = read(oldpath+fname, format="gml")
		 
		all_set = set(g.vs['id'])
		
		unmarked_set = all_set - src_set
		
		for v in g.vs:
		 
			if v['id'] in unmarked_set:
				 
				v["survey"] = False
				
			else:
				v["survey"] = True
		
		hash_reverse_pair = dict()
		for e in g.es():
			sid = g.vs[e.source]['id']
			tid = g.vs[e.target]['id']
			if tid not in hash_reverse_pair:
				hash_reverse_pair[tid] = [sid]
			else:
				hash_reverse_pair[tid].append(sid)
		
			
		### get nodes referring to the unsurveyed nodes
		for node in unmarked_set:
			if node in hash_reverse_pair:
				flist = hash_reverse_pair[node]
				
				print str(node)+":"+str(flist)
			
		  
		print "Total nodes = "+str(len(all_set))
		print "surveyed nodes = "+str(len(src_set))
		print "Unsurveyed nodes = "+str(len( unmarked_set))
		#print "Unsurveyed nodes = "+str(unmarked_set)
		
		write(g, newpath+fname, format = "gml")
				
 		#except e:
			#error_list.append(fname)
			#print e
			
 
	
mark()
