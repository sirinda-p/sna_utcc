import featureUtil as futil
import sklearn.linear_model as linmodel
import operator

def main():
	
	machine = "aws"
	if machine == "amm":
		prefix = "/home/amm/Desktop/upwork/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/upwork/"
		
	fname_arr = ["paid.csv","churn.csv" ]
	datapath = prefix+"data/"
	
	## Compare 
	## 1. Churn paid (1) vs Active paid (0)
	## 2. Churn (churn_free + churn_paid) vs Active (Paid)
 	## 3. Paid (active_paid + churn_paid) vs Free 
	
	## 1. Active paid = 0 vs churn_paid = 1 
	fname0 = "active_paid_transformed_continent.csv"
	fname1 = "churn_paid_transformed_continent.csv"
	XData, YData, newfeature_arr = futil.makeXYforClassifier(datapath, [fname0, fname1])
	
	## Build a logistic regression 
  	logit = linmodel.LogisticRegression()
	logit.fit(XData, YData)
	coef_arr = logit.coef_
	positive_coef = dict()
	negative_coef = dict()
	
	for feature, coef in zip(newfeature_arr, coef_arr[0]):
 		if coef >0:
			positive_coef[feature] = coef
		else:
			negative_coef[feature] = coef
 
 	sorted_positive_coef = sorted(positive_coef.items(), key=operator.itemgetter(1),reverse=True) 
 	sorted_negative_coef = sorted(negative_coef.items(), key=operator.itemgetter(1)) 
	#print sorted_positive_coef
 	print "Positive features"
	for pos_tuple in sorted_positive_coef :
		print pos_tuple
	
	print "Negative features"
	for neg_tuple in sorted_negative_coef:
		print neg_tuple
	 
	## Build a decision tree
	#acc_score = logit.score(XData, YData)
 	
main()
	
'''
for fname in fname_arr:
		f_r = open(datapath+fname, "r")
		print fname + ":"+str(len(f_r.readlines()))
		f_r.close()
		
	active_paid.csv:96
	churn_free.csv:851
	churn_paid.csv:63


'''	
