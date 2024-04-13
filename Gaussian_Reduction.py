import math

v = [846835985, 9834798552]
u = [87502093, 123094980]


def gaussian_reduction(v1, v2):
    while 1:
        if math.sqrt(sum(x**2 for x in v2)) < math.sqrt(sum(x**2 for x in v1)):
            v1, v2 = v2, v1
        m = int(sum(v1[i] * v2[i] for i in range(len(v1))) // sum(x**2 for x in v1))
        if m == 0:
            return v1, v2
        v2 = [v2[i] - m * v1[i] for i in range(len(v1))]


v1, v2 = gaussian_reduction(v, u)
inner_product = sum(v1[i] * v2[i] for i in range(len(v1)))

print(inner_product)
