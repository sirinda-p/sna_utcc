import os
from igraph import *

def mark():
	oldpath = "/home/amm/Desktop/sna-git/data/"
	newpath = oldpath+"mark_unsurveyed/"
	error_list = []
	fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
	for fname in fname_list:
		## get source nodes
		print "\n"
		print fname
		 
		src_set = set()
		f_r = open(oldpath+fname,"r")
		for line in f_r.readlines():
			if len(line.split())>1:
				fst, snd = line.split()
				if fst.strip() == "source":
					nid = snd.strip()
					src_set.add(float(nid))
		 
		try:
			g = read(oldpath+fname, format="gml")
			all_set = set(g.vs['id'])
		
			unmarked_set = all_set - src_set
			
			for v in g.vs:
				 
				if v['id'] in unmarked_set:
					 
					v["survey"] = False
				else:
					v["survey"] = True
				 
			print "Total nodes = "+str(len(all_set))
			print "surveyed nodes = "+str(len(src_set))
			print "Unsurveyed nodes = "+str(len(unmarked_set))
			
			write(g, newpath+fname, format = "gml")
				
 		except:
			error_list.append(fname)
			print error_list
			
	 
		
 		
		
		
	 
	
mark()
