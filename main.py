#!/usr/bin/env python3
"""Publish the Wednesday 25 November 2026 front page (final edition).

The broadsheet ships pre-rendered as entry.png next to this file. This
program copies it to /output/entry.png and proves the copy is intact:
PNG signature, the 1 MiB competition cap, and a SHA-256 match against
the digest recorded below. Python standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DIGEST = "51f42fa6a0b6eda60ef9c5953d2a00aba7c1374b3065b40cff96560e7cab053c"
LIMIT = 1024 * 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def digest_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(65536)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def run():
    target_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    size = os.path.getsize(SOURCE)
    if size > LIMIT:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as fh:
        if fh.read(len(MAGIC)) != MAGIC:
            print("entry.png is not a PNG file", file=sys.stderr)
            return 1
    if digest_of(SOURCE) != DIGEST:
        print("entry.png does not match its recorded SHA-256", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, target)
    if os.path.getsize(target) != size or digest_of(target) != DIGEST:
        print("copied file failed verification", file=sys.stderr)
        return 1
    print(f"wrote {target} ({size} bytes, sha256 {DIGEST[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
