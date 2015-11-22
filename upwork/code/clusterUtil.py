from sklearn.metrics import silhouette_samples, silhouette_score
import sklearn.cluster as skcluster
import numpy as np
from pprint import pprint
from random import shuffle
from concept_formation.cobweb3 import Cobweb3Tree
import concept_formation.cluster as cluster

def kmean_bestK(data, minK, maxK):
 
	## perform k-mean and select the best k
	maxsilh = float('-inf')
	centroid_best = []
	kbest = 0
	
	for ncluster in range(minK,maxK):
		
		clusterer = skcluster.KMeans(n_clusters=ncluster)
		clusterer.fit(data)
		cluster_labels = clusterer.fit_predict(data)
		print cluster_labels
		# The silhouette_score gives the average value for all the samples.
		# This gives a perspective into the density and separation of the formed clusters
		silhouette_avg = silhouette_score(data, cluster_labels)
   		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
			centroid_best = clusterer.cluster_centers_
			kbest = ncluster
	print (kbest, maxsilh)
	return centroid_best, kbest
 	 
def affinity(data):
	maxsilh = float('-inf')
	centroid_best = []
	for  damping in np.arange(0.5,1,0.1):
		clusterer = skcluster.AffinityPropagation(damping = damping, affinity='euclidean')
		clusterer.fit(data)
		cluster_labels = clusterer.fit_predict(data)
		silhouette_avg = silhouette_score(data, cluster_labels) 
 
 		ncluster =  len(clusterer.cluster_centers_indices_)
  		
 		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
			centroid_best = clusterer.cluster_centers_ 
			kbest = ncluster
	print (kbest, maxsilh)
	return centroid_best, kbest

def birch(data):
	'''
	for branching_factor in np.arange(50,60,10):
		print "\nBranch factor = "+str(branching_factor)
		clusterer = skcluster.Birch(branching_factor=branching_factor, n_clusters=None, threshold=0.5, compute_labels=True)
		clusterer.fit(data)
		clusterer.fit_predict(data)
		cluster_labels = clusterer.fit_predict(data)
		silhouette_avg = silhouette_score(data, cluster_labels) 
		print "Default cluster"
 		print (len(set(cluster_labels)), silhouette_avg)

		for ncluster in np.arange(3,4,1):
		'''	
	maxsilh = float('-inf')
	centroid_best = []
 	
	for ncluster in range(3,11):
		clusterer = skcluster.Birch(n_clusters=ncluster,  compute_labels=True)
		clusterer.fit(data)
		clusterer.fit_predict(data)
		cluster_labels = clusterer.fit_predict(data)
		silhouette_avg = silhouette_score(data, cluster_labels) 
		
		
 		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
 			kbest = ncluster
			
			center_avg_hash = dict()
			center_num_hash = dict()
			
			for label, centers in zip(clusterer.subcluster_labels_,clusterer.subcluster_centers_):
				if label not in center_avg_hash:
					center_avg_hash[label]  = np.array(centers)
					center_num_hash[label] = 1
				else:
					center_avg_hash[label]  += np.array(centers)
					center_num_hash[label] += 1
			centroid_best = []	
			for label, sum_center in center_avg_hash.items():
				#print label
				avg_center = sum_center/(center_num_hash[label]*1.)
				centroid_best.append(avg_center)
		
	print (kbest, maxsilh)
	return np.array(centroid_best), kbest
	

def cobweb(data, attname_arr,integer_arr_list, norm_data):
	
 	#shuffle(irises)
	maxsilh = float('-inf')
	centroid_best = []

	tree = Cobweb3Tree()
	cobweb_data = []
	first = True
	
	for row in data:
		datadict = dict()
		 
		for att_name, att_val in zip(attname_arr, row):
			if att_name in integer_arr_list:
				datadict[att_name] = float(att_val)
			else:
				datadict[att_name] =  att_val 
		cobweb_data.append(datadict)
		if first:
			#print cobweb_data	
			first = False
	#cobweb_data = [{a: iris[a] for a in iris } for row in data]
	
	tree.fit(cobweb_data)
	
	#print len( cobweb_data)
	print "nodes in tree"
	pprint(tree.root.output_json())
	print ""
	for k in range(2,11):
		#cobweb_labels = [ c for c in cluster.k_cluster(tree, cobweb_data, k)[0]]
		
		 
		cluster_labels = np.array([ c for c in cluster.k_cluster(tree, cobweb_data, k=k)],)
		print set(cluster_labels)
		try:
			silhouette_avg = silhouette_score(norm_data, cluster_labels) 
		except :
			print "error in silhouette_score"
			continue
		print (k, silhouette_avg)
		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
			centroid_best = set(cluster_labels)
			kbest = k
	
	print "kbest"
	print (kbest, maxsilh)
	
	return set(cluster_labels), kbest 
	 	
