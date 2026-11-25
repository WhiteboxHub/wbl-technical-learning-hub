# Module 5: The Database as the Usual Bottleneck

Story anchor: **The Growing City**. The central bank's records room is overflowing. Adding more bank tellers (app servers) doesn't help because all tellers must queue up at the same single ledger book (database). The ledger is the true bottleneck.

## Objectives
By the end of this module, candidates can:
1. Explain why the database is almost always the first bottleneck in scaling.
2. Differentiate read-heavy vs write-heavy workloads.
3. Design a database scaling progression: Indexes -> Caching -> Read Replicas -> Partitioning/Sharding.
4. Explain replication lag and eventual consistency in master-replica setups.

## Stack Requirements
- Running stack: `scripts/setup.sh` (or `docker compose -f docker-compose.yml -f docker-compose.nocache.yml up -d`)

---

### Beat 5.1 — Why the Database Jams First
- **Slides:** Diagram: 10 Stateless App Nodes hitting 1 Relational Database.
- **Say:**
  - App servers are cheap and easy to scale: just launch more stateless containers.
  - Databases manage **state**, **concurrency locks**, **ACID transactions**, and **disk I/O**.
  - As app servers multiply, database connection pools get exhausted, disk I/O hits 100%, and query latency explodes.
  - Engineers who say "let's add more web servers" when an app slows down under load make the problem worse.
- **Demo (run: agent):**
  ```bash
  # Start app with simulated database latency and no cache
  ./scripts/setup.sh --nocache
  # Measure response time when hitting the database directly
  curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"
  ```
  - **Point out:** Without the cache, every query waits on the database disk lock; response time increases by 200ms+ per request.
- **Ask:**
  - Q: Why doesn't adding more app servers solve a database bottleneck?
  - A: More app servers open more simultaneous connections and queries, causing greater lock contention and disk thrashing on the single database.
- **Done when:** Candidates articulate why stateful storage cannot scale by simple container replication.

---

### Beat 5.2 — Scaling Reads: Read Replicas & Replication Lag
- **Slides:** Diagram: Primary (Master) Write Node -> Asynchronous Replication -> Read Replicas.
- **Say:**
  - Most web apps have a 9:1 or 100:1 read-to-write ratio (e.g. Twitter: reading tweets vs posting tweets).
  - **Primary-Replica (Master-Slave) Pattern**:
    - All writes (`INSERT`, `UPDATE`, `DELETE`) go to the Primary DB.
    - The Primary streams changes to one or more Read Replicas.
    - Application routes read queries (`SELECT`) to Read Replicas.
  - **The Cost: Replication Lag & Eventual Consistency**:
    - Asynchronous replication takes time (milliseconds to seconds).
    - If a user updates their profile and immediately reloads, reading from a replica might show old data until the replica catches up ("Read-Your-Own-Writes" problem).
- **Demo (run: instructor):**
  - Discuss the architectural fix: Write to Primary, and for 5 seconds after a user write, route that user's read to Primary; all other reads go to replicas.
- **Ask:**
  - Q: A user updates their password and immediately logs in, but gets "invalid credentials". What distributed systems issue likely occurred?
  - A: Replication lag: the authentication query hit a read replica that had not yet received the password update from the primary.
- **Done when:** Candidates explain read replicas, write routing, and replication lag.

---

### Beat 5.3 — Scaling Writes: Partitioning & Sharding
- **Slides:** Diagram: Vertical Partitioning (Splitting Tables) vs Horizontal Sharding (Splitting Rows by Shard Key).
- **Say:**
  - What happens when writes exceed what a single primary database can handle?
  - **Vertical Partitioning**: Moving different tables to different databases (e.g. Users DB vs Orders DB).
  - **Horizontal Sharding**: Splitting rows of the same table across multiple database machines based on a **Shard Key** (e.g. `user_id % 4`).
  - **The Massive Cost of Sharding**:
    1. Cross-shard joins become impossible or painfully slow.
    2. Distributed transactions (2-Phase Commit) are complex and fragile.
    3. Resharding (rebalancing data when a shard fills up) is extremely risky.
    - Rule of thumb: Exhaust indexes, caching, and read replicas before considering sharding!
- **Demo (run: agent):**
  - Restore stack to cached baseline:
  ```bash
  ./scripts/fix.sh
  ```
- **Ask:**
  - Q: Why is sharding considered a last resort in database scaling?
  - A: It introduces immense operational complexity, breaks foreign key constraints, and makes cross-shard joins and transactions difficult.
- **Done when:** Candidates can list the scaling steps in order: Indexing -> Caching -> Read Replicas -> Sharding.

---

## Exercise (~15 min)
1. Write down the database scaling progression for an e-commerce platform starting with 1,000 users and growing to 10,000,000 users.
2. For each stage (1K, 100K, 1M, 10M), name the primary database scaling lever you would apply and what problem it solves.

## Done-Check
- [ ] Understands why databases become bottlenecks before web servers.
- [ ] Can explain the primary-replica architecture and read-query offloading.
- [ ] Can define replication lag and eventual consistency.
- [ ] Knows horizontal sharding and why it is avoided until absolutely necessary.

## Clean-Up
`scripts/fix.sh`
