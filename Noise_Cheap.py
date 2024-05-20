from pwn import *
import json

HOST = "socket.cryptohack.org"
PORT = 13413

r = remote(HOST, PORT)


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


request = {"option": "get_flag", "index": "1"}
