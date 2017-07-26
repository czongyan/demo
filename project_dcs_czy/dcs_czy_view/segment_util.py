import csv
import numpy as np
import pandas as pd
import os
import itertools
from project_dcs_czy.dcs_czy_control.data_processing import *
from project_dcs_czy.dcs_czy_control.data_select import *

def convertWater(x):
    y=[]
    if (x=="1")|(x==1):
        y=[30,60]
    if (x=="2")|(x==2):
        y=[20,30]
    if (x=="3")|(x==3):
        y=[0,20]
    return y
#根据MW阈值限制转换为工况状态取值
def convertMWToState(x):
    y=-1
    if ((x[0]=='900')&(x[1]=='1000'))|((x[0]==900)&(x[1]==1000)): #90%-100%
        y=1
    if ((x[0]=='800')&(x[1]=='900'))|((x[0]==800)&(x[1]==900)): #80%-90%
        y=2
    if ((x[0]=='700')&(x[1]=='800'))|((x[0]==700)&(x[1]==800)): #70%-80%
        y=3
    if ((x[0]=='600')&(x[1]=='700'))|((x[0]==600)&(x[1]==700)): #60%-70%
        y=4
    return y
#根据负荷状态转化为负荷阈值上下限值
def convertStateToMW(x):
    y=[]
    if x==1:
        y.append(900,1000)
    if x==2:
        y.append(800,900)
    if x==3:
        y.append(700,800)
    if x==4:
        y.append(600,700)
    return y
#根据负荷限制获取所有可能的工况决定参数组合
def get_allModeInput(val):
    # converMW(val)
    args=[]
    args.append({'flag':1,'MWMin':900,'MWMax':1100,'coal':5,'water':1})
    args.append({'flag':2,'MWMin':900,'MWMax':1100,'coal':5,'water':2})
    args.append({'flag':3,'MWMin':900,'MWMax':1100,'coal':5,'water':3})
    args.append({'flag':4,'MWMin':800,'MWMax':900,'coal':5,'water':1})
    args.append({'flag':5,'MWMin':800,'MWMax':900,'coal':5,'water':2})
    args.append({'flag':6,'MWMin':800,'MWMax':900,'coal':5,'water':3})
    args.append({'flag':7,'MWMin':800,'MWMax':900,'coal':4,'water':1})
    args.append({'flag':8,'MWMin':800,'MWMax':900,'coal':4,'water':2})
    args.append({'flag':9,'MWMin':800,'MWMax':900,'coal':4,'water':3})
    args.append({'flag':10,'MWMin':700,'MWMax':800,'coal':5,'water':1})
    args.append({'flag':11,'MWMin':700,'MWMax':800,'coal':5,'water':2})
    args.append({'flag':12,'MWMin':700,'MWMax':800,'coal':5,'water':3})
    args.append({'flag':13,'MWMin':700,'MWMax':800,'coal':4,'water':1})
    args.append({'flag':14,'MWMin':700,'MWMax':800,'coal':4,'water':2})
    args.append({'flag':15,'MWMin':700,'MWMax':800,'coal':4,'water':3})
    args.append({'flag':16,'MWMin':700,'MWMax':800,'coal':3,'water':1})
    args.append({'flag':17,'MWMin':700,'MWMax':800,'coal':3,'water':2})
    args.append({'flag':18,'MWMin':700,'MWMax':800,'coal':3,'water':3})
    args.append({'flag':19,'MWMin':600,'MWMax':700,'coal':4,'water':1})
    args.append({'flag':20,'MWMin':600,'MWMax':700,'coal':4,'water':2})
    args.append({'flag':21,'MWMin':600,'MWMax':700,'coal':4,'water':3})
    args.append({'flag':22,'MWMin':600,'MWMax':700,'coal':3,'water':1})
    args.append({'flag':23,'MWMin':600,'MWMax':700,'coal':3,'water':2})
    args.append({'flag':24,'MWMin':600,'MWMax':700,'coal':3,'water':3})
    args.append({'flag':25,'MWMin':500,'MWMax':600,'coal':4,'water':1})
    args.append({'flag':26,'MWMin':500,'MWMax':600,'coal':4,'water':2})
    args.append({'flag':27,'MWMin':500,'MWMax':600,'coal':4,'water':3})
    args.append({'flag':28,'MWMin':500,'MWMax':600,'coal':3,'water':1})
    args.append({'flag':29,'MWMin':500,'MWMax':600,'coal':3,'water':2})
    args.append({'flag':30,'MWMin':500,'MWMax':600,'coal':3,'water':3})

    for row in args:
        print(row['MWMin'])
    return args
