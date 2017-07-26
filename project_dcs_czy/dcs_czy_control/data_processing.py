from pandas import Series,DataFrame
from project_dcs_czy.dcs_czy_control.data_stat import *
from scipy.stats import mode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from decimal import Decimal
import scipy.integrate as sci
import os
import csv

#导入一个文件夹下的所有.csv文件并按照文件名顺序排列好
def getAllCSVName(path):
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]  # 获取的所有文件名
    order = []  # 获取的所有文件名后序号
    files = []  # 排序后的文件列表
    dir = fns[1].split('page')[0];
    for f in fns:  # 获取的所有文件名
        num = f.split('page')
        if (f.__len__() > 1):
            order.append(int(num[1].split('.')[0]))
    order.sort()
    for num in order:
        file_in = dir + "page" + str(num) + ".csv"
        files.append(file_in)
    return files

#不带表头读取csv文件,并且格式化
def import_csv_noHead(file_in):
    csvfile=open(file_in,'r')
    lineArr=[]
    resultArr=[]
    # for line in csvfile.readlines()[0:1]:
    #     arr=line.strip().split(',')
    #     for i in arr:
    #         i.replace('时间','date').replace('UNIT3','').replace('数值','').replace('状态','')
    #         print(i)
    #     heading.append(line.strip().split(','))
    # print(heading)
    for line in csvfile.readlines()[1:]:
        lineArr.append(line.strip().split(','))

    def isEmpty(str):
        if(str==""):
            return True
        else:
            return False

    def replaceStr(str,flag):
        if flag==0:
            return str.replace("        ", "").replace("     ", "").replace("\t", "")
        else:
            return str.replace("        ", "").replace("     ", "").replace(" ","").replace("\t", "")

    len=lineArr.__len__();
    for i in range(0,len):
        if lineArr[i]!="": #判断本行是不是为空
            str=[]
            str .append(replaceStr(lineArr[i][0],0))
            for val in lineArr[i][1:]:
                if isEmpty(val)==True : #为空时(取上一行或者下一行想对应的数据)
                    index=lineArr[i].index(val)
                    if(i<=0):
                        val=lineArr[i+1][index]
                    if(i>len):
                        val = lineArr[i + 1][index]
                    val = replaceStr(val,1)
                    str.append(val)
                else:
                    val = replaceStr(val,1)
                    if(val<'0'):   #判断取值是否为负值
                        val=0
                    str.append(val)
            resultArr.append(str[:-1])
    return(resultArr)
#表头自定义
def processingCSVNOHead(file_in,file_out,heading):
    csvfile=open(file_in,'r')
    lineArr=[]
    resultArr=[]
    for line in csvfile.readlines()[0:]:
        lineArr.append(line.strip().split(','))

    def isEmpty(str):
        if(str==""):
            return True
        else:
            return False

    def replaceStr(str,flag):
        if flag==0:
            return str.replace("        ", "").replace("     ", "").replace("\t", "")
        else:
            return str.replace("        ", "").replace("     ", "").replace(" ","").replace("\t", "")

    len=lineArr.__len__();
    for i in range(0,len):
        if lineArr[i]!="": #判断本行是不是为空
            str=[]
            str .append(replaceStr(lineArr[i][0],0))
            for val in lineArr[i][1:]:
                if isEmpty(val)==True : #为空时(取上一行或者下一行想对应的数据)
                    index=lineArr[i].index(val)
                    if(i<=0):
                        val=lineArr[i+1][index]
                    if(i>len):
                        val = lineArr[i + 1][index]
                    val = replaceStr(val,1)
                    str.append(val)
                else:
                    val = replaceStr(val,1)
                    if(val<'0'):   #判断取值是否为负值
                        val=0
                    str.append(val)
            resultArr.append(str[:-1])
    print(list(resultArr))

    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        for item in resultArr[:-1]:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(resultArr.index(item))
            else:
                writer.writerow(item)
    print('processing'+file_in+' success!')



