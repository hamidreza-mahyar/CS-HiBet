from collections import defaultdict
import numpy as np
import networkx as nx

graph_path = "dataset/BA.txt"
cs_path = "result/__ordered_BA_m100_l200_k75.txt"
k_list = np.arange(0.05, 0.45, 0.05)
graph = nx.read_edgelist(graph_path)
n_nodes = nx.number_of_nodes(graph)
n_links = nx.number_of_edges(graph)
print("Graph", graph_path, "Nodes=", n_nodes, ", Links=", n_links)


def computeF_mesure(topK_Xhat_index, topK_X_index, n):
    X = np.zeros(n)
    Xhat = np.zeros(n)

    X[topK_X_index] = 1
    Xhat[topK_Xhat_index] = 1
    tp, tn, fp, fn = 0, 0, 0, 0

    for v in range(len(X)):
        if Xhat[v] == 0 and X[v] == 0:
            tn = tn + 1
        if Xhat[v] == 1 and X[v] == 1:
            tp = tp + 1
        if Xhat[v] == 0 and X[v] == 1:
            fn = fn + 1
        if Xhat[v] == 1 and X[v] == 0:
            fp = fp + 1
    p = tp / (tp + fp)
    r = tp / (tp + fn)
    if p + r == 0: return 0
    F = (2 * (p * r) / (p + r))
    return F


f_cs = open(cs_path, 'r')
lines_cs = f_cs.readlines()[1:]
v = []
result_between = defaultdict(lambda :[])
result_hibet = defaultdict(lambda :[])
for x in lines_cs:
    x_split = x.split('\t')
    v = x_split[0]
    result_between[v] = float(x_split[1])
    result_hibet[v] = float(x_split[2])
result_between_sorted = sorted(result_between, key=result_between.get, reverse=True)
result_hibet_sorted = sorted(result_hibet, key=result_hibet.get, reverse=True)

for k in k_list:
    slice = int(n_nodes * k)
    k_result_bw = result_between_sorted[:slice]
    k_result_hibet = result_hibet_sorted[:slice]
    fMeasure_hibet = computeF_mesure(topK_Xhat_index=[int(i) for i in k_result_hibet],
                               topK_X_index=[int(i) for i in k_result_bw], n=max([int(i) for i in result_between])+100)
    print("HiBet  k=%.2f F-measure=%.2f"%(k, fMeasure_hibet))
