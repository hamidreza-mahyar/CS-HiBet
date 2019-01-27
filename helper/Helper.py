import numpy as np
import random


def computeF_mesure(Xhat, X, k):
    topK_X_index = sorted(range(len(X)), key=lambda i: X[i])[-k:]
    topK_Xhat_index = sorted(range(len(Xhat)), key=lambda i: Xhat[i])[-k:]

    X = np.zeros(len(X))
    Xhat = np.zeros(len(X))

    X[topK_X_index] = 1
    Xhat[topK_Xhat_index] = 1
    tp, tn, fp, fn = 0, 0, 0, 0

    for v in range(len(X)):
        if Xhat[v] == 0 and X[v] == 0:
            tn = tn + 1
        if Xhat[v] == 1 and X[v] == 1:
            tp = tp + 1
        if Xhat[v] == 1 and X[v] == 0:
            fn = fn + 1
        if Xhat[v] == 0 and X[v] == 1:
            fp = fp + 1
    p = tp / (tp + fp)
    r = tp / (tp + fn)
    print("F measure,tp,tn,fp,fn, p,r", tp, tn, fp, fn, p, r)
    if p + r == 0: return 0
    F = (2 * (p * r) / (p + r))
    return F


def top_k_index(arr, k):
    return np.argsort(arr)[::-1][:k]


def randomwalk_step_ju(g, k, is_er=False):
    n = g.vcount()
    d = min(g.degree())
    c = g.maxdegree() / d

    T = 1
    if (is_er): T = pow(np.log2(n), 4)

    l = (n * d) / (pow(c, 3) * k * T)

    return np.ceil(l)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"
