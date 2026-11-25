# Module 6: Monolith vs. Microservices: Honest Costs Both Ways

Story anchor: **The Growing City**. The village grew around a single central market hall (Monolith). Everything is under one roof: butchers, bakers, fishmongers. As the city grows, some say "tear it down and build 50 separate boutique shops across the city!" (Microservices). But now, customers must cross gridlocked streets, and if the butcher can't reach the baker, breakfast fails.

## Objectives
By the end of this module, candidates can:
1. Explain the architectural trade-offs between monolithic architectures and microservices.
2. Defend a **monolith-first** approach for new systems and early-stage companies.
3. Identify the true costs of microservices: network failures, distributed debugging, data consistency, and operational overhead.
4. Define bounded contexts and identify when splitting a monolith is genuinely justified.

## Stack Requirements
- Running stack: `scripts/setup.sh`
- Port 8080 (Gateway).

---

### Beat 6.1 — Monolith: The Central Market Hall
- **Slides:** Diagram: Monolithic Architecture (One codebase, in-memory function calls, single database, atomic transactions).
- **Say:**
  - "Default to the market hall until pain is proven."
  - Why monoliths are exceptionally good:
    - **Performance**: Calling a function in another module takes 5 nanoseconds in memory (zero network hops).
    - **ACID Transactions**: A single database commit guarantees atomicity across orders, inventory, and billing.
    - **Simplicity**: One repository, simple deployments, trivial local development, straightforward debugging and stack traces.
  - When does a monolith actually hurt?
    - Massive engineering orgs (500+ developers) stepping on each other's code.
    - Disproportionate scaling requirements (e.g. video encoding needing 100 GPUs while the rest is simple text).
- **Demo (run: agent):**
  ```bash
  # Check monolith structure in api/app/main.py
  grep -n "@app" api/app/main.py | head -n 6
  ```
  - **Point out:** All endpoints share one runtime, memory space, and database connection. Fast, clean, and straightforward.
- **Ask:**
  - Q: What is the single biggest advantage of a monolith over microservices in early development?
  - A: Speed of iteration, refactoring ease, in-memory function calls, and atomic database transactions without network latency.
- **Done when:** Candidates can defend why 90% of projects should begin as a modular monolith.

---

### Beat 6.2 — Microservices: The True Hidden Costs
- **Slides:** The Fallacies of Distributed Computing (The network is reliable, latency is zero, bandwidth is infinite, topology doesn't change).
- **Say:**
  - Microservices trade **code complexity** for **operational complexity**.
  - In a monolith: `user = getUser(id)` is an in-memory pointer dereference (nanoseconds, 100% reliable).
  - In microservices: `user = http.get("http://user-service/users/id")`:
    - Incurs DNS resolution, TCP handshake, TLS encryption, HTTP parsing, serialization, and network latency (20ms vs 5ns).
    - What happens if the network drops? What if user-service takes 10 seconds?
    - Now you need: Service Discovery, Circuit Breakers, Retries with Exponential Backoff, Distributed Tracing (`X-Request-Id`), and eventual consistency.
- **Demo (run: agent):**
  ```bash
  # Gateway inspecting distributed request tracing
  curl -sI http://localhost:8080/health | grep -i X-Request-Id
  ```
  - **Point out:** The requirement for `X-Request-Id` across service boundaries so errors can be correlated in log aggregation systems.
- **Ask:**
  - Q: Name two real costs introduced the moment you adopt microservices.
  - A: Any two: Network failure modes, distributed debugging/tracing difficulty, data inconsistency (loss of ACID transactions), and high infrastructure/ops overhead.
- **Done when:** Candidates explain how microservices replace compiler errors with network errors.

---

### Beat 6.3 — Bounded Contexts & When to Split
- **Slides:** Domain-Driven Design (DDD) Bounded Contexts & Team Boundaries.
- **Say:**
  - Don't split services by technical layers (e.g., "controller service", "database service").
  - Split by **independent business boundaries** (Domain-Driven Design):
    - Example: Orders vs Shipping vs Recommendations.
  - Two legitimate reasons to extract a microservice:
    1. **Organizational**: Two separate engineering teams need to deploy on independent schedules without merge conflicts.
    2. **Resource Characteristics**: One component has radically different scaling needs (e.g., machine learning inference or video transcoding).
- **Demo (run: instructor):**
  - Walk through how the Worker service in our stack is decoupled from the API: it scales workers based on queue length, while the API scales on HTTP request throughput.
- **Ask:**
  - Q: If a team of 4 engineers builds a new startup product, should they start with 15 microservices? Why or why not?
  - A: No. They will spend more time managing network calls, deployment pipelines, and service contracts than writing business logic.
- **Done when:** Candidates can define a bounded context and state the two legitimate reasons to split a service.

---

## Exercise (~15 min)
1. Read a scenario: "A fintech startup with 5 developers wants to rewrite their 6-month-old working monolith into 12 microservices."
2. Write a 4-bullet point critique as a Staff Engineer advising the CTO:
   - Identify 2 hidden risks they haven't accounted for.
   - Propose an alternative (e.g. modular monolith with clean domain interfaces).

## Done-Check
- [ ] Can articulate the benefits of a monolith without bias.
- [ ] Can list the 4 primary operational costs of microservices.
- [ ] Understands why in-memory calls beat network RPCs.
- [ ] Can defend a monolith-first architecture in an interview.

## Clean-Up
`scripts/fix.sh`
