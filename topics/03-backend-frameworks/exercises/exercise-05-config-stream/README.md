# Exercise 05 — Canteen Slips + Token Tape (config + NDJSON stream)

**Story:** Staging booted with prod keys missing (silent!), and the export endpoint loads 1M rows into RAM.

## Task
In `solution.py`:
- `Settings` (pydantic-settings `BaseSettings`): fields `env="dev"`, `database_url`, `llm_key=""`; method `must_have_llm()` raising `ValueError` when `env == "prod"` and key empty; method `masked()` returning key as `first3 + "***"` or `"(empty)"`
- `ndjson(rows)` — generator yielding `json.dumps(r) + "\n"` per row (lazy!)

## Acceptance
- Prod without key raises; dev passes; `masked()` never contains the full key
- `ndjson` is a generator; `list(ndjson([{"a": 1}])) == ['{"a": 1}\n']`
