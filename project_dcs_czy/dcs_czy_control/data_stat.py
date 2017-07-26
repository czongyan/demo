import scipy.integrate as sci
import numpy as np
import csv

#数值积分
#1、使用梯形法则进行数值积分
def stat_trapz(data,type):
    arr=[]
    for i in data:
        arr.append(round(i,6))
    # print(data.describe())
    ti=np.linspace(0,(data.__len__()-1),data.__len__())
    xi=[]
    for i in range(0, data.__len__()):
        xi.append(i)
        # 做标准化处理 （积分f(x)）
    return round((np.trapz(data, xi)/data.__len__()),4)

