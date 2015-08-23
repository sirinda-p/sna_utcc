import os
from igraph import *

def mark():
	oldpath = "/home/amm/Desktop/sna-git/data/"
	newpath = oldpath+"mark_unsurveyed/"
	error_list = []
	fname_list = ["ICT55_friend.gml","ICT55_bf.gml","ICT55_study.gml"]
	for fname in fname_list:
	#for fname in os.listdir(oldpath):
		## get source nodes
		 
 		f_r = open(oldpath+fname,"r")
 		id_set = set()
		lines = f_r.readlines()
		
		for line in lines:
		
			if len(line.split())>1:
				fst, snd = line.split()
 				 
  				if fst.strip()=="id":
					newid = snd.strip()[5::]
					if newid not in id_set:
						id_set.add(newid)
		
			
		 
		## get IDs not in id_set (IDs still in official student list but are unreachable)
		## These IDs won't appear as 'source' but can be 'target'
		## Have to remove those edges whose targets are the unreachable
		
		
 		
		
		
	 
	
mark()
