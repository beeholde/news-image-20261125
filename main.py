#!/usr/bin/env python3
"""Write the pre-rendered front page for Wednesday 25 November 2026.

The image is baked into this repository as entry.png; this program only
copies it to /output/entry.png, then verifies the copy byte-for-byte
against the recorded SHA-256 and enforces the competition's 1 MiB cap.
Standard library only: hashlib, os, shutil, sys.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
EXPECTED_SHA256 = "d81a4d41d2edcd652e620106a898ed9fb77dac2c1775d8975b5669b1248ce68c"
MAX_BYTES = 1 * 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as handle:
        if handle.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            print("entry.png is not a PNG file", file=sys.stderr)
            return 1
    if sha256_file(SOURCE) != EXPECTED_SHA256:
        print("entry.png does not match its recorded SHA-256", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, dest)
    if os.path.getsize(dest) != size or sha256_file(dest) != EXPECTED_SHA256:
        print("copied file failed verification", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({size} bytes, sha256 {EXPECTED_SHA256[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
