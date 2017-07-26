from project_dcs_czy.dcs_czy_control.data_raw import combine_allRawData,del_stateCol
from sklearn.decomposition import PCA
from project_dcs_czy.dcs_czy_data.pca import pca,plotBestFit
from project_dcs_czy.dcs_czy_data.kmeans import *
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from scipy import io as spio
from sklearn.preprocessing import StandardScaler
raw_data=combine_allRawData()
data=del_stateCol(raw_data)
len,dim=data.shape
dataRange=[np.min(data['date']),np.max(data['date'])]
'''pca检测'''
def test_pca(data):
    X=data.drop(['date'],axis=1).as_matrix(columns=None)
    d1,d2=pca(X)
    plotBestFit(d1,d2)
def test_kmeans(data):
    dataSet=data.loc[:2000,['MW']]
# dataSet.reset_index()
# dataSet=pd.concat(dataSet.index,dataSet['MW'])
# print(list(dataSet))
    dataSet=dataSet.as_matrix(columns=None)
## step 2: clustering...
    print("step 2: clustering...")
    dataSet = mat(dataSet)
    k = 10
    centroids, clusterAssment = kmeans(dataSet, k)
    # print(centroids) #图心

    ## step 3: show the result
    print("step 3: show the result...")
    showCluster(dataSet, k, centroids, clusterAssment)