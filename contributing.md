# Contributing to BRC-8888

Welcome! BRC-8888 is a fully open, pseudonymous, community-driven protocol.  
Everything is MIT licensed — no permission needed to fork, build, or earn.

We especially welcome **indexers**, **wallet teams**, **marketplace devs**, and **anonymous contributors**.

## How to Contribute

| Type               | How to do it                                                                                           |
|---------------------|---------------------------------------------------------------------------------------------------------|
| **Code**            | Fork → create branch → make changes → open PR (you can do this completely anonymously via GitHub web editor) |
| **Bug / Idea**      | Open an Issue (no login optional)                                                                   |
| **Docs / Tutorials**| Edit any `.md` file directly on GitHub → “Propose changes”                                            |
| **Indexer**         | Fork `deploy_ledger_validation.py`, implement full state engine, run a public node/API               |

All contributions are merged on technical merit. No KYC, no Discord verification, no personal info ever required.

## Priority Tasks & Bounties (Live)

| Task                                          | Bounty                                      | How to claim                                                                 |
|-----------------------------------------------|---------------------------------------------|--------------------------------------------------------------------------------|
| First 3 public, verifiable BRC-8888 indexers | **0.5% of all protocol fees forever** + 100,000 UNQ grant | Announce on X with endpoint + proof of correct UNQ state → on-chain payout |
| Node.js / Rust / Go indexer implementation    | 50,000–100,000 UNQ                         | Open PR + public testnet/mainnet node                                        |
| Wallet integration (UniSat, Xverse, Leather, OKX, etc.) | 25,000–75,000 UNQ               | PR or tweet demo → grant sent                                                 |
| Marketplace listing + phased mint UI          | 50,000 UNQ                                  | Live integration → grant sent                                                 |
| High-quality tutorial / video / dashboard     | 10,000–30,000 UNQ                          | Post link in Issues                                                           |

Grants are paid from the protocol treasury — transparent, on-chain, no KYC, no questions asked.

## Indexer Integration Checklist (to qualify for the 0.5% bounty)

- Correctly parse `p: "brc8888-1"`
- Enforce phased pricing (2100 / 4200 sats)
- Enforce user cap (10,000 UNQ), cooldown (144 blocks), founder vesting & lock
- Reject mints without required outputs (1% treasury + phased cost to reserve)
- Expose public API (`/state/UNQ`, `/balance/<address>`, etc.)

First three to go live and stay online win the 0.5% lifetime revenue share.

## Code Style
- Python: PEP8, type hints welcome
- JSON examples: pretty-printed, no trailing commas
- Commit messages: imperative mood (“Add phased pricing”, “Fix vesting calculation”)

## Community
- #BRC8888

No gatekeeping. No team tokens beyond the disclosed vested founder allocation.  
All revenue goes to treasury → community → builders.

**Ship code, earn forever.**

Let’s turn Bitcoin into programmable, evolving life.  
Pull requests are love letters.
