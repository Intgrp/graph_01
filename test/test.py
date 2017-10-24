import util.readXls
import util.graph
import copy

name,hometown,dialect = util.readXls.read_xls()
graph = util.graph.graph()
degree = graph.Degree(name)
print("degree:",degree)
graph.Clustering(name)
#graph.connect_component(name)
data=copy.deepcopy(name)
data = graph.Floyd(data)
#print("Floyd:",data)
avg_shortset_path = graph.avg_shortest_path(data)
print("avag_shortest:",avg_shortset_path)
data=copy.deepcopy(name)
core=graph.corona(data)

dist_r = graph.radom_attack(name)
print("random attack:",dist_r)
mmax=0
for i in range(len(degree)):
    if degree[mmax]<degree[i]:
        mmax=i
dist_i = graph.intential_attack(name,mmax)
print("intention attack",dist_i)
