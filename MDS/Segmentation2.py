# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
import csv

waterpath=r'E:\TimeSeriesProj\preprocessing\data\water_march_1min.csv'
basicpath=r'E:\TimeSeriesProj\preprocessing\data\basic_march_1min.csv'
inputpath=r'E:\TimeSeriesProj\preprocessing\data\O2coal_march_1min.csv'
controlpath=r'E:\TimeSeriesProj\preprocessing\data\control_march_1min.csv'
begin=[]
end=[]
#选择分段方式0---原始赋值，1---赋阈值自动切割，2---等间距分段
def segment(sel):
    global begin
    global end
    if sel==0:
        # 指定稳定段
        begin=['2016-03-03 14:10:00','2016-03-04 10:03:00','2016-03-04 13:32:00','2016-03-08 09:53:00',
               '2016-03-08 13:05:00','2016-03-09 14:22:00','2016-03-11 06:19:00',
               '2016-03-14 08:37:00','2016-03-15 06:28:00','2016-03-18 06:25:00',
               '2016-03-22 21:39:00','2016-03-25 05:55:00','2016-03-30 09:18:00',
               '2016-03-30 13:58:00']
        end=['2016-03-03 16:49:33','2016-03-04 11:00:00','2016-03-04 16:36:00','2016-03-08 11:28:00',
             '2016-03-08 17:17:00','2016-03-09 16:14:00','2016-03-11 07:50:00',
             '2016-03-14 10:48:00','2016-03-15 07:54:00','2016-03-18 07:46:00',
             '2016-03-22 22:45:00','2016-03-25 06:45:00','2016-03-30 11:27:00',
             '2016-03-30 18:17:00']
        # return begin, end
    if sel==1:
        # 通过阈值进行切割的时间段
        limit = 980
        date = []
        df = pd.read_csv(basicpath)
        for i in range(0, len(df)):
            if round(df['MW'][i], 2) >= limit:
                date.append(df['date'][i])

        begin = [date[0]]
        end=[]
        for i in range(0, len(date) - 1):
            if pd.Timestamp(date[i + 1]) - pd.Timestamp(date[i]) != dt.timedelta(minutes=1):
                begin.append(date[i + 1])
                end.append(date[i])
        end.append(date[len(date) - 1])
        print "begin", len(begin)
        print "end", len(end)

        df.index = df['date']
        beginremove = []
        endremove = []
        timerange = zip(begin, end)
        for i, v in timerange:
            if (i == v or pd.Timestamp(v) - pd.Timestamp(i) <= dt.timedelta(minutes=5)):
                print "remove", i, v
                beginremove.append(i)
                endremove.append(v)
        begin = [i for i in begin if i not in beginremove]
        end = [i for i in end if i not in endremove]
        # print begin, end
        # return begin, end
    if sel==2:
        # 等间距切割的时间段
        timerange = pd.date_range('2016-03-01 00:00:00', periods=372, freq='2h')
        begin=[]
        end=[]
        pydate_array = timerange.to_pydatetime()
        date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d %H:%M:%S'))(pydate_array )

        for i in range(0, len(date_only_array)-1):
            begin.append(date_only_array[i])
            end.append(date_only_array[i+1])
        # print "begin\n",begin
        # print "end\n",end

segment(1)
print begin
print end

# begin=['2016-03-15 06:28:00']
# end=['2016-03-15 07:54:00']
basicparameter=['MW','THRTEMP','MSP','YRHRTEMPT','RRHRTEMPT']
waterparameter=['LAE11CG101XQ01','LAE12CG101XQ01','LAE13CG101XQ01','LAE14CG101XQ01','LAE21CG101XQ01','LAE22CG101XQ01','LAE23CG101XQ01','LAE24CG101XQ01']
inputparameter=['O2','TAF','TOTALCOAL']
controlparameter=['HHA11','HHA31','HHA51','HHA71','HHA81','HNA01A','HNA02A']
parameter=basicparameter+waterparameter+controlparameter+inputparameter
print parameter
arr=[]
outputs=[]
flag=0

