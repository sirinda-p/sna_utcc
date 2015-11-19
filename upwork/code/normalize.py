import numpy as np
from sklearn import preprocessing
import warnings
from scikits.statsmodels.tools import categorical
from sklearn.cluster import KMeans
from sklearn.preprocessing import Imputer

def cluster(data):
	k = 5
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(data) 
 	centroids = kmeans.cluster_centers_
 	for c in centroids:
		print c
		
def normalize():
	
	machine = "amm"
	min_max_scaler = preprocessing.MinMaxScaler()
	imp = Imputer(missing_values='NaN', strategy='median', axis=1) 
	
	if machine == "amm":
		prefix = "/home/amm/"
	else:
		prefix = "/home/ubuntu/"
	
	path = prefix+"Desktop/upwork/data/"
	f_r = open(path+"appt_dump_transformed.csv", "r")
	f_w = open(path+"appt_dump_normMinMax.csv", "w")
	
	att_name_list = ['ID', 'AllowPush', 'AdOptedIn', 'NumCampaignMatch', 'Carrier', 'AppVersion', 
	'AllowiBeacon', 'AllowGeo', 'AllowFeaturePush', 'ScreenHeight', 'AllowBT', 'HaveUniqueGlobalID', 
	'NumCrash', 'DailyUsage', 'LastUpdateDays', 'DeviceModel', 'BlockPushTF', 'BlockPushSameday', 'BlockPushAfterDays', 
	'OS', 'OSVersion', 'RevokePushTF', 'RevokePushBefore', 'RevokePushSameday', 'RevokePushAfterDays', 'SignIn', 
	'UninstalledTF', 'UninstalledSameday', 'UninstalledAfter', 'ScreenWidth', 'EmailExist', 'EmailAddress', 
	'InstallDays', 'PushCount', 'Timezone', 'UserType', 'Questions', 'CorrectQuestion']
	
	print len(att_name_list)
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress",'BlockPushTF','BlockPushSameday','RevokePushTF',
	'RevokePushBefore', 'RevokePushSameday', 'UninstalledTF','UninstalledSameday']
	
	category_arr_list = ["Carrier","AppVersion", "DeviceModel","OS","UserType", "OSVersion","Timezone","ScreenWidth","ScreenHeight" ] 
 	
	integer_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", 'BlockPushAfterDays', 'RevokePushAfterDays', 'UninstalledAfter', 'LastUpdateDays']
	
	#print len(boolean_arr_list)+len(category_arr_list)+len(integer_arr_list)
	#print set(att_name_list).difference(set(boolean_arr_list).union(category_arr_list).union(integer_arr_list))
	 
	att_value_hash = dict()
	norm_value_hash = dict()
	newname_arr = [] 
	for att_name in att_name_list:
		att_value_hash[att_name] = []
		
	for line in f_r.readlines()[1::]:
		att_arr = line.strip().split(",") 
		for val, att_name in zip(att_arr,att_name_list):
 			val = val.strip() 
 			if val == "None":
				val = np.nan 
 			att_value_hash[att_name].append(val)
		 
  	
	norm_value_hash["ID"] = np.array([att_value_hash["ID"]]) 
	 
	## keep original boolean att
	for att_name in  boolean_arr_list:
		norm_value_hash[att_name] = np.array([att_value_hash[att_name]])
		newname_arr.append(att_name)
		
	## normalize interger attributes 
	for att_name in integer_arr_list:
		#print att_name
		val_arr = np.array([att_value_hash[att_name]])
		#print len(val_arr[0])
		norm_val_arr = min_max_scaler.fit_transform(val_arr )	
		norm_value_hash[att_name] = norm_val_arr
		newname_arr.append(att_name)
		
	## 1-to-k encode categorical data 
	newcatname_arr = []
	for att_name in   category_arr_list:
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
			
	
	data = np.array([norm_value_hash["AllowPush"][0]] )
	 
	
	for newname in newname_arr:
		#print newname
		#print data.shape 
		if newname == "AllowPush": continue
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
 			#print b
			data = np.concatenate((data,  b), axis=0)
	
	## write to a file 
	data =  np.transpose(data) ## row = one sample
	cluster(data)
	for row in data:
		#print row 
		f_w.write(str(row[0]).strip("[").strip("]").replace("'","")+"\n")
 	f_w.close()
 	  
normalize()
		
