# System Design Instructor Guide

Course: **System Design — Scaling, Load Balancing, Caching, Queues, Microservices & The 5-Step Method**
Audience: Whitebox Learning Agentic AI & Engineering Program
Story Anchor: **The Growing City**

---

## 1. How the Course Works
- **Storytelling Rule**: Tell them what you are going to tell them. Tell them. Tell them what you told them.
- **The Anchor**: Every concept is anchored to the growth of a city:
  - Client = Resident
  - Network = Roads and traffic
  - Monolith = Central Market Hall
  - Load Balancer = Traffic Controller at the junction
  - Stateless Replicas = Multiple identical market stalls
  - Cache = Corner Shop with daily goods
  - Message Queue = Delivery Depot with order buffering
  - Microservices = Specialized boutique shops across the city
  - Database = The Central City Ledger
- **One Live System**: The **Growing City URL Shortener** (`api/`, `gateway/`, `worker/`, `redis/`) runs live in Docker. Demos measure real latency, real cache hits, real 429 throttling, and real worker queues.

---

## 2. Module Syllabus & Timing (8 Modules, ~3 Hours Total)

| Module | Title | Story Anchor Point | Live Demo |
|---|---|---|---|
| **1** | Client-Server, Scaling & Statelessness | The single road jams; why drivers cannot keep private state in cars. | Scale up vs out; request tracing over curl. |
| **2** | Load Balancing & Traffic Routing | Traffic controller at the roundabout directing cars down parallel streets. | 3 replicas behind Nginx; round-robin distribution. |
| **3** | Caching & Cache Strategies | The Corner Shop keeps popular groceries near homes so trips to the warehouse are rare. | Redis Cache-Aside; measuring latency: 200ms -> 2ms. |
| **4** | Message Queues & Asynchronous Decoupling | The Depot takes order tickets (202 Accepted) during morning rush so clerks don't crash. | Async write queue; worker consuming click analytics. |
| **5** | Database as the Usual Bottleneck | The bank ledger is the one book all tellers must wait to write in. | Disabling cache (`--nocache`); observing database disk lock latency. |
| **6** | Monolith vs. Microservices Trade-offs | The market hall under one roof vs. 50 separate shops across gridlocked streets. | Monolith simplicity vs microservices network failures and tracing. |
| **7** | The Repeatable 5-Step Design Method | Urban planning: requirements, capacity estimates, sketch, bottlenecks, trade-offs. | Live 25-minute design of a URL Shortener on the board. |
| **8** | Capstone Studio & Fault-Finding Workshop | Opening Day: real traffic, unexpected incidents, triage from system evidence. | `scripts/break.sh`: diagnosing 4 live production outages. |

---

## 3. Running Class with the AI Co-Pilot
Open Claude Code / Antigravity in `wbl-technical-learning-hub/System Design` and say:
`teach module 1`

### Instructor Controls:
- `next` / `back` — Advance or retreat a beat.
- `repeat` — Re-execute the live demo.
- `answer` — Reveal the hidden answer key.
- `take over` — Pause the agent while you sketch on the whiteboard.
- `jump N.M` — Jump to beat N.M.
- `status` — Show progress and pacing.
- `end` — Wrap up the module and review candidate deliverables.

---

## 4. Fault Injection Runbook (Module 8)
When conducting the live triage workshop in Module 8, use `scripts/break.sh`:

1. `./scripts/break.sh redis-down`:
   - **Symptom**: Reads still succeed, but latency increases and every request shows `X-Cache: MISS`. App logs report Redis connection timeouts.
   - **Lesson**: Graceful degradation vs database overload.
2. `./scripts/break.sh db-bottleneck`:
   - **Symptom**: Direct database reads stall for >1500ms; clients timeout.
   - **Lesson**: What happens when database locks saturate under concurrency.
3. `./scripts/break.sh rate-limit`:
   - **Symptom**: After 1 request, subsequent requests receive `429 Too Many Requests`.
   - **Lesson**: Token bucket edge throttling and client backoff.
4. `./scripts/break.sh queue-backlog`:
   - **Symptom**: Async URL creation returns `202 Accepted`, but URLs take minutes to appear in database; queue length metric climbs.
   - **Lesson**: Worker crashes, queue monitoring, and backpressure.

Always run `./scripts/fix.sh` to return to a clean baseline.
