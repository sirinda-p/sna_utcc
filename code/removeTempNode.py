import os
from igraph import *

def main():
	path = "/home/amm/Desktop/sna-git/data/gml/"
	newpath = "/home/amm/Desktop/sna-git/data/gml/notempnode/"
	
	
	for fname in os.listdir(path):
		if fname.endswith ("gml"): continue
		print fname
		g = read(path+fname, format="gml")
		 
		for v in g.vs():
			if v['id'] in [99999.0, 9999.0]:
 				g.delete_vertices(v)				 
		write(g,  newpath+fname)

 
def main2():
	path = "/home/amm/Desktop/sna-git/data/gml/"
	newpath = "/home/amm/Desktop/sna-git/data/gml/notempnode/"
	
	
	for fname in ["ICT57-All_friend.gml"]:
 		g = read(newpath+fname, format="gml").as_undirected().simplify()
		 
		for v in g.vs():
			print (v['id'], v.degree())

main2()

