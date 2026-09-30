# Contributing

This is a personal practice repo, but keep it interview-ready:

1. One topic at a time: create/update `notes/`, `examples/`, `exercises/`, `interview-questions.md`.
2. Keep examples minimal and runnable. Include command + expected output in the example README or docstring.
3. Never commit secrets (`.env`, keys, tokens). Use `.env.example` only.
4. Run before pushing:
   ```
   uv run ruff check . ; uv run ruff format . ; uv run pytest -q
   ```
5. PRs: fill the template, link the checklist section, add 1-3 line "interview takeaway".

## Conventions
- Topics live in `topics/` as `NN-kebab-case` (already scaffolded 01-29).
- Notes: `topics/NN-slug/notes/NN-short-name.md`, start with mental model, end with recap + one-liners.
- Exercises: `topics/NN-slug/exercises/exercise-NN-slug/README.md` with acceptance criteria.
- No large binaries/models/data in git. Use local `data/` (gitignored) or releases.
