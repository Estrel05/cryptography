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

    return s0


a1, a2, a3 = extended_gcd(187, 5), extended_gcd(85, 11), extended_gcd(55, 17)
if a1 < 0:
    a1 += 5
if a2 < 0:
    a2 += 11
if a3 < 0:
    a3 += 17

x = 2 * 187 * a1 + 3 * 85 * a2 + 5 * 55 * a3
print(x % 935)
