import os
import json

# 2^128 collision protection!
BLOCK_SIZE = 32

# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [
    0x6B17D1F2,
    0xE12C4247,
    0xF8BCE6E5,
    0x63A440F2,
    0x77037D81,
    0x2DEB33A0,
    0xF4A13945,
    0xD898C296,
]
X = [
    0x4FE342E2,
    0xFE1A7F9B,
    0x8EE7EB4A,
    0x7C0F9E16,
    0x2BCE3357,
    0x6B315ECE,
    0xCBB64068,
    0x37BF51F5,
]
Y = [
    0xC97445F4,
    0x5CDEF9F0,
    0xD3E05E1E,
    0x585FC297,
    0x235B82B5,
    0xBE8FF3EF,
    0xCA67C598,
    0x52018192,
]
Z = [
    0xB28EF557,
    0xBA31DFCB,
    0xDD21AC46,
    0xE2A91E3C,
    0x304F44CB,
    0x87058ADA,
    0x2CB81515,
    0x1E610046,
]

# Lets work with bytes instead!
W_bytes = b"".join([x.to_bytes(4, "big") for x in W])
X_bytes = b"".join([x.to_bytes(4, "big") for x in X])
Y_bytes = b"".join([x.to_bytes(4, "big") for x in Y])
Z_bytes = b"".join([x.to_bytes(4, "big") for x in Z])


def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len] * padding_len)


def blocks(data):
    return [data[i : (i + BLOCK_SIZE)] for i in range(0, len(data), BLOCK_SIZE)]


def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]


def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return data[-x:] + data[:-x]


def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block


def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i, b in enumerate(msg_blocks):
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i + 11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i + 6)
        initial_state = xor(initial_state, mix_in)
    return initial_state.hex()


def reverse_scramble_block(block):
    for _ in range(40):
        block = rotate_left(block, 17)
        block = xor(X_bytes, block)
        block = rotate_right(block, 6)
        block = xor(W_bytes, block)
    return block


def solve():
    a = os.urandom(32)
    scr = scramble_block(a)

    b = os.urandom(32)
    mix_in = xor(scr, b)

    b = rotate_right(b, 7)
    b = xor(b, X_bytes)
    b = rotate_left(b, 12)

    mix_rev = reverse_scramble_block(mix_in)
    b_rev = reverse_scramble_block(b)

    assert cryptohash(mix_rev + b_rev) == cryptohash(a)
    return json.dumps({"m1": (mix_rev + b_rev).hex(), "m2": a.hex()})


print(solve())
