import numpy as np
import warnings
from scikits.statsmodels.tools import categorical

import extractUtil as extUtil
import featureUtil as futil
import clusterUtil as mycluster
		
def main():
	
	 
	prefix = "/home/amm/Desktop/upwork/"
	
	datapath = prefix+"data/"
	resultpath = prefix+"results/"
	
	original_filename = "appt_dump.csv" 
	
	max_num_att = 36
	
	#checked_fname = extUtil.checkFile(datapath, original_filename, max_num_att )
	checked_fname = original_filename.replace(".csv","_checked.csv")
	#transformed_fname =  "appt_dump_transformed.csv"
	transformed_fname = extUtil.transformFeature(datapath, checked_fname)
 	''' 
	## New feature names after data transformation
	att_name_list = ["ID", "AllowPush", "AdOptedIn", "NumCampaignMatch", "Carrier", "AppVersion", 
	"AllowiBeacon", "AllowGeo", "AllowFeaturePush", "ScreenHeight", "AllowBT", "HaveUniqueGlobalID", 
	"NumCrash", "DailyUsage","Country", "LastUpdateDays", "DeviceModel", "BlockPushTF", "BlockPushSameday", "BlockPushAfterDays", 
	"OS", "OSVersion", "RevokePushTF", "RevokePushBefore", "RevokePushSameday", "RevokePushAfterDays", "SignIn", 
	"UninstalledTF", "UninstalledSameday", "UninstalledAfter", "ScreenWidth", "EmailExist", "EmailAddress", 
	"InstallDays", "PushCount", "Timezone", "UserType", "Questions", "CorrectQuestion"]
	
	## Boolean feature list
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress","BlockPushTF","BlockPushSameday","RevokePushTF",
	"RevokePushBefore", "RevokePushSameday", "UninstalledTF","UninstalledSameday"]
	
	## Categorical feature list
	category_arr_list = ["AppVersion","Carrier", "DeviceModel","OS","UserType", "OSVersion","Timezone","ScreenWidth","ScreenHeight","Country" ] 
 	
	integer_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", "BlockPushAfterDays", "RevokePushAfterDays", "UninstalledAfter", "LastUpdateDays"]
	
	## Low variance features will be excluded
	ignore_arr_list = ["ID", "AdOptedIn","Carrier","AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"]
 	 
	## Impute missing data
	original_data, att_value_hash = futil.imputeMissingValue(datapath, transformed_fname, att_name_list, category_arr_list)		
  	
    ## Select features
   	#futil.VarianceThreshold(original_data)
   	
   	## Set minimum and maximum number of features to keep 
   	kpcamin = 10
   	kpcamax = kpcamin+1 
   	
   	## Set minimum and maximum number of principle components, we typically keep only the first few components
   	ncompmin =  2
   	ncompmax =  3
   	
   	## Indicate a clustering algorithm
   	algorithm = "birch" ## Available algorithms = cobweb, kmean, Affinity, dbscan, birch
   	
   	
   	## Perform grid search to find the best parameter setting
	for kpca in np.arange(kpcamin,kpcamax, 5):
		for ncomp in np.arange(ncompmin,ncompmax, 2):
		
		
			## Perform feature selection
			print "pca="+str(kpca)+", ncom="+str(ncomp)
			select_features = futil.pca(ncomp, original_data, kpca, att_name_list, ignore_arr_list)
			
			
			# Uncomment these lines of code to print selected features
			print "#features = "+str(len(select_features))
			for f in select_features:
				print f
			print ""
		 
			
			## Normalize selected features
			data, newname_arr, newcatname_arr, minmax_hash = futil.normalize(att_value_hash, boolean_arr_list, integer_arr_list, ignore_arr_list, select_features, category_arr_list)
			data =  np.transpose(data)
			
			if 	algorithm == "kmean":
				minK = 3 
				maxK = 5
				print "kmean"
				centroid_best, kbest = mycluster.kmean_bestK(data, minK, maxK)
					
			elif algorithm == "Affinity":
				print "Affinity"
				centroid_best,kbest = mycluster.affinity(data)
				 
			elif algorithm == "dbscan":
			
				print "dbscan"
				centroid_best,kbest= mycluster.dbscan(data)
				 	
			elif  algorithm == "birch":
				
				print "birch"
				centroid_best,kbest = mycluster.birch(data)
 			
			elif algorithm == "cobweb": ## Cobweb algorithm requires different data format  
				
				print "conceptual clustering"
				cobweb_data, cobweb_features = futil.selectFeatures(att_value_hash, select_features, ignore_arr_list )
 				centroid_best,kbest = mycluster.cobweb(cobweb_data, cobweb_features, integer_arr_list, data)
		 
			else:
				print "Invalid algorithm"
			
			if algorithm != "cobweb": ## Cobweb returns different output format. 
				
				## Convert normalized values to original values		
				centroid_hash_allclusters = mycluster.getCentroidValues(centroid_best, kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list, minmax_hash)
				
				## Save output to a file
				rname = algorithm+"_nfeatures"+str(len(select_features))+"_pca"+str(kpca)+"_ncomp"+str(ncomp)+".csv"
				f_w = open(resultpath+rname, "w")
				tow = ""
				for k in range(0,kbest):
					tow += ",Cluster #"+str(k)
				f_w.write(tow+"\n")
				for name in sorted(centroid_hash_allclusters.keys()):
					val_arr = centroid_hash_allclusters[name]
					print name+":"+str(val_arr)
					tow = name 
					for val in val_arr:
						tow += ","+val
					f_w.write(tow+"\n")
				f_w.close()
				''' 
main()
		
