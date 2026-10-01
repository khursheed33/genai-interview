# Software Architecture Notes

## Boundaries
Architecture defines responsibility and dependency boundaries. A modular monolith can provide strong boundaries without distributed-system cost. Microservices add deployment and failure isolation but also network, data, and operational complexity.

## Clean and hexagonal architecture
A useful dependency direction is API/UI → application use case → domain ← ports ← infrastructure adapters. Business rules should not depend on a database or framework.

## DDD and events
DDD introduces bounded contexts, aggregates, entities, value objects, and domain events when domain complexity justifies them. Event-driven systems improve decoupling but require handling eventual consistency, duplicates, replay, and versioning. CQRS separates read/write models when their needs differ.

## Migration and SaaS
API gateways centralize cross-cutting concerns; BFFs shape APIs for a client; the strangler pattern replaces legacy capabilities incrementally. Multi-tenancy trades isolation against operational cost. Enforce tenant identity at data-access boundaries.

## Practice
Refactor CRUD into ports/adapters, design an outbox workflow, compare modular monolith vs microservices in an ADR, and design shared-schema vs separate-schema tenancy.