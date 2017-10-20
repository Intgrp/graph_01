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


    print("degree（度分布）:",degree)
    # 计算各个节点的群聚系数
    cluster = nx.clustering(G)
    print("Cluster（聚类系数）:",cluster)
    # 计算核数
    print("k_corona(核数):",nx.core_number(G))

    graphs = nx.connected_component_subgraphs(G)
    #通过核的方法获得图的子图
    for g in graphs:
        #计算平均最短路
        print("average_shortest_path_length（平均最短路径长度）:", nx.average_shortest_path_length(g))
        #print("all_shortest_path",nx.all_pairs_shortest_path_length(G))
    #计算中心
    #centrality = nx.degree_centrality(G)
    #print("centrality（中心度）:", centrality)
    #nx.betweenness_centrality(G,)

    plt.subplot(1, 2, 1)
    plt.bar(range(len(degree)), degree)#画直方图展示出来
    plt.subplot(1, 2, 2)
    nx.draw(G,with_labels=True)
    plt.show()


name,hometown,dialect = read_xls()
drwa_map(name,"name")
#drwa_map(hometown,"hometown")
#drwa_map(dialect,"dialect")
#plt.show()