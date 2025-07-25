# RSA – Near‑Prime – Personalised Write‑up

**Category:** Reverse Engineering – 400 pts
**Flag:** `flag{near_prime_math}`

---

## Challenge Flow

1. Running `crackme_rsa_mid` just asks for a private exponent.
2. Using a `strings` search shows three numbers: 16000000472000002997, 65537, 13929899205717235763
3. Square‑rooting N ≈ 4000000059 hints that p and q must be the two
   nearest primes of 4000000037, 4000000081
4. Compute the entire RSA equation to get the solution of d = 9520118682479822273
5. putting d back into the binary yields:
   the flag{near_prime_math}

---

## How Difficulty Was Increased and Defence Mechanisms

I used a near-square massive 64-bit modulus so that using naive trial division would fail but using the fermat factoristion allows it to become more factorable. I also stored the numbers as decimal ASCII to make the grep filters more dodgable, making sure that they would not be gotten easily. I then stripped the binary by compiling with -02 which hides most of the helpers, meaning that the user needs to reverse engineer just to locate the numbers. 
I also hid the pair of 64‑bit primes only 44 apart inside a stripped ­‑O2 binary and left N, e, C as plain decimal strings. This disallows naive trial‑division yet collapses under classic Fermat factorisation, forcing solvers to reverse‑engineer the ELF, spot the near‑square modulus and apply the right math.






---

## Related & Future Variants
- Fermat‑style near‑square variants with adjustable prime gaps
- Obfuscated ELF segments or packed code hiding N, e, and C
- Flags embedded in the binary, so reverse‑engineers must reconstruct the flag bit by bit



---

### Sources

- **Fermat Factorisation:** https://crypto.stanford.edu/pbc/notes/contfactor/fermat.html
- **RSA key guidelines:** NIST SP 800‑56B rev3
- **Binary Ninja Docs** docs.binary.ninja
- **CTFTime Write‑ups Archive** ctftime.org/writeups


---

