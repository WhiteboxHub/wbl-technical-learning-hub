# System Design Stack Backlog & Verification

**Status: All components are built, containerised, and verified.**
Running application example: **The Growing City URL Shortener Service** (`api/`, `worker/`, `gateway/`, `redis/`, `db/`).

| ID | Component | Needed By | What Was Built | Verification Check |
|---|---|---|---|---|
| **API** | Stateless FastAPI Service | M1, M2, M3, M4, M5, M6, M7, M8 | URL Shortener with sync DB write and async queue ingestion. Returns instance ID in response headers. | `curl -sf http://localhost:8000/health` returns `healthy` + instance id. |
| **STATELESS** | State Externalisation | M1, M2 | No server-side session or memory state stored in the container; all state in DB and Redis. | Spin up 3 replicas; requests route freely with zero session drop. |
| **GATEWAY** | Nginx Load Balancer | M2, M6, M8 | Reverse proxy with round-robin load distribution, `X-Request-Id`, upstream header tracking, and rate limiting (`429`). | `curl -sI http://localhost:8080/r/wbl` shows `X-Handled-By` and `X-Request-Id`. |
| **CACHE** | Redis Cache-Aside | M3, M8 | Redis caching short URL target redirects with configurable TTL and hit/miss counters. | 1st read returns `X-Cache: MISS`; 2nd read returns `X-Cache: HIT`. |
| **QUEUE** | Background Depot Worker | M4, M8 | Python worker consuming `shorten:queue` and `analytics:queue` from Redis. | Async shorten returns `202 Accepted`; worker records DB item without blocking read path. |
| **BOTTLENECK** | Database Delay Simulator | M5, M8 | `SIMULATE_DB_DELAY` and `NO_CACHE` flags to simulate disk locking and database saturation. | Load test with `docker-compose.nocache.yml` shows latency spikes from 2ms to 200ms+. |
| **FAULTS** | Break-it Fault Injector | M8 | `scripts/break.sh` injecting 4 real-world failure modes (`redis-down`, `db-bottleneck`, `rate-limit`, `queue-backlog`). | All faults injected, symptoms isolated, and restored via `scripts/fix.sh`. |
