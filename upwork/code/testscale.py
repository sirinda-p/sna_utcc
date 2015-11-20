import numpy as np
from sklearn import preprocessing
from scikits.statsmodels.tools import categorical
from sklearn.cluster import KMeans

def testScale():
	x = np.array([[1, 2, 1, 0, 2]])  # values of var1 of all samples
	print x.shape
	 
	y_arr  = np.array([['T','F2','F2','T','F1']])
	z = np.array([[1,2,2,1,2]])
	
	min_max_scaler = preprocessing.MinMaxScaler( ).fit(z )
	print z
 	x_train_minmax = min_max_scaler.fit_transform(z )
 	cat_arr = categorical(y_arr, drop=True) ## each row belong to one sample
	cat_arr_trans = np.transpose(cat_arr) ## each row = 1 var
 	
	data_temp = np.array([x_train_minmax[0]])
	print x_train_minmax[0]
	'''
  	data_temp = np.concatenate((data_temp,  np.array([cat_arr_trans[0]])), axis=0)
 	data_temp = np.concatenate((data_temp,  np.array([cat_arr_trans[1]])), axis=0)
	print data_temp
	data =  np.transpose(data_temp) ## row = one sample
	print ""
	for row in data:
		print row
		
 	k = 3
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(data) 
	labels = kmeans.labels_
	centroids = kmeans.cluster_centers_
 	 '''
	
testScale()
