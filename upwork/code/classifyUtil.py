from sklearn import linear_model, decomposition, datasets
import sklearn.svm as mysvm
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np
	
def logistic_plot():
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
 
def logistic(X, Y):
	## Build a logistic regression 
	param_grid = {'penalty':['l2', 'l1'],'C': [0.1, 1, 10, 100, 1000]},
  	logit =  linear_model.LogisticRegression()
	
	estimator =  GridSearchCV(logit, param_grid)
	estimator.fit(X, Y)
	best_estimator = estimator.best_estimator_
	acc_score = best_estimator.score(X,Y)
	print estimator.best_params_
	print acc_score
	
	
def svm(X, Y):
	param_grid = {'C': [0.1, 1, 10, 100, 1000], 'loss' : ['hinge', 'squared_hinge'],  'penalty':['l2']},
 	
	svm = mysvm.LinearSVC()
	
	estimator = GridSearchCV(svm, param_grid)
	
	estimator.fit(X, Y)
	best_estimator = estimator.best_estimator_
	acc_score = best_estimator.score(X,Y)
	''' Check out for posts on how to get informative features from svm
	http://stackoverflow.com/questions/11116697/how-to-get-most-informative-features-for-scikit-learn-classifiers 
	http://stats.stackexchange.com/questions/39243/how-does-one-interpret-svm-feature-weights
	'''
 		
def pca_logistic(X, Y):
 
	logistic = linear_model.LogisticRegression()

	pca = decomposition.PCA()
	pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])
 
	###############################################################################
	# Plot the PCA spectrum
	pca.fit(X)

	plt.figure(1, figsize=(4, 3))
	plt.clf()
	plt.axes([.2, .2, .7, .7])
	plt.plot(pca.explained_variance_, linewidth=2)
	plt.axis('tight')
	plt.xlabel('n_components')
	plt.ylabel('explained_variance_')

	###############################################################################
	# Prediction

	n_components = [2,  6, 10]
	Cs = np.logspace(-4, 4, 3)

	#Parameters of pipelines can be set using '__' separated parameter names:

	estimator = GridSearchCV(pipe,
							 dict(pca__n_components=n_components,
								  logistic__C=Cs))
	estimator.fit(X, Y)
	best_estimator = estimator.best_estimator_
 	acc_score = best_estimator.score(X,Y)
 	print acc_score
 	
	'''
	
	#plt.scatter(transformed_data[:, 0], transformed_data[:, 1],  c=colors[Y].tolist(), s=10)
	 
	plt.axvline(estimator.best_estimator_.named_steps['pca'].n_components,
				linestyle=':', label='n_components chosen')
	plt.legend(prop=dict(size=12))
	plt.show()
	 '''
	
	
