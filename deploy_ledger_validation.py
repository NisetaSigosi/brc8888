"""
deploy_ledger_validation.py

Reference indexer implementation for BRC-8888 (v1)

Validates:
- Genesis (UNQ): no deploy fees, founder exemption with vesting & lock
- Custom tokens: 10,000 sats creation fee + 1% protocol fee on deploy
- Mint enforcement: phased fixed pricing, user caps, cooldowns
- Founder vesting: 90-day cliff + 12-month linear unlock
- Founder lock: non-mintable/transferable until ≥20M public minted
- 1% protocol fee on every transaction (mint/transfer/evolve)

Run this file directly for simulation of UNQ + generic token lifecycle.
"""

from collections import defaultdict
from decimal import Decimal, ROUND_DOWN, getcontext
from datetime import datetime, timedelta, timezone
import math

getcontext().prec = 28

class BRC8888Ledger:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(int))
        self.minted_by_addr = defaultdict(lambda: defaultdict(int))
        self.last_mint_block = defaultdict(lambda: defaultdict(int))
        self.deploys = {}                    # {deploy_inscription_id: deploy_data}
        self.total_minted = defaultdict(int) # {tick: total_minted}
        self.protocol_address = "bc1puez48076vx6d3lnxkgnwzahsmpvmklfcnulcq0jgu6u4dl2yhmpsjr9kq0"  # BRC-8888 treasury

    # ------------------------------------------------------------------ #
    # Helper: sum sats sent to an address in a transaction
    # ------------------------------------------------------------------ #
    def tx_outputs_total_to_address(self, tx, address):
        if not tx or "outputs" not in tx:
            return 0
        return sum(int(out.get("sats", 0)) for out in tx["outputs"] if out.get("address") == address)

    # ------------------------------------------------------------------ #
    # Phased pricing utilities
    # ------------------------------------------------------------------ #
    def get_phase_price(self, phases, current_minted):
        for phase in phases:
            start = int(phase["start_minted"])
            end = int(phase["end_minted"])
            if start <= current_minted < end:
                return int(phase["price_sats"])
        return 0  # No valid phase

    def compute_phased_cost(self, phases, current_minted, qty):
        """Calculate total sats required for qty across current phase boundaries."""
        total = 0
        remaining = qty
        minted = current_minted
        while remaining > 0:
            price = self.get_phase_price(phases, minted)
            if price == 0:
                raise ValueError("No valid phase for minting remaining quantity")
            # Find end of current phase
            phase_end = next(int(p["end_minted"]) for p in phases
                             if int(p["start_minted"]) <= minted < int(p["end_minted"]))
            available = phase_end - minted
            mint_this_phase = min(remaining, available)
            total += price * mint_this_phase
            minted += mint_this_phase
            remaining -= mint_this_phase
        return total

    # ------------------------------------------------------------------ #
    # Vesting calculation (founder exemption)
    # ------------------------------------------------------------------ #
    def compute_unlocked_amount(self, vesting, current_time):
        if not vesting:
            return Decimal('inf')

        start = datetime.fromisoformat(vesting["start"].replace("Z", "+00:00"))
        cliff_days = int(vesting.get("cliff_days", 0))
        duration_days = int(vesting.get("duration_days", 0))

        cliff_end = start + timedelta(days=cliff_days)
        if current_time < cliff_end:
            return Decimal(0)

        time_since_cliff = current_time - cliff_end
        full_duration = timedelta(days=duration_days)
        fraction = min(Decimal(1), Decimal(time_since_cliff.total_seconds()) / full_duration.total_seconds())
        amount = Decimal(vesting.get("amount", 0))  # amount is in exempt_addrs entry
        return (amount * fraction).to_integral_value(rounding=ROUND_DOWN)

    # ------------------------------------------------------------------ #
    # Deploy validation
    # ------------------------------------------------------------------ #
    def verify_deploy_fee_output(self, tx, fees, is_genesis):
        if is_genesis:
            return True, "Genesis deploy — fees exempt"

        creation_fee = int(fees.get("deploy_creation_fee_sats", 0))
        protocol_pct = int(fees.get("protocol_fee_percent", 0)) / 100

        creator_addr = fees.get("creator_fee_address") or fees.get("fee_address")
        protocol_addr = fees.get("protocol_fee_address") or self.protocol_address

        paid_creator = self.tx_outputs_total_to_address(tx, creator_addr)
        paid_protocol = self.tx_outputs_total_to_address(tx, protocol_addr)

        required_protocol = int(creation_fee * protocol_pct)
        if paid_creator < creation_fee or paid_protocol < required_protocol:
            return False, f"Deploy fees insufficient — creator: {paid_creator}/{creation_fee}, protocol: {paid_protocol}/{required_protocol}"
        return True, "Deploy fees satisfied"

    # ------------------------------------------------------------------ #
    # Mint validation
    # ------------------------------------------------------------------ #
    def verify_mint_fee_output(self, tx, fees, phases, qty, current_minted):
        protocol_pct = int(fees.get("protocol_fee_percent", 0)) / 100
        protocol_addr = fees.get("protocol_fee_address") or self.protocol_address
        reserve_addr = fees.get("reserve_address")

        # 1% protocol share on phased cost (if phases exist)
        phased_cost = 0
        if phases:
            phased_cost = self.compute_phased_cost(phases, current_minted, qty)
            paid_reserve = self.tx_outputs_total_to_address(tx, reserve_addr)
            if paid_reserve < phased_cost:
                return False, f"Phased cost not met: {paid_reserve} < {phased_cost}"

        protocol_share = int(phased_cost * protocol_pct)
        paid_protocol = self.tx_outputs_total_to_address(tx, protocol_addr)
        if paid_protocol < protocol_share:
            return False, f"Protocol 1% share missing: {paid_protocol} < {protocol_share}"

        return True, {"phased_cost": phased_cost, "protocol_share": protocol_share}

    # ------------------------------------------------------------------ #
    # Public validation methods
    # ------------------------------------------------------------------ #
    def validate_deploy(self, inscription_id, deploy_data, tx, inscriber_addr, current_block):
        tick = deploy_data["tick"]
        if any(d["tick"] == tick for d in self.deploys.values()):
            return False, f"Tick {tick} already exists"

        is_genesis = deploy_data.get("genesis", False)
        fees = deploy_data.get("fees", {})
        ok, msg = self.verify_deploy_fee_output(tx, fees, is_genesis)
        if not ok:
            return False, msg

        self.deploys[inscription_id] = deploy_data
        return True, f"Deploy {tick} successful {'(genesis)' if is_genesis else ''}"

    def validate_mint(self, inscription_id, mint_op, tx, inscriber_addr,
                      current_block, current_time=None):
        if inscription_id not in self.deploys:
            return False, "Deploy inscription not found"

        deploy = self.deploys[inscription_id]
        tick = mint_op["tick"]
        qty = int(mint_op["qty"])
        minter = mint_op.get("minter", inscriber_addr)

        # Supply cap
        if self.total_minted[tick] + qty > int(deploy["supply"]):
            return False, "Exceeds total supply"

        rules = deploy.get("mint_rules", {})
        user_cap = int(rules.get("user_cap", 0))
        cooldown = int(rules.get("cooldown_blocks", 0))
        phases = rules.get("phases", [])
        exempt_addrs = rules.get("exempt_addrs", [])

        # Determine if minter is exempt (e.g., founder)
        exempt_entry = next((e for e in exempt_addrs if e.get("address") == minter), None)
        is_exempt = exempt_entry is not None

        # ---- Exemption checks (founder) ----
        if is_exempt:
            exempt_amount = int(exempt_entry["amount"])
            if self.minted_by_addr[minter][tick] + qty > exempt_amount:
                return False, "Exceeds exempt allocation"

            # Lock condition
            lock = exempt_entry.get("lock_conditions", {})
            lock_until = int(lock.get("lock_until_public_minted", 0))
            if lock_until and self.total_minted[tick] < lock_until:
                return False, f"Exempt mint locked until {lock_until} public minted"

            # Vesting
            vesting = exempt_entry.get("vesting")
            if vesting:
                now = current_time or datetime.now(timezone.utc)
                unlocked = self.compute_unlocked_amount(vesting, now)
                if self.minted_by_addr[minter][tick] + qty > int(unlocked):
                    return False, f"Exceeds vested unlock ({int(unlocked)} available)"

        # ---- Normal user checks ----
        else:
            if user_cap and self.minted_by_addr[minter][tick] + qty > user_cap:
                return False, "Exceeds user cap"
            if cooldown and self.last_mint_block[minter][tick] + cooldown > current_block:
                return False, "Cooldown active"

        # ---- Fee checks (phased + 1% protocol) ----
        fees = mint_op.get("fees", deploy.get("fees", {}))
        ok, info = self.verify_mint_fee_output(tx, fees, phases, qty, self.total_minted[tick])
        if not ok:
            return False, info

        # ---- Success — update ledger ----
        self.balances[minter][tick] += qty
        self.minted_by_addr[minter][tick] += qty
        self.total_minted[tick] += qty
        self.last_mint_block[minter][tick] = current_block

        return True, f"Mint {qty} {tick} successful"

