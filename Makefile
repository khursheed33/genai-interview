.DEFAULT_GOAL := help

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "%-16s %s\n", $$1, $$2}'

setup: ## Initial setup (uv + node + pre-commit)
	uv sync --group dev
	npm install
	pre-commit install

lint: ## Ruff + mypy
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src || true

format: ## Auto-format
	uv run ruff check --fix .
	uv run ruff format .

test: ## Run pytest
	uv run pytest -q

eval-demo: ## Placeholder for LLM evals (ragas/deepeval/promptfoo per-topic)
	@echo "Add per-topic evals, e.g. topics/19-rag/exercises/*/eval.py"

up: ## Start local infra (postgres+pgvector, redis, qdrant)
	docker compose up -d

down: ## Stop local infra
	docker compose down

clean: ## Clean caches
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage*
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
