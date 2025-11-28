# BRC-8888 Specification (v1)
**Protocol ID:** brc8888-1  
**Genesis Inscription:** https://ordinals.com/inscription/111675299  
**Date:** November 26, 2025  
**Author:** Niseta Sigosi  
**License:** MIT

## Summary
BRC-8888 is a Bitcoin-native protocol for **stateful, evolving, AI-aware, and post-quantum-secure digital objects**. It defines a universal object layer on top of Ordinals inscriptions, supporting fungible tokens, NFTs, semi-fungibles, AI agents, quantum identities, and generic objects — with Merkle-anchored `evolve` operations for verifiable state transitions.

No consensus changes. No sidechains. Everything enforced via deterministic indexers.

Genesis object: **UNQ** — 21,000,000 fixed supply, 8 decimals, fair-launch with phased minting (Phase 1: 0–10M at 2100 sats; Phase 2: 10M+ at 4200 sats + AI perks), founder 1M vested/locked, and mandatory 1% protocol fee on every transaction.

## Goals
- Unified extensible object model on Bitcoin  
- Verifiable off-chain AI/compute via Merkle proofs  
- Post-quantum security from day one  
- Sustainable economics via enforced 1% fee  
- Fair-launch mechanics (caps, phases, vesting, locks)

## Canonical JSON Schema (High Level)
All fields are strings unless noted. Parsers must ignore unknown keys.

```json
{
  "p": "brc8888-1",
  "v": "1",
  "op": "deploy|mint|transfer|evolve",
  "tick": "string",                    // 3–12 uppercase alphanumeric
  "genesis": true|false,               // deploy only
  "otype": "u-token|u-nft|u-sft|u-ai|u-qid|u-object",
  "supply": "integer_string",          // deploy only
  "decimals": integer,                 // optional, default 0
  "qty": "integer_string",             // mint/transfer
  "minter": "bc1p...",                 // mint only, optional override
  "from": "bc1p...", "to": "bc1p...",  // transfer only
  "ref": "inscription_id",             // evolve only

  "mint_rules": {                      // deploy only
    "user_cap": "integer_string",
    "exempt_addrs": [ /* founder exemptions */ ],
    "cooldown_blocks": integer,
    "phases": [ { "start_minted": "...", "end_minted": "...", "price_sats": integer, "perks": "string" } ]
  },

  "ai": { "enabled": true|false, "model_id": "...", "model_hash": "sha256:...", "dynamic_traits": true|false },
  "quantum": { "post_quantum_secure": true|false, "identity_pub": "pq:<scheme>:<BASE64>", "algorithm": "dilithium3" },

  "merkle_root": "sha256:<64hex>",     // evolve only
  "proof_uri": "ipfs://...|ar://...",  // evolve only
  "sig_pq": "BASE64_SIGNATURE",        // evolve only
  "trigger": { ... },                  // evolve only

  "fees": {
    "fee_type": "onchain_output",
    "protocol_fee_percent": 1,
    "fee_address": "bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0",
    "fee_scope": "per_tx",
    "deploy_creation_fee_sats": integer,   // non-genesis deploy only
    "creator_fee_address": "bc1p..."
  },

  "meta": { "name": "...", "description": "...", "uri": "...", "tokenomics": "...", "timestamp": "ISO8601", "created_by": "..." }
}

**Object Types**

Type,Description,Typical Use Cases
u-token,Fungible with decimals,"Tokens, governance (UNQ)"
u-nft,Unique (supply=1),"Collectibles, credentials"
u-sft,Batch semi-fungibles,"Game items, editions"
u-ai,AI-provenanced with dynamic traits,"Generative agents, evolving art"
u-qid,Post-quantum identity,"Secure credentials, reputation"
u-object,Generic extensible (default for UNQ),Custom hybrids

**Operations**

op,Purpose,Key Enforcement Points
deploy,Register object class,"Tick uniqueness, fee outputs, valid rules"
mint,Emit units,"Supply cap, user cap, cooldown, phase price, vesting/lock, 1% fee"
transfer,Move balance,"Sufficient balance, respect locks, 1% fee"
evolve,Update state immutably,"Valid PQ sig, Merkle proof, trigger, 1% fee"

**Evolution Model**

merkle_root: SHA-256 root of off-chain bundle (state.json, traits.json, etc.)
proof_uri: IPFS/Arweave archive containing full files + Merkle proofs
sig_pq: Post-quantum signature over canonical (ref || merkle_root || trigger)
Indexers must recompute root and verify signature + trigger before accepting

**Mandatory Fee Enforcement**

Every valid transaction must contain an output to the protocol treasury (bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0) of ≥1% of the transaction value (or phased cost for mints).
Non-genesis deploy: additional 10,000 sats to creator_fee_address.
Indexers reject inscriptions without correct outputs.

**Post-Quantum Identity**

quantum.identity_pub: pq:dilithium:<BASE64> or pq:falcon:<BASE64>
sig_pq required for evolve if post_quantum_secure: true
Indexers must verify using liboqs or equivalent

**AI Provenance**

ai.model_hash and ai.model_id for deterministic trait generation
Optional attestation signatures in proof bundle
Enables reproducible AI traits and provenance badges

**Indexer Requirements**

Deterministic validation (see deploy_ledger_validation.py)
Enforce exact fee outputs, caps, cooldowns, vesting, locks, phase pricing
Verify Merkle proofs and PQ signatures for evolve
Publish /state/{tick}, /events/{tick}, and simulation endpoints

**Genesis Token UNQ**

Tick: UNQ
Supply: 21,000,000 (8 decimals)
Phase 1: 0–10,000,000 @ 2100 sats
Phase 2: 10,000,001–21,000,000 @ 4200 sats + AI perks
Founder: 1M vested (90-day cliff + 12-month linear), locked until ≥20M public minted
1% protocol fee on every transaction → treasury

**Security & Best Practices**

Air-gapped PQ key generation
Canonical JSON (sorted keys, no whitespace) for signing
Multi-pin archives (IPFS + Arweave)
Simulate every inscription before broadcasting

BRC-8888 — Bitcoin objects that live, evolve, and survive the quantum era.