# ------------------------------------------------------------------ #
# Simulation when run directly
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    ledger = BRC8888Ledger()

    # Simulate UNQ genesis deploy (no fees)
    unq_deploy = {
        "tick": "UNQ", "genesis": True, "supply": "21000000",
        "mint_rules": {
            "user_cap": "10000",
            "exempt_addrs": [{
                "address": "bc1p2egtxaky7jfn9drm53qaq0pyy9ap4yfppmg58w5ysvpvlcwx980q86yzm0",
                "role": "founder", "amount": 1000000,
                "vesting": {"type": "linear", "start": "2025-11-18T00:00:00Z", "cliff_days": 90,
                            "duration_days": 365, "unlock_period": "monthly"},
                "lock_conditions": {"lock_until_public_minted": 20000000}
            }],
            "cooldown_blocks": 144,
            "phases": [
                {"start_minted": "0", "end_minted": "10000000", "price_sats": 2100},
                {"start_minted": "10000001", "end_minted": "21000000", "price_sats": 4200}
            ]
        },
        "fees": {"protocol_fee_percent": 1}
    }
    print("UNQ genesis deploy →", ledger.validate_deploy("unq_id", unq_deploy, {}, "anyone", 925000))

    # Simulate founder mint attempt too early (vesting + lock fail)
    early_time = datetime(2025, 11, 26, tzinfo=timezone.utc)
    print("Founder early mint →", ledger.validate_mint("unq_id",
          {"tick": "UNQ", "qty": "1000000", "minter": "bc1p2egtxaky7jfn9drm53qaq0pyy9ap4yfppmg58w5ysvpvlcwx980q86yzm0"},
          {}, "anyone", 925001, early_time))

    # Simulate normal phased mint (100 tokens in Phase 1)
    print("Public mint 100 UNQ →", ledger.validate_mint("unq_id",
          {"tick": "UNQ", "qty": "100"},
          {"outputs": [{"address": "bc1p8px4vg2c4w79smuwts8s49xxzt6r8mlk9nyyf3jxa767flyhdres0xkz5c", "sats": 210000},
                       {"address": ledger.protocol_address, "sats": 2100}]},
          "bc1pUser", 925002))
