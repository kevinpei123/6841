## 1. simple‑xor - Personalised Write-up


**Category:** Cryptography – 100 pts  
**Flag:** `flag{simple_xor}`



## Challenge Flow

1. Hex‑decode `cipher.txt`
2. Brute‑force single‑byte keys: from 0x20 to 0x7F with xor     
3. Submit the flag{simple_xor}
    
    

## How Difficulty Was Adjusted and Defense Mechanisms

I was not confident with doing these types of xors so that I wrote an initial cryptography task where the task is very simple, I reused the key and only used one byte to keep it intentionally week allowing for minimal scripting to find the solution
    


## Related / Future

- Repeating‑Key XOR (Vigenère‑Style)
- Multi‑Time Pad/Key‑Reuse scenarios and crib‑dragging
- Bit‑Flipping attacks in stream‑cipher/CTR modes

    

### Sources

- **XOR cipher basics**: https://en.wikipedia.org/wiki/XOR_cipher
- **Cryptopals S1C3**: https://cryptopals.com/sets/1/challenges/3
- **What is xor** https://ctf101.org/cryptography/what-is-xor/