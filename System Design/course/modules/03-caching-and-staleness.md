# Module 3: Caching and Cache Strategies

Story anchor: **The Growing City**. The city warehouse is 20 miles away. Every time a resident needs milk or bread, driving to the warehouse causes massive traffic. The solution: a **corner shop** (Cache) that keeps the most frequently bought goods right in the neighborhood.

## Objectives
By the end of this module, candidates can:
1. Explain the purpose of caching: reducing latency and offloading database pressure.
2. Contrast Cache-Aside, Read-Through, Write-Through, and Write-Back patterns.
3. Understand the two hardest problems: **Staleness** and **Cache Invalidation**.
4. Prevent cache stampedes (thundering herd) using Time-To-Live (TTL) and warming.

## Stack Requirements
- Running stack: `scripts/setup.sh`
- Redis `:6379`, Gateway `:8080`.

---

### Beat 3.1 — The Corner Shop: Latency & Read Offloading
- **Slides:** Diagram: Memory Hierarchy & Latency Numbers Every Programmer Should Know (RAM ~100ns vs SSD ~100μs vs Network DB ~10ms).
- **Say:**
  - Reading from RAM (Redis) is 1,000x to 100,000x faster than reading from disk or making a remote DB query.
  - 80/20 Rule (Pareto Principle): In most systems, 80% of reads target 20% of popular data (e.g., viral URLs, trending tweets, homepage catalog).
  - Caching protects the database from crashing under read traffic.
- **Demo (run: agent):**
  ```bash
  # 1st request: Cache MISS (must query DB and populate Redis)
  curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"
  # 2nd request: Cache HIT (served directly from Redis memory)
  curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"
  ```
  - **Point out:** `X-Cache: MISS` on first read vs `X-Cache: HIT` on subsequent reads, with response time dropping drastically.
- **Ask:**
  - Q: Why not cache every single piece of data in RAM?
  - A: RAM is expensive and limited in capacity compared to disk storage. You only cache hot, frequently accessed data.
- **Done when:** Candidates can explain the speedup and purpose of memory caching.

---

### Beat 3.2 — Caching Patterns: Cache-Aside vs Write-Through
- **Slides:** Flowcharts: Cache-Aside (Lazy Loading) vs Write-Through vs Write-Back.
- **Say:**
  - **Cache-Aside (Lazy Loading)**:
    - Application reads cache. If miss, app reads DB, writes to cache, and returns.
    - Advantage: Only requested data is cached; cache failures don't crash the app.
    - Disadvantage: Cache miss penalty on the first read.
  - **Write-Through**:
    - Application writes to cache and DB simultaneously.
    - Data is never stale, but write latency is higher.
  - **Write-Back (Write-Behind)**:
    - Write to cache immediately, write to DB asynchronously in background.
    - Ultra-fast writes, but risk of data loss if cache crashes before flush.
- **Demo (run: agent):**
  ```bash
  # Check cache key in Redis
  docker compose exec -T redis redis-cli GET "url:wbl"
  ```
  - **Point out:** The raw string stored in Redis key `url:wbl` matching the database record.
- **Ask:**
  - Q: In Cache-Aside, what happens if the cache is down?
  - A: The system slows down because every read hits the database, but it continues functioning (graceful degradation).
- **Done when:** Candidates can compare Cache-Aside, Write-Through, and Write-Back.

---

### Beat 3.3 — Staleness & Invalidation: The Price of Caching
- **Slides:** Two Hard Problems in CS: Naming things and Cache Invalidation.
- **Say:**
  - When the database record updates, the cache holds old, stale data.
  - Solutions:
    1. **TTL (Time-To-Live)**: Keys expire automatically after N seconds.
    2. **Explicit Invalidation**: App sends `DEL url:{code}` whenever the URL is updated or deleted.
  - What is a **Cache Stampede (Thundering Herd)**?
    - When a popular cached key expires, thousands of concurrent requests all miss at once and hammer the DB simultaneously.
- **Demo (run: agent):**
  ```bash
  # Flush cache to simulate invalidation
  curl -X POST http://localhost:8080/api/cache/flush
  # Verify immediate MISS on next read
  curl -sI http://localhost:8080/r/wbl | grep X-Cache
  ```
  - **Point out:** Purging the cache immediately forces the system back to the database until re-warmed.
- **Ask:**
  - Q: Why is TTL by itself often not enough for critical data?
  - A: Because during the TTL window, clients read stale data. Critical changes require active cache eviction.
- **Done when:** Candidates explain how staleness occurs and how TTL/invalidation manage it.

---

## Exercise (~15 min)
1. Shorten a new URL: `curl -s -X POST http://localhost:8080/api/shorten -H "Content-Type: application/json" -d '{"url":"https://google.com","custom_code":"my-search"}'`
2. Test read 1 and read 2 to observe cache transition from MISS to HIT.
3. Check system hit ratio: `curl -s http://localhost:8080/api/metrics`

## Done-Check
- [ ] Can explain the 80/20 read rule and memory hierarchy speed advantage.
- [ ] Can draw and explain the Cache-Aside pattern step by step.
- [ ] Understands TTL and cache invalidation mechanics.
- [ ] Can define a cache stampede and explain how to mitigate it.

## Clean-Up
`scripts/fix.sh`
