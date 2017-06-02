# -*- coding:utf-8 -*-
from numpy import *
from pandas import *
import scipy.spatial.distance as dis
from matplotlib.pyplot import *
import demjson
import csv

from flask import Flask, jsonify, render_template, request
app=Flask(__name__)

parameters = ['MW', 'MSP','THRTEMP','TOTALCOAL','O2']
timedata=read_csv('static/TRAPZ.csv').loc[:, ['timeSegBegin', 'timeSegEnd']]

@app.route('/info')
def getinfo():
    b = list(timedata['timeSegBegin'])[0]
    e = list(timedata['timeSegEnd']).pop()
    jstr = {'begin': b, 'end': e,'parameter':parameters}
    return jsonify(jstr)


@app.route('/mds')
def calMDS():
    data = read_csv('static/TRAPZ.csv')
    begin=list(timedata['timeSegBegin'])
    end=list(timedata['timeSegEnd'])
    data1 = data.loc[:, parameters]
    print "原始数据\n", data1
    data1 = data1.apply(lambda x: (x - min(x)) / (max(x) - min(x)))
    # print isnull(data1['TOTALCOAL'])
    data1=data1.fillna(0)
    print "归一化后\n", data1

    distype = request.args.get('distype', 0, type=str)
    # distype="cosine"
    D=dis.squareform(dis.pdist(data1,distype))
    print distype,"\n",D


    def MDS(D, K):
        N = np.shape(D)[0]
        D2 = D ** 2
        H = np.eye(N) - 1.0 / N
        T = -0.5 * np.dot(np.dot(H, D2), H)
        eigVal, eigVec = np.linalg.eig(T)
        indices = np.argsort(eigVal)  # 返回从小到大的索引值
        indices = indices[::-1]  # 反转

        eigVal = eigVal[indices]  # 特征值从大到小排列
        eigVec = eigVec[:, indices]  # 排列对应特征向量

        m = eigVec[:, :K]
        n = np.diag(np.sqrt(eigVal[:K]))
        X = np.dot(m, n)

        return X

    mds = MDS(D, 2)
    print "MDS结果坐标\n",mds
    x = mds[:, 0]
    y = mds[:, 1]
    # print DataFrame(mds).to_json(orient='values')
    xarr=[]
    yarr=[]
    for i in range(1,len(x)):
        xarr.append(x[i].real)
        yarr.append(y[i].real)
    print "xarr\n",begin
    jstr={'x':xarr,'y':yarr,'begin':begin,'end':end}
    # jstr=DataFrame(mds).to_json(orient='values')
    # d = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]
    # jsons = demjson.encode(d)
    # print jsons
    # jsonstr = json.dumps(mds)
    print '转json字符串\n',jstr

    # figure(1)
    # plot(x, y, 'bo')
    # xlabel('x')
    # ylabel('y')
    # title('MDS-' + distype)
    # for i in range(0, len(x)):
    #     annotate(
    #         '(%s)' % (i),
    #         xy=(x[i], y[i]),
    #         xytext=(0, -10),
    #         textcoords='offset points',
    #         ha='center',
    #         va='top')
    # show()

    return jsonify(jstr)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


mds=calMDS()



# vector1 = [1,2,3]
# vector2 = [4,5,6]
#
# # 欧氏距离
# # print "euclidean",sqrt((vector1-vector2)*((vector1-vector2).T))
#
# # cosV12 = dot([1,2,3],[4,7,5])/(linalg.norm([1,2,3])*linalg.norm([4,7,5]))
# cosV12 = dot(vector1,vector2)/(linalg.norm(vector1)*linalg.norm(vector2))
# print "cos",cosV12