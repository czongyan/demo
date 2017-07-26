import numpy as np
import pandas as pd
from project_dcs_czy.dcs_czy_control.data_processing import *
import os

#import_rawData按照指定的路径导入所有的原始数据并导出为一个csv文档和多个按月的csv文档
def import_bottomLayerData(file_in):
    path_all = getAllCSVName(file_in)
    frames = import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        df = import_csv_noHead(f)
        frames.extend(df[1:])
    header = getHeading(path_all[0])
    result=[]
    for item in frames:
        if(len(item)>0):
            result.append(item)
    return pd.DataFrame(result,columns=header)
def import_rawData(file_in):
    parentDir = eachFile(file_in)
    '''初始化首个文件'''
    file_out = 'E:/Data/rawData/rawData' + parentDir[0].split('/')[3].split('-')[0] + '.csv'
    raw_data = DataFrame()
    dir = eachFile(parentDir[0])
    raw_data = import_bottomLayerData(dir[0])
    for i in range(1, len(dir)):
        temp_data = import_bottomLayerData(dir[i])
        raw_data = combine_csv(raw_data, temp_data, ['date'])
    raw_col = raw_data.columns
    del_col = []
    # 删除状态码属性列
    for val in raw_col[:]:
        if val.find('State') > 0:  # 不匹配返回-1，匹配返回>0的值
            del_col.append(val)
    result_data = raw_data.drop(del_col, axis=1, inplace=False)
    exportCSV_DF(result_data, file_out)
    '''循环合并其他文件下数据'''
    for raw in parentDir[1:]:
        file_out = 'E:/Data/rawData/interval-1min/rawData' + raw.split('/')[3].split('-')[0] + '.csv'
        raw_data = DataFrame()
        dir = eachFile(raw)
        raw_data = import_bottomLayerData(dir[0])
        for i in range(1, len(dir)):
            temp_data = import_bottomLayerData(dir[i])
            raw_data = combine_csv(raw_data, temp_data, ['date'])
        raw_col = raw_data.columns
        del_col = []
        # 删除状态码属性列
        for val in raw_col[:]:
            if val.find('State') > 0:  # 不匹配返回-1，匹配返回>0的值
                del_col.append(val)
        data = raw_data.drop(del_col, axis=1, inplace=False)
        exportCSV_DF(data, file_out)
        '''按行合并多个csv文件'''
        resultData=pd.concat([result_data,data],axis=0)
        print(resultData)
    file_out='E:/Data/rawData/interval-1min/allRawData.csv'
    exportCSV_DF(resultData, file_out)
    return True
'''重采样原始数据：interval-采样间隔'''
def resample_rawData(file_in,interval):
    parentDir = eachFile(file_in)
    file_out='E:/Data/rawData/interval-'+interval+'/'
    for row in parentDir:
        data=readCSV_Head(row)
        '''重采样'''
        data['date'] = data['date'].astype(pd.datetime)
        data = data.set_index('date')
        data=data.resample(rule=interval).mean()
        data=data.reset_index()
        exportCSV_DF(data, file_out+row.split('/')[4])
    print(True)
    return True
# 遍历指定目录，显示目录下的所有文件名 只能显示当前目录下所有文件夹 不能递归去查找在下一层的文件夹
def eachFile(filePath):
    pathDir=os.listdir(filePath)
    child=[]
    for allDir in pathDir:
        child.append(os.path.join('%s/%s'%(filePath,allDir)))
        # print(child.decode('gbk'))
    print(child)
    return child
# eachFile(filePath)
#遍历指定目录下所有文件夹
def readDir(filePath):
    rootDir = filePath # refer root dir
    for parent, dirNames, fileNames in os.walk(rootDir):#三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for dirname in dirNames: #输出目录信息
            print(parent)
            print(dirname)
        for filename in fileNames:#输出文件信息
            print(parent)
            print(filename)
            print("path:"+os.path.join(parent, filename))# perfect path#文件的完整路径

#预处理风氧煤数据（加载原始多个csv）
#添加新标题 导出为新的数据
def merge(x, y):
    for k,v in y.items():
        try:
            a_v = []
            x_pre = x[k]
            if isinstance(x_pre,list):
                a_v.extend(x_pre)
            else:
                a_v.append(x_pre)
            a_v.append(v)
            x[k] = list(set(a_v))
        except KeyError:
            x[k] = v
    return x
