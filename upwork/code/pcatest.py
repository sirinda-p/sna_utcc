import numpy as np
from sklearn.decomposition import PCA

X = np.array([[-1, -1, 0], [-2, -1, 0], [-3, -2, 0], [1, 1, 0], [2, 1, 0], [3, 2, 0]]) ## row = sample
print X.shape

pca = PCA(n_components=1)
pca.fit(X)
#print(pca.explained_variance_ratio_) 
print pca.components_.shape
#print pca.transform(X)
 
