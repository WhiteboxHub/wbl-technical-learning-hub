# System Design Course Table of Contents & Syllabus

Based on Whitebox Learning Agentic AI Engineering Program (Week 1 PM: Architecture & Cloud).
Running Application: **The Growing City URL Shortener & Scaling Stack**.

---

## Module Breakdown

### Module 1: Client-Server Architecture, Scaling & Statelessness
1. The Client-Server Model and Request Lifecycle (Client, DNS, Reverse Proxy, App Server, DB).
2. Vertical Scaling (Scale-Up): Hardware limits, cost curves, and single point of failure (SPOF).
3. Horizontal Scaling (Scale-Out): Commodity hardware, elasticity, and redundancy.
4. The Non-Negotiable Rule of Statelessness: Externalizing state to DB/cache.

### Module 2: Load Balancing & Traffic Routing
1. The Role of the Load Balancer (Reverse Proxy) as the entry door to horizontal scale.
2. Balancing Algorithms: Round Robin, Least Connections, and IP Hash (consistent hashing).
3. Layer 4 (Transport / TCP) vs. Layer 7 (Application / HTTP) Load Balancing.
4. Active vs. Passive Health Checks and Graceful Degradation.

### Module 3: Caching & Cache Strategies (The Corner Shop)
1. The Memory Hierarchy: RAM vs SSD vs Network Database latency.
2. The 80/20 Pareto Principle in System Design.
3. Caching Topologies: In-memory cache vs Distributed Cache (Redis/Memcached).
4. Patterns: Cache-Aside (Lazy Loading), Write-Through, and Write-Back.
5. Invalidation, TTL (Time-To-Live), and Mitigating Cache Stampedes (Thundering Herd).

### Module 4: Message Queues & Asynchronous Decoupling (The Depot)
1. Synchronous Blocking RPCs vs. Asynchronous Decoupled Queues.
2. Peak Shaving (Load Leveling) and Buffering Traffic Bursts.
3. The Producer-Consumer Pattern and Dynamic Worker Pool Scaling.
4. Delivery Semantics (At-least-once, At-most-once) and Consumer Idempotency.

### Module 5: The Database as the Usual Bottleneck
1. Why Databases Jam First: Statefulness, ACID Locks, and Disk I/O.
2. Read-Heavy vs. Write-Heavy Workloads.
3. Primary-Replica (Master-Slave) Architecture for Read Scaling.
4. Replication Lag, Eventual Consistency, and Read-Your-Own-Writes Guarantees.
5. Partitioning and Horizontal Sharding: Shard Keys, Cross-Shard Joins, and Operational Costs.

### Module 6: Monolith vs. Microservices: Honest Costs Both Ways
1. Monolith First: Why 90% of systems should start under one roof (zero network hops, atomic transactions).
2. The Fallacies of Distributed Computing.
3. True Costs of Microservices: Network failure modes, distributed debugging, tracing, and infrastructure sprawl.
4. Domain-Driven Design (DDD): Bounded Contexts and Justified Reasons to Split.

### Module 7: The Repeatable 5-Step System Design Method
1. Step 1: Requirements & Scope (Functional, Non-Functional, Out-of-Scope).
2. Step 2: Capacity Estimation (Back-of-the-envelope math, QPS, storage, bandwidth).
3. Step 3: High-Level Architecture Sketch.
4. Step 4: Bottleneck Identification (Finding where the city jams first).
5. Step 5: Trade-off Defense (Naming the price of every chosen lever).

### Module 8: Capstone Studio & Fault-Finding Workshop
1. End-to-End Live Walkthrough across all 6 architectural hops.
2. Live Fault-Finding Incident Triage (`scripts/break.sh`):
   - Fault 1: Cache Outage (`redis-down`)
   - Fault 2: Database Bottleneck (`db-bottleneck`)
   - Fault 3: Aggressive Rate Limiting (`rate-limit`)
   - Fault 4: Queue Worker Stalled (`queue-backlog`)
3. Candidate Project Presentations: Defending the 1M-User Photo-Sharing Platform Design.
4. Program Exit Gate Verification.
