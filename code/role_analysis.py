import igraph as ig
import communityUtil as commutil

def getCliqueMembers(comm_arr, g):	
	clique_members = set()
	all_members = set()
	for comm in comm_arr:
		comm_set = set(comm)
		comm_size = len(comm_set)*1.0
		if comm_size<2: continue
		for n in comm:
			##get all edges of each node
			all_members.add(n) 
			nbrs = set(g.neighbors(n))
			intersect_size = len(nbrs.intersection(comm_set))
			 		
			if (intersect_size/comm_size) > 0.75:
			 
				clique_members.add(n)
				
	return clique_members, all_members 
	
def getIsolators(g, directed, nodeid_surveyed_set):
	isolator_index_all = set()
	isolator_id_set = set()
	for v in g.vs():
		if directed:		 
			if v.indegree()<2 and v.outdegree()<1:
				isolator_index_all.add(v.index)
				isolator_id_set.add(v['id'])
		else:
			if v.degree() <1 :
				isolator_index_all.add(v.index)	
				isolator_id_set.add(v['id'])
				
	isolator_id_surveyed = set(isolator_id_set.intersection(nodeid_surveyed_set))
	return isolator_index_all	, isolator_id_surveyed						

def getBrokers(comm_arr, isolator_all, g, clique_members):
	
	all_nodes = set([v.index for v in g.vs()])
 	## find brokers who have 2 links to clique members (or 2 links to other brokers)
 	potential_brokers  = all_nodes.difference(isolator_all).difference(clique_members)
	broker_set = set()

	for b in potential_brokers:
		b_neighbors = set([v.index for v in g.vs[b].neighbors()])
		##check if b has 2 links to cliques members
	 
		if len(b_neighbors.intersection(clique_members))>1:
			 broker_set.add(b)
	
	## find other brokers who have 2 linls with other brokers	

	for b in potential_brokers:
		b_neighbors = set([v.index for v in g.vs[b].neighbors()])
		##check if b has 2 links to cliques members
	 
		if len(b_neighbors.intersection(broker_set))>1:
			 broker_set.add(b)
			 	 
	return broker_set
	
def main():
	## Rely on a community detction technique ** must record what technique is used ** 
	## Find clique members, brokers, isolators
	## community has 3+ members
	## clique members have >50% of their links within group 
	## brokers  are not in any community but have at least 2 links to non-isolators
	## Isolators have less than 2 links (undirected) and less than 1 in-link and out-link
	## Steps: find clique members, isolators then brokers
	
	machine = "ubuntu"
	comm_technique = "fastgreedy" #"edge_btwness" ## edge_btwness (for directed graphs)
	print comm_technique
	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/community/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	surveyd_gml_path =  prefix+"data/surveyed_only/"
	flist = ["Niti56","Ac57", "Biz55", "EC55","Eng55","HM Act57","HM Korea57","HM Thai57","ICT55","ICT56","ICT57-All","Nited56","Niti55"]
	type_arr = ["bf", "friend", "study"]
	 
	for t in type_arr:
		 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			print fullname
			if t == "friend":
				directed = False
				g = ig.read(gml_path+fullname, format="gml").as_undirected().simplify()
				surveyed_g = ig.read(surveyd_gml_path+fullname, format="gml").as_undirected().simplify()
			else:
				directed = True
				if comm_technique == "fastgreedy":
					g = ig.read(gml_path+fullname, format="gml").as_undirected().simplify() 	
					surveyed_g = ig.read(surveyd_gml_path+fullname, format="gml").as_undirected().simplify() 						
				else:
					g = ig.read(gml_path+fullname, format="gml").simplify() 
					surveyed_g = ig.read(surveyd_gml_path+fullname, format="gml").simplify() 	
			
			nodeid_surveyed_set = set([v['id'] for v in surveyed_g.vs])
			
			## find communities
			comm_arr = commutil.findCommunity(g, comm_technique)
			## find clique members
			clique_members_set, all_members = getCliqueMembers(comm_arr, g)
			## find isolators
			isolators_index_all_set, isolators_id_surveyed_set = getIsolators(g, directed, nodeid_surveyed_set)
			## find brokers
			broker_set = getBrokers(comm_arr, isolators_index_all_set, g, clique_members_set)
		 	
		 	noposition_member_set = 
			## check a relationship between positions in communities and grade 
			
			gpa_clique_arr =  [g.vs[idx]['gpa'] for idx in  clique_members_set]
			gpa_broker_arr =  [g.vs[idx]['gpa'] for idx in  broker_set]
			gpa_isolator_arr = [g.vs[idx]['gpa'] for idx in  isolators_index_all_set]
			print "#cliques"
			if len(gpa_clique_arr)>0:
				print sum(gpa_clique_arr)/len(gpa_clique_arr)
			print "#brokers"
			if len(gpa_broker_arr)>0:
				print sum(gpa_broker_arr)/len(gpa_broker_arr)
			print "#isolators"
			if len(gpa_isolator_arr)>0:
				print sum(gpa_isolator_arr)/len(gpa_isolator_arr)
			 
		print ""
	 
		
		
main()
			
