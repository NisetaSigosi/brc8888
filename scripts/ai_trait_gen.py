#!/usr/bin/env python3
"""
Simple AI trait generator demo for BRC-8888 evolvable objects.
Generates deterministic dynamic traits based on a seed (e.g., for u-ai objects).
Uses stdlib random for reproducibility; hash seed for Merkle-compatibility.

Usage:
  python3 scripts/ai_trait_gen.py <seed> [--num-traits N] [--output json]

Example: python3 ai_trait_gen.py "my_seed_123" --num-traits 5
"""

import argparse
import hashlib
import json
import random
import sys

TRAIT_CATEGORIES = ["color", "element", "power", "rarity", "mood"]
TRAIT_OPTIONS = {
    "color": ["red", "blue", "green", "gold", "silver"],
    "element": ["fire", "water", "earth", "air", "ether"],
    "power": ["strength", "speed", "intelligence", "agility", "luck"],
    "rarity": ["common", "uncommon", "rare", "epic", "legendary"],
    "mood": ["happy", "angry", "calm", "excited", "mysterious"]
}

def generate_traits(seed: str, num_traits: int) -> dict:
    """Generate deterministic traits using hashed seed for random state."""
    # Hash seed to int for random.seed (SHA256 for BRC-8888 consistency)
    seed_hash = hashlib.sha256(seed.encode('utf-8')).digest()
    seed_int = int.from_bytes(seed_hash, 'big')
    random.seed(seed_int)
    
    traits = {}
    selected_categories = random.sample(list(TRAIT_OPTIONS.keys()), min(num_traits, len(TRAIT_OPTIONS)))
    for cat in selected_categories:
        traits[cat] = random.choice(TRAIT_OPTIONS[cat])
    
    return traits

def main() -> int:
    p = argparse.ArgumentParser(description="Generate AI evolvable traits for BRC-8888 demo.")
    p.add_argument("seed", help="Seed string for deterministic generation (e.g., model_hash or txid).")
    p.add_argument("--num-traits", type=int, default=3, help="Number of traits to generate (1-5).")
    p.add_argument("--output", choices=["json", "text"], default="json", help="Output format (json or text).")
    args = p.parse_args()
    
    if args.num_traits < 1 or args.num_traits > 5:
        print("Error: num_traits must be between 1 and 5.", file=sys.stderr)
        return 1
    
    traits = generate_traits(args.seed, args.num_traits)
    
    if args.output == "json":
        print(json.dumps(traits, indent=2))
    else:
        for k, v in traits.items():
            print(f"{k}: {v}")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
