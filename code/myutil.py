import numpy as np
import collections, itertools

def getTopK(score_arr, v_arr, k):
	
	np_score_arr = np.array(score_arr)
	np_v_arr = np.array(v_arr)
	topk_index_arr = np_score_arr.argsort()[-k:][::-1] ## sort in descending order
 
	np_v_arr[topk_index_arr]
	np.sort(np_score_arr) [-k:][::-1]

	return np_v_arr[topk_index_arr], np.sort(np_score_arr) [-k:][::-1]

def getBottomK(score_arr, v_arr, k):
	
	np_score_arr = np.array(score_arr)
	np_v_arr = np.array(v_arr)
	topk_index_arr = np_score_arr.argsort()[:k] ## sort in ascending order
 
	np_v_arr[topk_index_arr]
	np.sort(np_score_arr) [:k]

	return np_v_arr[topk_index_arr], np.sort(np_score_arr) [:k]
	
def getTopKAtt(topK_nodeid_arr,node_arr,k):
	
	topK_gpa = [n['gpa'] for n in node_arr if n['id'] in topK_nodeid_arr and not str(n['id']).startswith('999')]
	topK_gender = [n['gender'] for n in node_arr if n['id'] in topK_nodeid_arr and not str(n['id']).startswith('999')]
	 
 
	return topK_gpa[0:k], topK_gender[0:k] 
	
def plotMotif(result_path, fname, g, size):
	
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
		 
		ig.plot(subg, plotpath+gname )  #

## construct a hash of :key = node id, value = gpa		
def getGPAHash(g):
	gpa_hash = dict()
	for v in g.vs():
		gpa_hash[v['id']] = v['gpa']
	return gpa_hash
	
## assume that node sequence stay the same
def getGPAHash_intID(g):
	gpa_hash = dict()
	  
	for v in g.vs():
		gpa_hash[v.index] = v['gpa']
		 
		
	return gpa_hash	

## assume that node sequence stay the same
def getGenderHash_intID(g):
	gender_hash = dict()
	  
	for v in g.vs():
		gender_hash[v.index] = v['gender']
		
	return gender_hash	
	 
def countGender(comm_arr, g):
	
	gender_freq_list = []
	for comm in comm_arr:
		gender_arr = [] 
		if len(comm)<2: continue
		for n in comm:
			gender_arr.append(g.vs[n]['gender'])
	
		letter_freqs = collections.Counter(gender_arr)
		gender_freq_list.append(letter_freqs)
	
	return gender_freq_list
	
	 
def countValuesFeatures(node_arr, g, feature_name):
	
	freq_list = []
	for n in node_arr:
		gender_arr.append(g.vs[n][feature_name])
	
	letter_freqs = collections.Counter(gender_arr)
	freq_list.append(letter_freqs)
	
	return freq_list
			



 
