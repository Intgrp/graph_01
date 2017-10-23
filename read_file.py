#-*- coding=utf-8 -*-
import numpy as np
import pandas as pd
import networkx as nx
import xlrd
import matplotlib.pyplot as plt

#读取Excel表格数据
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

#对数据去除第一行和第一列的索引条目，得到纯粹的数据，并对y,n,m设值为1,0,1
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
                rr.append(0)
        result.append(rr)
    return result

#打印table
def printList(table):
    for row in table:
        print(row)

#构建图，并且绘制图的结构
def drwa_map(data,ss):
    G = nx.Graph()
    for i in range(0,len(data)):
        G.add_node(i)
    Matrix = np.array(data)
    G = nx.from_numpy_matrix(Matrix)
    degree=[]
    for i in range(len(Matrix)):
        temp=0
        for j in range(len(Matrix)):
            if Matrix[i][j]==1:
                G.add_weighted_edges_from([(i, j, 1)])
                #G.add_edge(i,j)
                temp = temp + 1
        degree.append(temp)#求度数和

    print("degree:",degree)
    # 计算各个节点的群聚系数
    cluster = list(nx.clustering(G).values())
    print("Cluster:",cluster)
    # 计算核数
    core_number = list(nx.core_number(G).values())
    print("k_corona:",core_number)


    if nx.is_connected(G):
        #average_shortest = nx.average_shortest_path_length(G)
        average_shortest = []
        for node in G:
            path_length=nx.single_source_dijkstra_path_length(G, node)
            average_shortest.append(sum(path_length.values())/len(path_length))
        print("average_shortest:", average_shortest)
    else:
        # 获得图的子图
        graphs = nx.connected_component_subgraphs(G)
        average_shortest = []
        for g in graphs:
            # 计算平均最短路
            print(g)
            if len(g)<=1: #公式是avg/(n*(n-1))，所以连1都不能
                #len(g)返回的是g的节点数
                average_shortest.append(0)
            else:
                average_shortest = []
                for node in G:
                    path_length = nx.single_source_dijkstra_path_length(G, node)
                    average_shortest.append(sum(path_length.values()) / len(path_length))
                print("average_shortest:", average_shortest)
    plt.subplot(2,3,1)
    plt.bar(range(len(degree)), degree)#画度分布的直方图展示出来
    plt.title("degree")
    plt.subplot(2,3,2)
    plt.plot(range(len(cluster)),cluster)#画每个点的聚类系数
    plt.title("cluster")
    plt.subplot(2,3,3)
    plt.plot(range(len(core_number)),core_number)#画核数分布图
    plt.title("core_number")
    plt.subplot(2,3,4)
    plt.bar(range(len(average_shortest)),average_shortest)#画平均最短路径长度
    plt.title("average_shortest")
    plt.subplot(2,3,5)
    nx.draw(G,with_labels=True,hold=True)
    plt.title(ss + (" network"))
    plt.show()


name,hometown,dialect = read_xls()
drwa_map(name,"name")
drwa_map(hometown,"hometown")
drwa_map(dialect,"dialect")
plt.show()