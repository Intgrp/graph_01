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
    #print("Cluster:", cluster)
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
    #print("core:",sort_core)
    return sort_core

def random_attack(data):
    INF=1000000
    length = len(data)
    tmpMatrix = [[data[i][j] for i in range(length)]
                                    for j in range(length)]
    flagArray = [0 for i in range(length)]
    avgLength={}
    for i in range(length-1):
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
    #print("random_attack:",avgLength)
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
    #print("intent_attack:", avgLength)
    return avgLength

def plot_random_intentional_Map(data,ss):
    avgLength = random_attack(name)
    x = [i / 63 for i in range(len(avgLength))]
    y = [avgLength[i] for i in range(len(avgLength))]
    plt.scatter(x, y, c='r', marker='s')  # 画随机攻击
    plt.xlabel("node name")
    plt.ylabel("average_shortest")
    plt.title(ss + " random attack")
    filename = ss + " random attack.png"
    plt.savefig(filename)
    plt.show()

    avgLength = intent_attack(name)
    x = [i / 63 for i in range(len(avgLength))]
    y = [avgLength[i] for i in range(len(avgLength))]
    plt.scatter(x, y, c='r', marker='s')  # 画特定攻击
    plt.xlabel("node name")
    plt.ylabel("average_shortest")
    plt.title(ss + " intentional attack")
    filename = ss + " intentional attack.png"
    plt.savefig(filename)
    plt.show()

def plot_corness_Map(data,ss):
    core = coreness(data)
    temp = [ core[i][1] for i in range(len(core))]
    plt.bar(range(len(temp)), temp)  # 画每个点的核数
    plt.xlabel("node name")
    plt.ylabel("core number")
    plt.title(ss+" core number")
    filename = ss + " coreness.png"
    plt.savefig(filename)
    plt.show()

def ssum(data):
    sum=0.0
    length=len(data)
    for i in range(length):
        for j in range(length):
            sum = sum + data[i][j]
    return sum/(length*(length-1)/2)


def output_result(data,ss):
    print("-------------------",ss,"-------------------------------------")
    degree = Degree(data)
    sum=0.0
    for i in range(len(degree)):
        sum = sum+degree[i]
    print("Average Degree:",sum/len(degree))
    cluster = Clustering(data)
    sum = 0.0
    for i in range(len(cluster)):
        sum = sum + cluster[i]
    print("Average Clustering:",sum/len(cluster))
    print("Averege_shortest_path:",avg_shortest_path(data,len(data)))
    core = coreness(data)
    sum = 0.0
    for i in range(len(core)):
        sum = sum + core[i][1]
    print("Average Coreness:",sum/len(core))
    r_attack = random_attack(data)
    sum =0
    for i in range(len(r_attack)):
        sum = sum +r_attack[i]
    print("Average random attack:",sum/len(r_attack))
    i_attack =intent_attack(data)
    sum = 0
    for i in range(len(i_attack)):
        sum = sum + i_attack[i]
    print("Average intentional attack:",sum/len(i_attack))

visit=[0 for i in range(63)]
def DFS(arr,i,list2):
    list2.append(i)
    visit[i]=True
    for j in range(63):
        if arr[i][j]==1 and visit[j]==False:
           DFS(arr,j,list2)
    return list2
#遍历整个网络

def traverse(arr):
    # 标记数据
    for i in range(63):
        visit.append(False)
    list1=[]
    for i in range(63):
        if visit[i]==False:
            list2=[]
            #list3为一个连通图所有节点
            list3=DFS(arr,i,list2)
            list1.append(list3)
    visit.clear()
    return list1

def S_random_attack(data):
    temp = traverse(data)
    smax = max([len(temp[i]) for i in range(len(temp))])
    s=[]
    INF=1000000
    length = len(data)
    tmpMatrix = [[data[i][j] for i in range(length)]
                                    for j in range(length)]
    flagArray = [0 for i in range(length)]
    avgLength={}
    for i in range(length-1):
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
        temp = traverse(tmpMatrix)
        s.append(max([len(temp[i]) for i in range(len(temp))])/smax)
    avgLength[length-1]=0
    s.append(0)
    #print("random_attack:",avgLength)
    return avgLength,s


def S_intent_attack(data):
    INF = 1000000
    temp = traverse(data)
    smax = max([len(temp[i]) for i in range(len(temp))])
    s = []
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
        temp = traverse(tmpMatrix)
        s.append(max([len(temp[i]) for i in range(len(temp))]) / smax)
    avgLength[length - 1] = 0
    s.append(0)
    #print("intent_attack:", avgLength)
    return avgLength,s

def draw_S_attack(data,ss,rr):
    if rr == "random":
        y, s = S_random_attack(name)
    else:
        y, s = S_intent_attack(name)
    x = [i / 63 for i in range(63)]
    plt.scatter(x, s, c='r', marker='s')  # 画S的随机攻击
    plt.xlabel("f")
    plt.ylabel("S")
    plt.title(ss + " "+rr+" attack")
    filename = ss + " S "+rr+" attack.png"
    plt.savefig(filename)
    plt.show()

name,hometown,dialect = util.readXls.read_xls()
# draw_S_attack(name,"name","random")
# draw_S_attack(name,"name","intent")
# draw_S_attack(name,"hometown","random")
# draw_S_attack(name,"hometown","intent")
# draw_S_attack(name,"dialect","random")
# draw_S_attack(name,"dialect","intent")
output_result(name,"name")
output_result(hometown,"hometown")
output_result(dialect,"dialect")
#plotMap(name,"name")
# plot_random_intentional_Map(hometown,"hometown")
# plot_random_intentional_Map(dialect,"dialect")

#plot_corness_Map(name,"name")
# plot_corness_Map(hometown,"hometown")
# plot_corness_Map(dialect,"dialect")

#print(Floyd(name))
#
# avgLength = random_attack(name)
# x = [i/63 for i in range(len(avgLength))]
# y=[avgLength[i] for i in range(len(avgLength))]
# plt.scatter(x, y,c='r',marker='s')  # 画随机攻击
# plt.xlabel("node name")
# plt.ylabel("average_shortest")
# plt.title("name"+" random attack")
# #plt.show()
#
# avgLength = intent_attack(name)
# x = [i/63 for i in range(len(avgLength))]
# y=[avgLength[i] for i in range(len(avgLength))]
# plt.scatter(x, y,c='r',marker='s')  # 画特定攻击
# plt.xlabel("node name")
# plt.ylabel("average_shortest")
# plt.title("name"+" intentional attack")
# plt.savefig("filename.png")
# plt.show()




