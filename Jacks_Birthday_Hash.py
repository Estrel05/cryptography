k = 1

while True:
    if pow(2047 / 2048, k) < 0.5:
        break
    k += 1

print(k)
