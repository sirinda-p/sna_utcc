import igraph  as ig

def main():
	path = "/media/sf_analysis/data/"
	fname = "test.gml"
	print path+fname
	#g = ig.Graph.Full(3)
	g = ig.read(path+fname, format="gml")
	#print g

main()  
