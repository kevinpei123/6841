#!/usr/bin/env python3
import random
import pathlib

def bytes_to_long(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def is_prime(n: int, k: int = 5) -> bool:
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def get_prime(bits: int) -> int:
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def main():
    flag = b"flag{cube_root_rsa}"
    m = bytes_to_long(flag)
    e = 65537

    while True:
        p = get_prime(256)
        q = get_prime(256)
        N = p * q
        if m**3 < N:
            break

    C = pow(m, e, N)

    output = (
        f"N = 0x{N:x}\n"
        f"e = {e}\n"
        f"C = 0x{C:x}\n"
    )
    pathlib.Path("rsa3.txt").write_text(output)

if __name__ == "__main__":
    main()
