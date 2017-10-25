from pylab import *
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import copy
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
            if len(temp)<=1:
                cluster.append(0)
            else:
                for k in range(len(temp)):
                    for l in range(k, len(temp)):
                        if k != l and data[temp[k]][temp[l]] == 1:
                            sum = sum + 1
                cluster.append(sum / (len(temp) * (len(temp) - 1) / 2.0))
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
        for i in range(lengthD):
            for j in range(lengthD):
                for k in range(lengthD):
                    if data[i][j] > data[i][k] + data[j][k]:  # 两个顶点直接较小的间接路径替换较大的直接路径
                        data[i][j] = data[i][k] + data[j][k]
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i][j]==65535:
                    data[i][j]=0
        return data

    def avg_shortest_path(self,data):
        data = copy.deepcopy(data)
        # G = self.dataToG(data)
        # G = max(nx.connected_component_subgraphs(G), key=len)  # 返回最大连通子图
        # data = self.gToData(G)
        data = self.Floyd(data)
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

    def dataToG(self,data):
        G = nx.DiGraph()

        for i in range(0, len(data)):
            G.add_node(i)
        Matrix = np.array(data)
        G = nx.from_numpy_matrix(Matrix)
        degree = []
        for i in range(len(Matrix)):
            for j in range(len(Matrix)):
                if Matrix[i][j] == 1:
                    G.add_edges_from([(i, j)])
        return G

    def gToData(self,G):
        # edges = G.edges()
        # dd = [[0 for i in range(len(G))]
        #       for j in range(len(G))]
        # for i in range(len(edges)):
        #     # if data[edges[i][0]][edges[i][1]] == 1:
        #     dd[edges[i][0]][edges[i][1]] = 1
        # return dd
        return nx.adjacency_matrix(G).todense()

    def DrawMap(self,data,ss):
        G = self.dataToG(data)
        nsize=[]
        bigestSize=800
        for i in range(len(data)):
            nsize.append(G.degree(i)/63*900)
        nx.draw_networkx(G,node_size=nsize)
        #nx.draw(G,node_size=nsize)
        plt.title(ss + (" network"))
        plt.show()

    def find_Min_degree_index(self,degree):
        mmin=0
        for i in range(len(degree)):
            if degree[mmin] > degree[i]:
                mmin = i
        return mmin


    def coreness(self,data):
        G = self.dataToG(data)
        G = max(nx.connected_component_subgraphs(G), key=len)  # 返回最大连通子图
        # nx.draw(G)
        # plt.show()
        edges = G.edges()
        dd=[ [0 for i in range(len(data))]
            for j in range(len(data))]
        for i in range(len(edges)):
            #if data[edges[i][0]][edges[i][1]] == 1:
            dd[edges[i][0]][edges[i][1]]=1
        data=dd
        core={}
        for i in range(len(data)):
            core[i]=0
        for m in range(len(data)):
            degree=[]
            for i in range(len(data)):
                degree.append(0)
            for i in range(len(data)):
                for j in range(len(data)):
                    if data[i][j]==1:
                        degree[i]=degree[i]+1
            mmin = -1
            for i in range(len(degree)):
                if degree[i] !=0 :
                    mmin = degree[i]
            for i in range(len(degree)):
                if degree[i] != 0 and degree[i] < mmin:
                    mmin = degree[i]
            flag=0
            for i in range(len(data)):
                if degree[i]==mmin:
                    for j in range(len(data)):
                        if data[i][j]==1:
                            data[i][j]=0
                        if data[j][i]==1:
                            data[j][i]=0
                    core[i]=mmin
                    flag=1
                    break
                if flag==1:
                    break
        print("coreness",core,len(core))
        core = sorted(core.items())
        print("sort_cor:", core)
        return core

    # 按照度数排序
    def by_degree(self, degree):
        return degree[1]

    def corona(self,data):
        G = self.dataToG(data)
        G = max(nx.connected_component_subgraphs(G), key=len)#返回最大连通子图
        core = {}
        for k in range(len(data)):
            degree = G.degree()
            mmin=-1
            if len(degree):
                degree_sort = sorted(degree.items(), key=lambda item:item[1])#从小到大排序
                print("degree_sort:",degree_sort)
                mmin = degree_sort[0][0]
                core[mmin] = degree_sort[0][1]
                G.remove_node(mmin)
        #for i in range(len(core)):
        core = sorted(core.items())
        #print("sort_cor:", core)
        return core

    def remove_node_adj(self,data,i):
        for j in range(len(data)):
            data[i][j]=0
            data[j][i]=0
        return data

    def intential_attack(self,data,i):
        data = self.remove_node_adj(data, i)
        dd = self.Floyd(data)
        return self.avg_shortest_path(dd)

    def radom_attack(self,data):
        result=[]
        for i in range(len(data)):
            flagArray ={}
            for k in range(len(data)):
                flagArray[k]=0
            temp = copy.deepcopy(data)
            #随机去除i个点
            for j in range(0,i):
                randomNum = random.randint(0, 62)
                #print("randomNum:",randomNum,flagArray[randomNum])
                if flagArray[randomNum]==0:
                    flagArray[randomNum]=1
                    temp = self.remove_node_adj(temp, randomNum)
                else:
                    j=j-1
            dd = self.Floyd(temp)
            sum = 0
            for k in range(len(dd)):
                for j in range(k,len(dd)):
                    sum = sum + dd[k][j]
            nn=len(data)-i
            print("sum:",sum,nn*(nn-1)/2)
            if nn<=1:
                result.append(0)
            else:
                result.append(sum/(nn*(nn-1)/2))
        return result

