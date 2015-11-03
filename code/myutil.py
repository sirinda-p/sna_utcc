import numpy as np

def getTopK(score_arr, v_arr, k):
	
	np_score_arr = np.array(score_arr)
	np_v_arr = np.array(v_arr)
	topk_index_arr = np_score_arr.argsort()[-k:][::-1] ## sort in descending order
 
	np_v_arr[topk_index_arr]
	np.sort(np_score_arr) [-k:][::-1]

	return np_v_arr[topk_index_arr], np.sort(np_score_arr) [-k:][::-1]

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

 