#使用自带表头(导出的文件最后总多一个空行)
def processingCSV(file_in, file_out):
    csvfile=open(file_in,'r')
    lineArr=[]
    resultArr=[]
    stateArr=[]
    for line in csvfile.readlines()[0:]:
        lineArr.append(line.strip().split(','))
    def isEmpty(str):
        if(str==""):
            return True
        else:
            return False

    def replaceStr(str,flag):
        if flag==0:
            return str.replace("        ", "").replace("     ", "").replace("\t", "").replace("       ","")
        else:
            return str.replace("        ", "").replace("     ", "").replace(" ","").replace("\t", "").replace("       ","")

    def countState(state,row):
        if(row>0):
            str=state.split('x')
            if(str.__len__()>1):
                if(str[1]!="0000"):
                    stateArr.append([row,lineArr[i][0],state])

    len=lineArr.__len__()
    # len=2
    for i in range(0,len):
        # print(lineArr[i])
        if lineArr[i].__len__()>0: #判断本行是不是为空
            str=[]
            str .append(replaceStr(lineArr[i][0],0))
            for val in lineArr[i][1:]:
                if isEmpty(val)==True : #为空时(取上一行或者下一行想对应的数据)
                    index=lineArr[i].index(val)
                    if(i<=0):
                        val=lineArr[i+1][index]
                    if(i>len):
                        val = lineArr[i + 1][index]
                    val = replaceStr(val,1)
                    str.append(val)
                else:
                    val = replaceStr(val,1)
                    countState(val, i)
                    if(val<'0'):   #判断取值是否为负值
                        val=0
                    str.append(val)
                 # print(str[:-1])
            resultArr.append(str[:-1])

    with open(file_out, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        for item in resultArr[:-1]:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(resultArr.index(item))
            else:
                writer.writerow(item)
        if(stateArr.__len__()>1):
            print(file_in+'存在异常状态详细情况：')
            print(stateArr)
        print('processing'+file_in+' success!')



#二次数据处理

#读取时间格式csv
#方法一：csv文件无标题
def readCSVDateTime_NoHead(file_in,col_names,):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    lines = pd.read_csv(file_in, sep=',', header=1, names=col_names, index_col='date', parse_dates=[0],
                        date_parser=dateparse, skip_blank_lines=True)
    return lines
#方法二：csv文件存在标题
#使用文件自带标题
def readCSVDateTime_Head(file_in):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    lines = pd.read_csv(file_in, sep=',',header=0,index_col='date', parse_dates=[0],date_parser=dateparse,skip_blank_lines=True,encoding="utf-8")
    return lines

#使用文件自带标题  时间格式化（2016-01-01 01:01:01）
def readCSV_Head(file_in):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    lines = pd.read_csv(file_in, sep=',',header=0, parse_dates=[0],date_parser=dateparse,skip_blank_lines=True,encoding="utf-8")
    return lines

#使用文件自带标题 不限制时间格式
def readCSV_HeadSE(file_in):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')
    lines = pd.read_csv(file_in, sep=',',header=0,skip_blank_lines=True,encoding="utf-8")
    return lines

#获取一段时间段数据,保留有效数字bit
def cutDataStartToEnd(data,type,startDate,endDate):
    temp_data = data[(startDate < data.index) & (data.index < endDate)]
    # 截取需要的行，列
    dt=temp_data.loc[:,[type]]
    arr=[];
    for i in dt[type]:
         val=Decimal(i).quantize(Decimal('0.0000'))
         arr.append(val)
    return arr;

#获取一段时间段数据多参数统计结果,保留有效数字bit dataFrame 设置index=date
def cutAllDataStartToEnd(data,type,startDate,endDate):
    temp_data = data[(startDate <=data.index) & (data.index <= endDate)]
    # 截取需要的行，列
    dt=temp_data.loc[:,type]
    # result=[];
    # for col in type:
    #     arr = [];
    #     for i in dt[col]:
    #         val=Decimal(i).quantize(Decimal('0.0000'))
    #         arr.append(val)
    # result.append([col,arr])
    # print(result)
    return dt;
#获取一段时间段数据多参数统计结果,保留有效数字bit, data为普通的DataFrame 没有设置index
def cutAllDataStartToEnd_NoIndex(data,type,startDate,endDate):
    temp_data = data[(startDate <=data['date']) & (data['date'] <= endDate)]
    # 截取需要的行，列
    dt=temp_data.loc[:,type]
    # result=[];
    # for col in type:
    #     arr = [];
    #     for i in dt[col]:
    #         val=Decimal(i).quantize(Decimal('0.0000'))
    #         arr.append(val)
    # result.append([col,arr])
    # print(result)
    return dt

# 截取mpt flag:统计算法标志
def cutData(condition_path,file_path,flag):
    f=open(condition_path,'r')
    line=f.readline()
    dateLag=[]
    while line:
        start_end = []
        for val in line.replace('\n','').split('至'):
            start_end.append(val)
        dateLag.append(start_end)
        line=f.readline()
    f.close()
    return cutData_mpt_std(file_path,dateLag,flag)

'''截取原始数据并作统计处理,最终返回DataFrame类型'''
def cutData_byStat(data,dataLag,flag):
    end_index=[]
    end_data=[]
    type=[]
    for i in data.columns:
        if(i.find('State')<0):
            if(i.find('date')<0):
                type.append(i)
    if(flag=="meanAndStd"):
        end_index=['startDate','endDate','MWStd']
    else:
        end_index = ['startDate', 'endDate']
    end_index.extend(type)
    for row in dataLag:
        cutData=data[(row[0] <=data['date']) & (data['date'] <=row[1])]
        std_data = row[:]
        for col in type:
            if flag == 'ptp':  # 极差:极差是只考虑了最大值和最小值的发散程度指标
                std_data.append(round(np.ptp(cutData[col]), 8))
            if flag == 'Variance':  # 方差：相对，方差包含了更多的信息
                std_data.append(round(np.var(cutData[col]), 8))
            if flag == 'std':  # 标准差：标准差基于方差但是与原始数据同量级
                std_data.append(round(np.std(cutData[col]), 8))
            if flag == 'cv':  # 变异系数：变异系数基于标准差但是进行了无量纲处理
                std_data.append(np.std(cutData[col]) / np.mean(cutData[col]))
            if flag == 'mode':  # 众数
                arr = mode(cutData[col]).mode
                if (arr.__len__() > 1):
                    std_data.append(arr)
                else:
                    std_data.append(arr[0])
            if flag == 'mean':  # 均值
                std_data.append(np.mean(cutData[col]))
            if flag == 'med':  # 中位数
                std_data.append(np.median(cutData[col]))
            if flag == 'max':  # 最大数
                std_data.append(max(cutData[col]))
            if flag == 'min':  # 最小数
                std_data.append(min(cutData[col]))
            if flag == "trapz":  # 梯形法则积分
                std_data.append(stat_trapz(cutData[col], col))
            if flag == "meanAndStd":  # 分模块统计功率和其他参数
                if (col == "MW"):
                    std_data.append(np.std(cutData[col]))
                    std_data.append(np.mean(cutData[col]))
                else:
                    if (col == 'MWD2'):
                        std_data.append(np.mean(cutData[col]))
                    else:
                        std_data.append(np.mean(cutData[col]))
                        # std_data.append(round(np.std(cutData[col]), 6))
        end_data.append(std_data)
    return pd.DataFrame(end_data,columns=end_index)
#end_data 多个我稳定时间段mpt方差list
def cutData_mpt_std(file_path,dateLag,flag):
    data = readCSVDateTime_Head(file_path)
    end_data=[]
    type=[]
    for i in data.columns:
        if(i.find('State')<0):
            type.append(i)
    if(flag=="meanAndStd"):
        end_data=[['startDate','endDate','MWStd']]
    else:
        end_data = [['startDate', 'endDate']]
    end_data[0].extend(type)#'MW', 'MSP', 'THRTEMP', 'MWD2','YRHRPRS','RRHRPRS','YRHRTEMPT','RRHRTEMPT']]
    index=0;
    print(dateLag)
    for row in dateLag:
        # std_data=[]
        cutData=cutAllDataStartToEnd(data,type,row[0],row[1])
        std_data=row[:]
        # print(row)
        #发散程度：对数据的中心位置有所了解以后，一般我们会想要知道数据以中心位置为标准有多发散。如果以中心位置来预测新数据，那么发散程度决定了预测的准确性(ptp,variance,std,cv)
        for col in type:
            if flag=='ptp': #极差:极差是只考虑了最大值和最小值的发散程度指标
                std_data.append(round(np.ptp(cutData[col]), 8))
            if flag=='Variance':#方差：相对，方差包含了更多的信息
                std_data.append(round(np.var(cutData[col]), 8))
            if flag=='std':#标准差：标准差基于方差但是与原始数据同量级
                std_data.append(round(np.std(cutData[col]),8))
            if flag=='cv':#变异系数：变异系数基于标准差但是进行了无量纲处理
                std_data.append(np.std(cutData[col])/np.mean(cutData[col]))
            if flag=='mode':#众数
                arr=mode(cutData[col]).mode
                if(arr.__len__()>1):
                    std_data.append(arr)
                else:
                    std_data.append(arr[0])
            if flag=='mean': #均值
                std_data.append(np.mean(cutData[col]))
            if flag=='med':#中位数
                std_data.append(np.median(cutData[col]))
            if flag=='max':#最大数
                std_data.append(max(cutData[col]))
            if flag == 'min':  # 最小数
                std_data.append(min(cutData[col]))
            if flag=="trapz": #梯形法则积分
                std_data.append(stat_trapz(cutData[col],col))
            if flag=="meanAndStd":#分模块统计功率和其他参数
                if (col=="MW"):
                    std_data.append(np.std(cutData[col]))
                    std_data.append(np.mean(cutData[col]))
                else:
                    if (col=='MWD2'):
                        std_data.append(np.mean(cutData[col]))
                    else:
                        std_data.append(round(np.std(cutData[col]),8))
        end_data.append(std_data)
    return end_data

#合并（根据下标）两个csv的列，key为合并的标识列
def combine_csv(data1,data2,key):
    return pd.merge(data1,data2,on=key)

#list数据存储为csv文件
def exportCSV_List(data,file_out):
    with open(file_out, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        for item in data:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(data.index(item))
            else:
                writer.writerow(item)
        print(file_out+'export success!')

# 处理喷水list数据存储为csv文件
def exportCSV_ListSum(data, file_out):
    with open(file_out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        head=data[0]
        LAE1=[]
        LAE2=[]
        arr=[]
        for i in head:
            if i.find('LAE1')==0:
                LAE1.append(head.index(i))
            if i.find('LAE2')==0:
                    LAE2.append(head.index(i))
            if (i=="startDate")|(i=="endDate")|(i=='LAE11')|(i=='LAE21'):
                arr.append(i)
        arr.append('sumLAE')
        writer.writerow(arr)
        for item in data[1:]:
            if item.__len__() == 0:  # 去除空行
                    # print("存在空的")
                print(data.index(item))
            else:
                sumLAE1 = 0
                sumLAE2 = 0
                sumArr=[]
                for i in LAE1:
                    sumLAE1=sumLAE1+item[i]
                for i in LAE2:
                    sumLAE2=sumLAE2+item[i]
                for j in (0,1):
                    sumArr.append(item[j])
                sumArr.append(sumLAE1)
                sumArr.append(sumLAE2)
                sumArr.append((sumLAE1+sumLAE2))
                # print(sumArr)
                writer.writerow(sumArr)
        print('export success!')
def exportCSV_ListAF(data,file_out):
    with open(file_out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        head = data[0]
        arr = []
        arr_index=[]
        for i in head:
            if (i=="startDate")|(i=="endDate")| (i == 'HHA11') | (i == 'HHA31')|(i == 'HHA51'):
                # print(i)
                arr.append(i)
                arr_index.append(head.index(i))
        writer.writerow(arr)
        for item in data[1:]:
            if item.__len__() == 0:  # 去除空行
                # print("存在空的")
                print(data.index(item))
            else:
                exArr = []
                for i in arr_index:
                    exArr.append(item[i])
                # print(exArr)
                writer.writerow(exArr)
        print(file_out+'export success!')
def exportCSV_ListAGP(data,file_out):
    with open(file_out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        head = data[0]
        arr = []
        arr_index=[]
        for i in head:
            if (i=="startDate")|(i=="endDate")| (i == 'HHA71') | (i == 'HHA81'):
                # print(i)
                arr.append(i)
                arr_index.append(head.index(i))
        writer.writerow(arr)
        for item in data[1:]:
            if item.__len__() == 0:  # 去除空行
                # print("存在空的")
                print(data.index(item))
            else:
                exArr = []
                for i in arr_index:
                    exArr.append(item[i])
                # print(exArr)
                writer.writerow(exArr)
        print(file_out+'export success!')
#dataframe存储为csv文件
def exportCSV_DF(data,file_out):
    data.to_csv(file_out, index=False, sep=',')

