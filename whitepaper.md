# BRC-8888 — Whitepaper (v1.0)

**Author:** Niseta Sigosi  
**Launch Date:** November 26, 2025  
**Genesis Inscription:** https://ordinals.com/inscription/111675299  
**License:** MIT (Open-Source)

---

## Abstract

BRC-8888 is the first Bitcoin-native protocol for **stateful, evolving, AI-aware, and post-quantum-secure digital objects**. Built entirely on Ordinals inscriptions, it introduces a universal object model and the `evolve` primitive — enabling fungible tokens, NFTs, AI agents, quantum identities, and arbitrary hybrids to live and adapt on-chain.

No consensus changes. No sidechains. No trusted third parties.

The genesis object **UNQ** (21,000,000 fixed supply, 8 decimals) is live on Bitcoin mainnet as of November 26, 2025. It features:
- Fair launch with 10,000 per-wallet cap
- Founder 1,000,000 tokens (90-day cliff + 12-month linear vesting, locked until ≥20M public minted)
- Two-phase fixed-price minting:
  - Phase 1 (0–10,000,000): **2100 sats per UNQ**
  - Phase 2 (10,000,001–21,000,000): **4200 sats per UNQ** + AI trait unlocks
- Mandatory 1% protocol fee on every transaction → treasury

BRC-8888 turns Bitcoin from a static ledger into a canvas for **living, intelligent, future-proof assets**.

---

## 1. The Problem

Current Bitcoin standards are powerful but limited:

| Standard     | Strength                     | Critical Limitation                         |
|--------------|------------------------------|---------------------------------------------|
| BRC-20       | Simple fungibles             | Static, no evolution, no NFTs               |
| Ordinals     | Rich immutable data          | No state transitions                        |
| Runes        | Efficient fungibles          | No AI, no PQ, no evolutions                 |

Result: Developers must juggle multiple protocols. AI-generated art, adaptive game items, and quantum-secure identities remain impossible on Bitcoin.

---

## 2. BRC-8888 — The Solution

A single, extensible protocol for **all digital objects**:

| Object Type   | Description                         | Example Use Case                     |
|---------------|-------------------------------------|--------------------------------------|
| `u-token`     | Fungible (decimals, supply)         | Governance, utility tokens (UNQ)     |
| `u-nft`       | Unique (supply=1)                   | Collectibles, credentials            |
| `u-sft`       | Semi-fungible batches               | Game items, editions                 |
| `u-ai`        | AI-provenanced + dynamic traits     | Evolving agents, generative art      |
| `u-qid`       | Post-quantum identities             | Future-proof wallets, reputations    |
| `u-object`    | Generic (UNQ default)               | Custom hybrids                       |

### The `evolve` Primitive

The breakthrough: objects can **change state immutably**.

- Anchor off-chain bundle via SHA256 Merkle root
- Prove integrity with IPFS/Arweave URI
- Authorize with **post-quantum signature** (Dilithium3/Falcon)
- Trigger via transfer, time, or oracle

Unlimited evolutions. Fully verifiable. No forks.

---

## 3. Economic Model — Sustainable & Fair

| Operation           | Required Output                                          |
|---------------------|----------------------------------------------------------|
| Deploy (non-genesis)| ≥10,000 sats → creator + 1% → treasury                  |
| Mint (public)       | Exact phased cost → reserve + **1% of cost → treasury**  |
| Mint (exempt)       | Dust only (founder exemption)                            |
| Transfer / Evolve   | **1% of transferred value → treasury**                  |

Treasury address (immutable):  
`bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0`

All fees **indexer-enforced** — no opt-out, no central control.

---

## 4. UNQ — The Genesis Object

- **Supply:** 21,000,000 (8 decimals)  
- **Fair Launch:** 10,000 per wallet, 144-block cooldown  
- **Founder:** 1,000,000 tokens (locked until 20M public minted, vested over 15 months)  
- **Phased Minting:**
  - Phase 1 (0–10M): **2100 sats per UNQ**
  - Phase 2 (10M+): **4200 sats per UNQ** + AI trait unlocks
- **Role:** Governance token, ecosystem fuel, AI/PQ testbed

UNQ is live. Phase 1 is open. Rush now.

---

## 5. Security — Built for the Long Term

| Threat                  | Protection                                          |
|-------------------------|-----------------------------------------------------|
| Quantum attacks         | Dilithium3/Falcon signatures (NIST 2024)           |
| State tampering         | Merkle roots + on-chain anchoring                   |
| Fee skipping            | Indexers reject invalid outputs                     |
| Indexer bugs            | Deterministic reference impl + multi-indexer sync   |
| Archive loss            | Multi-pin (IPFS + Arweave) + public redundancy      |

Full details: [security.md](security.md)

---

## 6. Launch Status — November 26, 2025

**The protocol is live.**  
Genesis inscription: https://ordinals.com/inscription/111675299  
Reference implementation: https://github.com/NisetaSigosi/brc8888  

Next:  
- Early indexers claim 0.5% lifetime fee share + 100k UNQ  
- Wallets integrate BRC-8888 balances and evolutions  
- Phase 1 minting begins

---

## 7. Conclusion

BRC-8888 is not another token standard.

It is **the evolution of Bitcoin itself** — turning immutable inscriptions into living, intelligent, quantum-secure objects.

The code is open.  
The treasury is filling.  
The future starts with your inscription.

**Deploy. Evolve. Survive.**

GitHub: https://github.com/NisetaSigosi/brc8888  
X: #BRC8888  

**Bitcoin was just the beginning.**
