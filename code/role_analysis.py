import igraph as ig
import communityUtil as commutil
import numpy as np
import collections, itertools
import randomizationGraphUtil as randomutil
import myutil as myutil

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

	for v in g.vs():
		if directed:		 
			if v.indegree()<2 and v.outdegree()<1:
				isolator_index_all.add(v.index)

		else:
			if v.degree() <1 :
				isolator_index_all.add(v.index)	

				
	isolator_index_surveyed = set(isolator_index_all.intersection(nodeid_surveyed_set))
	return isolator_index_all	, isolator_index_surveyed						

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
	
	
def ExtGenderGPA_4rndRoles(g, surveyed_g, comm_technique, nodeid_surveyed_set, rndmnumber, directed, ftype, gpa_intID_hash, gender_intID_hash ):
	
	mratio_arr_hash = dict()
	fratio_arr_hash = dict()
	gpa_role_arr_hash = dict()
	
	for i in range(0,rndmnumber):
	
		if comm_technique == "fastgreedy": ## fastgreedy works on undirected graphs only
			rndg =  randomutil.swapedges_withAttributes("friend", g, gpa_intID_hash, gender_intID_hash).simplify()
		else:
			rndg =  randomutil.swapedges_withAttributes(ftype, g, gpa_intID_hash, gender_intID_hash)
		
		 
		
		gpa_role_hash, mratio_hash, fratio_hash = ExtGenderGPA(rndg, surveyed_g, comm_technique, nodeid_surveyed_set , directed)
		for role, mratio in mratio_hash.items():
			fratio = fratio_hash[role]
			if role not in mratio_arr_hash:
				mratio_arr_hash[role] = [mratio]
				fratio_arr_hash[role] = [fratio]
			else:
				mratio_arr_hash[role].append(mratio)
				fratio_arr_hash[role].append(fratio)
		gpa_role_arr_hash[role] = gpa_role_hash
	 
	return gpa_role_arr_hash, mratio_arr_hash, fratio_arr_hash
	
	
def ExtGenderGPA(g, surveyed_g, comm_technique, nodeid_surveyed_set, directed):

	
	## find communities
	comm_arr = commutil.findCommunity(g, comm_technique)
	## find clique members
	clique_members_set, all_members = getCliqueMembers(comm_arr, g)
	## find isolators
	isolators_index_all_set, isolators_index_surveyed_set = getIsolators(g, directed, nodeid_surveyed_set)
	## find brokers
	broker_set = getBrokers(comm_arr, isolators_index_all_set, g, clique_members_set)
		 	
	## check a relationship between positions in communities and grade 
	norole_set = nodeid_surveyed_set.difference(clique_members_set).difference(broker_set).difference(isolators_index_all_set)
			
	gpa_role_hash = dict()
	gpa_role_hash['clique'] =  [g.vs[idx]['gpa'] for idx in  clique_members_set]
	gpa_role_hash['broker']=  [g.vs[idx]['gpa'] for idx in  broker_set]
	gpa_role_hash['isolator'] = [g.vs[idx]['gpa'] for idx in  isolators_index_all_set]
	gpa_role_hash['norole'] = [g.vs[idx]['gpa'] for idx in  norole_set]
			
	gender_role_hash = dict()
	gender_role_hash['clique'] =  [g.vs[idx]['gender'] for idx in  clique_members_set]
	gender_role_hash['broker'] =  [g.vs[idx]['gender'] for idx in  broker_set]
	gender_role_hash['isolator'] = [g.vs[idx]['gender'] for idx in  isolators_index_all_set]
	gender_role_hash['norole'] = [g.vs[idx]['gender'] for idx in  norole_set]
			
			
	role_arr = ['clique', 'broker', 'isolator', 'norole']
	mratio_hash = dict()
	fratio_hash = dict()
	for role in role_arr:
		## Cal ratio of gender in each role
		if len(gender_role_hash[role])>0:
			gender_freqs = collections.Counter(gender_role_hash[role])
			m = gender_freqs['M']*1.0
			f = gender_freqs['F']
			mratio_hash[role] = m/(f+m)
			fratio_hash[role] = f/(f+m)
				
			## Calculate mean and std of gpa in each role
			mean = np.mean(np.array(gpa_role_hash[role]))
			std = np.std(np.array(gpa_role_hash[role]))
		else:
			mratio_hash[role] = 0.0
			fratio_hash[role] = 0.0
			
			mean = 0.0
			std = 0.0
			
	return gpa_role_hash, mratio_hash, fratio_hash

def calPvalue_ratioDifference( mratio_arr_hash, fratio_arr_hash, difratio_hash, rndmnumber):
	pval_hash = dict()
	for role, truedif in difratio_hash.items():
		nom = 0.
		mratio_arr = mratio_arr_hash[role]
		fratio_arr = fratio_arr_hash[role]
		for matio, fratio in zip(mratio_arr, fratio_arr):
			if abs(matio-fratio) >= truedif:
				nom += 1
		pval_hash[role] = nom/rndmnumber
	return 	 pval_hash
	
def main():
	## Rely on a community detction technique ** must record what technique is used ** 
	## Find clique members, brokers, isolators
	## community has 3+ members
	## clique members have >50% of their links within group 
	## brokers  are not in any community but have at least 2 links to non-isolators
	## Isolators have less than 2 links (undirected) and less than 1 in-link and out-link
	## Steps: find clique members, isolators then brokers
	
	machine = "ubuntu"
	ttype = "friend"
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
	
	#type_arr = ["bf", "friend", "study"]
	type_arr = [ttype]
	rndmnumber = 100 ## for a permutation test to build a random network
	f_w = open(result_path+"compareGenderRatioInEachRole_0.1dif_"+ttype+"100rnd.txt", "w")
	
	for t in type_arr:
		
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
			print fullname
			#if fname != "HM Act57": continue
			f_w.write(fname+" (role, absolute difference, p-value)\n")
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
			
			gpa_intID_hash = myutil.getGPAHash_intID(g)
			gender_intID_hash = myutil.getGenderHash_intID(g)
			
			role_arr = ['clique', 'broker', 'isolator', 'norole'] 
			nodeid_surveyed_set = set([v.index for v in surveyed_g.vs])
			gpa_role_hash, mratio_hash, fratio_hash  = ExtGenderGPA(g, surveyed_g, comm_technique, nodeid_surveyed_set , directed)

	 		gpa_role_hash_rdn, mratio_arr_hash, fratio_arr_hash = ExtGenderGPA_4rndRoles(g, surveyed_g, comm_technique, nodeid_surveyed_set, rndmnumber, directed,t, gpa_intID_hash, gender_intID_hash)
			
 
			## H1: percentage of male and female members in each role are different  -> true_dif = |mratio-fratio|
			## Count number of random networks that abs dif >= true_dif
			truedif_hash = dict()
			for role in mratio_hash.keys():
				truedif_hash[role] = abs(mratio_hash[role]-fratio_hash[role])  
			
			pval_hash = calPvalue_ratioDifference(mratio_arr_hash, fratio_arr_hash, truedif_hash, rndmnumber)
	  		
	  		for role, pval in pval_hash.items(): 
	  			print (role, truedif_hash[role], pval)
	  			tow = "%8s, %2.1f, %5.4f\n"  %(role, truedif_hash[role], pval)
	  			f_w.write(tow)
			f_w.write("\n")
			
main()
			
