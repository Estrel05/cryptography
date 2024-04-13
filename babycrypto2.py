from pwn import *
import base64

HOST = "host3.dreamhack.games"
PORT = 8286

r = remote(HOST, PORT)

r.recvuntil(b"test Command: ")
ciphertext = r.recv()
decoded = base64.b64decode(ciphertext)
decoded_first = decoded[:16]

r.recvuntil(b"Enter your command: ")
r.send(ciphertext)
plaintext = r.recv()
plain_first = plaintext[:16]
test_replaced = plain_first.replace("test", "show") + plaintext[16:]
