from scipy import stats 
import myutil 
## Perform statistical testing on 2 sample means
def test2Means(node_all, motif_nodes, g):
	gpa_hash = myutil.getGPAHash(g)
	score_all = getGPA(node_all, gpa_hash)
	score_motif = getGPA(motif_nodes, gpa_hash)

	tval, pval = stats.ttest_ind(score_motif,score_all, equal_var=False)
	return tval,pval/2
	

def getGPA(node_arr, gpa_hash):
	gpa_arr = []
	 
	for n in node_arr:
		
		gpa_arr.append(gpa_hash[n])
	return gpa_arr
		
	
	
	
