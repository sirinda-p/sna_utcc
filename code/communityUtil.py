from igraph import *

def findCommunity(g, technique):
	 
	if technique == "fastgreedy":
		group_arr = g.community_fastgreedy().as_clustering()
	else:
		group_arr = g.community_edge_betweenness().as_clustering()
		
	return  group_arr ## each group contains internal node ids (not my id)


