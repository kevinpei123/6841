# Cube Root RSA - Personalised Write‑up

**Category:** Cryptography – 150 pts
**Flag:** `flag{cube_root_rsa}`
-------------------------------

## Challenge Flow

1. Read `rsa3.txt` to extract the modulus, exponent and ciphertext.
2. factor n into primes of p and q
3. Compute the totient as Phi(n) = (p-1)(q-1)
4. Compute the private exponent of d = e^-1 mod(Phi(n))
5. Decrypt the ciphertext as m = C^d mod N
6. Convert m back into bytes to recover the plaintext: using somthing like flag = m.to_bytes((m.bit_length() + 7) // 8, 'big')
7. The flag is flag{cube_root_rsa}.



---

## How Difficulty Was Increased and Defense Mechanisms

Misleading task name due to the task being an expansion on cube rooting rsa , but the exponent is actually the standard e=65537, this means that trivial low‑exponent attacks no longer apply. No padding and a non-trivial size so the solver must still be somewhat knowledgable about modular arithmatic as after decryption, the solution is very clear. 






---

## Related & Future Variants

- Factoring‑based attacks like Small‑Prime, Common‑Factor, Fermat’s Factorization
- Low‑exponent exploits like Hastad’s Broadcast, Franklin–Reiter Related‑Message
- Coppersmith/Lattice techniques like Partial‑Padding, Short‑Root Extraction


---

### Sources
- **ctf101** https://ctf101.org/cryptography/what-is-rsa/
- **Basics - Crypto - RSA** https://vm-thijs.ewi.utwente.nl/ctf/rsa
- **Practical CTF** https://book.jorianwoltjer.com/cryptography/asymmetric-encryption/rsa