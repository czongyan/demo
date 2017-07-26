import pandas as pd
import numpy as np
import sys
import datetime as dt
from project_dcs_czy.dcs_czy_control.data_processing import *
def segment_dataBySet(data,flag,std_flag,coal_flag,water_flag,values):
    begin=[]
    end=[]
    return_flag=0
    if flag==1:
        # 通过阈值进行切割的时间段
        minLimit=values[0]
        maxLimit = values[1]
        std_set=values[2]
        PABMin=water_flag[0]
        PABMax=water_flag[1]
        date = []
        select_data=[]
        df = data
        for i in range(0, len(df)):
            if (round(df['MW'][i], 4) <= maxLimit) & (round(df['MW'][i], 4) >= minLimit):
                if coal_flag==5:
                    if (df['coalMill'][i]>=coal_flag)&(df['PAB10CT101'][i]>=PABMin)&(df['PAB10CT101'][i]<=PABMax):
                        date.append(df['date'][i])
                        select_data.append([df['date'][i],df['MW'][i]])
                else:
                    if (df['coalMill'][i]==coal_flag)&(df['PAB10CT101'][i]>=PABMin)&(df['PAB10CT101'][i]<=PABMax):
                        date.append(df['date'][i])
                        select_data.append([df['date'][i],df['MW'][i]])
        if(len(date)>0):
            begin = [date[0]]
            end = []
            print('合并前',len(date))
            for i in range(0, len(date) - 1):
                if pd.Timestamp(date[i + 1]) - pd.Timestamp(date[i]) != dt.timedelta(minutes=1):
                    begin.append(date[i + 1])
                    end.append(date[i])
            end.append(date[len(date) - 1])
            # print("begin", len(begin))
            # print("end", len(end))
            print('合并后',len(begin))
            df.index = df['date']
            beginremove = []
            endremove = []
            timerange = zip(begin, end)
            for i, v in timerange:
                if (i == v or pd.Timestamp(v) - pd.Timestamp(i) < dt.timedelta(minutes=30)):
                    # print("remove", i, v)
                    beginremove.append(i)
                    endremove.append(v)
            begin = [i for i in begin if i not in beginremove]
            end = [i for i in end if i not in endremove]
            # print begin, end
            # return begin, end
    else:
        return_flag=1
    if flag==2:
        # 等间距切分时间段,获取移动平均值
        interval='2h'
        DAX=['']
    result=[]
    for i in range(0,len(begin)):
        result.append([begin[i],end[i]])
    print("标准差限制前的begin-end")
    print(result,len(result))
    if(len(result)>0):
        if(std_flag==True):
            select_data=pd.DataFrame(select_data,columns=['date','MW'])
            max_std=select_data['MW'].mean()*std_set
            print(max_std)
            for row in result[:]:
                temp_cutData=cutAllDataStartToEnd_NoIndex(select_data,'MW',row[0],row[1])
                temp_cutStd=np.std(temp_cutData)
                if(temp_cutStd>=max_std):
                    result.remove(row)
    else:
        return_flag=1
    print("标准差限制之后的begin-end")
    print(result,len(result))
    if return_flag==0:
        return result
    else:
        return 0

#采用5min数据裁剪
def segment_dataBySet_5min(data,flag,std_flag,coal_flag,water_flag,values):
    begin=[]
    end=[]
    return_flag=0
    if flag==1:
        # 通过阈值进行切割的时间段
        minLimit=values[0]
        maxLimit = values[1]
        std_set=values[2]
        PABMin=water_flag[0]
        PABMax=water_flag[1]
        date = []
        select_data=[]
        df = data
        for i in range(0, len(df)):
            if (round(df['MW'][i], 4) <= maxLimit) & (round(df['MW'][i], 4) >= minLimit):
                if coal_flag==5:
                    if (df['coalMill'][i]>=coal_flag)&(df['PAB10CT101'][i]>=PABMin)&(df['PAB10CT101'][i]<=PABMax):
                        date.append(df['date'][i])
                        select_data.append([df['date'][i],df['MW'][i]])
                else:
                    if (df['coalMill'][i]==coal_flag)&(df['PAB10CT101'][i]>=PABMin)&(df['PAB10CT101'][i]<=PABMax):
                        date.append(df['date'][i])
                        select_data.append([df['date'][i],df['MW'][i]])
        if(len(date)>0):
            begin = [date[0]]
            end = []
            print('合并前',len(date))
            for i in range(0, len(date) - 1):
                if pd.Timestamp(date[i + 1]) - pd.Timestamp(date[i]) != dt.timedelta(minutes=1):
                    begin.append(date[i + 1])
                    end.append(date[i])
            end.append(date[len(date) - 1])
            # print("begin", len(begin))
            # print("end", len(end))
            print('合并后',len(begin))
            df.index = df['date']
            beginremove = []
            endremove = []
            timerange = zip(begin, end)
            for i, v in timerange:
                if (i == v or pd.Timestamp(v) - pd.Timestamp(i) < dt.timedelta(minutes=30)):
                    # print("remove", i, v)
                    beginremove.append(i)
                    endremove.append(v)
            begin = [i for i in begin if i not in beginremove]
            end = [i for i in end if i not in endremove]
            # print begin, end
            # return begin, end
    else:
        return_flag=1
    if flag==2:
        # 等间距切分时间段,获取移动平均值
        interval='2h'
        DAX=['']
    result=[]
    for i in range(0,len(begin)):
        result.append([begin[i],end[i]])
    print("标准差限制前的begin-end")
    print(result,len(result))
    if(len(result)>0):
        if(std_flag==True):
            select_data=pd.DataFrame(select_data,columns=['date','MW'])
            max_std=select_data['MW'].mean()*std_set
            print(max_std)
            for row in result[:]:
                temp_cutData=cutAllDataStartToEnd_NoIndex(select_data,'MW',row[0],row[1])
                temp_cutStd=np.std(temp_cutData)
                if(temp_cutStd>max_std):
                    result.remove(row)
    else:
        return_flag=1
    print("标准差限制之后的begin-end")
    print(result,len(result))
    if return_flag==0:
        return result
    else:
        return 0

