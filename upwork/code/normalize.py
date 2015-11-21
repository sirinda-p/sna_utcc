import numpy as np
from sklearn import preprocessing
import warnings
from scikits.statsmodels.tools import categorical
from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score

def cluster(data, ncluster):
	 
	clusterer = KMeans(n_clusters=ncluster)
	clusterer.fit(data)
	cluster_labels = clusterer.fit_predict(data)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
	silhouette_avg = silhouette_score(data, cluster_labels)
    
	return clusterer.cluster_centers_, silhouette_avg
		
def normalize():
	
	machine = "aws"
	aws = preprocessing.MinMaxScaler()
	imp = Imputer(missing_values='NaN', strategy='mean', axis=1)
	min_max_scaler = preprocessing.MinMaxScaler()
	
	if machine == "amm":
		prefix = "/home/amm/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	path = prefix+"upwork/data/"
	f_r = open(path+"appt_dump_transformed.csv", "r")
	f_w = open(path+"appt_dump_normMinMax.csv", "w")
	
	## new attribute names in transformed file
	att_name_list = ["ID", "AllowPush", "AdOptedIn", "NumCampaignMatch", "Carrier", "AppVersion", 
	"AllowiBeacon", "AllowGeo", "AllowFeaturePush", "ScreenHeight", "AllowBT", "HaveUniqueGlobalID", 
	"NumCrash", "DailyUsage","Country", "LastUpdateDays", "DeviceModel", "BlockPushTF", "BlockPushSameday", "BlockPushAfterDays", 
	"OS", "OSVersion", "RevokePushTF", "RevokePushBefore", "RevokePushSameday", "RevokePushAfterDays", "SignIn", 
	"UninstalledTF", "UninstalledSameday", "UninstalledAfter", "ScreenWidth", "EmailExist", "EmailAddress", 
	"InstallDays", "PushCount", "Timezone", "UserType", "Questions", "CorrectQuestion"]
	
	print len(att_name_list)
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress","BlockPushTF","BlockPushSameday","RevokePushTF",
	"RevokePushBefore", "RevokePushSameday", "UninstalledTF","UninstalledSameday"]
	
	category_arr_list = ["Carrier","AppVersion", "DeviceModel","OS","UserType", "OSVersion","Timezone","ScreenWidth","ScreenHeight","Country" ] 
 	
	integer_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", "BlockPushAfterDays", "RevokePushAfterDays", "UninstalledAfter", "LastUpdateDays"]
	
	ignore_arr_list = ["ID", "Carrier","AdOptedIn","AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"]
	#print len(boolean_arr_list)+len(category_arr_list)+len(integer_arr_list)
	#print set(att_name_list).difference(set(boolean_arr_list).union(category_arr_list).union(integer_arr_list))
	 
	att_value_hash = dict()
	norm_value_hash = dict()
	newname_arr = [] 
	for att_name in att_name_list:
		att_value_hash[att_name] = []
	
		
	for line in f_r.readlines()[1::]:
		att_arr = line.strip().split(",") 
 		if len(att_arr)>39:
			print att_arr
		for val, att_name in zip(att_arr,att_name_list):
 			val = val.strip() 
 			if val == "None":
				val = np.nan 
 			att_value_hash[att_name].append(val)
	
	b = att_value_hash["AllowPush"]
	imp.fit(b)
	impb = imp.transform(b)
		
	original_data = impb
	#print original_data.shape
	for att_name, val_arr in att_value_hash.items():
		if att_name  == "ID": continue
 
  		b = np.array([att_value_hash[att_name]])
		#print att_name
		if att_name in category_arr_list:
			cat_matrix, cat_dict = categorical(b, drop=True, dictnames=True)
			inv_dict = {v: k for k,v in cat_dict.items()}
  			newb = np.array([[inv_dict[d] for d in b[0]]])
			#print newb
 		else:
 			newb = b
		
		imp.fit(newb)
		impb = imp.transform(newb)
		original_data = np.concatenate((original_data,  impb), axis=0)
			
  	
 	k=30
   	## Select features
   	pca = PCA(n_components=1)
   	transpose_data = original_data.transpose()
 	pca.fit(transpose_data) 
	#new_data = pca.fit_transform(original_data) 
  	topk_arr = np.abs(pca.components_[0]).argsort()[::-1][:k]
	select_features = list(set([att_name_list[i] for i in topk_arr]).difference(set(ignore_arr_list)))
	
	
	## normalize feature values
	#norm_value_hash["ID"] = np.array([att_value_hash["ID"]]) 
	 
	## keep original boolean att
	for att_name in  boolean_arr_list:
		if att_name in ignore_arr_list: continue
		if att_name in select_features:
			norm_value_hash[att_name] = np.array([att_value_hash[att_name]])
			newname_arr.append(att_name)
		
	## normalize interger attributes 
	minmax_hash = dict()
	for att_name in integer_arr_list:
		if att_name in ignore_arr_list: continue
		if att_name in select_features:
			val_arr = np.array([[float(val.strip()) for val in att_value_hash[att_name]]]).transpose()
			 
			minmax_hash[att_name] = (min(val_arr), max(val_arr))
			
			norm_val_arr = min_max_scaler.fit_transform(val_arr )	
			norm_value_hash[att_name] = norm_val_arr.transpose()
			newname_arr.append(att_name)
	 
	## 1-to-k encode categorical data 
	newcatname_arr = []
	for att_name in   category_arr_list:
		if att_name in ignore_arr_list: continue
		if att_name in select_features:
			val_arr = np.array([att_value_hash[att_name]])
			#print att_name
			#print set(val_arr[0])
			cat_matrix = categorical(val_arr[0], drop=True, dictnames=True) ##  need to indicate dimension, its the first dimension (0), each row = 1 sample
			cat_matrix_trans = np.transpose(cat_matrix[0]) ## transpose so that each row = 1 var   
			for index, ori_val in  cat_matrix[1].items():
				#print ori_val
				#print cat_matrix_trans[index]
				new_att_name = att_name+"-"+ori_val
				norm_value_hash[new_att_name] = cat_matrix_trans[index]
				newname_arr.append(new_att_name)
				newcatname_arr.append(new_att_name)
		
 	b = norm_value_hash[select_features[0]][0]
	#print b 
	imp.fit(b)
	b = imp.transform(b)
	data = np.array(b )
	 
	
	for newname in newname_arr:
		#print newname
		#print data.shape 
		if newname == select_features[0]: continue
		if newname not in newcatname_arr:
			
			b = norm_value_hash[newname][0]
			#print b 
			imp.fit(b)
			b = imp.transform(b)
  			#print b
 			#print b.shape
			data = np.concatenate((data, b  ), axis=0)
		else:
			b = np.array([norm_value_hash[newname]])
 			#print b.shape
			data = np.concatenate((data,  b), axis=0)
	
 	data =  np.transpose(data) ## row = one sample
 	
	## perform k-mean and select the best k
	maxsilh = float('-inf')
	centroid_best = []
	kbest = 0
	for ncluster in range(4,5):
		
 		centroid_arr, silhouette_avg = cluster(data, ncluster)
 		if silhouette_avg> maxsilh:
			maxsilh = silhouette_avg
			centroid_best = centroid_arr
			kbest = ncluster
		#print (ncluster, silhouette_avg)
	#noncatname_arr = list(set(newname_arr).difference(newcatname_arr))
	
	print "Best k = "+str(kbest)
	
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
	'''
	for cno in cat_hash_cluster.keys():
		print cno
		cat_hash = cat_hash_cluster[cno]
		for name, val in cat_hash.items():
			print (name, val)
	'''
	 		
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
				print val
			else: 
				print val  
 		cat_hash = cat_hash_cluster[no]
		for name, val in cat_hash.items():
			print val
			
		print ""
		
		
		#print  cat_cenarr_name
		#print cat_cenarr_val
		#print ""	
	''' 
	for row in data:
		#print row 
		f_w.write(str(row).strip("[").strip("]").replace("'","")+"\n")
 	f_w.close()
 	  
	'''
 	
 	
 	
normalize()
		
