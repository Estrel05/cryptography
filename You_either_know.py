from Crypto.Util.number import *

c = bytes.fromhex(
    "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
)
k = [b"m", b"y", b"X", b"O", b"R", b"k", b"e", b"y"]

i = 0
for j in c:
    print(chr(j ^ bytes_to_long(k[i % 8])), end="")
    i += 1
