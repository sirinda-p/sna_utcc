import igraph as ig
import communityUtil as commutil
import numpy as np
import collections, itertools
import randomizationGraphUtil as randomutil
import myutil as myutil
import time
from scipy import stats 

def getCliqueMembers(comm_arr, g):	
	clique_members = set()
	all_members = set()
	for comm in comm_arr:
		comm_set = set(comm)
		comm_size = len(comm_set)*1.0
 		if comm_size<2: continue
 	
		for n in comm:
			#print "for each node: "+str(n)
			##get all edges of each node
			all_members.add(n) 
			nbrs = set(g.neighbors(n))
			allfrieds_size = len(nbrs)*1.
			
			## Neighbors that are in the same clique
			intersect_size = len(nbrs.intersection(comm_set))
 			if (intersect_size/allfrieds_size) >= 0.5:
 				clique_members.add(n)
		
	return clique_members, all_members 
	
def getIsolators(g, directed, nodeid_surveyed_set):
	isolator_index_all = set()

	for v in g.vs():
		if directed:		 
			if v.indegree()<1 and v.outdegree()<1:
				isolator_index_all.add(v.index)

		else:
			if v.degree() <1 :
				isolator_index_all.add(v.index)	

				
	isolator_index_surveyed = set(isolator_index_all.intersection(nodeid_surveyed_set))
	return isolator_index_all	, isolator_index_surveyed						

def getBrokers(comm_arr, isolator_surveyed, g, clique_members, nodeid_surveyed_set):
	
 	## find brokers who have 2 links to clique members (or 2 links to other brokers)
 	potential_brokers  = nodeid_surveyed_set.difference(isolator_surveyed).difference(clique_members)
	broker_set = set()

	for b in potential_brokers:
		b_neighbors = set([v.index for v in g.vs[b].neighbors()])
		##check if b has 2 links to cliques members
	 
		if len(b_neighbors.intersection(clique_members))>1:
			 broker_set.add(b)
	
	## find other brokers who have 2 linls with other brokers	

	#for b in potential_brokers:
		#b_neighbors = set([v.index for v in g.vs[b].neighbors()])
		###check if b has 2 links to cliques members
	 
		#if len(b_neighbors.intersection(broker_set))>1:
			 #broker_set.add(b)
			 	 
	return broker_set
	
 
		
def ExtGenderGPA_4rndRoles_WithGender(g, surveyed_g, comm_technique, nodeid_surveyed_set, rndmnumber, directed, ftype, gpa_intID_hash, gender_intID_hash , csize):
	
	mratio_arr_hash = dict()
	fratio_arr_hash = dict()
	gpa_role_arr_hash = dict()
	n = len(g.vs())
	m = len(g.es())
	for i in range(0,rndmnumber):
		start = time.time()
		if comm_technique == "fastgreedy": ## fastgreedy works on undirected graphs only
			rndg =  randomutil.ER_withAttributes(ftype,  gpa_intID_hash, gender_intID_hash, n,m ).simplify()
		else:
			rndg =  randomutil.ER_withAttributes(ftype,  gpa_intID_hash, gender_intID_hash, n,m )
		
		gpa_role_hash, mratio_hash, fratio_hash = ExtGenderGPA(rndg, surveyed_g, comm_technique, nodeid_surveyed_set , directed, csize)
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
	

		
def ExtGenderGPA_4rndRoles(g, surveyed_g, comm_technique, nodeid_surveyed_set, nodeid_all_set,rndmnumber, directed, ftype, gpa_intID_hash,  csize):
	
	mratio_arr_hash = dict()
	fratio_arr_hash = dict()
	gpa_arr_hash = dict()
	n = len(g.vs())
	m = len(g.es())
	 
		
	for i in range(0,rndmnumber):
		start = time.time()
		if comm_technique == "fastgreedy": ## fastgreedy works on undirected graphs only
			rndg =  randomutil.ER_withAttributes(ftype, gpa_intID_hash,  n,m ).simplify()
		else:
			rndg =  randomutil.ER_withAttributes(ftype, gpa_intID_hash,  n,m )
		
		gpa_arr_hash[i]  = ExtGenderGPA(rndg, surveyed_g, comm_technique, nodeid_surveyed_set, nodeid_all_set,directed, csize)
		 
			
   	return gpa_arr_hash 
  	
def ExtGenderGPA_WithGender(g, surveyed_g, comm_technique, nodeid_surveyed_set, directed, csize):

	
	## find communities
	if comm_technique== "clique":
		comm_arr = g.cliques(min=csize, max=csize)
	else:
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
	
