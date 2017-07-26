import pandas as pd
import numpy as np
from project_dcs_czy.dcs_czy_control.data_processing import *
df=import_csv_noHead('C:/Users/ASUS/Desktop/aa.csv')
# print(DataFrame(df))
header=['date','LAE11','LAE12','LAE13','LAE14','LAE21','LAE22','LAE23','LAE24']
df=DataFrame(df,columns=header)
df.sort_values('date', inplace=True)
df=df.set_index('date')
df=df.reset_index()
print(df)
