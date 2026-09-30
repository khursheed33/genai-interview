# 05 — Crypto & TLS: Grinder, Locker, Postcard (hash vs enc vs encoding)

## 1. The trio (interviewers LOVE this)

| | Hash | Encryption | Encoding |
|---|---|---|---|
| Story | Coconut grinder (one-way, fixed chutney) | Locker with key (reversible) | Postcard in Hindi→English letters (readable by all!) |
| Reversible? | NO | YES (with key) | YES (no key — NOT security!) |
| Examples | SHA-256, **bcrypt/argon2** (passwords) | AES-256 (data), RSA (keys) | base64, hex, URL-encode |
| Fails when | rainbow tables (unsalted!) | key leaks | thinking base64 "hides" secrets |

- **Passwords**: `argon2id` (first choice) / `bcrypt` (cost 12) with RANDOM per-user salt + server-side **pepper** (from Vault, rotated). Verify in constant time (`hmac.compare_digest`). NEVER MD5/SHA1/plain, never reversible. Demo KDF with stdlib PBKDF2 in `../examples/01_password_hashing.py` (same salt+pepper principles).
- **Symmetric (AES-256-GCM)** = one key locks+unlocks (fast, bulk data; GCM adds tamper alarm). **Asymmetric (RSA/ECDSA)** = public locks, private unlocks (slow; used for key exchange + signatures like RS256).

## 2. Keys live in vaults, not code (KMS/HSM/envelope)

- **Envelope encryption**: data-key encrypts files (fast, per-file) → KMS **wraps** data-keys with a master key → master lives in **HSM** (tamper-proof hardware). Leak a data-key = one file; rotate master without re-encrypting everything.
- **Secrets**: Vault / AWS Secrets Manager / Key Vault → injected as env at deploy; rotation = new version + rolling restart; audit "who read prod key?" (see topic 03 config).

## 3. TLS handshake in 4 passes (what `curl -v` shows)

```
1. ClientHello (ciphers + random) → 2. ServerHello + cert chain + ServerHelloDone
3. client verifies chain → CA? → expiry? → hostname? → sends pre-master (encrypted with server pubkey / ECDHE)
4. both derive session keys → Finished → encrypted app data (AES-GCM)
```

- **Chain**: leaf (your domain) → intermediate(s) → root CA (in OS trust store). Serve the FULL chain (missing intermediate = mobile-app-only failures — classic!). **Let's Encrypt**: free 90-day certs via ACME (`certbot`), auto-renew at 60 days.
- **mTLS**: BOTH sides show certs (service mesh internal APIs, bank callbacks). Server verifies client cert against private CA → spoof-proof service identity (way stronger than API keys!).

One-liner: **"Hash passwords (argon2+salt+pepper), encrypt data (AES-GCM via envelope), encode NEVER for secrets; TLS verifies chain+host, mTLS for service-to-service."**
