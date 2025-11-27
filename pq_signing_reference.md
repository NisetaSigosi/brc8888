# Post-Quantum Signing Reference for BRC-8888

BRC-8888 **requires** post-quantum signatures for `evolve` operations and strongly recommends them for `u-qid` objects. This protects against future quantum attacks on ECDSA (Shor’s algorithm).

**Live example used in UNQ genesis** — fully quantum-resistant from day one.

---

### Supported NIST-Standardized Algorithms (2025)

| Algorithm       | Type      | Pubkey Size | Signature Size | Security Level | Recommended |
|-----------------|-----------|-------------|----------------|----------------|-------------|
| **Dilithium3**  | Lattice   | ~1,952 B    | ~2,420 B       | Level 3 (≈ AES-192) | **DEFAULT** |
| **Falcon-1024** | Lattice   | ~1,793 B    | ~1,280 B       | Level 5 (≈ AES-256) | Compact alternative |

**Use Dilithium3 unless you specifically need smaller signatures.**

---

### Format in JSON

```json
"quantum": {
  "post_quantum_secure": true,
  "identity_pub": "pq:dilithium3:BASE64_PUBKEY...",
  "algorithm": "dilithium3"
},

"sig_pq": "BASE64_SIGNATURE"

Installation

pip install oqs-python
(Uses liboqs — the official Open Quantum Safe library)

1. Key Generation (Air-Gapped)

import oqs
import base64

sig = oqs.Signature('Dilithium3')
public_key = sig.generate_keypair()
private_key = sig.export_secret_key()  # KEEP OFFLINE

# For deploy JSON
pub_b64 = base64.b64encode(public_key).decode()
print(f'"quantum.identity_pub": "pq:dilithium3:{pub_b64}"')

2. Signing an Evolve (Offline)

import oqs
import base64
import json

# Load private key (from secure storage)
sig = oqs.Signature('Dilithium3')
sig.import_secret_key(private_key_bytes)

# Canonical payload (sorted keys, no whitespace)
payload = {
    "ref": "68bc98a1b1e55c0ec7d5ffeae68b50d8fda0420ba5622e2ec943a87e8225d84ei0",
    "merkle_root": "sha256:3f2a9bdeadbeef...",
    "trigger": {"type": "time", "block": 925500}
}
payload_bytes = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode()

signature = sig.sign(payload_bytes)
sig_b64 = base64.b64encode(signature).decode()
print(f'"sig_pq": "{sig_b64}"')

3. Verification (Indexer Side)

import oqs
import base64
import json

# From inscription
ref = "68bc98..."
merkle_root = "sha256:3f2a9bdeadbeef..."
trigger = {"type": "time", "block": 925500}
sig_b64 = "BASE64_SIG..."
pub_b64 = "BASE64_PUB..."  # from deploy.identity_pub

# Rebuild payload
payload = json.dumps({"ref": ref, "merkle_root": merkle_root, "trigger": trigger},
                     separators=(',', ':'), sort_keys=True).encode()

# Verify
verifier = oqs.Signature('Dilithium3')
verifier.import_public_key(base64.b64decode(pub_b64))
if not verifier.verify(payload, base64.b64decode(sig_b64)):
    raise ValueError("Invalid PQ signature — reject evolve")

Best Practices

Generate keys air-gapped
Never expose private key online
Use the exact canonical format (sorted, compact JSON)
Prefer Dilithium3 (better verification speed)
Test signature round-trip before inscribing

This reference is already used in the live UNQ genesis deployment.