#根据传值获取初次分割条件组合
def get_allModeByLimit(mwMin,mwMax,coalNum,water):
    args=[]
    mwLim=[]
    coalLim=[[500,[3,4]],[600,[3,4]],[700,[3,4,5]],[800,[4,5]],[900,[5]]]
    for i in range(mwMin,mwMax,100):
        for row in coalLim:
            if row[0]==i:
                temp=list(set(row[1])&set(coalNum))#两个list交集
                # print(list(set(row[1])&set(coalNum)))
                if i==900:
                    mwLim.append([i,i+200,temp])
                else:
                    mwLim.append([i,i+100,temp])
    flag=1
    for row in mwLim:
        for val in row[2]:
            for i in water:
                args.append({'flag':flag,'MWMin':row[0],'MWMax':row[1],'coal':val,'water':i})
                flag+=1
    print(args)
    return args
def raw_multiSolution(data,date):
    cutData=[]
    result_data=data[:]
    result_data['date'] = result_data['date'].astype(pd.datetime)
    result_data = result_data.set_index('date')
    result_data=result_data.resample(rule='10min').mean()
    result_data = result_data.reset_index()
    # result_data['date'] = result_data['date'].astype('str')
    remove_col=[]
    for row in date[:]:
        cutData.append(data[(row[0] <=data['date']) & (data['date'] <=row[1])])
        for i in range(0,len(result_data)):
            if (result_data['date'][i]>=row[0])&(result_data['date'][i]<=row[1]):
                remove_col.append(i)
    print('需要移除行序号',remove_col)
    result_data.drop(remove_col,inplace=True)
    result_data['resolution']=0
    print("开始组合多分辨率数据结构")
    for row in cutData:
        temp=row.copy()
        temp['resolution']=1
        result_data=result_data.append(temp)

    #result_data=pd.contact(result_data,row)
    # print(result_data['date'])
    # 将数据按照日期从近到远排序
    result_data.sort_values('date', inplace=True)
    result_data = result_data.set_index('date')
    result_data = result_data.reset_index()
    # print(result_data['date'])
    return result_data
def raw_resample(data):
    result_data=data[:]
    result_data['date'] = result_data['date'].astype(pd.datetime)
    result_data = result_data.set_index('date')
    result_data=result_data.resample(rule='10min').mean()
    result_data['resolution'] = 0
    return result_data
def raw_allMultiModeByMW(data,args):
    #原始数据重采样
    # cutData=[]
    result_data=data[:]
    result_data['date'] = result_data['date'].astype(pd.datetime)
    result_data = result_data.set_index('date')
    result_data=result_data.resample(rule='10min').mean()
    result_data = result_data.reset_index()
    result_data['resolution'] = 0
    #获取所有工况mode
    arr = [['flag', 'date']]
    flag=0
    modeClass=[]
    for row in args:
        values = [row['MWMin'], row['MWMax'], 0.03]
        water=convertWater(row['water'])
        condition_date = segment_dataBySet(data.loc[:, ['date', 'MW', 'coalMill', 'PAB10CT101']], 1,False, row['coal'],water, values)
        if(condition_date==0):
            continue
        else:
            flag+=1
            arr.append([row['flag'], condition_date])
            modeClass.append([row['flag'],(get_modeClass(row['coal'],row['MWMin'])),row['coal'],row['MWMin']+50])
            for val in condition_date[:]:
                for i in range(0, len(result_data)):
                    if (result_data['date'][i] >= val[0]) & (result_data['date'][i] <= val[1]):
                        result_data['resolution'][i] =row['flag']
    print('mode时间段',arr)
    exportCSV_List(arr,'E:/python/project_dcs_czy/static/data/stat/segmentDate.csv')
    print("分类标记",modeClass)
    return result_data,flag,modeClass
def get_modeClass(x,y):
    f=0
    if y==900:
        f=y+50
    if y==800:
        if x==5:
            f=y+80
        if x==4:
            f=y+30
    if y==700:
        if x==5:
            f=y+90
        if x==4:
            f=y+50
        if x==3:
            f=y+10
    if y==600:
        if x==4:
            f=y+70
        if x==3:
            f=y+30
    if y==500:
        if x==4:
            f=y+70
        if x==3:
            f=y+30
    return f
