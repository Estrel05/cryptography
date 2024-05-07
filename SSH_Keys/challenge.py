import os
from Crypto.PublicKey import RSA

os.chdir("C:\\Users\\Estrel\\Documents\\GitHub\\Cryptography\\SSH_Keys")

with open("bruce_rsa.pem", "r") as file:
    data = file.read()
    rsa_key = RSA.importKey(data)

modulus = rsa_key.n
print(modulus)
