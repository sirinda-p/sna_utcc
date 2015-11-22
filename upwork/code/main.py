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
	
	datapath = prefix+"upwork/data/"
	resultpath = prefix+"upwork/results/"
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
	ignore_arr_list = ["ID", "AdOptedIn","AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"]
 	 
	
	original_data, att_value_hash = futil.imputeMissingValue(datapath, tfname, att_name_list, category_arr_list)		
  	
    ## Select features
   	#futil.VarianceThreshold(original_data)
   	
   	kpcamin = 35
   	kpcamax = kpcamin+1
   	ncompmin =  8
   	ncompmax =  9
   	algorithm = "cobweb" ## Available algorithms = cobweb, kmean, Affinity, dbscan, birch
   	
	for kpca in np.arange(kpcamin,kpcamax, 5):
		for ncomp in np.arange(ncompmin,ncompmax, 2):
		
		
			## Perform feature selection
			print "pca="+str(kpca)+", ncom="+str(ncomp)
			select_features = futil.pca(ncomp, original_data, kpca, att_name_list, ignore_arr_list)
			'''
			print "#features = "+str(len(select_features))
			for f in select_features:
				print f
			print ""
			'''
			
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
				#mycluster.getCentroidValues_kmean(centroid_best,kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list,minmax_hash)
			
			elif algorithm == "cobweb": ## Cobweb algorithm requires different data format  
				print "conceptual clustering"
				
				cobweb_data, cobweb_features = futil.selectFeatures(att_value_hash, select_features, ignore_arr_list )
				#print cobweb_data.shape
				centroid_best,kbest = mycluster.cobweb(cobweb_data, cobweb_features, integer_arr_list, data)
		 
			else:
				print "Invalid algorithm"
			
			if algorithm != "cobweb":		
				centroid_hash_allclusters = mycluster.getCentroidValues(centroid_best, kbest, newcatname_arr, newname_arr, integer_arr_list, boolean_arr_list, minmax_hash)
				
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
main()
		
