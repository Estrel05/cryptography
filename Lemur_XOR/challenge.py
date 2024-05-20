import os
import cv2

os.chdir("C:\\Users\\Estrel\\Documents\\GitHub\\cryptography\\Lemur_XOR")

lemur = cv2.imread("lemur.png")
flag = cv2.imread("flag.png")
decrypted = cv2.bitwise_xor(lemur, flag)

cv2.imwrite("decrypted.png", decrypted)
