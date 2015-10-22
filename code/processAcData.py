import os
from igraph import *

# Remove nodes and corresponding edges that are not in the colledted class section
def removeNodeAndEdge():
	
# keep nodes from 5702100227 to 5702100312 
	path = "/home/amm/Desktop/sna-project/sna-git/data/gml/"
	flist = ["Ac57-all_bf.gml","Ac57-all_friend.gml","Ac57-all_study.gml" ]
	
	for fname in flist:
		newfname = fname.replace("-all","-1sec")
		print newfname
		#f_w = open(path+fname, "w")
		g = read(path+fname, format="gml")
		vlist = []
		for v in g.vs():
			if int(v['id']) in range(227, 312):
				vlist.append(v)
			
		
		newg = g.subgraph(vlist) 
		write(newg, path+newfname)
		
		

removeNodeAndEdge()
