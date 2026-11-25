# Module 7: The Repeatable 5-Step System Design Method

Story anchor: **The Growing City**. An urban planner does not start by pouring concrete or buying lampposts. They ask: How many people live here? How many cars enter at rush hour? What happens if the river floods? System design is a repeatable methodology, not a guessing game.

## Objectives
By the end of this module, candidates can:
1. Master the standard **5-step system design framework**:
   - Step 1: Requirements & Scope (Functional vs Non-Functional)
   - Step 2: Scale & Capacity Estimation (Back-of-the-envelope math)
   - Step 3: High-Level Architecture Sketch (Data flow & core components)
   - Step 4: Bottleneck Identification (Finding where the city jams first)
   - Step 5: Trade-offs & Deep Dive (Defending decisions and naming their costs)
2. Perform back-of-the-envelope calculations for QPS, bandwidth, and storage.
3. Successfully drive a 45-minute technical system design interview.

## Stack Requirements
- Running stack: None required (Conceptual framework & Whiteboard methodology).

---

### Beat 7.1 — Step 1: Requirements & Scope
- **Slides:** Step 1 Template: Functional vs Non-Functional Requirements.
- **Say:**
  - Never start drawing boxes immediately in a system design session. That is an instant failure.
  - **Functional Requirements**: What the system does for the user.
    - Example (URL Shortener): User enters URL -> gets short code. User visits short code -> redirected to original URL. Custom alias support.
    - Explicitly state out-of-scope: No user login required in V1, no private links.
  - **Non-Functional Requirements**: System qualities and constraints.
    - Availability: 99.9% uptime (3 9s).
    - Latency: Redirection must be under 20ms.
    - Read-to-write ratio: Highly read-heavy (100:1).
- **Demo (run: instructor):**
  - Live whiteboard demonstration: writing out the 3 functional and 3 non-functional requirements for the URL Shortener.
- **Ask:**
  - Q: Why is defining out-of-scope features as important as defining in-scope features?
  - A: It prevents scope creep and keeps the design focused on core architectural challenges within the available time.
- **Done when:** Candidates write 3 functional and 3 non-functional requirements before touching architecture.

---

### Beat 7.2 — Step 2: Back-of-the-Envelope Estimation
- **Slides:** Math Cheat Sheet: Seconds in a day (~100,000), powers of 2 (2^10=1KB, 2^20=1MB, 2^30=1GB), QPS conversion.
- **Say:**
  - Math numbers to memorize: **86,400 seconds in a day ≈ 100,000 seconds**.
  - **Traffic Estimation (QPS - Queries Per Second)**:
    - 10 million write requests per month = 10,000,000 / (30 * 100,000) = ~3.3 writes/second.
    - If read ratio is 100:1 -> Read QPS = 3.3 * 100 ≈ 330 reads/second. Peak QPS (2x-5x) = ~1,500 reads/second.
  - **Storage Estimation**:
    - Each record: `short_code` (7 bytes) + `original_url` (500 bytes) + `timestamp` (8 bytes) ≈ 500 bytes.
    - 10M records/month * 500 bytes = 5 GB/month -> 60 GB/year -> 300 GB over 5 years.
    - Realization: 300 GB fits comfortably on a single modern SSD! We do NOT need distributed NoSQL sharding for storage volume alone.
- **Demo (run: agent):**
  - Walk through how back-of-the-envelope calculations dictate whether you actually need complex distributed systems.
- **Ask:**
  - Q: How many seconds are in a day, and why do engineers round it to 100,000 in design calculations?
  - A: 86,400 seconds. Rounding to 100,000 enables instant mental arithmetic and provides a built-in safety margin for peak loads.
- **Done when:** Candidates calculate QPS, storage/year, and bandwidth from raw user counts.

---

### Beat 7.3 — Steps 3, 4, 5: Sketch, Bottlenecks, and Trade-Offs
- **Slides:** Complete Architecture Blueprint: DNS -> CDN/LB -> App Cluster -> Cache -> Primary/Replica DB -> Async Queue -> Analytics.
- **Say:**
  - **Step 3: Sketch**: Connect Client -> Load Balancer -> App Servers -> Cache -> Database. Trace the write path and read path.
  - **Step 4: Bottlenecks**: Ask yourself: "Where will my city jam first?"
    - Is it database read throughput? (Add Redis cache).
    - Is it database write spikes? (Add message queue buffer).
    - Is it single point of failure? (Add standby replica and redundant load balancers).
  - **Step 5: Trade-offs**: Name the price of every lever out loud.
    - "I added Redis to reduce read latency to 2ms, but the trade-off is cache staleness and memory cost."
    - "I used asynchronous queues for analytics, accepting eventual consistency instead of real-time accuracy."
- **Demo (run: instructor):**
  - Complete the full 5-step diagram on the whiteboard, walking through the trade-off debate.
- **Ask:**
  - Q: What separates a junior engineer from a senior engineer during a system design review?
  - A: A junior engineer names components; a senior engineer identifies bottlenecks and defends the trade-offs of each choice.
- **Done when:** Candidates can walk through the 5 steps without hesitation.

---

## Exercise (~25 min)
1. Pick a scenario: **Design a Photo-Sharing Service (1M daily active users, 1 photo upload/day, 20 photo views/day)**.
2. Apply the 5 steps on paper or digital whiteboard:
   - Calculate Upload QPS and View QPS.
   - Calculate Image Storage per year (assuming 2MB per photo).
   - Draw the diagram with Blob Storage (S3), Metadata DB, Cache, and CDN.
   - Name 3 bottlenecks and defend 1 major trade-off.

## Done-Check
- [ ] Memorized the 5-step framework in order.
- [ ] Can estimate QPS and storage requirements using back-of-the-envelope math.
- [ ] Understands the role of CDN and object storage for binary media.
- [ ] Completed the 1M-user photo-sharing design draft.

## Clean-Up
None.
