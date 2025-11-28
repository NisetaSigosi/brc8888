# BRC-8888 Testnet Inscription Flow

Deploy, mint, transfer, and evolve BRC-8888 objects on **Bitcoin Testnet**—safe prototyping guide. Use UniSat or Xverse; simulate first with [deploy_ledger_validation.py](../deploy_ledger_validation.py). Assumes repo cloned.

**Current Height:** ~925,000+ (verify via [mempool.space/testnet](https://mempool.space/testnet)).  
**Cost:** ~0.002 tBTC (faucet-funded).  
**Explorers:** [ord.io/testnet](https://ord.io/testnet) for inscriptions; mempool.space/testnet for TXs.

---

## Prerequisites (5 min)
- **Wallet:** UniSat, Xverse, or Leather (Ordinals-enabled).  
- **Funds:** 0.002 tBTC from [Mempool Faucet](https://testnet-faucet.mempool.co/) or [Bitcoin Faucet](https://bitcoinfaucet.uo1.net/).  
- **Tools:** Python 3.10+; repo files (examples/*.json, scripts/*.py).  
- **Simulation:** Run `python3 deploy_ledger_validation.py` to test ops locally.

---

## Step-by-Step Flow

### 1. Wallet Setup & Fund (3 min)
- **UniSat:** Settings → Network → **Testnet**; fund (1-5 min confirm).  
- **Xverse:** Settings → Developer → **Enable Testnet Mode**; fund.  
- **Leather:** Preferences → Advanced → **Testnet**; fund.  
- **Verify:** Send 546 sats dust to self; check explorer.

### 2. Simulate Operations (5 min)
Test JSONs before spending sats:  
```bash
cd brc8888
python3 deploy_ledger_validation.py

Validates: UNQ deploy (exempt), example deploy (fees), mint (phased price + 1% fee), transfer (balances), founder vesting/lock failure.
Edit examples (e.g., spec/examples/exampletoken_deploy.json) and re-run.
Errors? Fix fees/outputs/caps/phases—ensures compliance.

3. Prepare JSON Templates (5 min)

Adapt from spec/examples/ (UTF-8 files). Use testnet addresses (tb1p...).

Deploy (deploy_test.json): Copy exampletoken_deploy.json.
Edits: "tick": "TESTX", tb1p... addresses (creator_fee, protocol_fee, reserve).
Fees: 10,000 sats creator + 1% protocol (non-genesis).
Sim: validate_deploy.

Mint (mint_test.json): Copy mint_example.json.
Edits: "tick": "TESTX", "qty": "100", minter address.
Outputs: Phased price (~2100 sats/unit in Phase 1) to reserve + 1% to protocol.
Sim: validate_mint.

Transfer (transfer_test.json): Copy transfer_example.json.
Edits: "tick": "TESTX", "qty": "50", from/to addresses.
Outputs: 1% to protocol.
Sim: Extend py with validate_transfer.

Evolve: Run python3 scripts/package_evolve.py <proof_dir> <ref_id> <tick>.
<proof_dir>: Bundle (e.g., state.json, traits from ai_trait_gen.py); generates evolve_TESTX_<ts>.json.
Edits: Update proof_uri (post-upload), sig_pq (PQ-sign payload).
Outputs: 1% to protocol.
Sim: Verify Merkle via scripts/merkle_root.py; extend py for sig/trigger.

4. Inscribe Operation

Open wallet inscription tool (e.g., UniSat → Inscribe → Upload File).
Select JSON (e.g., deploy_test.json).
Commit TX: ~546 sats fee (wallet auto).
Reveal TX: Manual outputs for fees (use wallet advanced or Ordinal Theory):
Deploy: 10k to creator_fee; 1% to protocol.
Mint: Phased total to reserve; 1% to protocol.
Transfer/Evolve: 1% to protocol.

Broadcast; wait 1-10 min. Note inscription ID from explorer.

Tip: For complex outputs, use bitcoin-cli (testnet) or Electrum; reference Ordinal Handbook.

5. Verify & Query

Explorer Check: Search inscription ID on ord.io/testnet → View JSON/raw.
Simulation Confirm: Load ID/deploy in py script → Re-run validation (e.g., validate_mint).
State Query: Future indexer API: /state/TESTX (balances, total_minted, phase).
Events: Check logs for deploy_accepted, mint_accepted (extend py for emits).

Common Pitfalls:

Fee Mismatch: TX outputs must exactly match (indexers reject < required).
Dust Limits: Ensure >546 sats per output.
Cooldowns/Caps/Phases: Sim first; Testnet height ~925K+ (use in triggers).

Mainnet Transition: Swap tb1p→bc1p; fund BTC. Bootstrap with unq_deploy_mainnet.json.

Quickstart | FAQ | #BRC8888 on X. Prototype securely! 🚀
