from project_dcs_czy.dcs_czy_data.data_import import *
# data_importMptO2('E:/Data/2016.04.01-2016.04.30(1min采样)/功率、负荷、主汽')
# data_importWater_path('E:/Data/2016年4月/WATER')
# data_importCoalMill('E:/Data/2016-3-1angle/磨煤机运行')
# data_importCycleWater('E:/Data/循环水温02-09')
# data_importCycleWater('E:/Data/2016.04.01-2016.04.30(1min采样)')
import os
# filePath='E:/Data/data'
# import_rawData(filePath)
filePath='E:/Data/rawData/interval-1min'
resample_rawData(filePath,'60min')


'''测试合并风氧煤csv'''
# data_importCoalO2()