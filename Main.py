from graph.Network import *
from cvx.lasso import *
import numpy as np


class Inline(object):
    pass


def hibet(data):

    g = data.net
    N = g.structure.vcount()
    M = int(data.measurement * N)
    L = int(data.step * N)
    K = int(data.sparsity * N)

    print(('m {} step {} K {}\n'.format(M, L, K)))

    # start Hibet
    A = g.random_walk_weighted_measurment_matrix(M, L)
    Y = g.compressSampling(A)
    X = lasso(A, Y)
    X_bet = np.array(X).transpose().reshape(-1).tolist()
    # end Hibetbet

    dic = [M]
    dic.append(L)
    dic.append(K)

    return dic, X_bet


def print_ordered(d, dic, nodeCount, bet, X_bet):
    path = _result_path + "__ordered_{}_m{}_l{}_k{}.txt".format(d, str(dic[0]), str(dic[1]), str(dic[2]))
    text_file = open(path, "w")
    text_file.write("v\tbet\thibet\n")
    for v in range(nodeCount):
        line = '{}\t{}\t{}'.format(v, bet[v], X_bet[v])
        text_file.write(line + "\n")

    text_file.close()


def run(d, measurment, step, sparsity):
    path = _dataset_path + d + '.txt'
    net = Network(path)
    bet = net.structure.betweenness() # set Global-Betweenness weights
    nodeCount = net.structure.vcount()
    net.set_bet_Weight()  # set ego-Betweenness wights

    data = Inline()

    data.net = net
    data.measurement = measurment
    data.step = step
    data.sparsity = sparsity

    [dic, X_bet] = hibet(data)

    print_ordered(d, dic, nodeCount, bet, X_bet)


if __name__ == '__main__':
    _result_path = "result/"
    _dataset_path = "dataset/"

    run(d= "BA", measurment=0.2, step=0.4, sparsity=0.15)
