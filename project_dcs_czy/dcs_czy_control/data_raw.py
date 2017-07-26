from project_dcs_czy.dcs_czy_data.data_import import *
import numpy as np
import pandas as pd
def combine_allRawData():
    time_flag='0301.csv'
    path_in='E:/Data/resultData/STD'
    path_other=['E:/Data/resultData/mode','E:/Data/resultData/definite','E:/Data/resultData/other']
    raw_data=DataFrame()
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path_in) for fn in files]
    for f in fns:
        temp_name=f.split('2016')[1]
        if(temp_name==time_flag):
            raw_data = readCSV_Head(f)
    for row in path_other:
        fns = [os.path.join(root, fn) for root, dirs, files in os.walk(row) for fn in files]
        for f in fns:
            temp_name = f.split('2016')[1]
            if (temp_name == time_flag):
                tempData = readCSV_Head(f)
                raw_data = combine_csv(raw_data, tempData, ['date'])
    # print("所有属性的未处理原始数据")
    # print(raw_data)
    return raw_data
def del_stateCol(raw_data):
    raw_col=raw_data.columns
    del_col=[]
    #删除状态码属性列
    for val in raw_col[:]:
        if val.find('State') > 0: #不匹配返回-1，匹配返回>0的值
            # print(val)
            del_col.append(val)
    data=raw_data.drop(del_col,axis=1,inplace=False)  #, inplace=False 会对原数组作出修改并返回一个新数组,inplace=False,对原数组直接进行更改
    # print(data)
    return data