import util.readXls
import util.graph
import copy

name,hometown,dialect = util.readXls.read_xls()
graph = util.graph.graph()
degreee = graph.Degree(name)
graph.Clustering(name)
#graph.connect_component(name)
data=copy.deepcopy(name)
data = graph.Floyd(data)
#graph.avg_shortest_path(data)
core=graph.corona(name)

dist_r = graph.radom_attack(name)
max=0
for i in range(len(degreee)):
    if degreee[max]<degreee[i]:
        max=i
dist_i = graph.intential_attack(name,max)

