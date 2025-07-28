## 1. simple‑xor - Personalised Write-up


**Category:** Cryptography – 100 pts  
**Flag:** `flag{simple_xor}`



## Challenge Flow

1. Hex‑decode `cipher.txt`
2. Brute‑force single‑byte keys: from 0x20 to 0x7F with xor     
3. Submit the flag{simple_xor}
    
    

## How Difficulty Was Adjusted and Defense Mechanisms

I was not confident with doing these types of xors so that I wrote an initial cryptography task where the task is very simple, I reused the key and only used one byte to keep it intentionally week allowing for minimal scripting to find the solution
    



### Build Notes

This task is a **single‑byte XOR**: the plaintext flag is XORed with one byte, then hex‑encoded into `cipher.txt`.

### Solution Notes

1. Hex‑decode the ciphertext

```bash
xxd -r -p cipher.txt > cipher.bin
```

2. Brute‑force single‑byte XOR (printable keys 0x20–0x7e)

```bash
python3 - <<'PY'
import string
c = bytes.fromhex(open('cipher.txt').read().strip())
for k in range(0x20, 0x7f):
    p = bytes(b ^ k for b in c)
    if b"flag{" in p and all(chr(x) in string.printable for x in p):
        print(f"key=0x{k:02x} -> {p.decode()}")
        break
PY
```

and it prints the flag.




## Related / Future

- Repeating‑Key XOR (Vigenère‑Style)
- Multi‑Time Pad/Key‑Reuse scenarios and crib‑dragging
- Bit‑Flipping attacks in stream‑cipher/CTR modes

    

### Sources

- **XOR cipher basics**: https://en.wikipedia.org/wiki/XOR_cipher
- **Cryptopals S1C3**: https://cryptopals.com/sets/1/challenges/3
- **What is xor** https://ctf101.org/cryptography/what-is-xor/