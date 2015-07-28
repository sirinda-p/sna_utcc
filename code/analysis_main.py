import igraph  as ig

def main():
	path = "/home/amm/Desktop/sna-git/data/"
	fname = "test.gml"
	print path+fname
	#g = ig.Graph.Full(3)
	g = ig.read(path+fname, format="gml")
	

main()  
