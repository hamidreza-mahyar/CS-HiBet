from igraph import Graph
import os.path
from helper.Helper import *


class Network:
    """description of class"""

    def __init__(self, filepath=None, isDirected=False, gient=True, rnd_graph_N=0, rnd_graph_p=0, rnd_graph_m=0):
        if rnd_graph_N > 0 and rnd_graph_p > 0:
            self.structure = Graph.Erdos_Renyi(rnd_graph_N, rnd_graph_p)
            self.path = "ER_" + str(rnd_graph_N) + "_" + str(rnd_graph_p)
        elif rnd_graph_N > 0 and rnd_graph_m > 0:
            self.structure = Graph.Barabasi(rnd_graph_N, rnd_graph_m)
            self.path = "BA" + str(rnd_graph_N) + "_" + str(rnd_graph_m)
        else:
            self.structure = Graph.Read_Ncol(filepath, directed=isDirected)
            self.path = filepath
        if gient:
            self.structure = self.structure.components().giant()
        for v in self.structure.vs():
            v["name"] = str(v.index)

    def printWeight(self):
        for v in self.structure.vs:
            x = self.getEgoCentricScore(v)
            v["weight"] = x
            print(v.index, x)

    def set_bet_Weight(self):
        wpath = self.path + "_w.txt"
        if not os.path.isfile(wpath):
            text_file = open(wpath, "w")
            for v in self.structure.vs:
                w = self.getEgoCentricScore(v)
                v["weight"] = w
                print(v.index, w)
                text_file.write("{}\t{}\n".format(v.index, w))
            text_file.close()
        else:
            print(wpath + " exists")
            file = open(wpath, "r")
            for line in file:
                sline = line.split("\t")
                self.structure.vs[int(sline[0])]["weight"] = float(sline[1])
            file.close()

        self.structure.vs(weight=None)["weight"] = 0

    def getEgoCentricScore(self, node):
        neigbs = self.structure.neighbors(node)
        neigbs.insert(0, node.index)
        adj = np.zeros((len(neigbs), len(neigbs)), dtype=np.int)
        for v1 in neigbs:
            for v2 in neigbs:
                i = neigbs.index(v1)
                j = neigbs.index(v2)
                if v1 != v2:
                    adj[i, j] = 1 if self.structure.are_connected(v1, v2) else 0
        adj2 = np.dot(adj, adj)
        score = 0
        for (x, y), value in np.ndenumerate(adj):
            if x < y and value == 0 and adj2[x, y] != 0:
                score = score + 1 / (adj2[x, y])

        return score

    def compressSampling(self, A):
        Y = np.zeros(len(A))
        for m in range(len(A)):
            row = np.asarray(A[m, :]).reshape(-1)
            non_zero = [i for i, e in enumerate(row) if e != 0]
            val = sum([self.structure.vs[v]["weight"] * row[v] for v in non_zero])
            Y[m] = val
        return Y

    def random_walk(self, step):
        current = random.randint(0, self.structure.vcount() - 1)
        length = 0
        walk = []
        while length < step:
            walk.append(current)
            length += 1
            current = random.choice(self.structure.successors(current))  # direction considerd

        return walk

    def random_walk_weighted(self, step):
        current = random.randint(0, self.structure.vcount() - 1)  # startNode
        length = 0
        walk = []
        while length < step:

            neigbs = self.structure.successors(current)
            not_visited = [i for i in neigbs if i not in walk]

            if len(not_visited) > 0:
                neigbs = not_visited
            elif len(walk) > 0:
                current = walk[-1]
                continue

            walk.append(current)
            length += 1

            neigbs_with_weight = {v: self.structure.vs[v]["weight"] for v in neigbs}

            current = max(neigbs_with_weight, key=neigbs_with_weight.get)
        return walk

    def random_walk_weighted_measurment_matrix(self, nom, step):
        N = self.structure.vcount()
        A = np.zeros((nom, N))
        for m in range(nom):
            rw = self.random_walk_weighted(step)
            for w in range(len(rw)):
                j = rw[w]
                A[m, j] = 1
        return A

    def random_walk_measurment_matrix(self, nom, step):

        N = self.structure.vcount()
        A = np.zeros((nom, N))
        for m in range(nom):
            rw = self.random_walk(step)
            # A[m, rw] = 1
            for w in range(len(rw)):
                j = rw[w]
                A[m, j] = 1

        return A

    def number_of_valid_row(self, A):
        valid_row = 0
        row_gient_count = []
        for m in range(len(A)):
            row = np.asarray(A[m, :]).reshape(-1)
            non_zero_index = [i for i, e in enumerate(row) if e != 0]
            sub_graph = self.structure.subgraph(non_zero_index)
            is_connected = sub_graph.is_connected()
            valid_row = valid_row + (1 if is_connected else 0)

            row_gient = sub_graph.components().giant().vcount() if len(non_zero_index) > 0 else 0

        return [valid_row, row_gient]
