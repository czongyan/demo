from project_dcs_czy.dcs_czy_control.data_select import *
# import pandas as pd
# path_in='E:/Data/resultData/mode/AFBurner20160301.csv'
# f=open(path_in,'r')
# line=f.readline()
# dateLag=[]
# i=0
# while line:
#     if(i.__mod__(5)==0):
#         print(line)
#         # start=line.split(',')[0]
#      #     start_end.append(val)
#      # dateLag.append(start_end)
#     i+=1
#     line=f.readline()
# f.close()

# from project_dcs_czy.dcs_czy_view.stat_coordinate import *
# get_stat_combineData()

path_in='E:/Data/resultData/STD/mpt20160301.csv'
cut_date=cut_MWByPath(path_in,1,True)
condition_date=cut_date
getAllStatDate(condition_date)
combineAllCutData()
#
# flag = 'mode'
# path = 'E:/Data/resultData/mode/FGDampe20160301.csv'
# mode_data = cutData_mpt_std(path, condition_date, flag)
# print(mode_data)
# exportCSV_List(mode_data,'E:/Data/StatData/combine/FGDampe20160301.csv');