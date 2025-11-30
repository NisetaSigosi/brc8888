# 🌐 BRC-8888 — Universal Object Protocol (v1)

**Creator of BRC-8888: Niseta Sigosi**

BRC-8888 is a Bitcoin-native protocol for **stateful, evolving, AI-aware, and post-quantum-ready digital objects**. It standardizes a universal layer atop Ordinals—supporting fungibles, NFTs, semi-fungibles, AI agents, PQ identities, and generics—while introducing Merkle-anchored `evolve` ops for dynamic state transitions. All enforced via inscriptions and indexers: No consensus changes, no sidechains.

Genesis object: **UNQ** — 21M fixed supply, 8 decimals; fair-launch with 10K user caps, founder exemption (1M tokens, vested/locked, no mint fees for founder), and phased fixed-price minting (Phase 1: First 10M at 2100 sats; Phase 2: Next 11M at 4200 sats with AI perk unlocks) to build urgency and FOMO.

**Live on Bitcoin:** Deploy UNQ via [unq_deploy_mainnet.json](https://github.com/NisetaSigosi/brc8888/blob/main/deploy_ledger_validation.py); build yours with [exampletoken_deploy.json](https://github.com/NisetaSigosi/brc8888/blob/spec/spec/examples/exampletoken_deploy.json).

**Genesis Inscription Links:**  
- https://ordinals.com/inscription/111675299  
- https://uniscan.cc/inscription/68bc98a1b1e55c0ec7d5ffeae68b50d8fda0420ba5622e2ec943a87e8225d84ei0  
- https://mempool.space/tx/68bc98a1b1e55c0ec7d5ffeae68b50d8fda0420ba5622e2ec943a87e8225d84e  

---

## 🔥 TL;DR — Quick Summary

BRC-8888 unlocks Bitcoin for **programmable digital life**—Satoshi-inspired, quantum-safe, AI-evolvable:

- ✔ **Object Types**: `u-token` (fungible), `u-nft` (unique), `u-sft` (semi-fungible), `u-ai` (AI-provenanced), `u-qid` (PQ identities), `u-object` (generic).  
- ✔ **Evolutions**: Merkle-rooted state updates with PQ sigs (`sig_pq`) and triggers (transfers, time, oracles).  
- ✔ **Fair Launch**: Caps, cooldowns, vesting (e.g., UNQ founder: 90-day cliff, 12-mo linear; 1M exempted, no mint fees for founder).  
- ✔ **Economics**: Phased mints for UNQ (2100 sats Phase 1, 4200 sats Phase 2 with perks); 10k sats deploy fee for custom tokens + 1% protocol fee on every transaction (mint/transfer/evolve); enforced via TX outputs to treasury (`bc1pBRC8888ProtocolTreasuryHere...`).  
- ✔ **Bitcoin-Native**: 100% inscriptions; deterministic indexers ([deploy_ledger_validation.py](deploy_ledger_validation.py)).  
- ✔ **Future-Proof**: Dilithium3/Falcon PQ; AI `model_hash` provenance with simple demos (e.g., [ai_trait_gen.py](scripts/ai_trait_gen.py) for evolvable traits).

**Why Now?** Ordinals >100M inscriptions (Nov 2025); BRC-8888 evolves static data into living assets. Community-driven from day one. To lure indexers: Clear docs, ref code, anonymous bounties (0.5% fee shares + 100k UNQ grants for early integrators), and encrypted outreach via X/Discord.

---

## 📊 Comparison: BRC-8888 vs. BRC-20 vs. Runes

| Feature                  | **BRC-8888**                          | **BRC-20**              | **Runes**               |
|--------------------------|---------------------------------------|-------------------------|-------------------------|
| **Fungible Tokens**      | ✔ (`u-token`; phased fixed-price mints) | ✔ (basic)             | ✔ (etched, efficient)   |
| **NFTs**                 | ✔ (`u-nft`; evolvable)               | ✖                       | ✖                       |
| **Semi-Fungibles**       | ✔ (`u-sft`; batches)                 | ✖                       | ✖                       |
| **AI Provenance**        | ✔ (`u-ai`; model_hash, dynamic traits) | ✖                     | ✖                       |
| **State Evolutions**     | ✔ Native `evolve` (Merkle + PQ)      | ✖                       | ✖                       |
| **PQ Security**          | ✔ (Dilithium3/Falcon)                | ✖                       | ✖                       |
| **Verifiable Off-Chain** | ✔ (proof_uri + triggers)             | ✖                       | ✖                       |
| **Fee Enforcement**      | ✔ Mandatory TX outputs (1% per tx)   | Weak (indexer-optional) | Medium (etch fees)      |
| **Data Format**          | JSON (extensible)                    | JSON (limited)          | Binary (compact)        |
| **Ideal For**            | AI/gaming/identities; programmable life | Memecoins               | Efficient fungibles     |

**Verdict**: BRC-20 for quick tokens; Runes for scale; **BRC-8888 for quantum-safe, AI-evolving ecosystems**.

---

## 🚀 Quick Testnet Tutorial

Prototype on Testnet: Simulate → Prepare → Inscribe → Verify. (~30 min; 0.002 tBTC).

### 1️⃣ Wallet Setup
- **UniSat**: Settings → Network → **Testnet**.  
- **Xverse**: Settings → Developer → **Enable Testnet**.  
- Fund: [Mempool Faucet](https://testnet-faucet.mempool.co/) (0.005 tBTC); confirm on [mempool.space/testnet](https://mempool.space/testnet).

### 2️⃣ Simulate Locally
```bash
git clone https://github.com/NisetaSigosi/brc8888
cd brc8888
python3 deploy_ledger_validation.py

Tests: UNQ deploy (exempt), example deploy (fees), mint (phased price), vesting fail.
Tweak: Edit exampletoken_deploy.json; re-run.

3️⃣ Prepare JSON
Adapt examples (UTF-8 files):

Deploy: Copy exampletoken_deploy.json → deploy_test.json.
Edits: "tick": "TESTX", testnet addresses (tb1p... for fees/reserve).
Outputs: 10K creator + 1% protocol.
Sim: validate_deploy.

Mint: Copy mint_example.json → mint_test.json.
Edits: "tick": "TESTX", "qty": "100".
Outputs: Phase-dependent price (e.g., 2100 sats/unit in Phase 1) to reserve + 1% to protocol.
Sim: validate_mint.

Evolve: python3 scripts/package_evolve.py proof_bundle/ <ref_id> TESTX --proof-uri "ipfs://QmCID".
Generates evolve_TESTX_<ts>.json; update sig_pq post-sign.
Outputs: 1% protocol.

4️⃣ Inscribe

Wallet → Inscribe → Upload JSON (e.g., deploy_test.json).
Commit: ~546 sats (auto).
Reveal: Add outputs (e.g., fees via advanced TX builder).
Broadcast; track on ord.io/testnet (1-10 min).

5️⃣ Verify

Explorer: Search ID → View JSON.
Sim: Load in py → Re-validate.
State: Future API /state/TESTX (balances, minted, phase).

Pitfalls: Exact outputs required; sim first for caps/cooldowns/phases. Mainnet: Swap tb1p → bc1p; start with UNQ.

📁 Repository Structure

BRC-8888/
│
├── README.md                    # ← This file
│
├── docs/
│   ├── whitepaper.md           # Full protocol overview
│   ├── roadmap.md              # Phased development
│   ├── quickstart.md           # End-to-end guide
│   ├── launch_thread.md        # X announcement
│   ├── security.md             # PQ/Merkle threats
│   ├── faq.md                  # Common questions
│   └── contributing.md          # Guidelines for anonymous contributions and bounties
│
├── spec/
│   ├── brc8888-spec.md         # Canonical JSON schema
│   ├── indexer_validation.md   # Deterministic rules
│   └── examples/
│       ├── unq_deploy_mainnet.json     # UNQ bootstrap
│       ├── exampletoken_deploy.json    # Custom token
│       ├── mint_example.json           # Public mint
│       ├── transfer_example.json       # Balance move
│       ├── evolve_example.json         # State update
│       └── mint_test.json              # Testnet free mint
│
├── scripts/
│   ├── merkle_root.py          # Compute bundle root
│   ├── package_evolve.py       # Template generator
│   ├── ai_trait_gen.py         # Simple AI demo for evolvable traits (e.g., generate dynamic attributes)
│   └── README.md               # Script docs
│
├── tools/
│   ├── cli_reference.md        # Usage details
│   ├── testnet_inscription_flow.md  # Step-by-step TX
│   ├── merkle_notes.md         # Tree construction
│   └── pq_signing_reference.md # Dilithium/Falcon guide
│
├── media/
│   ├── diagrams/               # Flowcharts
│   └── branding/               # Logos
│
├── deploy_ledger_validation.py # Ref indexer impl
├── deploy_ledger_validation.md # Validation algo
├── LICENSE                     # MIT
└── .gitignore

🧠 Core Concepts (Summary)

✔ Universal Object Types

u-token: Fungible (decimals, supply).
u-nft: Unique (supply=1).
u-sft: Batch semi-fungibles.
u-ai: AI traits (model_hash, seeds).
u-qid: PQ identities (Dilithium3).
u-object: Extensible generic (UNQ default).

✔ Evolutions
op: "evolve" commits new state:

merkle_root: SHA256 tree of bundle.
proof_uri: IPFS/Arweave archive.
sig_pq: PQ sig over (ref || root || trigger).
Triggers: Transfer (txid/from/to/qty), time (block/UTC), oracle.

Unlimited; transforms static into adaptive (e.g., AI learning—see ai_trait_gen.py demo).

✔ Fee Enforcement
fees block in every op:

Base: 1% per transaction (mint/transfer/evolve) to treasury.
Deploy: +10K sats creator (non-genesis).
Mint: Phase-dependent fixed price per UNQ to reserve + 1% treasury.
TX must output ≥ required; indexers reject otherwise.

🛡 Disclaimer
For research/education/reference. No warranties; consult experts for production/legal use. Bitcoin risks apply (volatility, forks). Founding promotes neutrality—verify code independently.

🤝 Contributions
PRs/issues for indexers, wallets, tools welcome. Follow roadmap.md and contributing.md; code in MIT. Anonymous submissions encouraged—use GitHub without login or proxies. Bounties for early indexers: 0.5% fee shares + 100k UNQ grants, distributed anonymously via on-chain claims.

🙏 Creator
Niseta Sigosi
2025: Evolving Bitcoin, one object at a time.
#BRC8888

**Keywords:** BRC-8888, UNQ token, Bitcoin Ordinals protocol, post-quantum evolutions, AI-aware objects, 1% protocol fee, phased minting
