# Module 2: Load Balancing and Traffic Routing

Story anchor: **The Growing City**. The traffic junction at the entrance of the city is gridlocked. A traffic controller (Load Balancer) stands at the roundabout, directing vehicles across open parallel avenues.

## Objectives
By the end of this module, candidates can:
1. Explain the role of a Load Balancer (Reverse Proxy) as the entry point to horizontal scaling.
2. Compare Layer 4 (Transport) vs. Layer 7 (Application) load balancing.
3. Evaluate load balancing algorithms: Round Robin, Least Connections, and IP Hash.
4. Understand active/passive health checks and graceful failover.

## Stack Requirements
- Running stack: `scripts/setup.sh --scale` (Nginx gateway + 3 API replicas).
- Port 8080 (Gateway).

---

### Beat 2.1 — What a Load Balancer Does
- **Slides:** Diagram: Clients -> Load Balancer -> Pool of Stateless Servers.
- **Say:**
  - A load balancer acts as a reverse proxy sitting between the internet and internal servers.
  - Responsibilities:
    1. Distributes incoming requests across healthy worker instances.
    2. Prevents any single server from becoming overwhelmed.
    3. Provides a single public IP/domain while hiding internal infrastructure.
    4. Terminates SSL/TLS and enforces security rate limits at the edge.
- **Demo (run: agent):**
  ```bash
  # Check load balancer routing upstream pool
  cat gateway/nginx.scale.conf | grep -A 5 "upstream backend_servers"
  ```
  - **Point out:** The upstream pool definition referencing `api-1:8000`, `api-2:8000`, `api-3:8000`.
- **Ask:**
  - Q: What happens if an app server dies when behind a load balancer?
  - A: The load balancer stops routing traffic to the failed node and redirects incoming requests to healthy instances.
- **Done when:** Candidates can describe the 4 core duties of a load balancer.

---

### Beat 2.2 — Balancing Algorithms
- **Slides:** Algorithm Comparison Table (Round Robin, Least Connections, IP Hash / Consistent Hashing).
- **Say:**
  - **Round Robin**: Requests go in circular order: 1 -> 2 -> 3 -> 1. Ideal when requests take similar processing time.
  - **Least Connections**: Request goes to the server currently handling the fewest active connections. Ideal for long-lived connections (e.g. file uploads, WebSocket streams).
  - **IP Hash / Source Hashing**: Hashes client IP to assign them consistently to the same server (used for sticky sessions when an app is regrettably stateful).
- **Demo (run: agent):**
  ```bash
  ./scripts/load-test.sh http://localhost:8080/health 15
  ```
  - **Point out:** The requests distribute evenly across `replica-node-1`, `replica-node-2`, and `replica-node-3`.
- **Ask:**
  - Q: If request processing time varies wildly (some take 10ms, some take 5 seconds), which algorithm is better than Round Robin?
  - A: Least Connections, because Round Robin might pile slow jobs onto an already struggling server.
- **Done when:** Candidates justify algorithm choice for variable vs uniform workloads.

---

### Beat 2.3 — L4 vs. L7 Load Balancing
- **Slides:** OSI Layers Diagram: Transport (L4) vs Application (L7).
- **Say:**
  - **Layer 4 (Transport / TCP/UDP)**:
    - Looks only at IP address and Port.
    - Does not decrypt or inspect the HTTP payload.
    - Extremely fast, lightweight, high throughput (e.g., AWS NLB, HAProxy TCP mode).
  - **Layer 7 (Application / HTTP/HTTPS)**:
    - Inspects HTTP headers, cookies, URL paths, and query parameters.
    - Can route `/api/*` to one service and `/static/*` to another.
    - Can terminate TLS, inject `X-Request-Id`, and enforce cookie affinity (e.g., Nginx, AWS ALB).
- **Demo (run: instructor):**
  - Show how Nginx routes `/api/limited` to a rate-limiting rule while passing `/r/*` directly upstream.
- **Ask:**
  - Q: If you need to route requests based on HTTP cookies or headers, do you use L4 or L7?
  - A: Layer 7 (Application), because L4 cannot read HTTP headers or cookies.
- **Done when:** Candidates can contrast L4 and L7 balancing in performance vs intelligence.

---

## Exercise (~15 min)
1. Run `./scripts/load-test.sh http://localhost:8080/health 30`.
2. Inspect `gateway/nginx.scale.conf`.
3. Modify the upstream directive to test `least_conn;` or observe how Nginx logs upstream addresses.

## Done-Check
- [ ] Can explain how a load balancer enables horizontal scaling.
- [ ] Can differentiate Round Robin, Least Connections, and IP Hash.
- [ ] Can articulate the difference between L4 and L7 load balancers.
- [ ] Confirmed traffic distribution across 3 container replicas in practice.

## Clean-Up
`scripts/fix.sh`
