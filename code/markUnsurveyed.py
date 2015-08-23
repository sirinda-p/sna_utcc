import os
from igraph import *

def mark():
	oldpath = "/home/amm/Desktop/sna-git/data/"
	newpath = oldpath+"mark_unsurveyed/"
	error_list = []
	#fname_list =["ICT57-All_friend.gml" ]
	fname_list = sorted(os.listdir(oldpath))
	ttsv = 0
	for fname in fname_list:
	#for fname in os.listdir(oldpath):
		## get source nodes
 		if os.path.isdir(oldpath+fname): continue
 		if fname.split(".")[1] !="gml": continue
 		#if not fname.startswith("ICT57-All"): continue
		src_set = set()
		f_r = open(oldpath+fname,"r")
		hash_reverse_pair = {}
 		for line in f_r.readlines():
			 
			if len(line.split())>1:
				try:
					fst, snd = line.split()
				except:
					print fname
 				if fst.strip() == "source":
					sid = snd.strip() 
					src_set.add(float(sid))
		print "\n"			
 		print  oldpath+fname			
 		
		 
		g = read(oldpath+fname, format="gml")
		print "Successful reading gml" 
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
				
				#print str(node)+":"+str(flist)
			
		tt = len(all_set)-1.
		sv = len(src_set)
		ttsv += sv
		print "Total nodes = "+str(tt)
		sv_p = int(sv/tt*100)
		print "surveyed nodes = "+str(sv)+"("+str(sv_p)+")"
		usv = len( unmarked_set)-1
		
		print "Unsurveyed nodes = "+str(usv)
		#print "Unsurveyed nodes = "+str(unmarked_set)
		
		#write(g, newpath+fname, format = "gml")
					
 		#except  :
			#print "error"
			#error_list.append(fname)
		
		#print error_list
		#print len(error_list)
 
	print ttsv/3
	
mark()
