# Indexer Validation Algorithm for BRC-8888 (v1)

**Genesis Inscription:** https://ordinals.com/inscription/111675299  
**Last Updated:** November 26, 2025  
**Reference Implementation:** `deploy_ledger_validation.py`

This document specifies the **deterministic validation steps** an indexer must apply to accept and apply BRC-8888 inscriptions. Indexers implementing these rules provide interoperability guarantees for wallets and marketplaces.

---

## High-level Rules
- Only process inscriptions where `p == "brc8888-1"` and `v == "1"`.  
- Reject/unacknowledge inscriptions that fail mandatory checks (fee output, schema validation, signature verification).  
- Maintain off-chain ledger state (balances, total_minted, last_mint_block) deterministically from prior events; use UTC timestamps for time-based checks (e.g., vesting).  
- Keep immutable event logs for deploys, mints, transfers, evolves, and fees for auditability.

---

## Validation Flow (per inscription transaction `T` containing inscription `I`)

1. **Parse & Basic Sanity**
   - Parse inscription JSON `J`. If parse fails → ignore.  
   - If `J.p != "brc8888-1"` or `J.v != "1"` → ignore.  
   - Extract `tick = J.tick`; ensure it's a valid string (e.g., uppercase alphanumeric, 3–12 chars).

2. **Schema Validation**
   - Verify `op` is one of: `"deploy"`, `"mint"`, `"transfer"`, `"evolve"`.  
   - Validate required/optional fields per op (e.g., deploy needs `supply`, `otype`; mint needs `qty`). Ignore unknown keys.  
   - Parse numerics as `int` or `Decimal`. Timestamps as ISO 8601 UTC.  
   - If missing required fields or invalid formats → mark as invalid and ignore.

3. **Fee Enforcement (Mandatory)**
   - For all ops: Read `protocol_fee_percent = J.fees.protocol_fee_percent` (default 1) and `fee_address = J.fees.fee_address`.  
   - Compute required base: **1% of transaction value** if `fee_scope == "per_tx"` (standard).  
   - Inspect all outputs of `T`. If no output pays ≥ required base to `fee_address` → **reject**.  
   - Op specials:  
     - **Deploy**: If `genesis: true`, exempt all fees (required base = 0). Else, add `deploy_creation_fee_sats` output to `creator_fee_address`.  
     - **Mint**: + phased price (check total_minted vs phase thresholds) to `reserve_address` + **1% of phased cost** to treasury.  
     - **Transfer/Evolve**: Base 1% only.  
   - Record the fee payment event (txid, amount, fee_address, protocol_share if applicable).

4. **Operation-specific Validation**

   ### deploy
   - Check `tick` not previously deployed (global uniqueness).  
   - If `genesis: true`, validate exempt `mint_rules` (e.g., `exempt_addrs` with `vesting`/`lock_conditions`).  
   - Validate `otype` (one of: `u-token`, `u-nft`, etc.), `supply` (>0 integer), `decimals` (0–18).  
   - If phases defined, validate params (e.g., start_minted < end_minted, price_sats > 0).  
   - Store deploy metadata immutably (tick → {supply, mint_rules, phases, quantum.identity_pub, ai, fees`).

   ### mint
   - Ensure deploy exists for `tick`; fetch its rules (`mint_rules`, `phases`, `fees`).  
   - Check `total_minted[tick] + qty ≤ supply`.  
   - Minter `addr = J.minter or inscriber_addr`.  
   - If exempt (`addr` in `exempt_addrs`):  
     - `already_minted + qty ≤ exempt.amount`.  
     - Lock: If `lock_until_public_minted > total_minted[tick]` → reject.  
     - Vesting: Compute unlocked = `amount * min(1, max(0, (current_time - cliff_end) / duration))` (linear, UTC); if `already_minted + qty > unlocked` → reject (floor to int).  
   - Else (public): `already_minted + qty ≤ user_cap`; check cooldown (`last_mint_block[addr][tick] + cooldown_blocks ≤ current_block`).  
   - Compute phased price for current phase (UNQ: Phase 1 = first 10,000,000 at 2100 sats; Phase 2 = next 11,000,000 at  at 4200 sats).  
   - If valid: Update ledger (`balances[addr][tick] += qty`, `total_minted[tick] += qty`, `last_mint_block[addr][tick] = current_block`); emit `mint_accepted`.

   ### transfer
   - Ensure deploy exists for `tick`.  
   - Verify `balances[from][tick] ≥ qty` (respect locks/vesting).  
   - Update ledger: `balances[from][tick] -= qty`; `balances[to][tick] += qty`.  
   - Record transfer event.

   ### evolve
   - Ensure `ref` points to valid deploy or latest accepted evolve for `tick`.  
   - Validate `merkle_root` format (`sha256:` + 64-hex chars).  
   - Fetch `proof_uri` (IPFS/Arweave, with timeouts/retries); verify archive contents hash to `merkle_root`.  
   - Retrieve `identity_pub` from deploy/quantum. If absent or `post_quantum_secure: false` and policy requires → reject.  
   - Canonical payload = `(ref || merkle_root || trigger)` (sorted JSON, no whitespace). Verify `sig_pq` using declared algorithm against `identity_pub`. If fails → reject.  
   - Verify `trigger` conditions (transfer, time, oracle).  
   - If valid: Update current state root; append immutable evolve event.

5. **Atomicity & Conflicts**
   - Process inscriptions in block/ordinal order.  
   - For same-block conflicts, use deterministic tie-breaker (lowest inscription ID).  
   - Reject non-canonical evolves.

6. **Post-validation**
   - Emit standardized events: `deploy_accepted`, `mint_accepted`, `transfer_accepted`, `evolve_accepted`, `fee_received`.  
   - Expose REST/GraphQL endpoints: `/state/{tick}`, `/history/{tick}`, `/proof/{evolve_id}`, `/fees/{address}`.

7. **Safety & Rate-limiting**
   - Enforce min fees (1%), rate limits per addr/tick.  
   - Configurable policy for high-value evolves (e.g., threshold sig thresholds).  
   - Sync with ≥2 independent indexers via gossip/state diffs.

---

## Recommended Policies for Indexer Operators
- Publish your acceptance policy, version, and sync status publicly.  
- Provide human-verifiable logs for disputed ops.  
- Sync with at least two independent indexers to detect divergence.

---

**This is the canonical validation algorithm.**  
Compliant indexers will track UNQ balances, enforce 1% fees, and unlock evolutions exactly as intended.

**BRC-8888 is live. Indexers: integrate now → claim your bounty.**
