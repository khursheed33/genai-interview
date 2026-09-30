$ErrorActionPreference = "Stop"
uv sync --group dev
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }
pre-commit install
Write-Host "Done. Run: make up; make test"