def getHeading(file_in):
    csvfile = open(file_in, 'r')
    resultArr = []
    heading=[]
    for line in csvfile.readlines()[0:1]:
        arr=line.strip().split(',')
        for i in arr[:-1]:
            i=i.replace('时间','date').replace('UNIT3:','').replace('数值','').replace('状态','State')
            heading.append(i)
    # resultArr.append(heading)
    return heading

def data_importCoalO2():
    path='E:/Data/2016-3-1angle/风氧煤水过热器焓值'
    path_all=getAllCSVName(path)
    frames=import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df =import_csv_noHead(f)
        frames.extend(df[1:])

    header=getHeading(path_all[0])
    print(header)
    file_out='E:/Data/resultData/STD/Coal20160301.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing'+file_out+' success!')

def data_importCoalO2_path(path):
    # path = 'E:/Data/2016-3-1angle/风氧煤水过热器焓值'
    path_all = getAllCSVName(path)
    frames = import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df = import_csv_noHead(f)
        frames.extend(df[1:])
    header = getHeading(path_all[0])
    print(header)
    file_out = 'E:/Data/resultData/STD/Coal20160401.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if (item.__len__() == 0):  # 去除空行
                #  print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing' + file_out + ' success!')
def data_importWater_path(path):
    path_all = getAllCSVName(path)
    frames = import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df = import_csv_noHead(f)
        frames.extend(df[1:])
    header = getHeading(path_all[0])
    print(header)
    file_out = 'E:/Data/resultData/definite/superHeat20160401.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if (item.__len__() == 0):  # 去除空行
                #  print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing' + file_out + ' success!')
def data_importMptO2(file):
    path=file
    path_all=getAllCSVName(path)
    frames=import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df =import_csv_noHead(f)
        frames.extend(df[1:])

    header=getHeading(path_all[0])
    print(header)
    file_out='E:/Data/resultData/STD/mpt20160210.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing'+file_out+' success!')
'''未找到原始数据位置'''
def data_importMptO3():
    path='E:/Data/2016年2月功率MW（10min间隔）'
    path_all=getAllCSVName(path)
    frames=import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df =import_csv_noHead(f)
        frames.extend(df[1:])

    header=getHeading(path_all[0])
    print(header)
    file_out='E:/Data/resultData/STD/mpt20160210.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing'+file_out+' success!')

'''导入并处理磨煤机台数'''
def data_importCoalMill(file):
    path=file
    path_all=getAllCSVName(path)
    frames=import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        df=import_csv_noHead(f)
        frames.extend(df[1:])
    #获取index
    header=['date','coalMill']
    result=[]
    for row in frames:
        arr = []
        arr.append(row[0])
        sumCoal=0
        for val in range(1,len(row)-1):
            if(row[val].find('0x')<0):
                sumCoal+=int(row[val])
        arr.append(sumCoal)
        result.append(arr)
    file_out = 'E:/Data/resultData/other/coalMill20160301.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in result:
            if (item.__len__() == 0):  # 去除空行
                # print("存在空的")
                print(result.index(item))
            else:
                writer.writerow(item)
    print('processing' + file_out + ' success!')
'''导入循环水温'''
def data_importCycleWater(file):
    path=file
    path_all=getAllCSVName(path)
    frames=import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        df =import_csv_noHead(f)
        frames.extend(df[1:])

    header=getHeading(path_all[0])
    print(header)
    file_out='E:/Data/resultData/other/cycleWater20160301.csv'
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if(item.__len__()==0):#去除空行
                # print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing'+file_out+' success!')

#按父文件夹导处理每个子文件下的文件
def importAllData_1(file_in,file_out):
    path_all = getAllCSVName(file_in)
    frames = import_csv_noHead(path_all[0])
    for f in path_all[1:]:
        # print(frames)
        df = import_csv_noHead(f)
        frames.extend(df[1:])
    header = getHeading(path_all[0])
    print(header)
    with open(file_out, 'w') as csvfile:
        writer = csv.writer(csvfile, dialect=("excel"))
        writer.writerow(header)
        for item in frames:
            if (item.__len__() == 0):  # 去除空行
                #  print("存在空的")
                print(frames.index(item))
            else:
                writer.writerow(item)
    print('processing ' + file_out + ' success!')

