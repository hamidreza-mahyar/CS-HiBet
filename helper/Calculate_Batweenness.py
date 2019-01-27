import networkx as nx
import betweenness as bw

dataset_path_list = ["BA"]
def run_bw(f_bw):
    betweenness = bw.betweenness()
    result_bw = betweenness.betweenness_centrality(graph, None, False, None, False, None)
    for item in result_bw:
        f_bw.write(str(item))
        f_bw.write("\n")

for path in dataset_path_list:
    graph = nx.read_edgelist("dataset/" + path + ".txt")
    with open("dataset/" + path + "_out_bw_withValue.txt", 'a+') as f_bw:
        run_bw(f_bw)