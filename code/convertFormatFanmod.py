import os
from igraph import *
## Create edgelist-formated files for fanmod programs

def convert():#F6F67B#F6F67B
	oldpath = "/home/amm/Desktop/sna-project/sna-git/data/"
	newpath = "/home/amm/Desktop/sna-project/shared_windows/motif/edgelist/"
	error_list = []
	#fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
	for fname in os.listdir(oldpath):
		## get source nodes
		
		if os.path.isdir(oldpath+fname): continue
		if fname.endswith("~"): continue
		try: 
			print "\n"
			print fname
			f_w = open(newpath+fname.strip(".gml"), "w")
			g = read(oldpath+fname, format="gml").simplify()
			for e in g.es():
				src = int(g.vs[e.source]["id"])
				dest = int(g.vs[e.target]["id"])
				if src in (9999, 99999) or dest in (9999, 99999): continue
				line = str(src)+" "+str(dest)+"\n"
				f_w.write(line)
			f_w.close()
			
		except:
			error_list.append(fname)
			#print error_list 
 		
		
		
	 
	
convert()
