#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

static uint64_t modexp(uint64_t base, uint64_t exp, uint64_t mod) {
    __uint128_t res = 1, b = base % mod;
    while (exp) {
        if (exp & 1) res = (res * b) % mod;
        b = (b * b) % mod;
        exp >>= 1;
    }
    return (uint64_t)res;
}

int main(void) {
    uint64_t d;

    puts("Enter private exponent:");
    if (scanf("%" SCNu64, &d) != 1) {
        puts("Input error");
        return 1;
    }

    const uint64_t N = 16000000472000002997ULL;
    const uint64_t C = 13929899205717235763ULL;

    uint64_t m = modexp(C, d, N);

    char buf[32];
    int idx = 0;
    while (m) {
        buf[idx++] = (char)(m & 0xFF);
        m >>= 8;
    }
    if (idx == 0) {
        puts("Decryption failed");
        return 1;
    }

    for (int i = idx - 1; i >= 0; --i){
        putchar(buf[i]);
    }
    putchar('\n');
    return 0;
}
