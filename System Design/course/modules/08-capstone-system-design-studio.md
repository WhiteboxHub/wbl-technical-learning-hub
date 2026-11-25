# Module 8: Capstone Studio & Fault-Finding Workshop

Story anchor: **The Growing City — Opening Day**. The city is built: roads paved, traffic controller at the roundabout, corner shops stocked, and delivery depots staffed. Today is opening day: real traffic surges into the streets, unexpected faults occur, and the engineers must diagnose and fix each incident using system evidence.

## Objectives
By the end of this capstone module, candidates can:
1. Trace an end-to-end request from Client -> Load Balancer -> Stateless App -> Cache -> DB -> Queue -> Worker, naming every system design concept live.
2. Diagnose and triage **4 real-world production failure modes** using status codes, headers, and logs (`scripts/break.sh`).
3. Present and defend a complete one-page system design for a **1M-user application** in front of peers.
4. Pass the System Design Exit Gate with demonstrable evidence.

## Stack Requirements
- Running stack: `scripts/setup.sh`
- Fault scripts: `scripts/break.sh` and `scripts/fix.sh`
- Port 8080 (Gateway), 8000 (App), 6379 (Redis).

---

### Beat 8.1 — End-to-End System Walkthrough
- **Slides:** Complete System Architecture Map.
- **Say:**
  - We will now trace a request through our live running stack and map every theoretical concept onto a running container.
  - Step 1: Client requests `GET http://localhost:8080/r/wbl`.
  - Step 2: Gateway (Nginx) terminates connection, logs `X-Request-Id`, checks rate limit.
  - Step 3: Gateway routes to stateless API replica (`api-1` / `api-2` / `api-3`).
  - Step 4: API queries Redis (The Corner Shop). Returns `X-Cache: HIT` if present.
  - Step 5: On miss, API queries SQLite/Postgres (The Warehouse), populates Redis, and returns.
  - Step 6: API pushes click tracking event into Redis `analytics:queue` (The Depot).
  - Step 7: Background Worker pops event from queue and updates analytics asynchronously.
- **Demo (run: agent):**
  ```bash
  # Execute full trace demonstration
  curl -i http://localhost:8080/r/wbl
  docker compose logs worker --tail=3
  ```
  - **Point out:** The HTTP status `302`, the `X-Cache: HIT`, `X-Instance-Id`, and the worker log showing asynchronous background processing.
- **Ask:**
  - Q: Which part of this request was synchronous, and which part was asynchronous?
  - A: URL lookup and redirect were synchronous; click analytics recording was asynchronous via the queue worker.
- **Done when:** Candidates can explain the path of data across all 6 architectural hops.

---

### Beat 8.2 — The Break-It Incident Workshop
- **Slides:** Incident Triage Runbook (Status Codes, Latency Spikes, Log Inspection).
- **Say:**
  - "In production, systems do not fail politely with a warning. You must diagnose from evidence: status codes, response headers, latency numbers, and logs."
  - We will inject 4 faults one at a time. The room must diagnose the root cause before we run `fix.sh`.
- **Fault 1: Cache Outage (`redis-down`)**
  - **Instructor runs:** `./scripts/break.sh redis-down`
  - **Symptom:** Requests to `/r/wbl` still succeed, but latency spikes and `X-Cache: MISS` is returned every time. Redis connection errors appear in app logs.
  - **Diagnosis:** The cache layer crashed; application is experiencing graceful degradation by falling back to the database, but DB load is spiking.
  - **Fix:** `./scripts/fix.sh`
- **Fault 2: Database Bottleneck (`db-bottleneck`)**
  - **Instructor runs:** `./scripts/break.sh db-bottleneck`
  - **Symptom:** Direct database queries take >1500ms; gateway times out or clients experience extreme lag.
  - **Diagnosis:** Database lock contention and disk I/O saturation.
  - **Fix:** `./scripts/fix.sh`
- **Fault 3: Aggressive Rate Limiting (`rate-limit`)**
  - **Instructor runs:** `./scripts/break.sh rate-limit`
  - **Symptom:** After 1 request, subsequent requests immediately return `429 Too Many Requests` with `Retry-After: 6`.
  - **Diagnosis:** Rate limiter token bucket depleted; client must implement exponential backoff.
  - **Fix:** `./scripts/fix.sh`
- **Fault 4: Queue Worker Stalled (`queue-backlog`)**
  - **Instructor runs:** `./scripts/break.sh queue-backlog`
  - **Symptom:** URL creation returns `202 Accepted`, but URL stats show 0 clicks and URLs take minutes to appear in database. Queue length metric grows continuously.
  - **Diagnosis:** Worker process died or is stalled; orders are buffering in the queue depot without being drained.
  - **Fix:** `./scripts/fix.sh`
- **Done when:** Room correctly diagnoses all 4 failure modes from CLI curl tests and logs alone.

---

### Beat 8.3 — Candidate Project Reviews: The Photo-Sharing App
- **Activity (run: instructor & candidates):**
  - Each candidate or pair presents their one-page architecture for the **Photo-Sharing App (1M daily active users)**:
    1. Show the diagram: Client, CDN, Load Balancer, App Replicas, Redis Cache, S3 Object Store, Metadata Database, and Async Processing Queue for image resizing.
    2. Answer one "Why did you do it this way?" question:
       - "Why store image files in S3 rather than in PostgreSQL columns?"
       - "Why use an asynchronous queue for image thumbnail generation?"
       - "How do you handle a celebrity user with 10 million followers posting a photo?"
  - Peer review: One strength and one risk identified using system design vocabulary.

---

## Exit Gate — Demonstrable Outcomes
The candidate can demonstrate:
1. [ ] Walk an end-to-end request across a multi-tier system with cache and queues.
2. [ ] Diagnose a live cache crash and database bottleneck from HTTP response headers and logs.
3. [ ] Defend a completed one-page architecture design for a 1M-user application.
4. [ ] Explain vertical vs horizontal scaling, load balancing algorithms, and monolith vs microservices trade-offs without notes.

## Clean-Up
`scripts/fix.sh`
