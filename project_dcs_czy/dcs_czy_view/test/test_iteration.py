from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from  project_dcs_czy.dcs_czy_control.data_processing import *
rawData=readCSV_Head('E:/Data/resultData/rawNOState20160301.csv')
#data = data.set_index('date')
temp_data=rawData[(rawData['date']>='2016-03-01 08:39:00')&(rawData['date']<='2016-03-01 12:12:00')]
# temp_data['date'] = temp_data['date'].astype('str')
x = np.array(list(temp_data.index), dtype=float)
y = np.array(list(temp_data['THRTEMP']))

inv=2
tck = interpolate.splrep(x, y, k=inv+1, s=0)
xnew = np.linspace(x[0], x[len(x)-1])

fig, axes = plt.subplots(3)

axes[0].plot(x, y, 'x', label = 'data')
axes[0].plot(xnew, interpolate.splev(xnew, tck, der=0), label = 'Fit')
axes[1].plot(x, interpolate.splev(x, tck, der=1), label = '1st dev')
dev_2 = interpolate.splev(x, tck, der=inv)
axes[2].plot(x, dev_2, label = str(inv)+'st dev')

turning_point_mask = dev_2 == np.amax(dev_2)
axes[2].plot(x[turning_point_mask], dev_2[turning_point_mask],'rx',
             label = 'Turning point')
# dev_3 = interpolate.splev(x, tck, der=inv+1)
# axes[3].plot(x, dev_3, label = str(inv+1)+'st dev')
#
# turning_point_mask = dev_3 == np.amax(dev_3)
# axes[3].plot(x[turning_point_mask], dev_3[turning_point_mask],'rx',
#              label = 'Turning point')

for ax in axes:
    ax.legend(loc = 'best')

plt.show()



# yinterp = np.interp(x, x, y) # simple as that
#
# plt.plot(x, y, 'r-')
# plt.plot(x, yinterp, 'g-')
# plt.show()



# def piecewise_linear(x, x0, y0, k1, k2):
#     return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])
#
#
# p , e = optimize.curve_fit(piecewise_linear, x, y)
# xd = np.linspace(x[0], x[len(x)-1])
# # xd = np.linspace(0, 15, 100)
# plt.plot(x, y, "o")
# plt.plot(xd, piecewise_linear(xd, *p))