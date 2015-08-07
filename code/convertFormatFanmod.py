import os
from igraph import *
## Create edgelist-formated files for fanmod programs

def convert():
	oldpath = "/home/amm/Desktop/sna-git/data/"
	newpath = oldpath+"edgelist/"
	error_list = []
	#fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
	for fname in os.listdir(oldpath):
		## get source nodes
 
		try: 
			print "\n"
			print fname
			f_w = open(newpath+fname.strip(".gml"), "w")
			g = read(oldpath+fname, format="gml")
			for e in g.es():
				line = str(int(g.vs[e.source]["id"]))+" "+str(int(g.vs[e.target]["id"]))+"\n"
				f_w.write(line)
			f_w.close()
			
		except:
			error_list.append(fname)
			#print error_list 
 		
		
		
	 
	
convert()
