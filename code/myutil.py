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
	
	
