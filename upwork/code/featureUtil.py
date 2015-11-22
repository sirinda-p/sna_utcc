import numpy as np
from scikits.statsmodels.tools import categorical
from sklearn.preprocessing import Imputer
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.feature_selection import VarianceThreshold

def VarianceThreshold(data):
	selector = VarianceThreshold(threshold=0.0)
	selector.fit(data)
	print selector.get_support()
	

def pca(ncomp, original_data, k, att_name_list, ignore_arr_list):
	pca = PCA(n_components=ncomp)
   	transpose_data = original_data.transpose()
 	pca.fit(transpose_data) 
	#new_data = pca.fit_transform(original_data) 
	topk_set = set()
	for n in range(0, ncomp):
		fset = set(np.abs(pca.components_[n]).argsort()[::-1][:k])
		#print fset
		topk_set = topk_set.union(fset)
		#print topk_set
		#print ""
	
	#print [att_name_list[i] for i in list(topk_set)]
	select_features = list(set([att_name_list[i] for i in list(topk_set)]).difference(set(ignore_arr_list)))
	
	return select_features
	
def imputeMissingValue(path, fname, att_name_list, category_arr_list):
	
	imp = Imputer(missing_values='NaN', strategy='mean', axis=1)
	
	att_value_hash = dict()
 
	for att_name in att_name_list:
		att_value_hash[att_name] = []
 
	f_r = open(path+fname, "r")
	for line in f_r.readlines()[1::]:
		att_arr = line.strip().split(",") 
 		 
		for val, att_name in zip(att_arr,att_name_list):
 			val = val.strip() 
 			if val == "None":
				val = np.nan 
 			att_value_hash[att_name].append(val)
	
	b = att_value_hash[att_name_list[1]]
	imp.fit(b)
	impb = imp.transform(b)
		
	data = impb
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
	 
		data = np.concatenate((data,  impb), axis=0)

	return data, att_value_hash


def selectFeatures(att_value_hash, pca_features, ignore_features ):
	 	
	select_features = list(set(pca_features).difference(ignore_features))
 	b = np.array([att_value_hash[select_features[0]]] )
 	#print b.shape
	data = np.array(b )
	#print data.shape
 	for newname in select_features[1::]:
 		b = np.array([att_value_hash[newname]])
 		#print b.shape
		data = np.concatenate((data,  b), axis=0)
	
	return np.transpose(data), select_features
	
def normalize(att_value_hash, boolean_arr_list, integer_arr_list, ignore_arr_list, select_features, category_arr_list):
	
	min_max_scaler = preprocessing.MinMaxScaler()
	
	newname_arr = [] 
 	norm_value_hash = dict()
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
			#print val_arr.transpose()
			#print len(val_arr[0])
			#min_max_scaler.fit(val_arr )	
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
	
	imp = Imputer(missing_values='NaN', strategy='mean', axis=1)			
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
	
	return data, newname_arr, newcatname_arr, minmax_hash
