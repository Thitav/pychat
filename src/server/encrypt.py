import hashlib
import base64

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def f(raw, key):
    return sha256(raw + key)

def xor(d1, d2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(d1, d2))

def execute(raw, key):
    left = raw[0]
    right = raw[1]
    k0 = key[0]
    k1 = key[1]

    left = xor(left, f(right, k0))
    left, right = right, left
    left = xor(left, f(right, k1))

    return [left, right]

def encode(raw, key):
    raw = raw.split(':')
    key = key.split(':')

    e = execute(raw, key)
    e = (e[0] + ':' + e[1]).encode()
    e = base64.b64encode(e).decode('utf-8')

    return e

def decode(cipher, key):
    cipher = base64.b64decode(cipher.encode()).decode('utf-8')
    cipher = cipher.split(':')
    key = key.split(':')
    key[0], key[1] = key[1], key[0]

    d = execute(cipher, key)
    d = d[0] + ':' + d[1]

    return d