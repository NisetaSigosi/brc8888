# deploy_ledger_validation.md

Reference indexer validation rules for BRC-8888 (v1)  
Implementation: [`deploy_ledger_validation.py`](deploy_ledger_validation.py)

This document describes exactly how indexers must process `deploy` and `mint` operations to be fully compliant with BRC-8888.

## Core Principles
- All state is derived from **inscriptions only** (Bitcoin-native).
- Indexers must enforce **exact output requirements** (no optional fees).
- 1% protocol fee on **every transaction** (mint/transfer/evolve) → `bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0`
- Genesis token **UNQ** has special exemptions (no deploy fees, founder 1M vested/locked).

## Deploy Validation (`op: "deploy"`)

| Condition                               | Rule                                                                                           | Required Outputs (mainnet)                                      |
|-----------------------------------------|------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| `genesis: true` (UNQ only)              | No fees allowed                                                                                | None                                                            |
| `genesis: false` (all other tokens)     | Must pay **10,000 sats creation fee** + **1% protocol fee** (100 sats)                        | ≥10,000 sats → `creator_fee_address`<br>≥100 sats → protocol treasury |
| Duplicate `tick`                        | Rejected                                                                                       | N/A                                                             |

## Mint Validation (`op: "mint"`)

### 1. Supply & Phase Checks
- `total_minted + qty ≤ supply`
- If `phases` defined → calculate exact **phased cost** across phase boundaries:
  - Phase 1 (0–10,000,000): **2100 sats per UNQ**
  - Phase 2 (10,000,001–21,000,000): **4200 sats per UNQ**
- Must send **exact phased cost** to `reserve_address`

### 2. User Restrictions (non-exempt)
- `user_cap` (UNQ: 10,000) → per-address lifetime limit
- `cooldown_blocks` (144 ≈ 24h) → blocks between mints per address

### 3. Founder Exemption (address `bc1p2egtx…yzm0`)
| Rule                                    | Enforcement                                                                                 |
|-----------------------------------------|---------------------------------------------------------------------------------------------|
| Max exempt amount                       | 1,000,000 UNQ                                                                               |
| Lock condition                          | Non-mintable/transferable until **≥20,000,000 public UNQ minted**                           |
| Vesting                                 | 90-day cliff (starts 2025-11-18) → 12-month linear unlock (monthly periods)                 |
| Mint fee                                | **Free** (no phased cost, only dust)                                                        |

### 4. Mandatory 1% Protocol Fee
- Always: **1% of phased cost** → protocol treasury address
- Example: Minting 100 UNQ in Phase 1 → 210,000 sats to reserve + **2,100 sats** to treasury

## Transaction Output Requirements Summary

| Operation                     | Required Outputs                                                                                   |
|-------------------------------|----------------------------------------------------------------------------------------------------|
| Genesis deploy (UNQ)          | None                                                                                               |
| Custom token deploy           | ≥10,000 sats → creator<br>≥100 sats → treasury                                                     |
| Public mint (phased)          | Exact phased cost → reserve<br>1% of phased cost → treasury                                        |
| Founder exempt mint           | Only dust (no phased cost, no 1% fee)                                                              |

## Indexer Implementation Notes
- Use UTC time for vesting calculations.
- Floor unlocked amount (conservative rounding).
- Reject any transaction missing required outputs.
- Run the provided `deploy_ledger_validation.py` as a full test suite — it simulates:
  - UNQ genesis deploy
  - Founder early mint → fails (vesting + lock)
  - Public phased mint → passes with correct fees

Compliant indexers will automatically track balances, enforce caps, and protect the 1% protocol treasury forever.

**BRC-8888 is live. Indexers: integrate now → claim your bounty.**
