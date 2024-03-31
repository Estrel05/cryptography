import sys


t = [0] * 101
t[0] = 1


def catalans(n):
    if t[n] != 0:
        return t[n]

    for i in range(n):
        t[n] += catalans(i) * catalans(n - 1 - i)
    return t[n]


for i in range(101):
    print(catalans(i))
