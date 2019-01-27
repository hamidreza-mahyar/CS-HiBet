from collections import defaultdict
import networkx as nx
import numpy as np

graph_path = "dataset/BA.txt"
cs_path = "result/__ordered_BA_m100_l200_k75.txt"
k_list = np.arange(0.05, 0.45, 0.05)
graph = nx.read_edgelist(graph_path)
n_nodes = nx.number_of_nodes(graph)
n_links = nx.number_of_edges(graph)
print(graph_path)
print("Nodes=", n_nodes, ", Links=", n_links)


def orderdCompare(g, k, real, predicted, between):
    predicted = list(predicted)
    s = 0
    wsum = 0
    N = nx.number_of_nodes(g)
    for i in range(0, k + 1):
        v = real[i]
        rank_real = i + 1
        rank_predicted = predicted.index(v) + 1
        w = between[v]  # g.degree(v)
        s = s + (w * abs(rank_real - rank_predicted)) / (N - (2 * i) - 1)
        wsum = wsum + w
    d = s / wsum
    return d


f_cs = open(cs_path, 'r')
lines_cs = f_cs.readlines()[1:]
v = []
result_between = defaultdict(lambda: [])
result_hibet = defaultdict(lambda: [])
for x in lines_cs:
    x_split = x.split('\t')
    v = x_split[0]
    result_between[v] = float(x_split[1])
    result_hibet[v] = float(x_split[2])
result_between_sorted = sorted(result_between, key=result_between.get, reverse=True)
result_hibet_sorted = sorted(result_hibet, key=result_hibet.get, reverse=True)

for k in k_list:
    slice = int(n_nodes * k)
    k_result_bw = result_between_sorted[:(slice + 1)]
    k_result = result_hibet_sorted
    d = orderdCompare(g=graph, k=slice, real=k_result_bw, predicted=k_result, between=result_between)
    print("HiBet  k=%.2f  Distance=%.3f" % (k, d))
