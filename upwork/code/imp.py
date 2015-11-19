import numpy as np
from sklearn.preprocessing import Imputer

imp = Imputer(missing_values='NaN', strategy='mean', axis=1)
x = np.array([1, 2, np.nan, 3])
print x
imp.fit(x)
x = imp.transform(x)
print x
 
