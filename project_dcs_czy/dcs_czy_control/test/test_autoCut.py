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
from project_dcs_czy.dcs_czy_control.data_select import *

raw_data=combine_allRawData()
data=del_stateCol(raw_data)
len,dim=data.shape
dataRange=[np.min(data['date']),np.max(data['date'])]
values=[900,1000,0.03]
water_flag=[10,30]
# temp=segment_dataBySet(raw_data)
condition_date = segment_dataBySet(data.loc[:,['date','MW','coalMill','PAB10CT101','PAB10CT103']], 1, True,6,water_flag,values)
print(condition_date)