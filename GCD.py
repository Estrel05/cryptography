import sys


def gcd(a, b):
    a %= b
    if a == 0:
        return b
    else:
        return gcd(b, a)


a = 66528
b = 52920
print(gcd(a, b))
