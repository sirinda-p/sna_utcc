import os
from igraph import *

def check():
	path = "/home/ubuntu/sna-utcc-research/data/gml/"
 
	error_list = []
 
	for fname in os.listdir(path):
	#for fname in os.listdir(oldpath):
		## get source nodes
		if not fname.startswith("Niti55"): continue
		print fname
 		f_r = open(path+fname,"r")
 		id_set = set()
		lines = f_r.readlines()
		f_r.close()
		for line in lines:
		
			if len(line.split())>1:
				fst, snd = line.split()
 				 
  				if fst.strip()=="id":
					newid = snd.strip()
					id_set.add(newid)
					
		print  len(id_set)
		missingID = set()
		allnode = set()
		for line in lines:
		
			if len(line.split())>1:
				fst, snd = line.split()
				
   				if fst.strip()=="source" or fst.strip()=="target" :
					mid = snd.strip()
					allnode.add(mid)
					if mid not in id_set:
						missingID.add(mid)
		
		print missingID
		print  id_set
		print allnode
 		
def dupID():
	oldpath = "/home/amm/Desktop/sna-git/data/"
	 
	error_list = []
	fname_list = ["ICT57-All_friend.gml"]
	for fname in fname_list:
	#for fname in os.listdir(oldpath):
		## get source nodes
		print oldpath+fname 
 		f_r = open(oldpath+fname,"r")
 		
		lines = f_r.readlines()
		f_r.close()
		
		id_set = set()
		dup_set = set()
		for line in lines:
		
			if len(line.split())>1:
				fst, snd = line.split()
 				 
  				if fst.strip()=="id":
					newid = snd.strip()
					if newid not in id_set:
						id_set.add(newid)
					else:
						dup_set.add(newid)
					
		print  dup_set
			 
		
	 
	
check()
