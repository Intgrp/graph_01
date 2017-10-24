import util.readXls
import util.graph
import copy

name,hometown,dialect = util.readXls.read_xls()
graph = util.graph.graph()
degree = graph.Degree(name)
#graph.Clustering(name)
#graph.connect_component(name)
#data=copy.deepcopy(name)
#data = graph.Floyd(data)
#print("Floyd:",data)
#graph.avg_shortest_path(data)
#core=graph.corona(name)

dist_r = graph.radom_attack(name)
print("dist_r",dist_r)
mmax=0
for i in range(len(degree)):
    if degree[mmax]<degree[i]:
        mmax=i
dist_i = graph.intential_attack(name,mmax)
print("dist_i",dist_i)

