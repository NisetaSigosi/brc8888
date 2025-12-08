# BRC-8888 — Universal Object Protocol

**Post-Quantum Evolvable Objects on Bitcoin Ordinals**  
**v1.1 Slim — UTXO-Optimized (100–150 byte payloads)**

[![v1.1 Slim](https://img.shields.io/badge/version-1.1%20Slim-blue?style=flat-square)](#) [![MIT License](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](#)

> Creator: **Niseta Sigosi** (pseudonymous)  
> Genesis Inscription: [`111675299`](https://ordinals.com/inscription/111675299)  
> Launched: December 2025

---

### What is BRC-8888?

Bitcoin-native protocol for **stateful, evolving, AI-aware, post-quantum-secure digital objects** built directly on Ordinals inscriptions.

- No sidechains
- No consensus changes
- 100% inscription + deterministic indexer enforcement

**v1.1 Slim** brings:
- Dynamic address derivation from deploy TX (saves ~80 bytes)
- Optional fields + hex encoding
- Payloads reduced to **100–150 bytes** (vs 224+ in v1.0)
- Indexer & UTXO-friendly — no BRC-20 added 85M UTXOs since 2022; BRC-8888 fights bloat

---

### Genesis Object — UNQ (Quantum Edge)

| Property              | Value                                 |
|-----------------------|---------------------------------------|
| Ticker                | UNQ                                   |
| Total Supply          | 21,000,000 (8 decimals)               |
| Phase 1 (0–10M)       | 2100 sats/unit                        |
| Phase 2 (10M+)        | 4200 sats/unit + AI trait unlocks     |
| Founder Allocation    | 1,000,000 — vested & locked           |
| Protocol Fee          | 1% on every mint/transfer/evolve      |

No presale. No VC. Pure fair launch.

---

### Key Features

| Feature                     | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Evolvable State             | Merkle-root commits + Dilithium3 PQ signatures                              |
| Unlimited On-Chain Evolution| Traits, vesting, game state, AI provenance — update forever                 |
| Universal Object Types      | `u-token` · `u-nft` · `u-sft` · `u-ai` · `u-qid` · `u-object`               |
| Phased Minting + Perks      | Real FOMO mechanics without sniping                                         |
| Mandatory 1% Treasury       | Sustainable funding — enforced by indexers                                  |
| Anti-Snipe Tools            | User caps, cooldowns, founder vesting/locks                                 |
| Post-Quantum Security       | Dilithium3 (NIST PQC) from day one                                          |

---

### v1.1 Slim — Indexer-Friendly by Design

- Addresses derived from deploy TX outputs  
- Optional fields (AI, quantum, proof_uri)  
- Hex encoding for hashes  
- Minimal meta (`ts` instead of ISO string)  
- Payloads ~40–60% smaller than v1.0

→ **Indexers love this** — less data, faster sync, lower UTXO impact.

---

### Quick Links

- Live Inscription Tool → https://nisetasigosi.github.io/brc-8888/
- Full Specification (v1.1 Slim) → [brc8888-spec-v1.1-slim.md](spec/brc8888-spec-v1.1-slim.md)
- Reference Indexer (Python) → [deploy_ledger_validation_v1.1_slim.py](scripts/deploy_ledger_validation_v1.1_slim.py)
- Repo → https://github.com/NisetaSigosi/brc8888

---

### Indexer Bounty (First Movers)

First **3 independent indexers** who ship BRC-8888 support receive:

- 0.5% lifetime share of the 1% protocol treasury (paid on-chain, no KYC)
- 100,000 UNQ grant

Just fork the v1.1-slim branch and ship — the treasury pays you forever.

---

### Treasury & Reserve (Live on-chain)

- Treasury (1% fees):  
  `bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0`
- Reserve (mint payments):  
  `bc1p8px4vg2c4w79smuwts8s49xxzt6r8mlk9nyyf3jxa767flyhdres0xkz5c`

---

**BRC-8888 — Bitcoin objects that live, evolve, and survive the quantum era.**  
**v1.1 Slim — leaner, faster, indexer-ready.**

Pseudonymous. Community-driven.  
Let’s evolve Bitcoin together.

#BRC8888 #UNQ #QuantumEdge #Ordinals #Bitcoin #PostQuantum