#读取csv文件并将需要的列提取出来

def preprocess(filepath):
    origins = pd.read_csv(filepath)
    #处理时间格式
    def seg(str,startspliter,endspliter):
        temp=str[str.index(startspliter)+1:]
        startIndex=str.index(startspliter)+1
        endIndex=startIndex+temp.index(endspliter)
        if len(str[startIndex:endIndex])<=2:
            return str[startIndex:endIndex]
        else:
            startIndex=startIndex+temp.index(startspliter)+1
            return str[startIndex:endIndex]

    for i in range(len(origins['date'])):
        day=seg(origins['date'][i],'-','-')
        day='0'+day if len(day)==1 else day
        month=seg(origins['date'][i],'-',' ')
        month='0'+month if len(month)==1 else month
        timestr=origins['date'][i][:origins['date'][i].index('-')]+'-'+month+'-'+day+origins['date'][i][origins['date'][i].index(' '):]
        origins.at[i, 'date'] =dt.datetime.strptime(timestr, "%Y-%d-%m %H:%M:%S")

    origins.index=origins['date']
    # print type(origins)
    # print origins.loc['2016-03-04 10:03:00':'2016-03-04 11:00:00']
    print "Exit preprocess\n"
    return origins



def calTrapz(data,columns,begin,end):
    #截取指定的时间段
    # print type(data)
    seg=data.loc[begin:end]
    # print seg
    # 选取参数
    seg = seg.loc[:, [columns]]
    # 处理空值
    seg.fillna(method='pad')
    # 处理数据
    global arr
    arr=[]
    for row in seg[columns]:
        arr.append(round(row, 2))
    print arr
    #积分计算函数
    trapz=np.trapz(arr)

    # print 'trapz\n',trapz
    print '标准化trapz\n',trapz/len(arr)
    return round(trapz/len(arr),4)

def calStd(data,columns,begin,end):
    # 截取指定的时间段
    seg = data.loc[begin:end]
    # 选取参数
    seg = seg.loc[:, [columns]]
    # 处理空值、空格
    seg.fillna(method='pad')
    # 处理数据
    global arr
    arr=[]
    for row in seg[columns]:
        if type(row)==type(" "):
            arr.append(round(float(row.strip()), 2)) if len(row)!=1 else arr
        else:#不是字符串直接保留小数
            arr.append(round(row,2))
        # print row
    print arr
    std = np.std(arr)
    # print 'std\n',std
    print '标准化std\n',std
    return round(std,4)

title=['timeSegBegin','timeSegEnd']


basicorigins=preprocess(basicpath)
waterorigins=preprocess(waterpath)
controlorigins=preprocess(controlpath)
inputorigins=preprocess(inputpath)


# print "走一走看一看了啊！",basicorigins.loc['2016-3-4 15:41:00','MWValue']

for i in range(0,len(begin)):
    print "processing NO.",(i+1),"segmentation"
    results = []
    for j in range(0,len(parameter)):
        print "calculating prameter",parameter[j]
        title.append(parameter[j]) if i==1 else title

        if j<len(basicparameter):
            results.append(calTrapz(basicorigins,parameter[j],begin[i],end[i]))
        else:
            if j<len(basicparameter+waterparameter):
                results.append(calTrapz(waterorigins,parameter[j],begin[i],end[i]))
            else:
                if j<len(basicparameter+waterparameter+controlparameter):
                    results.append(calTrapz(controlorigins,parameter[j],begin[i],end[i]))
                else:
                    results.append(calTrapz(inputorigins,parameter[j],begin[i],end[i]))

        # results.append(calTrapz(basicorigins,parameter[j],begin[i],end[i])) if j<len(basicparameter) \
        #     else results.append(calTrapz(basicorigins,parameter[j],begin[i],end[i]))
    outputs.append((begin[i],end[i])+tuple(results))


print title
# 写入文件
csvfile = file('static/TRAPZ.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(title)
writer.writerows(outputs)
csvfile.close()

# a='2.345'
# b=[78.79, 81.72, 84.77]
# print np.trapz(b)


