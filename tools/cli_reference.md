# BRC-8888 — CLI Reference

Official command-line tools in `scripts/`. All pure Python 3 (no external dependencies), fully deterministic, and production-ready.

Run from repository root:  
```bash
python3 scripts/<script>.py ...

1. merkle_root.py — Compute Merkle Root
Purpose: Deterministic SHA-256 Merkle root from all files in a directory (lexicographic order, streaming). Required for evolve anchoring.

python3 scripts/merkle_root.py <directory> [--json]

Output examples

sha256:3f2a9bdeadbeef00000000000000000000000000000000000000000000000000

{
  "directory": "proof_package/",
  "files": ["provenance.json", "state.json", "traits.json"],
  "algorithm": "sha256",
  "merkle_root": "sha256:3f2a..."
}

2. package_evolve.py — Generate Evolve Template

Purpose: Full evolve JSON template with auto-computed Merkle root, timestamp, and correct treasury address.

python3 scripts/package_evolve.py <proof_dir> <ref_inscription_id> <tick> \
  [--proof-uri URI] \
  [--trigger JSON_STRING]

Real treasury address used by default
bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0

Example

python3 scripts/package_evolve.py proof_package/ 68bc98...d84ei0 UNQ \
  --proof-uri "ipfs://QmYourCID" \
  --trigger '{"type":"transfer","txid":"abc123...","details":{"qty":"500"}'

Creates evolve_UNQ_20251126T183000Z.json with correct merkle_root, sig_pq placeholder, and 1% fee block.

3. ai_trait_gen.py — Generate AI Traits

Purpose: Deterministic trait generation for u-ai objects and Phase 2 perks.

python3 scripts/ai_trait_gen.py <seed> [--num-traits N] [--output json|text]

Example

python3 scripts/ai_trait_gen.py "phase2_unlock_tx123" --num-traits 5 --output json

Perfect for populating traits.json in evolve bundles.

Full Evolve Workflow (5 Minutes)

# 1. Generate traits
python3 scripts/ai_trait_gen.py "evolve123" --num-traits 5 > proof_package/traits.json

# 2. Compute root
python3 scripts/merkle_root.py proof_package/

# 3. Package evolve JSON
python3 scripts/package_evolve.py proof_package/ <ref_id> UNQ \
  --proof-uri "ipfs://QmYourCID"

# 4. Upload bundle → update proof_uri
# 5. Generate Dilithium3 signature → replace sig_pq
# 6. Inscribe (add 1% fee output)

These tools are used in the official UNQ launch.
