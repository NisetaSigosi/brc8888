# Security Considerations — BRC-8888 (v1)

**Last Updated:** November 26, 2025  
**Genesis Inscription:** https://ordinals.com/inscription/111675299

BRC-8888 is designed for maximum security and future-proofing on Bitcoin. All critical guarantees are enforced by deterministic indexers, post-quantum signatures, and Merkle-anchored proofs — no trust in any central party.

---

## 1. Post-Quantum (PQ) Security

Evolutions and high-value operations are protected against future quantum attacks.

| Feature               | Details                                                                                           |
|-----------------------|---------------------------------------------------------------------------------------------------|
| Supported Algorithms  | Dilithium3 (recommended), Falcon-1024                                                             |
| Key Format            | `pq:dilithium:<BASE64_PUBKEY>` or `pq:falcon:<BASE64_PUBKEY>`                                     |
| Signature Field       | `sig_pq` — signs canonical `(ref_inscription_id || merkle_root || trigger)`                      |
| Indexer Enforcement   | **MUST** verify signature using the deployed `identity_pub`. Reject if invalid or non-PQ.       |

**Best Practice:** Generate keys air-gapped. Use `oqs-python` or `liboqs` (see `tools/pq_signing_reference.md`).

---

## 2. Merkle-Anchored State & Proofs

All off-chain data in `evolve` operations is integrity-protected.

| Component           | Protection                                                                 |
|---------------------|----------------------------------------------------------------------------|
| `merkle_root`       | SHA256 tree of sorted, canonical JSON files (state.json, traits.json, etc.) |
| `proof_uri`         | IPFS / Arweave / Sia bundle containing full files + Merkle inclusion proofs |
| Indexer Requirement | Recompute root from fetched archive → reject on mismatch                   |

**Tamper Resistance:** Any change to the archive breaks the Merkle root → future evolutions impossible.

**Recommended Storage:** Multi-pin on IPFS + Arweave mirror.

---

## 3. Mandatory Economic Security (1% Protocol Fee)

No opt-out. Indexers **MUST** reject any transaction missing required outputs.

| Operation            | Required Outputs                                                                 |
|----------------------|----------------------------------------------------------------------------------|
| Deploy (non-genesis) | ≥10,000 sats → creator_fee_address<br>≥1% of creation fee → treasury            |
| Mint (public)        | Exact phased cost → reserve_address<br>≥1% of phased cost → treasury           |
| Mint (exempt)        | Only dust (no phased cost)                                                     |
| Transfer / Evolve    | ≥1% of transferred value → treasury                                            |

Treasury address (immutable):  
`bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0`

---

## 4. Key Threats & Mitigations

| Threat                     | Mitigation                                                                 |
|----------------------------|----------------------------------------------------------------------------|
| Indexer bugs / collusion   | Deterministic reference impl (`deploy_ledger_validation.py`)<br>Run multiple indexers → consensus required |
| Missing fee outputs        | Indexers reject TXs without exact outputs                                 |
| Quantum key compromise     | Mandate PQ signatures for evolves; rotate via new deploy                 |
| Archive tampering          | Merkle root + multi-gateway fetch + public pinning                       |
| Replay attacks             | Payload includes `ref` + `trigger` (e.g., txid) → one-time use            |
| Spam / DoS                 | Minimum fees, cooldowns, user caps, phased pricing                       |

---

## 5. Best Practices

### Deployers
- Generate PQ keys air-gapped  
- Use canonical JSON (sorted keys, no whitespace) for signing  
- Multi-pin archives (IPFS + Arweave)  
- Simulate every inscription with `deploy_ledger_validation.py`

### Indexers
- Verify **every** signature and output  
- Implement fallback gateways and timeouts  
- Sync state with at least one other indexer  
- Publish public API for transparency

### Users
- Query ≥2 indexers before trusting balances  
- Verify Merkle proofs manually when in doubt  
- Use wallets with BRC-8888 support (coming soon)

---

**Security is not optional — it’s enforced by math and incentives.**

Report vulnerabilities: Open a private GitHub issue.  
BRC-8888 — built to survive the quantum era.