def ExtGenderGPA(g, surveyed_g, comm_technique, nodeid_surveyed_set, nodeid_all_set,directed, csize):

	
	## find communities
	if comm_technique== "clique":
		comm_arr = g.cliques(min=csize, max=csize)
	else:
		comm_arr = commutil.findCommunity(g, comm_technique)
 	## find clique members
	clique_members_set, all_members = getCliqueMembers(comm_arr, g)
	 	
	## find isolators
	isolators_index_all_set, isolators_index_surveyed_set = getIsolators(g, directed, nodeid_surveyed_set)
	## find brokers
	broker_set = getBrokers(comm_arr, isolators_index_surveyed_set, g, clique_members_set, nodeid_surveyed_set)
		 	
	## check a relationship between positions in communities and grade 
	norole_set = nodeid_surveyed_set.difference(clique_members_set).difference(broker_set).difference(isolators_index_surveyed_set)
			
	gpa_role_hash = dict()
	 
	gpa_role_hash['clique'] =   [g.vs[idx]['gpa'] for idx in  clique_members_set]
	gpa_role_hash['broker']=   [g.vs[idx]['gpa'] for idx in  broker_set]
	gpa_role_hash['isolator'] =  [g.vs[idx]['gpa'] for idx in  isolators_index_all_set]
	gpa_role_hash['norole'] =  [g.vs[idx]['gpa'] for idx in  norole_set]

	return gpa_role_hash 

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

	
def main_withGender():
	## Rely on a community detction technique ** must record what technique is used ** 
	## Find clique members, brokers, isolators
	## community has 3+ members
	## clique members have >50% of their links within group 
	## brokers  are not in any community but have at least 2 links to non-isolators
	## Isolators have less than 2 links (undirected) and less than 1 in-link and out-link
	## Steps: find clique members, isolators then brokers
	
	machine = "ubuntu"
	ttype = "friend"
	comm_technique = "clique" #"edge_btwness" , "clique"## edge_btwness (for directed graphs)
	csize = 3
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
			#gender_intID_hash = myutil.getGenderHash_intID(g)
			
			role_arr = ['clique', 'broker', 'isolator', 'norole'] 
			nodeid_surveyed_set = set([v.index for v in surveyed_g.vs])
			print  "Processing original network"
			gpa_role_hash, mratio_hash, fratio_hash  = ExtGenderGPA(g, surveyed_g, comm_technique, nodeid_surveyed_set , directed, csize)
			print "Processing random network"
	 		gpa_role_hash_rdn, mratio_arr_hash, fratio_arr_hash = ExtGenderGPA_4rndRoles(g, surveyed_g, comm_technique, nodeid_surveyed_set, rndmnumber, directed,t, gpa_intID_hash, gender_intID_hash, csize)
			
 
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
			break

 
def checkMean_clique_non_clique( gpa_role_hash ):
	if len(gpa_role_hash['clique'])>0:
		clique_mean = sum(gpa_role_hash['clique'])/len(gpa_role_hash['clique'])
	else:
		return "NAN-nom"
	nonclique_arr = gpa_role_hash['broker']+gpa_role_hash['isolator']+gpa_role_hash['norole']
	
	if len(nonclique_arr)>0:
		nonclique_mean = sum(nonclique_arr)/len(nonclique_arr)
		 
		return clique_mean>nonclique_mean
	else:
		return "NAN-denom"
	
def checkMean_broker_nonBroker( gpa_role_hash ):
	if len(gpa_role_hash['broker'])>0:
		broker_mean = sum(gpa_role_hash['broker'])/len(gpa_role_hash['broker'])
	else:
		return "NAN-nom"
	nonbroker_arr =  gpa_role_hash['isolator']+gpa_role_hash['norole']+gpa_role_hash['clique']
	
	if len(nonbroker_arr)>0:
		nonbroker_mean = sum(nonbroker_arr)/len(nonbroker_arr)

		return broker_mean>nonbroker_mean	
	else:
		return "NAN-denom"
		
def checkMean_broker_IsoNorole( gpa_role_hash ):
	if len(gpa_role_hash['broker'])>0:
		broker_mean = sum(gpa_role_hash['broker'])/len(gpa_role_hash['broker'])
	else:
		return "NAN-nom"
	nonbroker_arr =  gpa_role_hash['isolator']+gpa_role_hash['norole']
	
	if len(nonbroker_arr)>0:
		nonbroker_mean = sum(nonbroker_arr)/len(nonbroker_arr)

		return broker_mean>nonbroker_mean	
	else:
		return "NAN-denom"