def dbscan(data):
	maxsilh = float('-inf')
	centroid_best = []
	
	algorithm_arr = ["auto", "ball_tree", "kd_tree", "brute"]
	metric_arr = ["cityblock", "cosine", "euclidean", "l1", "l2", "manhattan"]
	for algorithm in algorithm_arr:
		for metric in metric_arr:
 			clusterer = skcluster.DBSCAN(eps=0.5,  metric=metric, algorithm=algorithm ) 
			try:
				clusterer.fit(data)
			except ValueError as e:
				#print e
				continue
			
			cluster_labels = clusterer.fit_predict(data)
			
			if len(set(cluster_labels))>1:
				silhouette_avg = silhouette_score(data, cluster_labels) 
 				ncluster =  len(clusterer.components_)
				 
 				if silhouette_avg> maxsilh:
					maxsilh = silhouette_avg
					centroid_best = clusterer.core_sample_indices_ 
					kbest = ncluster
	
	print (kbest, maxsilh)
	 
 	
def getCentroidValues(centroid_best,kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list,minmax_hash):
	## convert dummy back to original 
	cat_hash_cluster = dict() 
	centroid_hash_allclusters = dict() ## key = feature name, val = an array of feature values in corresponding cluster 

	for centroid, no in zip(centroid_best, range(0,kbest)):
		cat_hash_cluster[no] = dict() 
		max_hash = dict()
		max_val = dict()
		#print centroid
		
		for attname in newcatname_arr:
			max_hash[attname] = 0
			max_val[attname] = ""
			
		for cval, attname in zip(centroid, newname_arr):
			
			if attname in newcatname_arr:
				#print (attname, cval)
				if attname.startswith ("Time"):
					mainname = "Timezone"
					catname = attname.replace("Timezone-","")
				else:
					mainname, catname = attname.split("-")
					
				if cval > max_hash[attname]:
					max_hash[attname] = cval
 					cat_hash_cluster[no][mainname] = catname
 
 
	for centroid, no in zip(centroid_best, range(0,kbest)):
		noncat_cenarr_val = []
		noncat_cenarr_name = []
		cat_cenarr_val = []
		cat_cenarr_name = [] 
		 
		
		for cval, attname in zip(centroid, newname_arr):
			if attname in newcatname_arr:
				if attname.startswith ("Time"):
					mainname = "Timezone"
					catname = attname.replace("Timezone-","")
				else:
					mainname, catname = attname.split("-")
					
				cval = cat_hash_cluster[no][mainname]
				cat_cenarr_val.append(cval)
				cat_cenarr_name.append(mainname)
			else:
				noncat_cenarr_val.append(cval)
				noncat_cenarr_name.append(attname)
 
		if no == 0:
			for name in noncat_cenarr_name:
				print name
			for name in cat_hash_cluster[no].keys():
				print name 
				
		print ""
		print "\nCluster no "+str(no)
		for val, name in zip(noncat_cenarr_val, noncat_cenarr_name):
			#print val
			if name in integer_arr_list:
 				fval = "%5.4f " %(val*(minmax_hash[name][1][0]-minmax_hash[name][0][0]) + minmax_hash[name][0][0])
 			elif name in boolean_arr_list:
 				#raw = str(val)+"("+str(bool(val>=0.5 ))+")"
				fval = "%5.4f (%s)" %(val, str(bool(val>=0.5)))		
			
			print fval  
			if name not in centroid_hash_allclusters:
				centroid_hash_allclusters[name] = [fval]
			else:
				centroid_hash_allclusters[name].append(fval)
		
		cat_hash = cat_hash_cluster[no]
		for name, val in cat_hash.items():
			if name not in centroid_hash_allclusters:
				centroid_hash_allclusters[name] = [val]
			else:
				centroid_hash_allclusters[name].append(val)
			
			
				
	return centroid_hash_allclusters

	
