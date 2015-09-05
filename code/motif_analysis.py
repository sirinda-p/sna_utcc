import os
import igraph as ig

def myplot(result_path, fname, g, size):
	
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
		
		
		
	'''	
	num_group = len(group_arr)
	color_dict = {0:"blue", 1:"green", 2:"red", 3:"cyan", 4:"magenta", 5:"yellow", 6:"black" }
	i = 0
	print "num groups = "+str(num_group)
	for group in group_arr:
		
		if len(group) == 1:
			for node in group:
				g.vs[node]["color"] = "white"
 		else:
			print "group "+str(i)
			for node in group:
				
				g.vs[node]["color"] = color_dict[i]
			i+=1
	gname = "/home/amm/Desktop/sna-git/result/"+fname.replace(".gml","")+"_"+gtype+".png"
	plot(g,gname)   '''
	
def main(): 
	result_path = "/home/amm/Desktop/sna-project/shared_windows/motif/results/"
	gml_path = "/home/amm/Desktop/sna-project/sna-git/data/gml/"
	size = 3 
	fname_list = ["ICT56_friend.gml","ICT56_bf.gml","ICT56_study.gml"]
	for fname in os.listdir(result_path):
		
		if fname.endswith(".csv.dump"):
			print fname
			gname = fname.strip(".csv.dump")+".gml"
  			g = ig.read(gml_path+gname,  format="gml")
			myplot(result_path, fname, g, size)
			 
			
main()