def raw_allMultiModeByMW5min(data,args):
    #原始数据重采样
    cutData=[]
    result_data=data[:]
    result_data['date'] = result_data['date'].astype(pd.datetime)
    result_data = result_data.set_index('date')
    result_data=result_data.resample(rule='10min').mean()
    result_data = result_data.reset_index()
    result_data['resolution'] = 0
    #获取所有工况mode
    arr=[['factor','date']]
    flag=0
    for row in args:
        values = [row['MWMin'], row['MWMax'], 0.03]
        water=convertWater(row['water'])
        condition_date = segment_dataBySet_5min(result_data.loc[:, ['date', 'MW', 'coalMill', 'PAB10CT101']], 1,True, row['coal'],water, values)
        arr.append(condition_date)
        if(condition_date==0):
            continue
        else:
            flag+=1
            for val in condition_date[:]:
                for i in range(0, len(result_data)):
                    if (result_data['date'][i] >= val[0]) & (result_data['date'][i] <= val[1]):
                        result_data['resolution'][i] =row['flag']
    print('mode时间段',arr)
    print(result_data['resolution'])
    return result_data,flag
def import_segmentDate():
    path='E:/python/project_dcs_czy/static/data/stat/segmentDate.csv'
    date=readCSV_HeadSE(path)
    result=[]
    temp=[]
    for i in range(0,len(date['flag'])):
        temp=[]
        arr = date['date'][i].replace("')", "").replace("Timestamp('", "").split('],')
        for row in arr:
            temp.append(row.replace('[[','').replace(']','').replace(' [','').replace(']]','').split(','))
            # print(temp)
        result.append([date['flag'][i],temp])
    return result
def get_stdLim(arg):
    result=0
    if(arg=="MW"):
        result=0.03
    if(arg=="THRTEMP")|(arg=="YRHRTEMPT")|(arg=="RRHRTEMPT"):
        result=0.04
    if(arg=="MSP")|(arg=="YRHRPRS")|(arg=="RRHRPRS"):
        result=0.02
    if(arg=="PAB10CT101"):
        result=0.05
    return result
def judgeSmoothByArg(data,args):
    seg_std=np.std(data)
    seg_mean=np.mean(data)
    flag=True
    for arg in args:
        stdLim=get_stdLim(arg)
        if(seg_std[arg]>=(stdLim*seg_mean[arg])):
            flag=False
            break
        if(flag==False):
            break
    return flag
#根据选择参数判断平滑度
def judeSmoothByArg_detail(data,args):
    begin=[]
    end=[]
    data= data.set_index('date')
    data_len=len(data.index)
    interval=10
    i=0
    for i in range(interval,data_len-1,interval):
        temp_data=data[i-interval:i]
        seg_std = np.std(temp_data)
        seg_mean = np.mean(temp_data)
        flag=True
        for arg in args:
            stdLim=get_stdLim(arg)
            if (seg_std[arg] >=(stdLim * seg_mean[arg])):
                flag=False
                break
            if(flag==False):
                break
        if(flag==True):
            begin.append(temp_data.index[0]._repr_base)
            end.append(temp_data.index[interval-1]._repr_base)
    if((data_len-i)>(interval/2)):
        temp_data = data[i:data_len]
        seg_std = np.std(temp_data)
        seg_mean = np.mean(temp_data)
        flag = True
        for arg in args:
            stdLim = get_stdLim(arg)
            if (seg_std[arg] >= (stdLim * seg_mean[arg])):
                flag = False
                break
            if (flag == False):
                break
        if (flag == True):
            begin.append(temp_data.index[0]._repr_base)
            end.append(temp_data.index[data_len-1-i]._repr_base)
    # for i in begin[1:]:
    #print(datetime.strptime( end[1], '%Y-%m-%d %H:%M:%S')-datetime.strptime(begin[1], '%Y-%m-%d %H:%M:%S'))
    # print('合并前',begin)
    # print(end)
    begin_remove=[]
    end_remove=[]
    for i in range(0,len(begin)-1):
        if (pd.Timestamp(begin[i+1]) - pd.Timestamp(end[i]) == dt.timedelta(minutes=1)):
            begin_remove.append(begin[i+1])
            end_remove.append(end[i])
    begin = [i for i in begin if i not in begin_remove]
    end = [i for i in end if i not in end_remove]
    # print('合并后',begin)
    # print('end',end)
    result=[]
    for i in range(0,len(begin)):
        result.append([begin[i],end[i]])
    print('合并后',result)
    return result
