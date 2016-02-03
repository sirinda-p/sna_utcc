import igraph as ig

def getDyad(g):
	dyad_arr = []
	for e in g.es():
		if g.is_mutual(e):
			 
			x = g.vs()[e.tuple[0]]["id"]
			y = g.vs()[e.tuple[1]]["id"] 
			dyad_arr.append((x,y) )
			 
	return dyad_arr
	
def main():
	machine = "ubuntu"
	ttype = "friend"
	comm_technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
	print comm_technique
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	path = prefix+"/data/gml/notempnode/"
	result_path =  prefix+"result/motif/fanmod/2nodes/"
	
 	flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55","Niti56","HM Act57","HM Korea57","HM Thai57","Nited56", "Biz55", "EC55"]

	for ftype in [ "bf.gml" , "study.gml"]: #[ "bf.gml","friend.gml", "study.gml"]:
 					
		for fname in flist:
			print fname
			inname = fname+"_"+ftype
			outname = inname.replace(".gml", ".txt.csv.dump")
			f_w = open(result_path+outname , "w")
			
			if ftype  == "friend.gml":
				g = ig.read(path+inname, format="gml").as_undirected().simplify()
			else:
				g = ig.read(path+inname, format="gml").simplify()
				
			dyad_arr = getDyad(g)
			f_w.write("Number of subgraphs: "+str(len(dyad_arr))+"\nFormat: adjacency matrix, <participating vertices>\n")
			 
			
			for (x,y) in dyad_arr:
				tow = "1,"+str(x).replace(".0","")+","+str(y).replace(".0","")+"\n"
				f_w.write(tow)
			f_w.close()
		
main()
