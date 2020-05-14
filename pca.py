# Principal Component Analysis
from numpy import array
from sklearn.decomposition import PCA
import math
# define a matrix
A = array([[1, 0.22], [3, 0.44], [5, 0.66]])
print(A)
# create the PCA instance
pca = PCA(2)
# fit on data
pca.fit(A)
# access values and vectors
print('pca.components_')
print(pca.components_)


print('pca.explained_variance_')
print(pca.explained_variance_)
# transform data
#B = pca.transform(A)
#print('pca.transform(A)')
#print(B)


pca_x = pca.components_[0][0]
pca_y = pca.components_[0][1]

d=math.sqrt(pca_x*pca_x + pca_y*pca_y)

print( math.degrees( math.asin(pca_x/d) ))