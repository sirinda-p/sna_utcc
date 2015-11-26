
def logistic()
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
	
