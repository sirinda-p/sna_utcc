import featureUtil as futil
import sklearn.linear_model as linmodel


import clusterUtil as mycluster
import extractUtil as extUtil
import classifyUtil as myclassifier


def main():
	
	machine = "amm"
	if machine == "amm":
		prefix = "/home/amm/Desktop/sna-project/sna-git/upwork/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/upwork/"
		
	fname_arr = ["active.csv","churn.csv" ]
	#fname_arr = ["active_paid.csv","active_free.csv","churn_free.csv","churn_paid.csv"]
	#fname_arr = ["paid.csv","free.csv","churn.csv","active.csv"]
	datapath = prefix+"data/"
	plotpath =  prefix+"results/plot/"
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
	fname0_arr = ["active_paid_transformed_continent.csv","active_free_transformed_continent.csv",
	"churn_transformed_continent.csv","paid_transformed_continent.csv"]
	fname1_arr = ["churn_paid_transformed_continent.csv","churn_free_transformed_continent.csv",
	"active_transformed_continent.csv","free_transformed_continent.csv"]
	
	## Set minimum and maximum number of features to keep 
   	kpcamin = 10
   	kpcamax = kpcamin+1 
   	kpca = 35
   	
   	## Set minimum and maximum number of principle components, we typically keep only the first few components
   	ncompmin =  3
   	ncompmax =  4
   	ncomp = 2
   	for fname0, fname1 in zip(fname0_arr, fname1_arr):
		print fname0+"-"+fname1
		XData, YData, newfeature_arr  = futil.makeXYforClassifier_combinedData(datapath, [fname0, fname1], ncomp, kpca)
		print "svm"
		print  len(newfeature_arr )
		myclassifier.svm(XData, YData, newfeature_arr)
		break
		#print "logistic"
		#myclassifier.logistic(XData, YData)
	
				
main()
	
'''
	for fname in fname_arr:
		f_r = open(datapath+fname, "r")
		print fname + ":"+str(len(f_r.readlines()))
		f_r.close()
'''
