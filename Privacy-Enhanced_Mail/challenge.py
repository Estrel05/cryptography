import os
from Crypto.PublicKey import RSA

os.chdir(
    "C:\\Users\\Estrel\\Documents\\GitHub\\Practice\\Python\\Privacy-Enhanced_Mail"
)

with open("privacy_enhanced_mail.pem", "r") as file:
    data = file.read()
    rsa_key = RSA.importKey(data)

private_key = rsa_key.d
print(private_key)