def checkMean_Isolator_nonIso( gpa_role_hash):
	if len(gpa_role_hash['isolator'])>0:
		isolator_mean = sum(gpa_role_hash['isolator'])/len(gpa_role_hash['isolator'])
	else:
		return "NAN-nom"
	nonisolator_arr =  gpa_role_hash['broker']+gpa_role_hash['norole']+gpa_role_hash['clique']
	
	if len(nonisolator_arr)>0:
		nonisolator_mean = sum(nonisolator_arr)/len(nonisolator_arr)

		return isolator_mean<nonisolator_arr	
	else:
		return "NAN-denom"
	
####
def testMean_clique_non_clique( gpa_role_hash ):
	clique_arr = gpa_role_hash['clique'] 
	nonclique_arr = gpa_role_hash['broker']+gpa_role_hash['isolator']+gpa_role_hash['norole']
	
	tval, pval = stats.ttest_ind(clique_arr,nonclique_arr, equal_var=False)
 	return tval,pval/2 
	
def testMean_broker_nonBroker( gpa_role_hash ):
	broker_arr =  gpa_role_hash['broker'] 
	nonbroker_arr =  gpa_role_hash['isolator']+gpa_role_hash['norole']+gpa_role_hash['clique']
	
	tval, pval = stats.ttest_ind(broker_arr,nonbroker_arr, equal_var=False)
 	return tval,pval/2  
		
def testMean_broker_IsoNorole( gpa_role_hash ):
	broker_arr =  gpa_role_hash['broker'] 
	nonbroker_arr =  gpa_role_hash['isolator']+gpa_role_hash['norole']
	
	tval, pval = stats.ttest_ind(broker_arr,nonbroker_arr, equal_var=False)
 	return tval,pval/2  
 	 
def testMean_Isolator_nonIso( gpa_role_hash):
	isolator_arr =  gpa_role_hash['isolator'] 
	nonisolator_arr =  gpa_role_hash['broker']+gpa_role_hash['norole']+gpa_role_hash['clique']
	
	tval, pval = stats.ttest_ind(nonisolator_arr,isolator_arr, equal_var=False)
 	return tval,pval/2  
 
		
