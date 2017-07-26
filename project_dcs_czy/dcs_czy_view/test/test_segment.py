from  project_dcs_czy.dcs_czy_view.segment_util import *
a=[1,2,3]
for i in range(0,len(a)):
    print(a[i])
# i=0
# while (i<len(a)):
#     print(a[i])
#     i+=1
# get_allModeByLimit(500,1000,[3,4,5],[3,2,1])
# print(dt.timedelta(minutes=5))
result=import_segmentDate()
rawData=readCSV_Head('E:/Data/resultData/rawNOState20160301.csv')
arg=['MW']
for row in result:
    print(len(row[1]))
result_date=[]
for row in result:
    temp_data=[]
    for val in row[1]:
        print('开始',val)
        data=rawData.loc[(rawData['date']>=val[0])&(rawData['date']<=val[1]),(['date']+arg)]
        seg_std=np.std(data)
        # print(np.std(data))
        temp_date=judeSmoothByArg_detail_version_2(data,arg)
        if(len(temp_date)>0):
            temp_data=temp_data+temp_date
    if len(temp_data)>0:
        result_date.append({"flag":row[0],'date':temp_data})
print(result_date)
print('稳态后')
for row in result:
    print(len(row[1]))
# print(rawData[(rawData['date']>='2016-03-01 00:00:00')&(rawData['date']<='2016-03-01 03:00:00')])