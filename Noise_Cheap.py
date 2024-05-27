import numpy as np
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DM
from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 13413

r = remote(HOST, PORT)

encrypt = {"option": "encrypt", "message": "0"}
get_flag = {"option": "get_flag", "index": "0"}


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def lattice_reduction():
    json_send(encrypt)
    sample = json_recv()
    print(sample)
    a = json.loads(sample["A"])
    b = json.loads(sample["b"])
    L = []
    N = len(a)

    for i, k in enumerate(a):
        v = [0] * (N + 1)
        v[i] = 1
        v[-1] = -k
        L.append(v)
    L.append([0] * N + [b])
    L = DM(L, ZZ)
    L = L.lll()
    return L


r.readline()
print(lattice_reduction())
