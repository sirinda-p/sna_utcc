import os
import igraph as ig

def plotMotif(result_path, fname, g, size):
	
	f_r = open(result_path+fname,"r")
	
	index_hash = dict()
	for v in g.vs():
		index_hash[v['id']] =  v.index
		v["label"] = v["gpa"]
		
	gidset = dict()	
	for line in f_r.readlines()[2::]:
		l_sp = line.strip().split(",") 
		gid  = int(l_sp[0], 2)
		 
		nodelist =  [index_hash[float(x)] for x in l_sp[1::]]
		subg = g.subgraph(nodelist)
		#for v in subg.vs():
			#print v
			
		plotpath = result_path+"/plots/size"+str(size)+"/"
		#plotpath = "/home/amm/Desktop/sna-project/"
		if gid not in gidset:
			i = 1
		else:
			i = gidset[gid]+1
		
		gidset[gid]	= i
		
		gname =   fname.strip(".csv.dump")+"-id"+str(gid)+"MotifNo"+str(i)+".png"
		print gname
		ig.plot(subg, plotpath+gname )  #
		
 
	
	
def main(): 
	result_path = "/home/ubuntu/Desktop/sna_utcc/results/analysis/"
	gml_path = "/home/ubuntu/Desktop/sna_utcc/data/gml/notempnode/"
	size = 2 
 
	for fname in os.listdir(gml_path):
		 
			
main()