#自动分割发电功率段,file_in：传入数据的文件地址，flag：裁剪的方式；1：阈值分割，2：滑动窗口分割 std_flag：是否限制标准差：True-是，False-否
#flag=1:通过阈值进行切割的时间段  values:【最小MW阈值，最大MW阈值，最大std阈值】
def cut_MWByPath(file_in,flag,std_flag,values):
    begin=[]
    end=[]
    if flag==1:
        # 通过阈值进行切割的时间段
        minLimit=values[0]
        maxLimit = values[1]
        max_std=values[2]
        date = []
        select_data=[]
        df = pd.read_csv(file_in)
        for i in range(0, len(df)):
            if (round(df['MW'][i], 4) <= maxLimit) & (round(df['MW'][i], 4) >= minLimit):
                date.append(df['date'][i])
                select_data.append([df['date'][i],df['MW'][i]])
        begin = [date[0]]
        end = []
        for i in range(0, len(date) - 1):
            if pd.Timestamp(date[i + 1]) - pd.Timestamp(date[i]) != dt.timedelta(minutes=1):
                begin.append(date[i + 1])
                end.append(date[i])
        end.append(date[len(date) - 1])
        print("begin", len(begin))
        print("end", len(end))

        df.index = df['date']
        beginremove = []
        endremove = []
        timerange = zip(begin, end)
        for i, v in timerange:
            if (i == v or pd.Timestamp(v) - pd.Timestamp(i) <= dt.timedelta(minutes=5)):
                print("remove", i, v)
                beginremove.append(i)
                endremove.append(v)
        begin = [i for i in begin if i not in beginremove]
        end = [i for i in end if i not in endremove]
        # print begin, end
        # return begin, end
    if flag==2:
        # 等间距切分时间段,获取移动平均值
        interval='2h'
        #freg频率 periods：生成长度
        timerange = pd.date_range('2016-03-01 00:00:00', periods=372, freq='2h')
        begin = []
        end = []
        pydate_array = timerange.to_pydatetime()
        date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d %H:%M:%S'))(pydate_array)

        for i in range(0, len(date_only_array) - 1):
            begin.append(date_only_array[i])
            end.append(date_only_array[i + 1])
        print(begin)

    result=[];
    for i in range(0,len(begin)):
        result.append([begin[i],end[i]])
    print("标准差限制前的begin-end")
    print(result)
    if(std_flag==True):
        select_data=pd.DataFrame(select_data,columns=['date','MW'])
        max_std=select_data['MW'].mean()*0.03
        print(max_std)
        for row in result[:]:
            temp_cutData=cutAllDataStartToEnd_NoIndex(select_data,'MW',row[0],row[1])
            temp_cutStd=np.std(temp_cutData)
            if(temp_cutStd>max_std):
                result.remove(row)
        print("标准差限制之后的begin-end")
        print(result)
    return result

