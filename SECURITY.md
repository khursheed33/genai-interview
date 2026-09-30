# Security Policy

- Do not commit API keys, tokens, certs, or customer data.
- Report suspected leaked secrets by rotating the key immediately and purging history if needed.
- Local practice infra (`docker-compose.yml`) binds to localhost only by default.
- Dependencies: enable Dependabot (add later via GitHub settings) + `uv lock` review for major bumps.
