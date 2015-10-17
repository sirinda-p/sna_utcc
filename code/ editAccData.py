import igraph as ig

## Remove nodes not in a class list 
def main():
	gml_path = "/home/ubuntu/sna-utcc-research/data/gml/Ac57_bf.gml"
	g = ig.read(gml_path+gname,  format="gml").simplify()
	min_id = 287
	max_id = 312
	
	for v in g.vs():
		if v[id] in range(287,312):
			print v

main()
