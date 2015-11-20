import numpy as np
from sklearn import preprocessing


X_train = np.array([[ 1., -1.,  2.] ]).transpose()
 
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(X_train)
print X_train_minmax.transpose()
