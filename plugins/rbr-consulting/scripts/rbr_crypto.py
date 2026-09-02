#!/usr/bin/env python3
"""Cifratura delle chiavi RBR in puro Python (solo libreria standard): AES-256-CBC + PBKDF2-HMAC-SHA256
(200.000 iterazioni) + HMAC-SHA256 di integrità. Serve per `rbr-chiavi.enc` dentro il plugin pubblico:
il file è illeggibile senza la passphrase, che sta solo nella Competenza personale «rbr-chiavi».

Formato: b"RBR1" | salt(16) | iv(16) | ciphertext | hmac(32)
Uso CLI:  rbr_crypto.py enc <in.json> <out.enc> <file-passphrase>
          rbr_crypto.py dec <in.enc> <out.json> <file-passphrase>
"""
import os, sys, hmac, hashlib

# --- AES (FIPS-197) ------------------------------------------------------------------------
def _build_tables():
    sbox = [0] * 256
    p = q = 1
    while True:
        p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)      # p *= 3
        q ^= q << 1; q ^= q << 2; q ^= q << 4; q &= 0xFF            # q /= 3
        if q & 0x80:
            q ^= 0x09
        x = q ^ (q << 1) ^ (q << 2) ^ (q << 3) ^ (q << 4)
        sbox[p] = (x ^ (x >> 8) ^ 0x63) & 0xFF
        if p == 1:
            break
    sbox[0] = 0x63
    inv = [0] * 256
    for i, v in enumerate(sbox):
        inv[v] = i
    return sbox, inv

SBOX, INV_SBOX = _build_tables()


def _xtime(a):
    a <<= 1
    return (a ^ 0x1B) & 0xFF if a & 0x100 else a


def _mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = _xtime(a); b >>= 1
    return r


def _expand_key(key):
    nk = len(key) // 4; rounds = nk + 6
    w = [list(key[4 * i:4 * i + 4]) for i in range(nk)]
    rcon = 1
    for i in range(nk, 4 * (rounds + 1)):
        t = list(w[i - 1])
        if i % nk == 0:
            t = t[1:] + t[:1]
            t = [SBOX[b] for b in t]
            t[0] ^= rcon; rcon = _xtime(rcon)
        elif nk > 6 and i % nk == 4:
            t = [SBOX[b] for b in t]
        w.append([w[i - nk][j] ^ t[j] for j in range(4)])
    return [sum(w[4 * r:4 * r + 4], []) for r in range(rounds + 1)], rounds


def _add_round_key(s, k):
    return [s[i] ^ k[i] for i in range(16)]


def _shift_rows(s, inv=False):
    out = [0] * 16
    for c in range(4):
        for r in range(4):
            src = (c + (-r if inv else r)) % 4
            out[4 * c + r] = s[4 * src + r]
    return out


def _mix_columns(s, inv=False):
    out = []
    for c in range(4):
        a = s[4 * c:4 * c + 4]
        if not inv:
            out += [_mul(a[0], 2) ^ _mul(a[1], 3) ^ a[2] ^ a[3],
                    a[0] ^ _mul(a[1], 2) ^ _mul(a[2], 3) ^ a[3],
                    a[0] ^ a[1] ^ _mul(a[2], 2) ^ _mul(a[3], 3),
                    _mul(a[0], 3) ^ a[1] ^ a[2] ^ _mul(a[3], 2)]
        else:
            out += [_mul(a[0], 14) ^ _mul(a[1], 11) ^ _mul(a[2], 13) ^ _mul(a[3], 9),
                    _mul(a[0], 9) ^ _mul(a[1], 14) ^ _mul(a[2], 11) ^ _mul(a[3], 13),
                    _mul(a[0], 13) ^ _mul(a[1], 9) ^ _mul(a[2], 14) ^ _mul(a[3], 11),
                    _mul(a[0], 11) ^ _mul(a[1], 13) ^ _mul(a[2], 9) ^ _mul(a[3], 14)]
    return out


def aes_encrypt_block(rk, rounds, block):
    s = _add_round_key(list(block), rk[0])
    for r in range(1, rounds):
        s = _mix_columns(_shift_rows([SBOX[b] for b in s]))
        s = _add_round_key(s, rk[r])
    s = _shift_rows([SBOX[b] for b in s])
    return bytes(_add_round_key(s, rk[rounds]))


def aes_decrypt_block(rk, rounds, block):
    s = _add_round_key(list(block), rk[rounds])
    for r in range(rounds - 1, 0, -1):
        s = [INV_SBOX[b] for b in _shift_rows(s, inv=True)]
        s = _mix_columns(_add_round_key(s, rk[r]), inv=True)
    s = [INV_SBOX[b] for b in _shift_rows(s, inv=True)]
    return bytes(_add_round_key(s, rk[0]))


# --- contenitore ----------------------------------------------------------------------------
MAGIC = b"RBR1"
ITER = 200_000


def _keys(passphrase, salt):
    km = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, ITER, 64)
    return km[:32], km[32:]


def encrypt(data: bytes, passphrase: str) -> bytes:
    salt, iv = os.urandom(16), os.urandom(16)
    k_enc, k_mac = _keys(passphrase, salt)
    rk, rounds = _expand_key(k_enc)
    pad = 16 - len(data) % 16
    data = data + bytes([pad]) * pad
    out, prev = bytearray(), iv
    for i in range(0, len(data), 16):
        blk = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        prev = aes_encrypt_block(rk, rounds, blk); out += prev
    body = MAGIC + salt + iv + bytes(out)
    return body + hmac.new(k_mac, body, hashlib.sha256).digest()


def decrypt(blob: bytes, passphrase: str) -> bytes:
    if blob[:4] != MAGIC or len(blob) < 4 + 16 + 16 + 16 + 32:
        raise ValueError("formato non riconosciuto")
    body, tag = blob[:-32], blob[-32:]
    salt, iv, ct = body[4:20], body[20:36], body[36:]
    k_enc, k_mac = _keys(passphrase, salt)
    if not hmac.compare_digest(hmac.new(k_mac, body, hashlib.sha256).digest(), tag):
        raise ValueError("passphrase errata o file alterato")
    rk, rounds = _expand_key(k_enc)
    out, prev = bytearray(), iv
    for i in range(0, len(ct), 16):
        blk = ct[i:i + 16]
        out += bytes(a ^ b for a, b in zip(aes_decrypt_block(rk, rounds, blk), prev)); prev = blk
    pad = out[-1]
    if not 1 <= pad <= 16:
        raise ValueError("padding non valido")
    return bytes(out[:-pad])


def _leggi_pass(p):
    return open(p, encoding="utf-8").read().strip()


if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] not in ("enc", "dec"):
        sys.exit(__doc__)
    _, mode, src, dst, pf = sys.argv
    data = open(src, "rb").read()
    out = encrypt(data, _leggi_pass(pf)) if mode == "enc" else decrypt(data, _leggi_pass(pf))
    open(dst, "wb").write(out)
    print(f"✅ {mode}: {src} → {dst} ({len(out)} byte)")
