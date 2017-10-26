from pylab import *
import util.readXls
import random
import matplotlib.pyplot as plt



def Degree(data):
    degree = []
    for i in range(len(data)):
        temp = 0
        for j in range(len(data)):
            if data[i][j] == 1:
                temp = temp + 1
        degree.append(temp)
    return degree

def Clustering(data):
    cluster = []
    for i in range(len(data)):
        sum = 0
        temp = []
        for j in range(len(data)):
            if data[i][j] == 1:
                temp.append(j)
        if len(temp) <= 1:
            cluster.append(0)
        else:
            for k in range(len(temp)):
                for l in range(k, len(temp)):
                    if k != l and data[temp[k]][temp[l]] == 1:
                        sum = sum + 1
            cluster.append(sum / (len(temp) * (len(temp) - 1) / 2.0))
    print("Cluster:", cluster)
    return cluster


def Floyd(data):
    temp = [[data[i][j] for i in range(len(data))]
            for j in range(len(data))]
    length = len(temp)
    #初始化无穷远
    INF = 1000000
    for i in range(length):
        for j in range(length):
            if temp[i][j]==-1 or temp[i][j]==0:
                temp[i][j]=INF

    for k in range(length):
        for i in range(length):
            for j in range(length):
                if temp[i][k]==0 or temp[k][j]==0 or temp[i][k]==-1 or temp[k][j]==-1:
                    continue
                if temp[i][k]+temp[k][j]<temp[i][j]:
                    temp[i][j]=temp[i][k]+temp[k][j]
    '''
    for i in range(length):
        for j in range(length):
            if temp[i][j]>=INF:
                temp[i][j]=0
    '''
    #print("Floyd:",temp)
    return temp

def avg_shortest_path(data,num):
    INF = 1000000
    temp = [[data[i][j] for i in range(len(data))]
            for j in range(len(data))]
    shortest = Floyd(temp)
    length = len(shortest)
    sum=0
    for i in range(length):
        for j in range(i+1,length):
            if shortest[i][j]<INF:
                sum = sum + shortest[i][j]
    if sum==0:
        return 0
    #print("num:",num,"sum=",sum,"avg_shortest:",sum/(num*(num-1)/2))
    #print("avg_shortest:",sum/(num*(num-1)/2))
    return sum/(num*(num-1)/2)

def coreness(data):
    temp = [[data[i][j] for i in range(len(data))]
            for j in range(len(data))]
    length = len(data)

    core = {}
    for m in range(length):
        degree = [ 0 for i in range(length)]
        for i in range(length):
            for j in range(length):
                if temp[i][j]==1:
                    degree[i]=degree[i]+1
        min=-1
        for i in range(length):
            if degree[i]!=0:
                min=degree[i]
                break
        for i in range(length):
            if degree[i]!=0 and degree[i]< min:
                min =degree[i]
        for i in range(length):
            if degree[i]==min:
                for j in range(length):
                    if temp[i][j] == 1:
                        temp[i][j] = 0
                    if temp[j][i] == 1:
                        temp[j][i] = 0
                core[i]=min
    sort_core = sorted(core.items(),key=lambda item:item[0])
    print("core:",sort_core)
    return core

def random_attack(data):
    INF=1000000
    length = len(data)
    tmpMatrix = [[data[i][j] for i in range(length)]
                                    for j in range(length)]
    flagArray = [0 for i in range(length)]
    avgLength={}
    for i in range(length-1):
        print("i=",i)
        for k in range(length):
            flagArray[k]=0
            for j in range(length):
                tmpMatrix[k][j] = data[k][j]
        #去除i个点
        for j in range(i):
            randomNum = random.randint(0,62)
            while flagArray[randomNum]==1:
                randomNum = random.randint(0, 62)
            if flagArray[randomNum]==0:
                flagArray[randomNum]=1
                for k in range(length):
                    if tmpMatrix[randomNum][k]==1:
                        tmpMatrix[randomNum][k] = -1
                        tmpMatrix[k][randomNum] = -1
        avgLength[i]=avg_shortest_path(tmpMatrix,length-i)
    avgLength[length-1]=0
    print("random_attack:",avgLength)
    return avgLength

def findMaxDegree(nodeMatrix):
    max = 0
    for j in range(len(nodeMatrix)):
        if nodeMatrix[j] > nodeMatrix[max]:
            max = j
    return max

def intent_attack(data):
    INF = 1000000
    length = len(data)
    tmpMatrix = [[data[i][j] for i in range(length)]
                 for j in range(length)]
    avgLength = {}
    for i in range(length - 1):
        for k in range(length):
            for j in range(length):
                tmpMatrix[k][j] = data[k][j]
        tmpDegreeMatrix = Degree(tmpMatrix)
        for j in range(i):
            currengtMaxDegree = findMaxDegree(tmpDegreeMatrix)
            tmpDegreeMatrix[currengtMaxDegree] = 0
            # 将第currengtMaxDegree节点到所有邻接点的值都设为 - 1, 模拟不相连
            for k in range(length):
                if tmpMatrix[currengtMaxDegree][k] == 1:
                    tmpMatrix[currengtMaxDegree][k] = -1
                    tmpMatrix[k][currengtMaxDegree] = -1
                    tmpDegreeMatrix[k] = tmpDegreeMatrix[k]-1
        avgLength[i] = avg_shortest_path(tmpMatrix, length - i)
    avgLength[length - 1] = 0
    print("intent_attack:", avgLength)
    return avgLength


name,hometown,dialect = util.readXls.read_xls()
#print(Floyd(name))

avgLength = random_attack(name)
x = [i/63 for i in range(len(avgLength))]
y=[avgLength[i] for i in range(len(avgLength))]
plt.scatter(x, y)  # 画随机攻击
plt.xlabel("node name")
plt.ylabel("average_shortest")
plt.show()



