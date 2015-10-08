import os
import igraph as ig

## Remove nodes not in a class list 
def main():
	gml_path = "/home/ubuntu/sna-utcc-research/data/gml/"
	
	for gname in os.listdir(gml_path):
		if not gname.startswith("Ac"): continue
		print gname
		g = ig.read(gml_path+gname,  format="gml")
		min_id = 227
		max_id = 312
		notinlist = [228+1, 242+1, 243, 308, 306, 303, 280, 252]
		todel_list = []
		c = 0
		print len(g.vs())
		print len(g.es())
		for v in g.vs():
			if v['id'] in notinlist:
				todel_list.append(v)
			elif v['id'] not in range(min_id-1,max_id+1):
				todel_list.append(v)
			 
		g.delete_vertices(todel_list)
		
		newname = gname.replace("raw","")
		ig.write(g, gml_path+newname, format="gml")
	 
	 	newg = ig.read(gml_path+newname, format="gml")
	 	print len(newg.vs())
		print len(newg.es())
		
		
main()
