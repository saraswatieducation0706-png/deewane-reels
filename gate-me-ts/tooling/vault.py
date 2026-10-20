#!/usr/bin/env python3
"""Encrypted store for paid GATE ME TS content inside this PUBLIC repo (gate-me-ts/vault/).
Files are AES-256-CBC encrypted (OpenSSL EVP_BytesToKey MD5, no salt — the scheme Make's
"crypto: AES Decrypt (simple)" module uses) and stored base64. Key from env GMTS_KEY; never print it.

  python3 vault.py put <local file> <vault path>     e.g. put out/x.docx TT05/x.docx  -> vault/TT05/x.docx.enc
  python3 vault.py get <vault path> <local file>     e.g. get TT12/TT12.json /tmp/TT12.json
  python3 vault.py ls
Make scenario 8060538 ("GATE ME TS – vault to Drive") turns vault/<path>.enc into the plain file in Drive:
  scenarios_run(8060538, responsive=true, data={"path": "<vault path>.enc", "folder_id": ..., "file_name": ...})
(the path is URL-encoded by Make; avoid '#', '?' and '%' in vault paths)."""
import os, sys, base64, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vault")


def _kv():
    s = os.environ.get("GMTS_KEY", "").strip().encode()
    if not s:
        sys.exit("GMTS_KEY not set")
    d, p = b"", b""
    while len(d) < 48:
        p = hashlib.md5(p + s).digest(); d += p
    return d[:32], d[32:48]


def enc(data):
    k, iv = _kv(); n = 16 - len(data) % 16; data += bytes([n]) * n
    e = Cipher(algorithms.AES(k), modes.CBC(iv)).encryptor()
    return base64.b64encode(e.update(data) + e.finalize())


def dec(b64):
    k, iv = _kv(); d = Cipher(algorithms.AES(k), modes.CBC(iv)).decryptor()
    p = d.update(base64.b64decode(b64)) + d.finalize(); return p[:-p[-1]]


if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    if cmd == "put":
        dst = os.path.join(ROOT, a[1] + ".enc"); os.makedirs(os.path.dirname(dst), exist_ok=True)
        raw = open(a[0], "rb").read(); open(dst, "wb").write(enc(raw))
        assert dec(open(dst, "rb").read()) == raw
        print("OK", os.path.relpath(dst, ROOT))
    elif cmd == "get":
        open(a[1], "wb").write(dec(open(os.path.join(ROOT, a[0] + ".enc"), "rb").read())); print("OK", a[1])
    elif cmd == "ls":
        for r, _, fs in os.walk(ROOT):
            for f in sorted(fs):
                print(os.path.relpath(os.path.join(r, f), ROOT))
