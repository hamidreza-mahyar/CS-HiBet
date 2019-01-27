from cvxpy import *


def lasso(A, y):
    m, n = A.shape
    x = Variable(n)
    objective = Minimize(sum_squares(A * x - y) + norm(x, 1))
    constraints = [x >= 0]
    p = Problem(objective, constraints)
    p.solve(solver='SCS', eps=1e-1)

    return x.value
