from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans


def kmean_bestK(data, minK, maxK):
 
	## perform k-mean and select the best k
	maxsilh = float('-inf')
	centroid_best = []
	kbest = 0
	for ncluster in range(minK,maxK):
		
		clusterer = KMeans(n_clusters=ncluster)
		clusterer.fit(data)
		cluster_labels = clusterer.fit_predict(data)

		# The silhouette_score gives the average value for all the samples.
		# This gives a perspective into the density and separation of the formed clusters
		silhouette_avg = silhouette_score(data, cluster_labels)
 		
 		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
			centroid_best = clusterer.cluster_centers_
			kbest = ncluster
	
	return centroid_best, kbest
	 	
	 
	
def getCentroidValues_kmean(centroid_best,kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list,minmax_hash):
	## convert dummy back to original 
	cat_hash_cluster = dict()
	
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
				ori = val*(minmax_hash[name][1][0]-minmax_hash[name][0][0]) + minmax_hash[name][0][0]
				print ori
			elif name in boolean_arr_list:
				#print str(bool(val>=0.5 ))
				print str(val)+"("+str(bool(val>=0.5 ))+")"
			else: 
				print val  
 		cat_hash = cat_hash_cluster[no]
		for name, val in cat_hash.items():
			print val
			
		print ""
		
