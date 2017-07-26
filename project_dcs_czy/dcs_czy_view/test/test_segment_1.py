from  project_dcs_czy.dcs_czy_view.segment_util import *
rawData=readCSV_Head('E:/Data/resultData/rawNOState20160301.csv')
val=['2016-03-03 08:26:00','2016-03-03 18:39:00']
arg=['MW','MSP','RRHRTEMPT','YRHRPRS']
data=rawData.loc[(rawData['date']>=val[0])&(rawData['date']<=val[1]),(['date']+arg)]
temp_date=judeSmoothByArg_detail_version_1(data,arg)
result_data=[]
if len(temp_date)>0:
    result_data.append({'date':temp_date})
    print('最终结果',result_data)