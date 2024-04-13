from pwn import *
import json
import time
from Crypto.Util.number import long_to_bytes
import hashlib

HOST = "socket.cryptohack.org"
PORT = 13372

r = remote(HOST, PORT)


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def generate_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()


def decrypt(b):
    key = generate_key()
    assert len(b) <= len(key), "Data package too large to decrypt"
    plaintext = b""
    for i in range(len(b)):
        plaintext += bytes([b[i] ^ key[i]])
    return plaintext


print(r.readline())

request = {"option": "get_flag"}
json_send(request)

response = json_recv()
encrypted_flag = bytes.fromhex(response["encrypted_flag"])
flag = decrypt(encrypted_flag)
print(flag)
