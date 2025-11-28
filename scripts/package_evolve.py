#!/usr/bin/env python3
"""
Package evolve proof files for BRC-8888.

Usage:
  python3 scripts/package_evolve.py <proof_dir> <ref_inscription_id> <tick> [--proof-uri IPFS_URI] [--fee-address ADDR] [--protocol-fee-sats N] [--trigger TRIGGER_JSON]

Computes the Merkle root (via scripts/merkle_root.py) and writes an evolve_<TICK>_<timestamp>.json template.
Assumes proof_dir contains bundle files (e.g., state.json, traits.json, provenance.json) in lex order.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from datetime import datetime
from subprocess import run, PIPE
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else "."
PROTOCOL_FEE_PERCENT_DEFAULT = 1  # BRC-8888 standard fee percent for evolves


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Package evolve proof directory into a BRC-8888 evolve JSON template.")
    p.add_argument("proof_dir", help="Directory containing proof bundle files (non-recursive; e.g., state.json, traits.json).")
    p.add_argument("ref_inscription", help="Inscription ID of deploy or last evolve (ref).")
    p.add_argument("tick", help="Ticker (e.g., UNQ).")
    p.add_argument("--proof-uri", default="ipfs://QmREPLACE_WITH_ACTUAL_CID", help="URI for proof archive (IPFS/Arweave).")
    p.add_argument("--fee-address", default="bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0", help="Protocol fee address (default: treasury).")
    p.add_argument("--protocol-fee-percent", type=int, default=PROTOCOL_FEE_PERCENT_DEFAULT, help="Protocol fee percent (default: 1).")
    p.add_argument(
        "--trigger",
        type=str,
        default='{"type": "time", "block": 0}',
        help="Trigger JSON as string (e.g., '{\"type\":\"transfer\",\"txid\":\"abcd...\",\"details\":{\"from\":\"bc1p...\",\"to\":\"bc1p...\",\"qty\":\"100\"}}')."
    )
    return p.parse_args()


def compute_merkle_root(proof_dir: str) -> str:
    """Compute and return hex Merkle root (sans 'sha256:' prefix) via merkle_root.py."""
    merkle_script = os.path.join(SCRIPT_DIR, "scripts", "merkle_root.py")
    if not os.path.isfile(merkle_script):
        raise FileNotFoundError(f"merkle_root.py not found: {merkle_script}")
    
    proc = run(["python3", merkle_script, proof_dir], stdout=PIPE, stderr=PIPE, text=True, check=True)
    if proc.returncode != 0:
        raise RuntimeError(f"merkle_root.py failed:\n{proc.stderr.strip()}")
    
    # Parse output: Expect "sha256:<hex>" or JSON with "merkle_root": "sha256:<hex>"
    out = proc.stdout.strip()
    root_match = re.search(r'sha256:([0-9a-fA-F]{64})', out)
    if not root_match:
        raise ValueError(f"Invalid Merkle root in output: {out!r}")
    
    return root_match.group(1)  # Return pure hex


def parse_trigger(trigger_str: str) -> Dict[str, Any]:
    """Parse trigger string to JSON dict; fallback to basic dict if invalid."""
    try:
        return json.loads(trigger_str)
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid trigger JSON '{trigger_str}'; using as type fallback. ({e})", file=sys.stderr)
        return {"type": trigger_str}


def build_evolve_json(args: argparse.Namespace, merkle_hex: str) -> Dict[str, Any]:
    """Build BRC-8888 evolve inscription JSON template."""
    trigger = parse_trigger(args.trigger)
    
    evolve: Dict[str, Any] = {
        "p": "brc8888-1",
        "v": "1",
        "op": "evolve",
        "ref": args.ref_inscription,
        "tick": args.tick,
        "merkle_root": f"sha256:{merkle_hex}",
        "proof_uri": args.proof_uri,
        "sig_pq": "BASE64_PQ_SIGNATURE",  # Placeholder: Generate via PQ lib (e.g., Dilithium3)
        "trigger": trigger,
        "fees": {
            "fee_type": "onchain_output",
            "protocol_fee_percent": args.protocol_fee_percent,
            "fee_address": args.fee_address,
            "fee_scope": "per_tx",
            "note": "Indexers require on-chain output >= protocol_fee_percent of tx value to fee_address in same TX."
        },
        "meta": {
            "version": "1",
            "purpose": "State evolution via Merkle-anchored proof (update traits/provenance).",
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "created_by": "EvolveAuthorPlaceholder"
        }
    }
    return evolve


def main() -> int:
    args = parse_args()
    
    if not os.path.isdir(args.proof_dir):
        print(f"Error: '{args.proof_dir}' is not a directory.", file=sys.stderr)
        return 2
    
    try:
        merkle_hex = compute_merkle_root(args.proof_dir)
        print(f"Computed Merkle root (hex): {merkle_hex}", file=sys.stderr)  # Log for user
    except Exception as e:
        print(f"Error computing Merkle root: {e}", file=sys.stderr)
        return 3
    
    evolve = build_evolve_json(args, merkle_hex)
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ").replace(":", "").replace("-", "")
    filename = f"evolve_{args.tick}_{timestamp}.json"
    out_path = os.path.join(os.getcwd(), filename)
    
    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(evolve, fh, indent=2, ensure_ascii=False)
        print(f"Wrote BRC-8888 evolve template: {out_path}")
        print(f"Next steps:\n- Upload proof_dir to IPFS/Arweave; update 'proof_uri'.\n- Generate PQ sig for payload; replace 'sig_pq'.\n- Inscribe via wallet (include fee output).", file=sys.stderr)
    except Exception as e:
        print(f"Error writing JSON: {e}", file=sys.stderr)
        return 4
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
}
