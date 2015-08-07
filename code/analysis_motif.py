import os
from igraph import *

# make motif outputs in gml format
def 

def main():
	path = "/home/amm/Desktop/sna-git/result/motif/raw/" ## raw motif outputs from fanmod
	result_path = "/home/amm/Desktop/sna-git/result/motif/gml/" ## motif outputs from fanmod in gml (for visualization)
	
 
		
	for fname in os.listdir(path):
		try:
			ftype2 = fname.split("_")[1]
			if ftype2 != ftype:
				continue
			print "\n"
			print fname
			
			if ftype2 == "friend.gml":
				g = read(path+fname, format="gml").as_undirected()
			else:
				g = read(path+fname, format="gml") 
				
				

