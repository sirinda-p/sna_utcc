import numpy as np
import warnings
from scikits.statsmodels.tools import categorical

import featureUtil as futil
import clusterUtil as mycluster
		
def main():
	
	machine = "amm"
 	
	if machine == "amm":
		prefix = "/home/amm/Desktop/sna-project/sna-git/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	path = prefix+"upwork/data/"
	tfname = "appt_dump_transformed.csv"
	
 	
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
	
	## Low variance features will be excluded
	ignore_arr_list = ["ID", "Carrier","AdOptedIn","AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"]
 	 
	
	original_data, att_value_hash = futil.imputeMissingValue(path, tfname, att_name_list, category_arr_list)		
  	
 	
   	## Select features
   	kpca=30
   	ncomp = 1
   	select_features = futil.pca(ncomp, original_data, kpca, att_name_list, ignore_arr_list)
	
	## normalize feature values
	data, newname_arr, newcatname_arr, minmax_hash = futil.normalize(att_value_hash, boolean_arr_list, integer_arr_list, ignore_arr_list, select_features, category_arr_list)
	
 	
 	data =  np.transpose(data)
 	minK = 3
 	maxK = 5
	centroid_best, kbest = mycluster.kmean_bestK(data, minK, maxK)
	mycluster.getCentroidValues_kmean(centroid_best, kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list, minmax_hash)
	
	
 
 	
 	
main()
		