'''手动选取没有磨煤机限制时'''
def cut_MWByData(data,flag,std_flag,values):
    begin=[]
    end=[]
    if flag==1:
        # 通过阈值进行切割的时间段
        minLimit=values[0]
        maxLimit = values[1]
        max_std=values[2]
        date = []
        select_data=[]
        df = data
        for i in range(0, len(df)):
            if (round(df['MW'][i], 4) <= maxLimit) & (round(df['MW'][i], 4) >= minLimit):
                date.append(df['date'][i])
                select_data.append([df['date'][i],df['MW'][i]])
        begin = [date[0]]
        end = []
        print('合并前',len(date))
        for i in range(0, len(date) - 1):
            if pd.Timestamp(date[i + 1]) - pd.Timestamp(date[i]) != dt.timedelta(minutes=1):
                begin.append(date[i + 1])
                end.append(date[i])
        end.append(date[len(date) - 1])
        # print("begin", len(begin))
        # print("end", len(end))
        print('合并后',len(begin))
        df.index = df['date']
        beginremove = []
        endremove = []
        timerange = zip(begin, end)
        for i, v in timerange:
            if (i == v or pd.Timestamp(v) - pd.Timestamp(i) <= dt.timedelta(minutes=5)):
                # print("remove", i, v)
                beginremove.append(i)
                endremove.append(v)
        begin = [i for i in begin if i not in beginremove]
        end = [i for i in end if i not in endremove]
        # print begin, end
        # return begin, end
    if flag==2:
        # 等间距切分时间段,获取移动平均值
        interval='2h'
        DAX=['']
    result=[];
    for i in range(0,len(begin)):
        result.append([begin[i],end[i]])
    print("标准差限制前的begin-end")
    print(result,len(result))
    if(std_flag==True):
        select_data=pd.DataFrame(select_data,columns=['date','MW'])
        max_std=select_data['MW'].mean()*0.03
        print(max_std)
        for row in result[:]:
            temp_cutData=cutAllDataStartToEnd_NoIndex(select_data,'MW',row[0],row[1])
            temp_cutStd=np.std(temp_cutData)
            if(temp_cutStd>max_std):
                result.remove(row)
    print("标准差限制之后的begin-end")
    print(result,len(result))
    return result

def getAllStatDate(condition_date):
    getModeData(condition_date)
    getTrapzData(condition_date)
    getMeanAndStdData(condition_date)
def combineAllCutData():
    # 合并统计后的参数文件
    data = readCSV_HeadSE('E:/Data/StatData/meanStd/mpt20160301.csv')
    path = 'E:/Data/StatData/combine'
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        tempData = readCSV_HeadSE(f)  #readCSV_Head()限制时间格式
        data = combine_csv(data, tempData, ['startDate', 'endDate'])
    file_out = 'E:/python/project_dcs_czy/static/data/stat/mean20160301.csv'
    exportCSV_DF(data, file_out)
    return data
def getModeData_dampe(condition_date):
    flag = 'mode'
    path = 'E:/Data/resultData/mode/FGDampe20160301.csv'
    mode_data = cutData_mpt_std(path, condition_date, flag)
    print(mode_data)
    exportCSV_List(mode_data,'E:/Data/StatData/combine/FGDampe20160301.csv')

def getModeData(condition_date):
    # #批量并合并处理众数
    # #多个csv文件处理
    flag='mode'
    path='E:/Data/resultData/mode'
    fns=[os.path.join(root,fn) for root,dirs,files in os.walk(path) for fn in files]
    # fns=['AFBurner20160301.csv','AGP20160301.csv','FGDampe20160301.csv']
    for f in fns:
        mode_data=[]
        file_name=f.split('\\')[1]
        mode_data = cutData_mpt_std(f, condition_date, flag)
        if(file_name=="AFBurner20160301.csv"):
            exportCSV_ListAF(mode_data,'E:/Data/StatData/combine/'+file_name)
        if file_name=="AGP20160301.csv":
            exportCSV_ListAGP(mode_data, 'E:/Data/StatData/combine/' + file_name)
        if file_name=="FGDampe20160301.csv":
            exportCSV_List(mode_data,'E:/Data/StatData/combine/'+file_name)

def getTrapzData(condition_date):
    # #喷水量批量处理积分并求和
    flag='trapz'
    path='E:/Data/resultData/definite'
    fns=[os.path.join(root,fn) for root,dirs,files in os.walk(path) for fn in files]
    for f in fns:
        spray_data=[]
        file_name=f.split('\\')[1]
        judge_name=file_name.split('2016')[0]
        spray_data=cutData_mpt_std(f,condition_date,flag)
        if judge_name=='superHeat':
            print(spray_data)
            #exportCSV_ListSum(spray_data,'E:/Data/StatData/combine/superHeatStat20160301.csv') #累加求和
            exportCSV_List(spray_data,'E:/Data/StatData/combine/nsuperHeat20160301.csv')  #直接分开积分
        else:
            if judge_name=='Coal':
                exportCSV_List(spray_data, 'E:/Data/StatData/combine/nCoal20160301.csv')
def getMeanAndStdData(condition_date):
    flag = 'meanAndStd'
    path = 'E:/Data/resultData/STD'
    fns = [os.path.join(root, fn) for root, dirs, files in os.walk(path) for fn in files]
    for f in fns:
        meanStd_data=[]
        file_name = f.split('\\')[1]
        meanStd_data = cutData_mpt_std(f,condition_date,flag)
        exportCSV_List(meanStd_data, 'E:/Data/StatData/meanStd/' + file_name)

def getTrapzData_Coal(condition_date):
    flag='trapz'
    path='E:/Data/resultData/STD/Coal20160301.csv'
    coal_data=[]
    coal_data = cutData_mpt_std(path,condition_date,flag)
    print(coal_data)
    exportCSV_List(coal_data, 'E:/Data/StatData/combine/nCoal20160301.csv')