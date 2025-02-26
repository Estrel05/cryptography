from pwn import *
import json
import numpy as np

HOST = "socket.cryptohack.org"
PORT = 13411

r = remote(HOST, PORT)
n = 64
p = 257
q = 0x10001


def json_recv():
    line = r.readline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def gaussian_elimination(matrix, vector, modulus):
    # 행렬의 크기 확인
    n = matrix.shape[0]
    # pivot 선택, 행 교환
    for i in range(n):
        pivot = matrix[i, i] % modulus
        if pivot == 0:
            for j in range(i + 1, n):
                if matrix[j, i] % modulus != 0:
                    matrix[[i, j]] = matrix[[j, i]]
                    vector[i], vector[j] = vector[j], vector[i]
                    break
            pivot = matrix[i, i] % modulus
        # 예외처리
        if pivot == 0:
            raise ValueError("No non-zero pivot found. Please try again.")
        # pivot의 역원 계산, 해당 행에 곱하기
        inv_pivot = pow(int(pivot), -1, modulus)
        matrix[i] = (matrix[i] * inv_pivot) % modulus
        vector[i] = (vector[i] * inv_pivot) % modulus
        # pivot 행을 사용해 소거
        for j in range(i + 1, n):
            factor = matrix[j, i] % modulus
            matrix[j] = (matrix[j] - factor * matrix[i]) % modulus
            vector[j] = (vector[j] - factor * vector[i]) % modulus
    # 후진대입법
    solution = np.zeros(n, dtype=np.int64)
    for i in range(n - 1, -1, -1):
        solution[i] = (
            b_vec[i] - np.sum(A_mtx[i, i + 1 :] * solution[i + 1 :])
        ) % modulus

    return solution


# S 계산
print(f"{r.readline()}")
request = {"option": "encrypt", "message": "0"}
mtx = []
vec = []
for i in range(n):
    json_send(request)
    response = json_recv()
    print(f"{i + 1}: {response}")
    mtx.append(json.loads(response["A"]))
    vec.append(int(response["b"]))
A_mtx = np.array(mtx, dtype=np.int64)
b_vec = np.array(vec, dtype=np.int64)
S = gaussian_elimination(A_mtx, b_vec, q)
print(f"S: {S}")
# 복호화
i = 0
response = ""
flag = ""
while True:
    request = {"option": "get_flag", "index": f"{i}"}
    json_send(request)
    response = json_recv()
    if "error" in response:
        break
    print(f"{i + 1}: {response}")
    A = np.array(json.loads(response["A"]), dtype=np.int64)
    b = int(response["b"])
    m = chr((b - np.dot(A, S)) % q)
    print(f"m: {m}")
    flag += m
    i += 1
print(f"flag: {flag}")
