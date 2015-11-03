from scipy import stats 
import myutil 
## Perform statistical testing on 2 sample means
def test2Means(nodeid_all, motif_nodeid, g):
	gpa_hash = myutil.getGPAHash(g) ## key = my id, value = gpa
	score_all = getGPA(nodeid_all, gpa_hash)
	score_motif = getGPA(motif_nodeid, gpa_hash)

	tval, pval = stats.ttest_ind(score_motif,score_all, equal_var=False)
	print (tval, pval)
	return tval,pval/2
	

def getGPA(node_arr, gpa_hash):
	gpa_arr = []
	 
	for n in node_arr:
		 
		gpa_arr.append(gpa_hash[n])
	return gpa_arr
		
	
	
	
