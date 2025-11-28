# BRC-8888 — Developer Scripts

This directory (`scripts/`) contains **official reference tooling** for preparing BRC-8888 `evolve` inscriptions and AI demos. All scripts are pure Python (no external deps), deterministic, and production-ready.

**Requirements**  
- Python 3.10+  
- Repo structure intact (scripts must be siblings with `merkle_root.py`)

Run from repo root:  
```bash
python3 scripts/<script>.py ...

1. merkle_root.py — Compute Merkle Root
Deterministic SHA-256 Merkle root from a directory of proof files (non-recursive, lexicographic order).
Output: sha256:<64hex> (BRC-8888 standard) or full JSON metadata.

Usage

# Simple hex
python3 scripts/merkle_root.py proof_package/

# Full JSON
python3 scripts/merkle_root.py proof_package/ --json

Perfect for: Anchoring evolution bundles (state.json, traits.json, etc.).

2. package_evolve.py — Generate Evolve Template

Computes Merkle root → builds ready-to-sign evolve_<TICK>_<timestamp>.json template.
Features

Calls merkle_root.py automatically
Customizable trigger, proof URI, fee address
Clear next-step instructions (IPFS upload + PQ signing)

Usage

python3 scripts/package_evolve.py proof_package/ <ref_inscription_id> <TICK> \
  --proof-uri "ipfs://QmYourCID" \
  --trigger '{"type":"transfer","txid":"abc123...","details":{"from":"bc1p...","qty":"500"}}'

Output: Timestamped JSON with correct merkle_root, placeholders for sig_pq, and full fees block.
Next steps printed:

Upload bundle → update proof_uri
Generate PQ signature → replace sig_pq
Inscribe (add 1% fee output)

3. ai_trait_gen.py — AI Evolvable Trait Demo
Deterministic trait generator for u-ai objects and Phase 2 perks.
Uses SHA-256-hashed seed → reproducible across runs and indexers.
Usage

python3 scripts/ai_trait_gen.py "my_seed_123" --num-traits 5 --output json

Ideal for populating traits.json in evolve bundles.

Full Evolve Workflow (5 Minutes)

# 1. Prepare bundle
mkdir proof_package && cp state.json traits.json provenance.json proof_package/

# 2. Generate traits (optional)
python3 scripts/ai_trait_gen.py "txid123" --num-traits 4 > proof_package/traits.json

# 3. Compute root (preview)
python3 scripts/merkle_root.py proof_package/

# 4. Package evolve JSON
python3 scripts/package_evolve.py proof_package/ 68bc98...d84ei0 UNQ \
  --proof-uri "ipfs://QmYourCID" \
  --trigger '{"type":"time","block":925500}'

# 5. Upload bundle → update proof_uri
# 6. Generate PQ sig → replace sig_pq
# 7. Inscribe via UniSat/Gamma (add 1% fee output)

You now have a fully valid, quantum-secure evolution.
These scripts are production-grade — used in the official UNQ launch.
No changes needed. Keep them exactly as they are.
Push and ship.
BRC-8888 tooling is complete.
