import csv
import numpy as np
import pandas as pd
import os
from project_dcs_czy.dcs_czy_control.data_processing import *
from project_dcs_czy.dcs_czy_control.data_select import *

condition_path = "E:/Data/steadyCondition.txt"
meanAndStd_type=['date','MW','MSP','THRTEMP','YRHRPRS','RRHRPRS','YRHRTEMPT','RRHRTEMPT','MWD2']
mode_type=['date','HHA11','HHA31','HHA51','HHA71','HHA81','HNA01A','HNA01B','HNA02A','HNA02B']
mean_type=['date','TOTALCOAL','TAF','O2','FWFLOW','A09M210SHH']
trapz_type=['date','LAE11','LAE12','LAE13','LAE14','LAE21','LAE22','LAE23','LAE24','TOTALCOAL','TAF','O2','FWFLOW','A09M210SHH']
stat_type=[meanAndStd_type,mode_type,mean_type,trapz_type]
'''自动选取稳定段'''
def auto_coordinateStat(data,values):
    condition_date = cut_MWByData(data.loc[:,['date','MW']], 1, True,values)
    resultData=cutData_byStat(data.loc[:,meanAndStd_type],condition_date,'meanAndStd')
    resultData = combine_csv(resultData,cutData_byStat(data.loc[:,mode_type],condition_date,'mode'), ['startDate', 'endDate'])
    # resultData = combine_csv(resultData, cutData_byStat(data.loc[:,mean_type],condition_date,'mean'), ['startDate', 'endDate'])
    resultData = combine_csv(resultData, cutData_byStat(data.loc[:, trapz_type], condition_date, 'trapz'),['startDate', 'endDate'])
    #stat=resultData.transpose().to_json()
    return resultData

'''手动选取稳定段'''
def view_processing_data():
    # 批量处理均值
    flag = 'meanAndStd'
    path = 'E:/Data/resultData/STD'
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        file_name = f.split('\\')[1]
        mode_data = cutData(condition_path, f, flag)
        exportCSV_List(mode_data, 'E:/Data/StatData/meanStd/' + file_name)
        get_stat_cocal()
    return get_stat_combineData()
def get_stat_cocal():
    flag='trapz'
    path='E:/Data/resultData/Coal20160301.csv'
    file_name = path.split('resultData/')[1]
    mode_data = cutData(condition_path, path, flag)
    exportCSV_List(mode_data, 'E:/Data/StatData/combine' + file_name)
def get_stat_combineData():

    # 合并统计后的参数文件
    data = readCSV_HeadSE('E:/Data/StatData/meanStd/mpt20160301.csv')
    path = 'E:/Data/StatData/combine'
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        tempData = readCSV_HeadSE(f)
        data = combine_csv(data, tempData, ['startDate', 'endDate'])
        # print(data1)
    file_out = 'E:/python/project_dcs_czy/static/data/stat/mean20160301.csv'
    exportCSV_DF(data, file_out)
    return data