def main():
	## Rely on a community detction technique ** must record what technique is used ** 
	## Find clique members, brokers, isolators
	## community has 3+ members
	## clique members have >50% of their links within group 
	## brokers  are not in any community but have at least 2 links to non-isolators
	## Isolators have less than 2 links (undirected) and less than 1 in-link and out-link
	## Steps: find clique members, isolators then brokers
	
	machine = "ubuntu"
	ttype = "study"
	comm_technique = "clique" #"edge_btwness" , "clique"## edge_btwness (for directed graphs)
	csize = 3
 	if machine == "ubuntu":
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	else:
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
		
	result_path = prefix+"result/community/analysis/"
	gml_path = prefix+"data/gml/notempnode/"	 	
	surveyd_gml_path =  prefix+"data/surveyed_only/"
	flist = ["Ac57","Eng55","ICT55","ICT56","ICT57-All","Niti55", "Niti56","HM Act57","HM Korea57","HM Thai57", "Nited56","Biz55", "EC55"]
	
	type_arr = [ "friend", "study", "bf"]
	#type_arr = [ttype]
	rndmnumber = 100 ## for a permutation test to build a random network
 	role_arr = ['clique', 'broker', 'isolator', 'norole'] 
	
	for t in type_arr:
		pclique_arr = []
		pbroker_arr = []
		piso_arr = []
 		tclique_arr = []
		tbroker_arr = []
		tiso_arr = []
		
		pclique_permute_arr = []
		pbroker_permute_arr = []
		piso_permute_arr = []
 		isGrtr_clique_permute_arr = []
		isGrtr_broker_permute_arr = []
		isGrtr_iso_permute_arr = []
		
 		print t
 
		for fname in flist:
			
			fullname = fname+"_"+t+".gml"
 			#if fname != "HM Act57": continue
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
			#gender_intID_hash = myutil.getGenderHash_intID(g)
			
			
			nodeid_surveyed_set = set([v.index for v in surveyed_g.vs])
			nodeid_all_set = set([v.index for v in  g.vs])
			
  			gpa_role_hash  = ExtGenderGPA(g, surveyed_g, comm_technique, nodeid_surveyed_set, nodeid_all_set, directed, csize)
			 
 	 		gpa_role_hash_arr_rdn  = ExtGenderGPA_4rndRoles(g, surveyed_g, comm_technique, nodeid_surveyed_set, nodeid_all_set,rndmnumber, directed,t, gpa_intID_hash,  csize)
			
			
			## test hypotheses
			## 1. Clique members have higher GPA than non-clique members
			## 2. Broker members have higher GPA than no-role + isolator members
			## 3. Isolators have lower GPA than non-isolator members
			## 4. Broker members hvae higher GPA than non-broker members
 			
 			t1, p1= testMean_clique_non_clique( gpa_role_hash )
 			t2, p2=testMean_broker_IsoNorole( gpa_role_hash )
 			t3, p3=testMean_Isolator_nonIso( gpa_role_hash )
 			t4, p4=testMean_broker_nonBroker( gpa_role_hash )
 			
 			pclique_arr.append(p1)
			pbroker_arr.append(p4)
			piso_arr.append(p3)
			tclique_arr.append(p1)
			tbroker_arr.append(p4)
			tiso_arr.append(p3)
 			
 
			isGreater = checkMean_clique_non_clique( gpa_role_hash )
			isGrtr_clique_permute_arr.append(isGreater)
			
  			if isGreater and isGreater!="NAN-denom" and isGreater!="NAN-nom":
				nom = 0.
 				for i in range(0, rndmnumber):
					
					isGreater_random = checkMean_clique_non_clique( gpa_role_hash_arr_rdn[i] )
					if isGreater_random:
						nom += 1.
			 
				p_value = nom/rndmnumber
				pclique_permute_arr.append(p_value)
 			else:
				pclique_permute_arr.append("nan")
			''' 
			## 2. Broker members have higher GPA than no-role + isolator members
		 
			isGreater = checkMean_broker_IsoNorole( gpa_role_hash )
			
			
			if isGreater and  isGreater!="NAN-denom" and isGreater!="NAN-nom":
				nom = 0.
				
 				for i in range(0, rndmnumber):
					
					isGreater_random = checkMean_broker_IsoNorole( gpa_role_hash_arr_rdn[i] )
					if isGreater_random:
						nom += 1
					
				p_value = nom/rndmnumber
				print "H2 (broker>Iso+Norole): pvalue = "+str(p_value)
			else:
				print "H2 (broker>Iso+Norole):"+str(isGreater)
			'''
			## 3. Isolators have lower GPA than non-isolator members
			isGreater = checkMean_Isolator_nonIso( gpa_role_hash )
			isGrtr_iso_permute_arr.append(isGreater)
		
			if isGreater and  isGreater!="NAN-denom" and isGreater!="NAN-nom":
				nom = 0.
				
 				for i in range(0, rndmnumber):
					
					isGreater_random = checkMean_Isolator_nonIso( gpa_role_hash_arr_rdn[i] )
					if isGreater_random:
						nom += 1
					
				p_value = nom/rndmnumber
				piso_permute_arr.append(p_value)
			else:
				piso_permute_arr.append("nan")
			
			## 4. Broker members hvee higher GPA than non-broker members
			isGreater = checkMean_broker_nonBroker( gpa_role_hash )
			isGrtr_broker_permute_arr.append(isGreater)
			
			if isGreater and  isGreater!="NAN-denom" and isGreater!="NAN-nom":
				nom = 0.
				
 				for i in range(0, rndmnumber):
					
					isGreater_random = checkMean_broker_nonBroker( gpa_role_hash_arr_rdn[i] )
					if isGreater_random:
						nom += 1
					
				p_value = nom/rndmnumber
				pbroker_permute_arr.append(p_value)
			else:
				pbroker_permute_arr.append("nan")
			
		print "Permutation test"	
		print "Clique Hypothesis"
		print pclique_permute_arr 
		print isGrtr_clique_permute_arr 
		print "Broker Hypothesis"
		print pbroker_permute_arr 
		print isGrtr_broker_permute_arr 
		print "Isolator Hypothesis"
		print piso_permute_arr 
 		print isGrtr_iso_permute_arr 
 		
		
		
		
		print "t test"
 		print "Clique Hypothesis"
		print pclique_arr
 		print "Broker Hypothesis"
		print pbroker_arr 
		print "Isolator Hypothesis"
		print piso_arr
main()
			
