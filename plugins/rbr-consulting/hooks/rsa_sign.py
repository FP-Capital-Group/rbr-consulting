#!/usr/bin/env python3
"""Firma RS256 (RSASSA-PKCS1-v1_5 + SHA-256) di un messaggio con una chiave privata PEM.

Serve per i JWT del service account Google negli hook e negli script del plugin.
Prova `openssl` (Mac/Linux); se manca (Windows) usa un'implementazione in puro Python
(solo libreria standard): parser DER minimo per PKCS#8 / PKCS#1 + esponenziazione modulare.
"""
import base64, hashlib, os, re, subprocess, tempfile

_SHA256_DIGESTINFO = bytes.fromhex("3031300d060960864801650304020105000420")


def _der_read(buf, pos):
    """Legge un elemento TLV DER: ritorna (tag, contenuto, posizione successiva)."""
    tag = buf[pos]; pos += 1
    ln = buf[pos]; pos += 1
    if ln & 0x80:
        n = ln & 0x7F
        ln = int.from_bytes(buf[pos:pos + n], "big"); pos += n
    return tag, buf[pos:pos + ln], pos + ln


def _der_seq(content):
    out, pos = [], 0
    while pos < len(content):
        tag, val, pos = _der_read(content, pos)
        out.append((tag, val))
    return out


def _rsa_key(pem):
    body = re.sub(r"-----[^-]+-----|\s", "", pem)
    der = base64.b64decode(body)
    tag, content, _ = _der_read(der, 0)
    items = _der_seq(content)
    if "BEGIN RSA PRIVATE KEY" not in pem and len(items) >= 3 and items[2][0] == 0x04:
        # PKCS#8: PrivateKeyInfo → privateKey OCTET STRING contiene RSAPrivateKey
        tag, content, _ = _der_read(items[2][1], 0)
        items = _der_seq(content)
    ints = [int.from_bytes(v, "big") for t, v in items if t == 0x02]
    # version, n, e, d, p, q, dp, dq, qinv
    n, e, d = ints[1], ints[2], ints[3]
    p, q, dp, dq, qinv = (ints[4:9] + [None] * 5)[:5] if len(ints) >= 9 else (None,) * 5
    return n, e, d, p, q, dp, dq, qinv


def _sign_python(pem, msg):
    n, e, d, p, q, dp, dq, qinv = _rsa_key(pem)
    k = (n.bit_length() + 7) // 8
    t = _SHA256_DIGESTINFO + hashlib.sha256(msg).digest()
    em = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    m = int.from_bytes(em, "big")
    if p and q and dp and dq and qinv:  # CRT: ~4x più veloce
        m1 = pow(m, dp, p); m2 = pow(m, dq, q)
        h = (qinv * (m1 - m2)) % p
        s = m2 + h * q
    else:
        s = pow(m, d, n)
    return s.to_bytes(k, "big")


def sign(pem, msg):
    """Firma `msg` (bytes) con la chiave PEM (str). Ritorna la firma (bytes)."""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
            os.chmod(f.name, 0o600); f.write(pem); path = f.name
        try:
            r = subprocess.run(["openssl", "dgst", "-sha256", "-sign", path], input=msg,
                               capture_output=True, timeout=10)
            if r.returncode == 0 and r.stdout:
                return r.stdout
        finally:
            os.unlink(path)
    except Exception:
        pass
    return _sign_python(pem, msg)
