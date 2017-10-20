#-*-coding=utf8-*-
import numpy as np
import pandas as pd
import networkx as nx
import xlrd
import matplotlib.pyplot as plt

def read_xls(filename="write.xls"):
    data = xlrd.open_workbook(filename)
    name = []
    hometown=[]
    dialect=[]
    name = data.sheets()[0]  # 通过索引顺序获取
    hometown = data.sheets()[1]  # 通过索引顺序获取
    dialect = data.sheets()[2]  # 通过索引顺序获取
    name = char_to_bit(name)
    hometown = char_to_bit(hometown)
    dialect = char_to_bit(dialect)
    return name,hometown,dialect

def char_to_bit(table):
    nrows = table.nrows
    ncols = table.ncols
    result=[]
    for row in range(1,nrows):
        temp = table.row_values(row)[1:]
        rr=[]
        for i in range(0,len(temp)):
            if temp[i]=='n':
                rr.append(0)
            elif temp[i]=='y':
                rr.append(1)
            else:
                rr.append(1)
        result.append(rr)
    return result

def printList(table):
    for row in table:
        print(row)

def draw_map(data,str):
    G = nx.Graph()
    Matrix = np.array(data)
    #G = nx.from_numpy_matrix(Matrix)
    #print("Matrix:",Matrix)
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i][j]==1:
                G.add_edge(i,j)

    #返回图中所有节点的度分布序列
    degree=[]
    for i in range(len(Matrix)):
        temp=0
        for j in range(len(Matrix)):
            if Matrix[i,j]==1:
                temp=temp+1
        degree.append(temp)
    print("degree",degree)
    
    x = range(len(degree))
    y = degree  # 将频次转换成频率s
    #y=[z / float(sum(degree)) for z in degree]#将频次转换成频率s
    plt.subplot(1,2,1)
    rects = plt.bar(x, y)#直方图画每个点的频次
    plt.title(str)
    #plt.loglog(x,y,color='blue',linewidth=2)#在双对数坐标轴上绘制 度分布曲线
    #average = nx.average_shortest_path_length(G)
    #print("average=", average)
    clustering = nx.clustering(G)
    print("clustering=",clustering)
    plt.subplot(1,2,2)
    nx.draw(G,with_labels=True)
    #plt.figure(str)
    plt.show(str)

name,hometown,dialect = read_xls()
#draw_map(name,"name")
#draw_map(hometown,"hometown")
#draw_map(dialect,"dialect")

plt.subplot(1,3,1)
draw_map(name,"name")
plt.subplot(1,3,2)
draw_map(hometown,"hometown")
plt.subplot(1,3,3)
draw_map(dialect,"dialect")
