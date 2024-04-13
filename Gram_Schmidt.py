import numpy as np

v = []
v += [np.array([4, 1, 3, -1])]
v += [np.array([2, 1, -3, 4])]
v += [np.array([1, 0, -2, 7])]
v += [np.array([6, 2, 9, -5])]

u = [v[0]]
for i in range(1, 4):
    uij = [sum(v[i] * uj) / sum(uj * uj) for uj in u[:i]]
    u += [v[i] - sum(uij[j] * u[j] for j in range(len(uij)))]

print(u[3][1])
