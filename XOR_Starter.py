c = b"label"

print("".join(chr(i ^ 13) for i in c))
