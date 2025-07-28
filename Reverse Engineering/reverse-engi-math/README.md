# RSA – Near‑Prime – Personalised Write‑up

**Category:** Reverse Engineering – 400 pts
**Flag:** `flag{flagRSA!}`

---

## Challenge Flow

1. Running `crackme_rsa_mid` just asks for a private exponent.
2. Using a `gdb command` search shows three numbers: 16000000472000002997, 65537, 13929899205717235763
3. Square‑rooting N ≈ 4000000059 hints that p and q must be the two
   nearest primes of 4000000037, 4000000081
4. Compute the entire RSA equation to get the solution of d = 9520118682479822273
5. putting d back into the binary yields:
   the flag{flagRSA!}



---

## How Difficulty Was Increased and Defence Mechanisms

I used a near-square massive 64-bit modulus so that using naive trial division would fail but using the fermat factoristion allows it to become more factorable. I also stored the numbers as decimal ASCII to make the grep filters more dodgable, making sure that they would not be gotten easily. I then stripped the binary by compiling with -02 which hides most of the helpers, meaning that the user needs to reverse engineer just to locate the numbers. 
I also hid the pair of 64‑bit primes only 44 apart inside a stripped ­‑O2 binary and left N, e, C as plain decimal strings. This disallows naive trial‑division yet collapses under classic Fermat factorisation, forcing solvers to reverse‑engineer the ELF, spot the near‑square modulus and apply the right math.




---

## Indepth Build and Solution Notes

### Build Section


This program is a compact RSA "crackme" that reads a 64-bit integer d and computers m = C^d mod N using 128-bit safe and square multiply, it then prints 'm' as text.
It implements 
`N = 16000000472000002997`
and 
`C = 13929899205717235763`
using modexp as a safety mechanisms with the uint128_t values linking in __umodti3 to do 128-bit modulus. Because the output comes out as encoded, I can print it in reverse and get human numbers. 
To compile this file I used gcc with 
```bash
gcc -o crackme_rsa_mid crackme_rsa_mid.c
```
to get the assembly code for the file which is given as the challenge. 
Because of N being a near square RSA modulus, its primes are very close to the square root of N, so that Fermat factorisation can be applied and is trivial. The public exponent is the common e = 65527, so once p and q are known, d is just the modular invers of e. mod phi(N). The major issue that I found with doing this was the overflow issue, especially in a language like C. so using the `__uint128_t` in `modexp` allowed for the code to actually run and properly show the numbers. I initially wanted this challenge to be solved using the `strings` command but because the constants are binary immediates, assembly is much more prefered. 


---

## Solution Section

1. First I extract the constants using gdb which the GNU Debugger, 
It is a powerful command-line debugging tool used to analyze and debug programs. It allows users to inspect the internal state of a program while it is executing or after it has crashed. As a result, it can be used to reverse engineer the number seen in the program so that the users can progress with the challenge. 
The command I used was `gdb ./crackme_rsa_mid -ex 'disassemble /r main' -ex quit`.

where `-ex` 'disassemble /r main' — tells gdb to execute a command right after loading
`disassemble` prints assembly for a function or address range.
`/r` means “raw” — include the opcode bytes
`main` is the symbol to disassemble



and it gave me the results of 
```
C = 0xc150f18619c59833 = 13929899205717235763
N = 0xde0b6ba85ba47bb5 = 16000000472000002997
```
2. Factor N with Fermat as it is nearsquare

Compute `a = ⌈√N⌉ = 4,000,000,059`.
Then `b² = a² − N = 484 = 22²` → `b = 22`.
Hence:
`p = a − b = 4,000,000,037`
`q = a + b = 4,000,000,081`




3. Compute phi(N) and the private exponent d

`phi(N) = (p−1)(q−1) = 16,000,000,464,000,002,880`
Take the standard `e = 65537` which can be found and computer the modular inverse
`d ≡ e⁻¹ (mod phi(N)) = 9,520,118,682,479,822,273`

4. Input the number to get the flag of flag{flagRSA!}





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

