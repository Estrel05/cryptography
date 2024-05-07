import math

k = 1

while True:
    p = 1 - math.factorial(2048) / (pow(2048, k) * math.factorial(2048 - k))
    if p > 0.75:
        break
    k += 1

print(k)
