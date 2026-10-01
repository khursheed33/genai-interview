# Testing and Quality Notes

## Test pyramid
Unit tests are fast and isolate logic. Integration tests verify component boundaries. Contract/API tests verify interfaces. End-to-end tests validate important user journeys but are slower and more fragile.

## TDD and BDD
TDD cycles red → green → refactor. BDD describes behavior in terms stakeholders can understand. Neither means every line needs a test; focus on valuable behavior and failure modes.

## Static quality
Use formatting, linting, type checking, dependency/security scanning, and code review to catch cheap failures before runtime.

## GenAI testing
LLM output is often nondeterministic. Use golden datasets, structured assertions, semantic evaluators, regression suites, and production sampling. Separate retrieval failures from generation failures. Track quality alongside latency and cost.

## Practice
Write unit/integration/contract tests for an API, add mutation-resistant assertions, build a golden dataset for an LLM feature, and test a RAG pipeline for retrieval and answer quality separately.