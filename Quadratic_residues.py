import sys

p = 29
ints = [14, 6, 11]

for i in ints:
    for j in range(p):
        if pow(j, 2, p) == i:
            print(j)
