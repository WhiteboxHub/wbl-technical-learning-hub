# Module 13 — Microservices (detailed TOC, draft v1)

Status: **Have** (slides 81–104, theory only) · **Thin** · **Add**. Needs a demo for every concept.

## 13.1 The world before microservices
- N-tier client/server, shared database
Slide 82 · **Have**

## 13.2 Monolith
- Single deployable unit: UI, logic, data together
- Strengths (simple, one deploy, easy debugging) and limits (scaling, slow releases, tech lock-in, blast radius)
Slides 83, 84 · **Have**

## 13.3 What are microservices
- Small, independent, single-purpose, own their data, communicate over the network
- Companies: Amazon, Netflix, eBay; when not to use microservices
Slides 85, 89, 90 · **Have** (add "when not to")

## 13.4 Characteristics and components
- Independent deployment, decentralized data, API contracts, automation
- Components: services, gateway, registry, config, message broker
Slides 86–88 · **Have**

## 13.5 Splitting the HR monolith
- Bounded contexts: employees, departments, leave, payroll
- Database per service; no shared tables
- Cross-service data: `employee.department_id` and the departments service
**Add** · Demo: split the monolith into two services

## 13.6 Domain-Driven Design
- Domain, subdomain, bounded context, entities, value objects, aggregates, ubiquitous language
- Layers in DDD
Slides 95, 96 · **Have** (HR examples)

## 13.7 Service communication
- Synchronous: REST, gRPC
- Asynchronous: message queues/brokers, events (RabbitMQ, Kafka)
- Choosing; coupling and failure modes
Slides 101–104 · **Have**

## 13.8 Service discovery and load balancing
- Registry (Consul/Eureka), DNS-based discovery (Docker Compose DNS)
- Client-side vs server-side load balancing
Slide 91 · **Thin**

## 13.9 Resilience patterns
- Timeouts, retries with backoff, **circuit breaker** (closed/open/half-open), bulkhead, fallback
- Cascading failures
Slide 91 · **Thin** · Demo: stop departments-service and watch the circuit open

## 13.10 Architectural patterns
- API gateway (see Module 12), CQRS, event sourcing, saga (Stretch)
Slides 93, 94, 97–100 · **Have**

## 13.11 CQRS and event sourcing
- Commands vs queries, separate models
- Events as source of truth: `EmployeeHired`, `SalaryChanged`
Slides 97–100 · **Have** (concept only, HR examples)

## 13.12 Distributed data (Stretch)
- No cross-service transactions; eventual consistency; saga (orchestration vs choreography)

## 13.13 Operating microservices
- Containers and Compose, health checks, config, logging with correlation ID, tracing (awareness)
**Add**

## 13.14 Testing and deployment
- Contract testing, test pyramid, CI/CD per service
**Add** (Stretch)

## Labs
1. `docker compose up`: gateway + employees + departments + postgres
2. Call across services (employee with department details)
3. Kill a service; observe timeouts, then add a circuit breaker
4. Publish `EmployeeHired` to a queue; a second service reacts
5. Candidate exercise: add a `leave-service` with its own database

## Candidate question bank (sample)
- Monolith vs microservices: when stay with a monolith?
- Why a database per service?
- What does a circuit breaker do?
- Sync vs async communication?

## Slide work
- **Fix:** HR examples throughout; trim and sequence 91–104
- **Add:** splitting the monolith, resilience, operations (about 10 slides)
- Image-only slides 87, 88, 92, 98, 100, 103 need review
