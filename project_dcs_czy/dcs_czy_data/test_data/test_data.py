from project_dcs_czy.dcs_czy_data.data_import import *
from project_dcs_czy.dcs_czy_control.data_select import *

#测试合并风氧煤csv
# data_importCoalO2()

#测试按阈值切割功率
path_in='E:/Data/resultData/STD/mpt20160301.csv'
# cut_MW(path_in,1)

#计算各类移动平均线，包括简单简单算术移动平均线MA、指数平滑移动平均线EMA；
df = pd.read_csv(path_in,index_col='date')
# ========== 计算移动平均线
# 分别计算5日、20日、60日的移动平均线
ma_list = [60]

# 计算简单算术移动平均线MA - 注意：df['close']为股票每天的收盘价
for ma in ma_list:
    df['MA_' + str(ma)] = pd.rolling_mean(df['MW'], ma)
    print(df['MA_60'][50:])
# 计算指数平滑移动平均线EMA
for ma in ma_list:
    df['EMA_' + str(ma)] = pd.ewma(df['MW'], span=ma)

# 将数据按照交易日期从近到远排序
df.sort('date', ascending=False, inplace=True)

