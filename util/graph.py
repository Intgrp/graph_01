from pylab import *
import random
import networkx as nx
sys.setrecursionlimit(1500) # set the maximum depth as 1500
class graph(object):
    def Degree(self,data):
        degree=[]
        for i in range(len(data)):
            temp = 0
            for j in range(len(data)):
                if data[i][j] == 1:
                    temp = temp + 1
            degree.append(temp)  # 求度数和
        #print("Degree:", degree)
        return degree

    def Clustering(self,data):
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
        return cluster

    def Floyd(self,data):
        #data = copy.deepcopy(dd)
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
        #print(avg_shortset_path)
        return avg_shortset_path

    def corona(self,data):
        core = []
        for k in range(len(data)):
            min = 0
            degree = self.Degree(data)
            for i in range(len(degree)):
                if degree[min] > degree[i] and degree[i]!=0 and degree[min]!=0:
                    min = i
            core.append(degree[min])
            #print("degree[min]",degree[min],min)
            for j in range(len(degree)):
                data[min][j] = 0
        print("core:",core)
        return core

    def remove_node(self,data,i):
        for j in range(len(data)):
            data[i][j]=0
            data[j][i]=0
        return data

    def intential_attack(self,data,i):
        data = self.remove_node(data, i)
        dd = self.Floyd(data)
        return self.avg_shortest_path(dd)

    def radom_attack(self,data):
        i = random.randint(1,63)
        data = self.remove_node(data, i)
        dd = self.Floyd(data)
        return self.avg_shortest_path(dd)

    '''
    # 所有点的最短路
    def short_path(self,G):
        average_shortest = []
        for node in G:
            path_length = nx.single_source_dijkstra_path_length(G, node)
            average_shortest.append(sum(path_length.values()) / len(path_length))
        return average_shortest
    
    #通过networkx，自己实现的随机攻击和特定攻击
    def intential_attack(self,G, i):
        G.remove_node(i)
        return self.short_path(G)

    def radom_attack(self,G):
        # i = random.random(1,63)
        i = random.randint(1, 63)
        G.remove_node(i)
        return self.short_path(G)
    '''