#根据选择参数判断平滑度
def judeSmoothByArg_detail_version_1(data,args):
    # begin=[]
    # end=[]
    result=[]
    data= data.set_index('date')
    data_len=len(data.index)
    interval=10
    s=0
    e=interval
    # begin.append(data.index[s]._repr_base)
    while(e<data_len):
        temp_data = data[s:e]
        seg_std = np.std(temp_data)
        seg_mean = np.mean(temp_data)
        flag = True
        for arg in args:
            stdLim = get_stdLim(arg)
            for val in temp_data[arg]:
                if((abs(val-seg_mean[arg])>=(stdLim*seg_mean[arg]))):
                    flag=False
                    break
            if (flag == False):
                break
        if (flag == False):
            if(e-1-interval<0):
                s=s+int(interval/2)
            else:
                if (pd.Timestamp(data.index[e - 1-1]._repr_base) - pd.Timestamp(data.index[s]._repr_base) <= dt.timedelta(
                    minutes=30)):
                    s = s + int(interval/2)
                else:
                    result.append([data.index[s]._repr_base, data.index[e - 1 - 1]._repr_base])
                    s = e
            e = s + interval
            if (e > data_len):
                break
        else:
            e=e+1
            if(e>=data_len-1):
                result.append([data.index[s]._repr_base, data.index[data_len - 1]._repr_base])
                break
    # for i in begin[1:]:
    #print(datetime.strptime( end[1], '%Y-%m-%d %H:%M:%S')-datetime.strptime(begin[1], '%Y-%m-%d %H:%M:%S'))
    # print('合并前',begin)
    # print(end)
    # begin_remove=[]
    # end_remove=[]
    # for i in range(0,len(begin)-1):
    #     if (pd.Timestamp(end[i]) - pd.Timestamp(begin[i]) <= dt.timedelta(minutes=15)):
    #         begin_remove.append(begin[i])
    #         end_remove.append(end[i])
    # begin = [i for i in begin if i not in begin_remove]
    # end = [i for i in end if i not in end_remove]
    # # print('合并后',begin)
    # # print('end',end)
    # result=[]
    # for i in range(0,len(begin)):
    #     result.append([begin[i],end[i]])
    print('合并后',result)
    return result
#根据选择参数判断平滑度
def judeSmoothByArg_detail_version_2(data,args):
    begin=[]
    end=[]
    data= data.set_index('date')
    # print(data['2016-03-01 07:27:00':'2016-03-01 07:30:00'])
    data_len=len(data.index)
    setMax={}
    setMin={}
    for val in args:
        setMax[val] = data[val][0]
        setMin[val] = data[val][0]
    diffBool=[]
    segBool=True
    interval=5
    s=0
    e=interval
    beforeBegin=data.index[s]._repr_base
    i=0
    while(e<=data_len):
        begin.append(data.index[s]._repr_base)
        temp_data = data[s:e]
        seg_mean = np.mean(temp_data)
        flag = True
        for arg in args:
            stdLim = get_stdLim(arg)
            setMax[arg] = max(temp_data[arg])
            setMin[arg] = min(temp_data[arg])
            diff=abs((setMax[arg]-setMin[arg])/(setMax[arg]+setMin[arg]))
            if(diff>=stdLim):
                flag=False
                segBool=False
                break
        diffBool.append(flag)
        end.append(data.index[e - 1]._repr_base)
        s = e
        e = s + interval
        if(e>data_len):
            if s<data_len-1:
                e=data_len
            else:
                break
    # for i in begin[1:]:
    #print(datetime.strptime( end[1], '%Y-%m-%d %H:%M:%S')-datetime.strptime(begin[1], '%Y-%m-%d %H:%M:%S'))
    # print('合并前',begin)
    # print(end)
    print(diffBool)
    begin_remove=[]
    end_remove=[]
    seg_date=[]
    if(segBool==False):
        seg_date=[]
        for i in range(0,len(diffBool)):
            if(diffBool[i]==False):
                begin_remove.append(begin[i])
                end_remove.append(end[i])
        begin = [i for i in begin if i not in begin_remove]
        end = [i for i in end if i not in end_remove]
        begin_remove = []
        end_remove = []
        for i in range(0,len(end)-1):
            if (pd.Timestamp(end[i]) - pd.Timestamp(begin[i+1])<=dt.timedelta(minutes=1)):
                begin_remove.append(begin[i+1])
                end_remove.append(end[i])
        begin = [i for i in begin if i not in begin_remove]
        end = [i for i in end if i not in end_remove]
        begin_remove = []
        end_remove = []
        for i in range(0, len(begin)):
            if(pd.Timestamp(end[i]) - pd.Timestamp(begin[i]) <=dt.timedelta(minutes=30)):
                begin_remove.append(begin[i])
                end_remove.append(end[i])
        begin = [i for i in begin if i not in begin_remove]
        end = [i for i in end if i not in end_remove]
        print('一次分割后',begin)
        for i in range(0, len(begin)):
            seg_date=seg_date+judge_seg(data[begin[i]:end[i]],args)
    else:
        seg_date=seg_date+judge_seg(data, args)
    print(seg_date)
    return seg_date
