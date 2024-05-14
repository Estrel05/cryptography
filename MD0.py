from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import pwn
import json

host = "socket.cryptohack.org"
port = 13388


def decrypt():
    pr = pwn.connect(host, port)

    try:
        pr.readline()
        pr.sendline('{"option":"sign","message":""}')

        c1 = bytes.fromhex(json.loads(pr.readline().strip().decode())["signature"])
        data = b"admin=True" + b"\x06" * 6
        fake = pwn.xor(AES.new(data, AES.MODE_ECB).encrypt(c1), c1).hex()
        data = (b"\x10" * 16 + b"admin=True").hex()
        pr.sendline(f'{{"option":"get_flag","signature":"{fake}","message":"{data}"}}')
        print(pr.readline())
    finally:
        pr.close()


decrypt()
