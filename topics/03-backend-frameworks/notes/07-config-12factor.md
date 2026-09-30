# 07 — Config & 12-Factor: One Tiffin, Many Canteens

Same code must run on your laptop, staging, and prod — only the **environment** changes. Config in code = rebuild per env = pain.

## 1. Rules (12-factor, the 5 that pay)

| Factor | Kid story | Practice |
|---|---|---|
| III Config in env | Spice level on a slip, not baked into roti | `DATABASE_URL`, `OPENAI_API_KEY` from env; defaults only for harmless stuff (`LOG_LEVEL=info`) |
| I Codebase, many deploys | One recipe, 3 canteens | same image → dev/staging/prod |
| IV Backing services as URLs | Water tap address on wall | Postgres/Redis/S3 all via URLs — swap without code |
| IX Disposability | Stall opens/closes in seconds | stateless + lifespan open/close fast; SIGTERM finishes in-flight |
| XI Logs as streams | Smoke goes to chimney, not diary | `print`/JSON to stdout → collector (Loki/CloudWatch) adds storage |

## 2. The pattern (pydantic-settings)

```python
from pydantic_settings import BaseSettings  # (uv add pydantic-settings)


class Settings(BaseSettings):
    env: str = "dev"
    database_url: str = "sqlite:///./dev.db"
    openai_api_key: str = ""  # empty in dev, REQUIRED in prod (validate!)

    class Config:
        env_file = ".env"  # local only — NEVER commit real .env!
```

- `.env` for laptop, real secrets from Vault/AWS Secrets Manager/Key Vault injected as env in prod (mounted files or sidecar). Fail fast at boot if prod secret missing (`ValueError: OPENAI_API_KEY required in prod`).
- Never log secrets; mask in `/debug/config` (`sk-***`). Rotate via env change + rolling restart (no rebuild!).

## 3. Interview checklist

- "Where do secrets live?" → env/Vault, never git (gitleaks in CI catches), never frontend bundle.
- "Dev vs prod DB?" → same code, different `DATABASE_URL`; migrations run as separate job.
- "Feature flag?" → env/config-service toggle (`NEW_RERANKER=true`) + gradual rollout — same binary, different behavior.

One-liner: **"One image, env decides; secrets from vaults, fail fast at boot, logs to stdout."**
Runnable: `../examples/06_config.py` (+ `.env.example` at repo root as the template).
