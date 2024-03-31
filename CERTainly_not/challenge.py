import os
from Crypto.PublicKey import RSA

os.chdir("C:\\Users\\Estrel\\Documents\\GitHub\\Practice\\Python\\CERTainly_not")

with open("RSA_Key.cer", "r") as file:
    data = file.read()
    rsa_key = RSA.importKey(data)

modulus = rsa_key.n
print(modulus)
