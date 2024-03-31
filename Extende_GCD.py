import sys


def extended_gcd(a, b):
    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1

    while r1 > 0:
        q = r0 // r1
        r = r0 % r1
        r0, r1 = r1, r

        s = s0 - s1 * q
        s0, s1 = s1, s

        t = t0 - t1 * q
        t0, t1 = t1, t

    print("u = {}\nv = {}".format(s0, t0))


p, q = 26513, 32321
extended_gcd(p, q)
