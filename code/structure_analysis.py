import os
from igraph import *
import numpy  as np
import myutil as myutil
import scipy.stats as stat
from collections import Counter
import matplotlib.pyplot as plt

def calCentrality(g, directed):
	
	'''
	Structure properties:
	- Centrality
		- Degree  x
		- Hub (directed only) x
		- Authority (directed only) x
		- Betweenness  x

	'''
	v_arr = g.vs()
 
	if directed:
 
		indegree_arr =  g.indegree()
 		outdegree_arr = g.outdegree()
		
		## Hub and Authority are for directed networks only
		hub_arr = g.hub_score() 
		authority_arr = g.authority_score() 
 		betweenness_arr = g.betweenness(directed=True)
 		return indegree_arr, outdegree_arr, hub_arr, authority_arr, betweenness_arr
 		
 		
	else:
		degree_arr =  g.degree()
		betweenness_arr = g.betweenness(directed=False)
		return degree_arr, betweenness_arr
	


def Centrality_grade_correlation_main(g, directed, cen_arr, cen_score_arr_all):
	
	gpa_arr = [n['gpa']for n in g.vs()]
	
	if directed:
		
		corr_val_arr = []
		pval_arr = []
		
		for cen, cen_score_arr in zip(cen_arr,cen_score_arr_all):
			corr_val, pval = stat.pearsonr(gpa_arr, cen_score_arr)
			corr_val_arr.append(corr_val)
			pval_arr.append(pval)
		
		'''
		indeg_corr, indeg_pval = scipy.stats.pearsonr(att_arr, indegree_arr)
		outdeg_corr, outdeg_pval = scipy.stats.pearsonr(att_arr, outdegree_arr)
		hub_corr, hub_pval = scipy.stats.pearsonr(att_arr, hub_arr)
		authority_corr, authority_pval = scipy.stats.pearsonr(att_arr, authority_arr)
		btw_corr, btw_pval = scipy.stats.pearsonr(att_arr, betweenness_arr)
		'''
		
	else:
		cen_arr = ["Degree", "Betweenness"]
		corr_val_arr = []
		pval_arr = []
		
		for cen, cen_score_arr in zip(cen_arr,cen_score_arr_all):
			corr_val, pval = stat.pearsonr(gpa_arr, cen_score_arr)
			corr_val_arr.append(corr_val)
			pval_arr.append(pval)
			
		'''
		degree_arr, betweenness_arr = calCentralityTopK(g, directed)
		deg_corr, deg_pval = scipy.stats.pearsonr(att_arr, degree_arr)
		btw_corr, btw_pval = scipy.stats.pearsonr(att_arr, betweenness_arr)
		'''
	return cen_arr,corr_val_arr, pval_arr
	
 
