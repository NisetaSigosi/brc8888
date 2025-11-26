# BRC-8888 Quickstart Guide

Deploy, mint, transfer, and evolve BRC-8888 objects on **Bitcoin Mainnet** in under 30 minutes.

**Time:** 20–40 min | **Cost:** ~0.00002 BTC (~$2) | **Prereqs:** Any Ordinals wallet (UniSat, Gamma, Magic Eden, Xverse, Leather)

**Genesis UNQ is LIVE** → inscription: https://ordinals.com/inscription/111675299

---

## 1. Get Ready (5 min)

1. **Wallet** → UniSat, Gamma.io, or Magic Eden (all support JSON upload).  
2. **Fund** → Send ≥0.001 BTC to your Taproot address (bc1p…).  
3. **Repo** → Clone or download: https://github.com/NisetaSigosi/brc8888  
   (Contains all JSON examples + reference indexer)

---

## 2. Simulate Locally (Optional but Recommended)

```bash
git clone https://github.com/NisetaSigosi/brc8888
cd brc8888
python3 deploy_ledger_validation.py

Tests UNQ deploy, phased mints, founder vesting/lock, and fee enforcement.
Edit any JSON and re-run — catch errors before spending sats.

**3. Deploy Your Own BRC-8888 Token (10 min)**

Copy spec/examples/exampletoken_deploy.json → my_token_deploy.json
Edit:
"tick": "YOURTICK" (uppercase, 4–12 chars)
Optional: change supply, phases, user_cap, add AI/PQ blocks

Inscribe:
UniSat → Inscribe → Upload my_token_deploy.json (as Text)
Fee rate: 8 sat/vB (economy)
Pay 10,000 sats creation fee + 1% protocol fee (100 sats) in the same TX
Broadcast → Wait 10–30 min

Done! Your token is live. Share the inscription ID.

**4. Mint Tokens (Public or Founder Exemption)**

**Public Mint (phased pricing)**

Copy spec/examples/mint_example.json → mint_my_token.json
Edit:
"tick": "YOURTICK"
"qty": "1000" (or any amount)

Inscribe → Pay:
Phase price to reserve_address
1% of phase price to protocol treasury

Tokens appear in your wallet once indexers adopt.

**Founder 1M Exemption Mint (UNQ only — free)**
{
  "p": "brc8888-1",
  "v": "1",
  "op": "mint",
  "tick": "UNQ",
  "qty": "1000000",
  "minter": "bc1p2egtxaky7jfn9drm53qaq0pyy9ap4yfppmg58w5ysvpvlcwx980q86yzm0"
}

Inscribe as Text → only dust fee → 1M UNQ minted (locked/vested per rules).

**5. Transfer & Evolve **

Transfer: Standard op: "transfer" inscription + 1% fee
Evolve: op: "evolve" with Merkle root + PQ signature (use scripts/package_evolve.py)

Templates and tools in repo.

**Mainnet Resources**

Genesis UNQ: https://ordinals.com/inscription/111675299
Repo: https://github.com/NisetaSigosi/brc8888
Spec: spec/brc8888-spec.md
Validation: deploy_ledger_validation.py

Indexers → claim your 0.5% fee share + 100k UNQ bounty (see docs/contributing.md).
You just deployed the future of Bitcoin objects.
Now go inscribe.
#BRC8888 #UNQ



