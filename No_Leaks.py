from pwn import *
import json
import base64

HOST = "socket.cryptohack.org"
PORT = 13370

r = remote(HOST, PORT)


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


print(r.readline())

table = [[0 for i in range(256)] for j in range(20)]
for i in range(5000):
    request = {"msg": "request"}
    json_send(request)

    response = json_recv()
    if "error" in response:
        continue
    encrypted_flag = base64.b64decode(response["ciphertext"])
    print(encrypted_flag)

    for j in range(20):
        table[j][encrypted_flag[j]] = 1

for i in range(20):
    for j in range(128):
        if table[i][j] == 0:
            print(chr(j), end="")