#大窗口二次过滤
def judge_seg(data,args):
    diff={}
    result=[]
    data_len = len(data.index)
    setMax = {}
    setMin = {}
    interval = 30
    s = 0
    e = interval
    again=True#是否开始重设窗口 :True 是 False 不是
    while (e <= data_len):
        temp_data = data[s:e]
        flag = True
        for arg in args:
            stdLim = get_stdLim(arg)
            if(again==True):
                setMax[arg]=max(temp_data[arg])
                setMin[arg]=min(temp_data[arg])
            else:
                add_data=data[e-5:e]
                if (max(add_data[arg])>setMax[arg]):
                    setMax[arg]=max(add_data[arg])
                if (min(add_data[arg]) < setMin[arg]):
                    setMin[arg] = min(add_data[arg])
            diff[arg] = abs((setMax[arg] - setMin[arg]) / (setMax[arg] + setMin[arg]))
            if (diff[arg] >= stdLim):
                flag = False
                break
        if (flag == False):
            again=True
            if (pd.Timestamp(data.index[e-1]._repr_base) - pd.Timestamp(data.index[s]._repr_base) <=dt.timedelta(minutes=30)):
                s=s+5
            else:
                result.append([data.index[s]._repr_base,data.index[e - 1-5]._repr_base,setMax,setMin,diff])
                s=e
            e=s+interval
            if(e>data_len):
                break
        else:
            again = False
            e=e+5
            if(e>data_len):
                result.append([data.index[s]._repr_base, data.index[data_len-1]._repr_base,setMax,setMin,diff])
                break
    print('二次合并后',result)
    return result

#根据选择参数判断平滑度
def judeSmoothByArg_detail_version_3(data,args):
    # begin = []
    # end = []
    result=[]
    data_len = len(data.index)
    setMax = {}
    setMin = {}
    diff={}
    interval = 30
    s = 0
    e = interval
    again=True#是否开始重设窗口 :True 是 False 不是
    while (e <= data_len):
        if(s==0):
            a=0
        temp_data = data[s:e]
        flag = True
        for arg in args:
            stdLim = get_stdLim(arg)
            if(again==True):
                setMax[arg]=max(temp_data[arg])
                setMin[arg]=min(temp_data[arg])
            else:
                add_data=data[e-5:e]
                if (max(add_data[arg])>setMax[arg]):
                    setMax[arg]=max(add_data[arg])
                if (min(add_data[arg]) < setMin[arg]):
                    setMin[arg] = min(add_data[arg])
            diff[arg] = abs((setMax[arg] - setMin[arg]) / (setMax[arg] + setMin[arg]))
            if (diff[arg] >= stdLim):
                flag = False
                break
        if (flag == False):
            again=True
            if (pd.Timestamp(data.index[e-1]._repr_base) - pd.Timestamp(data.index[s]._repr_base) <=dt.timedelta(minutes=30)):
                s=s+5
            else:
                # temp_result={}
                # temp_result['startDate']=data.index[s]._repr_base
                # temp_result['endDate']=data.index[e-1-5].repe_base
                # temp_result['setMax']=setMax

                result.append([data.index[s]._repr_base,data.index[e - 1-5]._repr_base,setMax,setMin,diff])
                # begin.append(data.index[s]._repr_base)
                # end.append(data.index[e - 1]._repr_base)
                s=e
            e=s+interval
            if(e>data_len):
                break
        else:
            again = False
            e=e+5
            if(e>data_len):
                result.append([data.index[s]._repr_base, data.index[data_len-1]._repr_base,setMax,setMin,diff])
                # begin.append(data.index[s]._repr_base)
                # end.append(data.index[data_len-1]._repr_base)
                break

    print('二次合并后',result)
    return result