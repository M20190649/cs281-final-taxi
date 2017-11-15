import numpy as np
import torch
from torch import Tensor
from torch.autograd import Variable


M, N = (10,35)

w = np.arange(M * N).reshape(M, N)

def weight(i, j):
    return w[i,j]

def min_cost(source, target):
    sx, sy = source
    tx, ty = target

    hor_dir = np.sign(tx - sx)
    ver_dir = np.sign(ty - sy)

    X = np.abs(tx - sx) + 1
    Y = np.abs(ty - sy) + 1
    cost = np.zeros((X, Y))
    paths = np.zeros((X, Y), dtype=object)

    cost[0, 0] = weight(sx, sy)
    paths[0, 0] = [source]

    for i in range(1, X):
        cost[i, 0] = cost[i - 1, 0] + weight(i * hor_dir + sx, sy)
        paths[i, 0] = paths[i - 1, 0] + [(i * hor_dir + sx, sy)]

    for j in range(1, Y):
        cost[0, j] = cost[0, j - 1] + weight(sx, sy + j * ver_dir)
        paths[0, j] = paths[0, j - 1] + [(sx, sy + j * ver_dir)]

    for i in range(1, X):
        for j in range(1, Y):
            if cost[i, j - 1] <= cost[i - 1, j]:
                cost[i, j] = cost[i, j - 1] + \
                    weight(sx + i * hor_dir, sy + j * ver_dir)
                paths[i, j] = paths[i, j - 1] + \
                    [(sx + i * hor_dir, sy + j * ver_dir)]
            else:
                cost[i - 1, j] = cost[i - 1, j] + \
                    weight(sx + i * hor_dir, sy + j * ver_dir)
                paths[i, j] = paths[i - 1, j] + \
                    [(sx + i * hor_dir, sy + j * ver_dir)]

    short = np.zeros((M,N))
    for i, j in paths[X-1,Y-1]:
        short[i,j] = 1
    return Variable(Tensor(short))
