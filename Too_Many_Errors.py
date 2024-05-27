import numpy as np
from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 13390

r = remote(HOST, PORT)

get_sample = {"option": "get_sample"}
reset = {"option": "reset"}


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def mode_vector():
    mtx = []

    for _ in range(10):
        json_send(get_sample)
        sample = json_recv()
        print(sample)
        vec = np.array(sample["a"] + [sample["b"]])
        mtx.append(vec)
        json_send(reset)
        r.readline()

    uvecs, cnts = np.unique(mtx, axis=0, return_counts=True)
    mode = uvecs[np.argmax(cnts)]

    return mode


def vec_collect(mode):
    mtx = [[] for _ in range(len(mode) - 1)]

    while any(row == [] for row in mtx):
        json_send(get_sample)
        sample = json_recv()
        print(sample)
        vec = np.array(sample["a"])
        idx = np.where(mode[:-1] != vec)[0]
        if len(idx) > 0:
            mtx[idx[0]] = [vec[idx[0]], sample["b"]]
        json_send(reset)
        r.readline()

    return mtx


def mod_solve(mode, mtx):
    flag = ""

    for i in range(len(mode) - 1):
        a = mode[i] - mtx[i][0]
        b = mode[-1] - mtx[i][1]
        if b < 0:
            b += 127
        s = np.arange(128)
        eq = (a * s) % 127 - b
        sol = s[eq == 0]
        flag += chr(sol[0])

    return flag


r.readline()
mode = mode_vector()
eq_mtx = vec_collect(mode)
flag = mod_solve(mode, eq_mtx)
print("flag: {}".format(flag))
