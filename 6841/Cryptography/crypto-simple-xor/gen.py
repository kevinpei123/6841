#!/usr/bin/env python3
import secrets, string, pathlib

FLAG = b"flag{simple_xor}"
key  = ord(secrets.choice(string.printable.strip()))

cipher = bytes(b ^ key for b in FLAG).hex()

pathlib.Path("cipher.txt").write_text(cipher + "\n")