def main_powerlaw():
	path = "/home/amm/Desktop/sna-git/data/gml/notempnode/"
	result_path = "/home/amm/Desktop/sna-git/result/analysis/"
	
	k = 10 # top k students with the highest centrality scores
	
	for ftype in [ "bf.gml","friend.gml", "study.gml"]: #[ "bf.gml","friend.gml", "study.gml"]:
		f_w = open(result_path+"Powerlaw_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		f_w.write("Name, P-value\n")
 		if ftype == "friend.gml":
			directed = False
		else:
			directed = True
			
 		err_list = []
 		for fname in os.listdir(path):
   			try:
				ftype2 = fname.split("_")[1]
				if ftype2 != ftype:
					continue
 				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected().simplify()
				else:
					g = read(path+fname, format="gml").simplify()
			except:
				err_list.append(fname)
				print "Error importing a graph"
				continue
			
			
			
			if directed:
				indeg_arr = [d for d in g.indegree() if d>0]
				pvalue_in = power_law_fit(indeg_arr,return_alpha_only=False).p
				pathfname = "/home/amm/Desktop/sna-git/result/freqDistPlot/"+fname.replace(".gml","_indegree.png")
				plotFreqDist(indeg_arr , pathfname, directed, 'Indegree')	
				
				outdeg_arr = [d for d in g.outdegree() if d>0]
				pvalue_out = power_law_fit(outdeg_arr,return_alpha_only=False).p
				pathfname = "/home/amm/Desktop/sna-git/result/freqDistPlot/"+fname.replace(".gml","_outdegree.png")
				plotFreqDist(outdeg_arr , pathfname, directed, 'Outdegree')	
				
				tow = "%10s, %5.4f %5.4f\n " %(fname, pvalue_in, pvalue_out)
				f_w.write(tow)
			else:
				deg_arr = [d for d in g.degree() if d>0]
				pvalue = power_law_fit(deg_arr,return_alpha_only=False).p
				pathfname = "/home/amm/Desktop/sna-git/result/freqDistPlot/"+fname.replace(".gml","_degree.png")
				plotFreqDist(deg_arr, pathfname, directed)
					
				tow = "%10s, %5.4f\n " %(fname, pvalue)
				f_w.write(tow)
				
		f_w.close()
		
		
def plotFreqDist(arr, pathfname, directed, degree='Degree'):
	
	plt.hist(arr)
	if directed:
		plt.xlabel('Indegree')
	else:
		plt.xlabel(degree)
	plt.ylabel('Frequency')
	#plt.show()
	plt.savefig(pathfname)
	plt.clf()
	
def main_structure():
	path = "/home/amm/Desktop/sna-git/data/gml/notempnode/"
	result_path = "/home/amm/Desktop/sna-git/result/analysis/"
	
	k = 10 # top k students with the highest centrality scores
	
	for ftype in [ "bf.gml","friend.gml", "study.gml"]: #[ "bf.gml","friend.gml", "study.gml"]:
		f_w = open(result_path+"CorrelationBtwCentrality-GPA_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		f_gpa = open(result_path+"GPA_of_topK_Centrality_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		f_gen = open(result_path+"Gender_of_topK_Centrality_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		f_stat=  open(result_path+"CentralityStatistic_wholegraph_allDept_"+ftype.replace(".gml",".csv"),"w")
		
		if ftype == "friend.gml":
			directed = False
			cen_arr = ["Degree", "Betweenness"]
		else:
			directed = True
			cen_arr = ["Indeg", "Outdeg", "Hub", "Authority", "Betweenness"]
 		
 		err_list = []
 	 
 		corr_hash = dict()
 		pval_hash = dict() 		
 		
 		cen_topK_hash = dict()
 		gpa_topK_hash = dict() 		
 		gender_topK_hash = dict()
 		gpa_all_hash = dict()
 		gender_all_hash = dict()
 		cen_all_hash = dict()
 		size_hash = dict()
 		
 		for cen in cen_arr:
			corr_hash[cen] = dict()
			pval_hash[cen] = dict()
			cen_topK_hash[cen] = dict()
			cen_all_hash[cen] = dict()
			gpa_topK_hash[cen] = dict() 		
			gender_topK_hash[cen] = dict()
			
					
		for fname in os.listdir(path):
   			try:
				ftype2 = fname.split("_")[1]
				if ftype2 != ftype:
					continue
 				
				if ftype2 == "friend.gml":
					g = read(path+fname, format="gml").as_undirected().simplify()
				else:
					g = read(path+fname, format="gml").simplify()
			except:
				err_list.append(fname)
 				print fname+"Error importing a graph"
				continue
			
 			##Calculate correlation between centrality scores and gpa
			cen_score_arr_all = calCentrality(g, directed)
			cen_arr,corr_val_arr, pval_arr = Centrality_grade_correlation_main(g, directed, cen_arr,cen_score_arr_all)
			
 		
			for cen, cval, pval in zip(cen_arr,corr_val_arr, pval_arr ):
				
 				corr_hash[cen][fname] = cval
				pval_hash[cen][fname] = pval
			
			
			id_arr = g.vs["id"]
			gsize = len(id_arr)
			size_hash[fname] = gsize
			node_arr = g.vs()
			temp = [n['gpa'] for n in node_arr]
			gpa_all_hash[fname] = (max(temp),min(temp), sum(temp)/len(temp))
			
			temp2 = Counter([n['gender'] for n in node_arr])
			gender_all_hash[fname] = dict()
 			for (key, f) in temp2.most_common():
				gender_all_hash[fname][key] = 1.*f/gsize
				
			 
			for cen, cen_score_arr in zip(cen_arr,cen_score_arr_all):
				## Get topK students 
				topK_nodeid_arr, topK_score_arr = myutil.getTopK(cen_score_arr, id_arr, k+1)
				if cen == "Degree":
					print fname
					print (topK_nodeid_arr[0], topK_score_arr[0])
				topK_gpa, topK_gender_arr  = myutil.getTopKAtt(topK_nodeid_arr,node_arr,k )
				 
				cen_topK_hash[cen][fname] = topK_score_arr
				gpa_topK_hash[cen][fname] = topK_gpa
				cen_all_hash[cen][fname] = cen_score_arr
				
				temp3 = Counter(topK_gender_arr)
				topK_gender_freq = dict()
				topK_gender_freq['M'] = 0.0
				topK_gender_freq['F'] = 0.0
				
				for (key, f) in temp3.most_common():
					topK_gender_freq[key]=1.*f/k
					
				
				gender_topK_hash[cen][fname] = (topK_gender_arr,topK_gender_freq)
 
		for cen in cen_arr:
			f_w.write("\n"+cen+"\n")
			f_w.write("DeptName, Correlation score, p-value\n")
			for fname in corr_hash[cen].keys():
				cval = corr_hash[cen][fname]
				pval = pval_hash[cen][fname]
				tow = "%10s, %5.4f, %5.4f, \n " %(fname, cval, pval)
				f_w.write(tow)
		f_w.close()
					
		for cen in cen_arr:
			f_gpa.write("\n"+cen+"\n")
			f_gen.write("\n"+cen+"\n")
			f_stat.write("\n"+cen+"\n")
 			f_gpa.write("GPA of top"+str(k)+": maxTopK(maxAll), minTopK(minAll), avgTopK(avgAll)\n")
			f_gen.write("Gender of top"+str(k)+": MaleTopK(MaleAll), FemaleTopK(FemaleAll)\n")
			for fname in corr_hash[cen].keys():
			 
				gpaK_arr = gpa_topK_hash[cen][fname]
				
				max_gpaK, min_gpaK, avg_gpaK =  (max(gpaK_arr),min(gpaK_arr), sum(gpaK_arr)/len(gpaK_arr))
				max_gpaAll, min_gpaAll, avg_gpaAll = gpa_all_hash[fname]
				tow1 = "%10s, %5.4f( %5.4f), %5.4f( %5.4f), %5.4f( %5.4f) \n " %(fname, max_gpaK, max_gpaAll,min_gpaK,min_gpaAll,avg_gpaK,avg_gpaAll)
				f_gpa.write(tow1)
				
				topK_gender_arr,topK_gender_freq  = gender_topK_hash[cen][fname] 
				all_gender_freq = gender_all_hash[fname] 
				cen_arr = cen_all_hash[cen][fname] 
				 
				tow2 = "%10s, %5.2f( %5.2f), %5.2f( %5.2f) \n " %(fname, topK_gender_freq['M'], all_gender_freq['M'] , topK_gender_freq['F'], all_gender_freq['F'] )
				f_gen.write(tow2)
				
				tow3 = "%10s, %5.4f, %5.4f , %5.4f , %5.4f  \n " %(fname, size_hash[fname], max(cen_arr), min(cen_arr), sum(cen_arr)/len(cen_arr))
				f_stat.write(tow3)
		f_gpa.close()
		f_gen.close()
		f_stat.close() 
			
			
#main_structure()
main_powerlaw()
'''
Structure properties:
- Centrality 
	- Degree x
	- Hub (directed only) x
	- Authority (directed only) x
	- Betweenness x
- Homophily  x
- Small world (friend) -> may be unnecessary since each network is quite small
- Power law distribution (study) x
'''
