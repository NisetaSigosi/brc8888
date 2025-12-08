# BRC-8888 Specification (v1.1 — Slim Payload Edition)

**Protocol ID:** brc8888-1  
**Version:** 1.1 (Slim Payload Edition)  
**Genesis Inscription:** https://ordinals.com/inscription/111675299  
**Date:** December 8, 2025  
**Author:** Niseta Sigosi  
**License:** MIT  

## Summary
BRC-8888 is a Bitcoin-native protocol for **stateful, evolving, AI-aware, and post-quantum-secure digital objects** built directly on Ordinals inscriptions.

v1.1 Slim introduces **UTXO-friendly optimizations**:
- Addresses derived from deploy TX outputs (save ~80 bytes)
- Optional fields + hex encoding (payloads 100–150 bytes)
- Minimal meta (Unix timestamps, short keys)
- 40–60 % smaller than v1.0 — indexer & blockchain friendly

Genesis object: **UNQ — Quantum Edge**  
21,000,000 supply · 8 decimals · phased minting · 1 % treasury forever

## Goals
- Unified extensible object model on Bitcoin
- Post-quantum security from day one
- Sustainable economics via enforced 1 % fee
- Fair-launch mechanics (caps, phases, vesting, locks)
- **v1.1:** Minimal payloads, dynamic TX reads, zero bloat

## Canonical JSON Schema (v1.1 Slim)
All fields are strings unless noted. Unknown keys ignored.

```json
{
  "p": "brc8888-1",
  "v": "1.1",
  "op": "deploy|mint|transfer|evolve",
  "tick": "UNQ",
  "genesis": true|false,
  "otype": "u-token|u-nft|u-sft|u-ai|u-qid|u-object",
  "supply": "21000000",
  "decimals": 8,
  "qty": "100",
  "minter": "bc1p...",               // optional
  "from": "bc1p...", "to": "bc1p...", // transfer
  "ref": "i111675299...",             // evolve
  "mint_rules": {                     // deploy only
    "user_cap": "10000",
    "cooldown_blocks": 144,
    "phases": [
      {"start":"0","end":"10000000","price":2100,"perks":"base"},
      {"start":"10000001","end":"21000000","price":4200,"perks":"ai"}
    ]
  },
  "ai": {"enabled":true,"model_id":"gpt-q-lite","model_hash":"0xabc...","dynamic_traits":true}, // optional
  "quantum": {"secure":true,"pub":"pq:dilithium:BASE64..."}, // optional
  "merkle": "0xdeadbeef...",          // evolve only (hex root)
  "uri": "ipfs://Qm...",              // evolve only (optional)
  "sig": "BASE64",                    // evolve only
  "trigger": {"type":"time","block":925000}, // evolve only
  "fees": {"type":"tx_output","pct":1}, // addresses derived from deploy TX
  "meta": {"name":"UNQ","ts":1736200000} // minimal
}

v1.1 Slim Optimizations

Change,Bytes Saved,Reason
Addresses from deploy TX,~80,"Dynamic read (output 1 = reserve, output 2 = treasury)"
Hashes as hex (0x...),~20,"vs ""sha256:..."""
Unix timestamps,~15,vs ISO string
Optional AI/quantum/uri,~100,skip when not needed
Minimal meta,~30,only essential

Object Types

Type,Description
u-token,Fungible (UNQ default)
u-nft,Unique (supply=1)
u-sft,Semi-fungible
u-ai,AI-aware (model_hash + traits)
u-qid,PQ identity
u-object,Generic (fallback)

Operations

op,Key Enforcement Points
deploy,"Tick uniqueness, valid rules, correct TX outputs"
mint,"Supply/user cap, cooldown, phase price, 1% fee"
transfer,"Balance ≥ qty, respect locks, 1% fee"
evolve,"Valid PQ sig, Merkle proof, trigger, 1% fee"

Mandatory Fee Enforcement

1 % of value to treasury (derived from deploy TX output 2)
Non-genesis deploy: 10 000 sats to creator_fee_address (output 3)
Indexers reject without correct outputs

Post-Quantum Identity (Slim)

quantum.pub optional: pq:dilithium:BASE64
sig required for evolve if quantum.secure: true

Indexer Requirements (Slim)

Derive addresses from deploy TX (mempool.space API)
Skip optional fields when absent
Reference implementation: deploy_ledger_validation_v1.1_slim.py

Genesis Token: UNQ — Quantum Edge

Tick: UNQ
Supply: 21,000,000 (8 decimals)
Phase 1: 0–10,000,000 @ 2100 sats
Phase 2: 10,000,001–21,000,000 @ 4200 sats + AI traits
Founder: 1M vested (90-day cliff + 12-mo linear), locked until ≥20M public minted
1% protocol fee on every transaction → treasury

BRC-8888 v1.1 Slim — leaner, faster, indexer-ready.
Same power. Zero bloat. Ready for Bitcoin.
