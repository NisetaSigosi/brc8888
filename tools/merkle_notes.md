# Merkle Tree Notes for BRC-8888

These notes define the **canonical Merkle tree construction** used in BRC-8888 `evolve` operations. Indexers **MUST** follow this exactly for deterministic, tamper-proof state anchoring.

Reference implementation: [`merkle_root.py`](https://github.com/NisetaSigosi/brc8888/blob/scripts/scripts/merkle_root.py)

---

## Design Principles
- Deterministic across all platforms  
- Streaming SHA-256 (handles >10 GB files)  
- Lexicographic file ordering (no randomness)  
- Last-leaf duplication for odd counts (no zero-padding)  
- Output format: `sha256:<64-hex>` (exact BRC-8888 requirement)

---

## Tree Construction (Canonical Algorithm)

1. **Leaves**
   - List **regular files only** in the directory (non-recursive)  
   - Sort filenames **lexicographically** (byte comparison)  
   - Hash each file: `SHA256(full_contents)` → 64-hex string  
   - Empty file → `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

2. **Internal Nodes**
   - Pair leaves left-to-right  
   - If odd number → duplicate last leaf  
   - Parent = `SHA256(left_bytes + right_bytes)` → 64-hex  
   - Repeat until single root

3. **Final Output**
   - Prefix with `sha256:` → inscription-ready

**Example (3 files → 4 leaves via duplication):**

leaf0      leaf1      leaf2      leaf2(dupe)
│          │          │          │
└──parent0──┘          └──parent1──┘
│                     │
└───────root──────────┘


---

## Recommended Bundle Structure

```text
proof_package/
├── state.json          # Core object state
├── traits.json         # AI-generated traits (from ai_trait_gen.py)
├── provenance.json     # Model hash, seed, generation proof
├── history.json        # Immutable evolve log
└── media.json          # Optional: IPFS CIDs for visuals

Best Practices

UTF-8 JSON only (canonical formatting)
Upload entire directory to Arweave (permanent) + IPFS (fast)
Always pin with at least two providers

Indexer Verification (MUST Implement)

1. Fetch bundle from proof_uri (timeout 10s, 3 retries, fallback gateways)
2. List + sort files exactly as merkle_root.py
3. Recompute leaves and tree
4. Compare final root → if mismatch → REJECT evolve
5. (Optional) Extract Merkle inclusion proofs for selective disclosure

Edge Cases

Empty directory → sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Missing/corrupt file → reject
Different file order → reject (prevents tampering)

Security Notes

SHA-256 collision resistance: >2¹²⁸ operations
Last-leaf duplication prevents pre-image attacks
Combined with sig_pq over (ref || root || trigger) → fully quantum-resistant
Archive tampering impossible without breaking Merkle root

This is the exact algorithm used in the UNQ genesis launch.
Indexers that deviate will fork from consensus.
