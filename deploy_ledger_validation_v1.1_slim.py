"""
deploy_ledger_validation_v1.1_slim.py
BRC-8888 Reference Indexer — Slim Payload Edition (v1.1)
- Addresses derived from deploy TX outputs (output 1 = reserve, output 2 = treasury)
- Optional fields skipped
- Minimal JSON parsing, smaller memory footprint
"""

from collections import defaultdict
from decimal import Decimal
from datetime import datetime, timezone
import requests

# Global protocol treasury (fallback if not in TX)
PROTOCOL_TREASURY = "bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0"

class BRC8888LedgerSlim:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(Decimal))
        self.minted_by_addr = defaultdict(lambda: defaultdict(Decimal))
        self.last_mint_block = defaultdict(lambda: defaultdict(int))
        self.deploys = {}           # {deploy_inscription_id: data}
        self.total_minted = defaultdict(Decimal)
        self.address_cache = {}     # {deploy_txid: (reserve_addr, treasury_addr)}

    # === Dynamic address derivation from deploy TX (v1.1 Slim) ===
    def get_addresses_from_deploy_tx(self, deploy_txid):
        if deploy_txid in self.address_cache:
            return self.address_cache[deploy_txid]

        try:
            url = f"https://mempool.space/api/tx/{deploy_txid}"
            tx = requests.get(url, timeout=10).json()
            outputs = tx.get("vout", [])
            reserve = outputs[0]["scriptpubkey_address"] if len(outputs) > 0 else None
            treasury = outputs[1]["scriptpubkey_address"] if len(outputs) > 1 else PROTOCOL_TREASURY
            self.address_cache[deploy_txid] = (reserve, treasury)
            return reserve, treasury
        except:
            return None, PROTOCOL_TREASURY

    # === Core validation ===
    def validate_deploy(self, inscription_id, deploy_json, deploy_txid):
        tick = deploy_json["tick"]
        if any(d["tick"] == tick for d in self.deploys.values()):
            return False, f"Tick {tick} already exists"

        # v1.1 Slim: addresses come from TX, not JSON
        reserve_addr, treasury_addr = self.get_addresses_from_deploy_tx(deploy_txid)
        if not reserve_addr:
            return False, "Failed to read reserve address from deploy TX"

        deploy_json["_derived_reserve"] = reserve_addr
        deploy_json["_derived_treasury"] = treasury_addr

        self.deploys[inscription_id] = deploy_json
        print(f"[Slim] Deployed {tick} | Reserve: {reserve_addr} | Treasury: {treasury_addr}")
        return True, "Deploy valid"

    def validate_mint(self, inscription_id, mint_json, mint_txid, current_block):
        if inscription_id not in self.deploys:
            return False, "Deploy not found"

        deploy = self.deploys[inscription_id]
        tick = mint_json["tick"]
        qty = Decimal(mint_json["qty"])
        minter = mint_json.get("minter", "unknown")

        # Supply & cap checks
        if self.total_minted[tick] + qty > Decimal(deploy["supply"]):
            return False, "Exceeds total supply"

        rules = deploy.get("mint_rules", {})
        user_cap = Decimal(rules.get("user_cap", 0))
        if user_cap and self.minted_by_addr[minter][tick] + qty > user_cap:
            return False, "Exceeds user cap"

        # Phase price (derived)
        phases = rules.get("phases", [])
        price_per_unit = 0
        if phases:
            current = int(self.total_minted[tick])
            for p in phases:
                if int(p["start_minted"]) <= current < int(p["end_minted"]):
                    price_per_unit = int(p["price_sats"])
                    break
        total_cost = price_per_unit * qty
        protocol_fee = int(total_cost * 0.01)  # 1%

        # Derive addresses from original deploy TX
        reserve_addr = deploy.get("_derived_reserve")
        treasury_addr = deploy.get("_derived_treasury", PROTOCOL_TREASURY)

        # Fetch mint TX to verify outputs
        try:
            tx = requests.get(f"https://mempool.space/api/tx/{mint_txid}").json()
            paid_reserve = sum(o["value"] for o in tx["vout"] if o.get("scriptpubkey_address") == reserve_addr)
            paid_treasury = sum(o["value"] for o in tx["vout"] if o.get("scriptpubkey_address") == treasury_addr)

            if paid_reserve < total_cost or paid_treasury < protocol_fee:
                return False, f"Insufficient outputs: reserve {paid_reserve} < {total_cost}, treasury {paid_treasury} < {protocol_fee}"
        except:
            return False, "Failed to verify TX outputs"

        # Update ledger
        self.balances[minter][tick] += qty
        self.minted_by_addr[minter][tick] += qty
        self.total_minted[tick] += qty
        self.last_mint_block[minter][tick] = current_block

        print(f"[Slim] Minted {qty} {tick} → {minter} | Cost: {total_cost:,} sats + {protocol_fee:,} fee")
        return True, "Mint valid"

# Quick test (run as script)
if __name__ == "__main__":
    ledger = BRC8888LedgerSlim()
    # Simulate a deploy + mint flow
    print("BRC-8888 v1.1 Slim indexer ready")
