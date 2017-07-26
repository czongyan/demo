from project_dcs_czy.dcs_czy_control.data_raw import *
def get_RawData():
    raw_data=combine_allRawData()
    # exportCSV_DF(raw_data,'E:/Data/resultData/raw20160301.csv')
    data=del_stateCol(raw_data)
    # exportCSV_DF(data, 'E:/Data/resultData/rawNOState20160301.csv')
    len, dim = data.shape
    dateRange = [np.min(data['date']), np.max(data['date'])]
    return data,dateRange
def get_autoSegmentMode(data):
    return data