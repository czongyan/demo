import numpy as np
from sklearn.decomposition import PCA
def pca_1(dataSet):
    # 构造聚类 类别数据
    # Data_Set = []
    # for k in range(5):
    #     arr = np.random.random([3000, 45])
    #     for i in np.arange(0, 3000):
    #         j = i % 3
    #         arr[i, k * 9 + j * 3:k * 9 + j * 3 + 3] = arr[i, k * 9 + j * 3:k * 9 + j * 3 + 3] + k * 0.25
    #     print
    #     arr.shape
    #     Data_Set.append(arr)
    Dim_Set = []
    for Cat_Num in range(len(dataSet)):
        pca = PCA()
        pca.fit(dataSet[Cat_Num])
        # 累计贡献率 又名 累计方差贡献率 不要简单理解为 解释方差！！！
        EV_List = pca.explained_variance_
        EVR_List = []
        for j in range(len(EV_List)):
            EVR_List.append(EV_List[j] / EV_List[0])
        for j in range(len(EVR_List)):
            if (EVR_List[j] < 0.10):
                Dim = j
                break
        Dim_Set.append(Dim)
    print(Dim_Set)


from numpy import *
import matplotlib.pyplot as plt


'''通过方差的百分比来计算将数据降到多少维是比较合适的，
函数传入的参数是特征值和百分比percentage，返回需要降到的维度数num'''
def eigValPct(eigVals,percentage):
    sortArray=sort(eigVals) #使用numpy中的sort()对特征值按照从小到大排序
    sortArray=sortArray[-1::-1] #特征值从大到小排序
    arraySum=sum(sortArray) #数据全部的方差arraySum
    tempSum=0
    num=0
    for i in sortArray:
        tempSum+=i
        num+=1
        if tempSum>=arraySum*percentage:
            return num

'''pca函数有两个参数，其中dataMat是已经转换成矩阵matrix形式的数据集，列表示特征；
其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
'''PCA返回参数：参数一指的是返回的低维矩阵，对应于输入参数二。参数二对应的是移动坐标轴后的矩阵。'''
def pca(dataMat,percentage=0.9):
    meanVals=mean(dataMat,axis=0)  #对每一列求平均值，因为协方差的计算中需要减去均值
    meanRemoved=dataMat-meanVals
    covMat=cov(meanRemoved,rowvar=0)  #cov()计算方差
    eigVals,eigVects=linalg.eig(mat(covMat))  #利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
    k=eigValPct(eigVals,percentage) #要达到方差的百分比percentage，需要前k个向量
    eigValInd=argsort(eigVals)  #对特征值eigVals从小到大排序
    eigValInd=eigValInd[:-(k+1):-1] #从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
    redEigVects=eigVects[:,eigValInd]   #返回排序后特征值对应的特征向量redEigVects（主成分）
    lowDDataMat=meanRemoved*redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
    reconMat=(lowDDataMat*redEigVects.T)+meanVals   #得到重构数据reconMat
    return lowDDataMat,reconMat


'''红色为降维后的数据的2维特征，绿色为原始数据'''
def plotBestFit(dataSet1, dataSet2):
    dataArr1 = array(dataSet1)
    dataArr2 = array(dataSet2)
    n = shape(dataArr1)[0]
    n1 = shape(dataArr2)[0]
    xcord1 = [];
    ycord1 = []
    xcord2 = [];
    ycord2 = []
    xcord3 = [];
    ycord3 = []
    j = 0
    for i in range(n):
        xcord1.append(dataArr1[i, 0]);
        ycord1.append(dataArr1[i, 1])
        xcord2.append(dataArr2[i, 0]);
        ycord2.append(dataArr2[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')

    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
