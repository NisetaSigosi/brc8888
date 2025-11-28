# BRC-8888 — FAQ

**Last Updated:** November 26, 2025  
**Protocol Version:** v1  
**Genesis Inscription:** [68bc98a1b1e55c0ec7d5ffeae68b50d8fda0420ba5622e2ec943a87e8225d84ei0](https://ordinals.com/inscription/111675299)  
**Reference:** [Spec](spec/brc8888-spec.md) | [Indexer Validation](deploy_ledger_validation.md) | [Reference Impl](deploy_ledger_validation.py)

---

### What is BRC-8888?
BRC-8888 is a **Bitcoin-native universal object protocol** built on Ordinals inscriptions. It enables **stateful, evolving, AI-aware, and post-quantum-secure** digital assets — fungibles, NFTs, semi-fungibles, AI agents, quantum identities — all in one extensible standard.  
No consensus changes. No sidechains. Pure inscriptions + deterministic indexers.

Key innovation: `evolve` operations with Merkle-anchored state and PQ signatures.

---

### Is BRC-8888 a competitor to BRC-20 or Runes?
No — it’s **complementary and far more powerful**:

| Feature                  | BRC-8888                          | BRC-20               | Runes               |
|--------------------------|-----------------------------------|----------------------|---------------------|
| Fungible tokens          | Yes (`u-token`)                   | Yes                  | Yes                 |
| NFTs / Semi-fungibles    | Yes (`u-nft`, `u-sft`)            | No                   | No                  |
| Evolvable state          | Yes (Merkle + PQ sigs)            | No                   | No                  |
| AI provenance            | Yes (`u-ai`, `model_hash`)        | No                   | No                  |
| Post-quantum security    | Yes (Dilithium3/Falcon)           | No                   | No                  |
| Mandatory 1% fee         | Yes (enforced by indexers)        | Optional             | Etch-only           |
| Phased minting           | Yes (fixed-price FOMO)            | No                   | No                  |

**Verdict**: BRC-20 = simple memecoins. Runes = efficient fungibles. **BRC-8888 = programmable, future-proof digital life on Bitcoin.**

---

### Does BRC-8888 require Bitcoin consensus changes?
**No.**  
Everything is standard Ordinals inscriptions (JSON payloads). Rules are enforced off-chain by deterministic indexers — exactly like BRC-20 and Runes.

---

### What is the genesis token UNQ?
**UNQ** is the first BRC-8888 object (`genesis: true`):  
- Supply: **21,000,000** (8 decimals)  
- Fair launch: 10,000 per wallet cap, 144-block cooldown  
- Founder: 1,000,000 tokens (vested: 90-day cliff + 12-month linear unlock, locked until ≥20M public minted)  
- Phased minting:  
  - Phase 1 (0–10,000,000): **2100 sats per UNQ**  
  - Phase 2 (10,000,001–21,000,000): **4200 sats per UNQ** + AI trait unlocks  
- 1% protocol fee on every transaction → treasury (`bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0`)

UNQ bootstraps the ecosystem. Anyone can deploy their own BRC-8888 objects.

---

### How does the 1% protocol fee work?
**Mandatory & indexer-enforced** — no opt-out:  
- Every mint/transfer/evolve must output **≥1% of value** to the protocol treasury.  
- Phased mints: additional fixed price to `reserve_address` + 1% of that price to treasury.  
- Deploy (non-genesis): 10,000 sats creation fee + 1% protocol share.  
Indexers reject transactions missing these outputs.

Revenue funds development, bounties, and long-term sustainability.

---

### When will wallets and marketplaces show BRC-8888?
**As soon as indexers add support** (1–4 weeks post-launch).  
- Wallets will show UNQ balances, phased prices, and simulation ("Mint cost: 2100 sats + 21 sats fee").  
- Marketplaces will list BRC-8888 objects with evolution history and AI/PQ badges.  
Early indexers get **0.5% lifetime fee share + 100k UNQ bounty** — claim anonymously.

---

### How do evolutions work?
`op: "evolve"` inscriptions update an object’s state immutably:  
- Merkle root of off-chain bundle (IPFS/Arweave)  
- Post-quantum signature over `(ref || root || trigger)`  
- Triggers: transfer, time, oracle, etc.  
Unlimited evolutions. Enables living NFTs, AI learning, dynamic traits, etc.

---

### Are post-quantum and AI features mandatory?
**No — fully optional**:  
- Add `quantum.identity_pub` for PQ-secure evolutions (future-proof).  
- Add `ai.model_hash` for provenance and dynamic traits (e.g., generative art).  
Strict indexers enforce them; lenient ones don’t.

---

### Can I deploy my own BRC-8888 token?
**Yes — anyone can**:  
- Inscribe a `deploy` JSON with your `tick`, supply, rules.  
- Pay 10,000 sats creation fee + 1% protocol.  
- Customize phases, caps, AI/PQ — see [exampletoken_deploy.json](spec/examples/exampletoken_deploy.json).

---

### Is the founder anonymous?
Yes. The protocol was launched pseudonymously by **Niseta Sigosi** to promote decentralization and neutrality. All actions are on-chain and verifiable.

---

### Where do I start?
- **Read**: [Spec](spec/brc8888-spec.md) | [Validation](deploy_ledger_validation.md)  
- **Code**: Clone repo → run `python3 deploy_ledger_validation.py` for simulations  
- **Examples**: [UNQ Deploy](spec examples/unq_deploy_mainnet.json) | [Mint](spec/examples/mint_example.json)  
- **Community**: #BRC8888 

**Launch your object today — fair, quantum-safe, and 100% Bitcoin.**
