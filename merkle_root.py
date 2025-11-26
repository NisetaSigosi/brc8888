#!/usr/bin/env python3
"""
Compute a deterministic Merkle root from all files inside a directory.
For BRC-8888: Anchors evolution bundles (e.g., state.json, traits.json, provenance.json).
- Files processed in lexicographic order for reproducibility.
- Large files hashed in streaming mode (chunked).
- Fixed to SHA256 (protocol requirement); outputs prefixed "sha256:<hex>".
- Exits with non-zero status on error.
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from typing import List

CHUNK_SIZE = 4 * 1024 * 1024  # 4 MiB


def file_hash(path: str) -> str:
    """Return hex digest of file hashed in streaming chunks (SHA256)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def merkle_parent(a_hex: str, b_hex: str) -> str:
    """Compute parent node by hashing concatenation of two hex leaf strings (SHA256)."""
    a = bytes.fromhex(a_hex)
    b = bytes.fromhex(b_hex)
    h = hashlib.sha256()
    h.update(a + b)
    return h.hexdigest()


def merkle_root_from_leaves(leaves: List[str]) -> str:
    """Compute Merkle root (hex) from list of hex digests. Leaves must be hex strings."""
    if not leaves:
        raise ValueError("No leaves provided to compute Merkle root.")

    cur = leaves[:]
    while len(cur) > 1:
        if len(cur) % 2 == 1:
            cur.append(cur[-1])  # Duplicate last for even pairing
        next_level: List[str] = []
        for i in range(0, len(cur), 2):
            next_level.append(merkle_parent(cur[i], cur[i + 1]))
        cur = next_level
    return cur[0]


def find_files(directory: str) -> List[str]:
    """Return lexicographically sorted regular files in the directory (non-recursive)."""
    try:
        entries = sorted(
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory not found: {directory}")
    return entries


def format_merkle_root(root_hex: str) -> str:
    """Format root as 'sha256:<hex>' for BRC-8888 compliance."""
    return f"sha256:{root_hex}"


def main() -> int:
    p = argparse.ArgumentParser(description="Deterministic Merkle root from BRC-8888 evolution bundle directory.")
    p.add_argument("directory", help="Directory containing bundle files (e.g., state.json, traits.json; non-recursive).")
    p.add_argument("--json", action="store_true", help="Output JSON object instead of prefixed hex.")
    args = p.parse_args()

    try:
        files = find_files(args.directory)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    if not files:
        print("Error: Directory contains no files.", file=sys.stderr)
        return 3

    leaves: List[str] = []
    for fn in files:
        path = os.path.join(args.directory, fn)
        try:
            digest = file_hash(path)
        except (IOError, OSError) as e:
            print(f"Error hashing {path}: {e}", file=sys.stderr)
            return 4
        leaves.append(digest)

    try:
        root_hex = merkle_root_from_leaves(leaves)
        root_formatted = format_merkle_root(root_hex)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 5

    if args.json:
        out = {
            "directory": args.directory,
            "files": files,
            "algorithm": "sha256",
            "merkle_root": root_formatted
        }
        print(json.dumps(out, indent=2))
    else:
        print(root_formatted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
}
