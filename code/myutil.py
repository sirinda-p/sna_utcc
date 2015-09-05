import numpy as np

def getTopK(score_arr, v_arr, k):
	
	np_score_arr = np.array(score_arr)
	np_v_arr = np.array(v_arr)
	topk_index_arr = np_score_arr.argsort()[-k:][::-1] ## sort in descending order
	
	return np_v_arr[topk_index_arr], np.sort(np_score_arr) [-k:][::-1]
