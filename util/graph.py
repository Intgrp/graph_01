import sys
from pylab import *
sys.setrecursionlimit(1500) # set the maximum depth as 1500
class graph(object):
    def printDegree(self,data):
        degree=[]
        for i in range(len(data)):
            temp = 0
            for j in range(len(data)):
                if data[i][j] == 1:
                    temp = temp + 1
            degree.append(temp)  # 求度数和
        print("Degree:", degree)

    def printClustering(self,data):
        cluster=[]
        for i in range(len(data)):
            sum=0
            temp = []
            for j in range(len(data)):
                if data[i][j]==1:
                    temp.append(j)
            for k in range(len(temp)):
                for l in range(k,len(temp)):
                    if k!=l and data[temp[k]][temp[l]]==1:
                        sum=sum+1
            cluster.append(sum/(len(temp)*(len(temp)-1)/2.0))
        print("Cluster:",cluster)
    '''
    def search(self,i,data,cnt):
        for j in range(len(data)):
            if data[i][j]==1:
                self.search(j,data,cnt+1)

    def connect_component(self,data):
        cnt=1
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j]==1:
                    self.search(i, data, cnt)
                    print("cnt:", cnt)
                    break
    '''
    def Floyd(self,data):
        INFINITY = 65535
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j]==0:
                    data[i][j]=65535
        lengthD = len(data)  # 邻接矩阵大小
        p = list(range(lengthD))
        P = []
        for i in range(lengthD):
            P.append(p)
        P = array(P)

        for i in range(lengthD):
            for j in range(lengthD):
                for k in range(lengthD):
                    if data[i][j] > data[i][k] + data[j][k]:  # 两个顶点直接较小的间接路径替换较大的直接路径
                        data[i][j] = data[i][k] + data[j][k]
                        P[i][j] = P[j][k]  # 记录新路径的前驱
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j]==65535:
                    data[i][j]=0
        return data

    def avg_shortest_path(self,data):
        avg_shortset_path=[]
        for i in range(len(data)):
            cnt=0
            sum=0
            for j in range(len(data)):
                if data[i][j]!=0:
                    cnt=cnt+1
                    sum = sum+data[i][j]
            if cnt==0:
                avg_shortset_path.append(0)
            else:
                avg_shortset_path.append(sum/cnt)
        print(avg_shortset_path)
        return avg_shortset_path
'''
    def ffloyd(self, data_matrix):

        #输入：原数据矩阵，即：一个二维数组
        #输出：顶点间距离


        INFINITY = 65535
        for i in range(len(data_matrix)):
            for j in range(len(data_matrix)):
                if data_matrix[i][j] != 0:
                    data_matrix[i][j] = 65535

        dist_matrix = []
        path_matrix = []
        vex_num = len(data_matrix)
        for h in range(vex_num):
            one_list = [65535] * vex_num
            path_matrix.append(one_list)
            dist_matrix.append(one_list)
        for i in range(vex_num):
            for j in range(vex_num):
                dist_matrix = data_matrix
                path_matrix[i][j] = j
        for k in range(vex_num):
            for i in range(vex_num):
                for j in range(vex_num):
                    if dist_matrix[i][k] == 65535 or dist_matrix[k][j] == 65535 :
                        temp = 65535
                    else:
                        temp = dist_matrix[i][k] + dist_matrix[k][j]
                    if dist_matrix[i][j] > temp:
                        dist_matrix[i][j] = temp
                        path_matrix[i][j] = path_matrix[i][k]
        return dist_matrix, path_matrix
'''

'''
    def printAvgPath(self):
        if nx.is_connected(G):
            # average_shortest = nx.average_shortest_path_length(G)
            average_shortest = []
            for node in G:
                path_length = nx.single_source_dijkstra_path_length(G, node)
                average_shortest.append(sum(path_length.values()) / len(path_length))
            print("average_shortest:", average_shortest)
        else:
            # 获得图的子图
            graphs = nx.connected_component_subgraphs(G)
            average_shortest = []
            for g in graphs:
                # 计算平均最短路
                print(g)
                if len(g) <= 1:  # 公式是avg/(n*(n-1))，所以连1都不能
                    # len(g)返回的是g的节点数
                    average_shortest.append(0)
                else:
                    average_shortest = []
                    for node in G:
                        path_length = nx.single_source_dijkstra_path_length(G, node)
                        average_shortest.append(sum(path_length.values()) / len(path_length))
                    print("average_shortest:", average_shortest)


'''