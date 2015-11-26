import featureUtil as futil
import sklearn.linear_model as linmodel
import operator

import clusterUtil as mycluster
import extractUtil as extUtil

def main():
	
	machine = "aws"
	if machine == "amm":
		prefix = "/home/amm/Desktop/upwork/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/upwork/"
		
	fname_arr = ["active.csv","churn.csv" ]
	#fname_arr = ["active_paid.csv","active_free.csv","churn_free.csv","churn_paid.csv"]
	#fname_arr = ["paid.csv","free.csv","churn.csv","active.csv"]
	datapath = prefix+"data/"
	
	
	
	
	'''	
	active_paid.csv:96
	active_free.csv:375
	churn_free.csv:851
	churn_paid.csv:63
	
	paid.csv:159
	free.csv:1226
	churn.csv:914
	active.csv:471
	'''
	
	## To do 
	## 0. Cluster 4 groups of data3
	## 1. Compare Churn paid (1) vs Active paid (0)
	## 2. Compare Churn vs Active  
 	## 3. Compare Paid  vs Free 
	
	## 1. Active paid = 0 vs churn_paid = 1 
	fname0 = "active_transformed_continent.csv"
	fname1 = "churn_transformed_continent.csv"
	
	## Set minimum and maximum number of features to keep 
   	kpcamin = 10
   	kpcamax = kpcamin+1 
   	kpca = 35
   	
   	## Set minimum and maximum number of principle components, we typically keep only the first few components
   	ncompmin =  2
   	ncompmax =  3
   	ncomp = 2
   	
	XData, YData, newfeature_arr, transformed_data = futil.makeXYforClassifier_combinedData(datapath, [fname0, fname1], ncomp, kpca)
	
	print YData[0].shape
	print "kmean"
	mycluster.kmean_plot(XData, YData[0], transformed_data)
	
	
				
main()
	
'''
	for fname in fname_arr:
		f_r = open(datapath+fname, "r")
		print fname + ":"+str(len(f_r.readlines()))
		f_r.close()
'''
