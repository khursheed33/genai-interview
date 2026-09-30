#!/usr/bin/env bash
set -euo pipefail
uv sync --group dev
cp -n .env.example .env || true
pre-commit install
echo "Done. Run: make up && make test"
