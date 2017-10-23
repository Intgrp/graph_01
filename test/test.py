import util.readXls
import util.graph


name,hometown,dialect = util.readXls.read_xls()
graph = util.graph.graph()
#graph.printDegree(name)
#graph.printClustering(name)
#graph.connect_component(name)
data = graph.Floyd(name)
graph.avg_shortest_path(data)
