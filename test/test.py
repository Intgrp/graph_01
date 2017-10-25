import util.readXls
import util.graph
import copy
import matplotlib.pyplot as plt

def main(graph,data,ss):
    #graph.DrawMap(name, "name")
    #---------------------------
    # degree = graph.Degree(data)
    # plt.bar(range(len(degree)), degree)  # 画度分布的直方图展示出来
    # plt.xlabel("node name")
    # plt.ylabel("number of node")
    # plt.title(ss+" degree")
    #---------------------------
    # cluster = graph.Clustering(data)
    # plt.bar(range(len(cluster)), cluster)  # 画每个点的聚类系数
    # plt.xlabel("node name")
    # plt.ylabel("cluster coefficient")
    # plt.title(ss+" cluster")
    #-----------------------------
    # average_shortest = graph.avg_shortest_path(data)
    # print("avg_path:",average_shortest)
    # plt.bar(range(len(average_shortest)), average_shortest)  # 画平均最短路径长度
    # plt.xlabel("node name")
    # plt.ylabel("average_shortest")
    # plt.title(ss+" average_shortest")
    #-----------------------------
    # dist_r = graph.radom_attack(data)
    # x = [i/63 for i in range(len(dist_r))]
    # plt.scatter(x, dist_r)  # 画随机攻击
    # plt.xlabel("node name")
    # plt.ylabel("average_shortest")
    # plt.title(ss+" random attack")
    #--------------------------------
    core = graph.corona(data)
    print("core_1:",core)
    temp = [ core[i][1] for i in range(len(core))]
    print("core_2:",temp)
    plt.bar(range(len(temp)), temp)  # 画每个点的核数
    plt.xlabel("node name")
    plt.ylabel("core number")
    plt.title(ss+" core number")

    plt.show()

name,hometown,dialect = util.readXls.read_xls()
graph = util.graph.graph()

main(graph,name,"name")
#main(graph,hometown,"hometown")
#main(graph,dialect,"dialect")


#graph.DrawMap(name,"name")
#graph.DrawMap(hometown,"hometown")
#graph.DrawMap(dialect,"dialect")

# print("degree:",degree)
# graph.Clustering(name)
# #graph.connect_component(name)
# data=copy.deepcopy(name)
# data = graph.Floyd(data)
# #print("Floyd:",data)
# avg_shortset_path = graph.avg_shortest_path(data)
# print("avag_shortest:",avg_shortset_path)
# data=copy.deepcopy(name)
# core=graph.corona(name)
#
# dist_r = graph.radom_attack(name)
# print("random attack:",dist_r)
# mmax=0
# for i in range(len(degree)):
#     if degree[mmax]<degree[i]:
#         mmax=i
# dist_i = graph.intential_attack(name,mmax)
# print("intention attack",dist_i)
