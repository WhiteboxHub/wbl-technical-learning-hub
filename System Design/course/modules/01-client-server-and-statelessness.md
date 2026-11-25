# Module 1: Client-Server Architecture, Scaling & Statelessness

Story anchor: **The Growing City**. A village has one small road connecting homes to the central market. As the population swells, the single road and market counter jam.

## Objectives
By the end of this module, candidates can:
1. Draw a client-server architecture and trace one request across client, network, application tier, and storage.
2. Differentiate vertical scaling (scale-up) from horizontal scaling (scale-out) with honest hardware limits.
3. Explain why **statelessness** in the application tier is the non-negotiable prerequisite for horizontal scaling.
4. Demonstrate how state externalization (to database or cache) enables seamless instance replication.

## Stack Requirements
- Running stack: `scripts/setup.sh`
- Port 8000 (direct app) and 8080 (gateway).

---

### Beat 1.1 — The Client-Server Model & Request Journey
- **Slides:** Whiteboard / Diagram 1 (Client, DNS, Reverse Proxy, App Server, Database).
- **Say:**
  - Every application starts as a client asking a server for work.
  - The client is the resident; the server is the market stall.
  - The network is the road: latency, packet loss, and connection setup happen here.
  - Trace `GET /r/wbl`: Client DNS lookup -> TCP handshake -> HTTP Request -> App reads storage -> HTTP Response.
- **Demo (run: agent):**
  ```bash
  curl -v http://localhost:8000/r/wbl
  ```
  - **Point out:** The connection to `127.0.0.1:8000`, the HTTP request headers, and the HTTP 302 redirect response with the `Location` header.
- **Ask:**
  - Q: Where does the physical boundary lie between the client and the server?
  - A: The network. Everything outside your machine is untrusted, subject to latency, and can drop packets.
- **Done when:** Candidates can draw the 4 boxes (Client, Network, App, DB) and trace a single request.

---

### Beat 1.2 — Vertical vs. Horizontal Scaling
- **Slides:** Diagram 2 (Bigger Server vs. More Servers).
- **Say:**
  - Vertical scaling (Scale Up): Buying a bigger truck with more CPU and RAM.
    - Advantages: Zero code changes, no distributed systems complexity.
    - Hard limits: Cost curve becomes exponential; maximum hardware ceiling; single point of failure (SPOF).
  - Horizontal scaling (Scale Out): Buying a fleet of standard delivery vans.
    - Advantages: Elasticity, fault tolerance, no theoretical ceiling.
    - Cost: Requires load balancing and stateless application nodes.
- **Demo (run: agent):**
  ```bash
  curl -s http://localhost:8000/health | grep instance_id
  ```
  - **Point out:** The single node identity (`standalone-instance`). If this process dies, all incoming traffic fails.
- **Ask:**
  - Q: Why can't we simply scale vertically forever?
  - A: Physical hardware limits, exponential pricing at top specs, and vertical scaling still leaves a single point of failure.
- **Done when:** Candidates can explain the economic and architectural boundaries of scale-up vs scale-out.

---

### Beat 1.3 — The Statelessness Rule
- **Slides:** Diagram 3 (Stateful Server vs. Stateless Server + Shared State).
- **Say:**
  - "Horizontal scaling only works if no driver keeps private state in their car."
  - If Server A remembers user login in local RAM, and the next request hits Server B, the user is logged out.
  - In a stateless application tier, every instance is interchangeable. Any server can handle any request.
  - Where does the state go? It is externalized into the database or distributed cache.
- **Demo (run: agent):**
  ```bash
  # Start scaled replicas
  docker compose -f docker-compose.yml -f docker-compose.scale.yml up -d
  # Send 3 requests through load balancer
  curl -sI http://localhost:8080/health | grep X-Handled-By
  curl -sI http://localhost:8080/health | grep X-Handled-By
  curl -sI http://localhost:8080/health | grep X-Handled-By
  ```
  - **Point out:** Each request lands on a different replica (`replica-node-1`, `replica-node-2`, `replica-node-3`), yet returns identical responses because state is shared in the DB/Redis volume.
- **Ask:**
  - Q: What breaks horizontal scaling immediately if an engineer isn't careful?
  - A: Storing state (session variables, uploaded files, local in-memory caches) inside the application instance memory.
- **Done when:** Candidate states: "Instances must be stateless, with state externalized to DB or cache."

---

## Exercise (~15 min)
1. Query the health endpoint across the scaled cluster 10 times:
   `for i in {1..10}; do curl -sI http://localhost:8080/health | grep X-Handled-By; done`
2. Identify how many unique instance IDs responded.
3. Write a 3-sentence justification answering: "Why would storing user session tokens in local memory fail in this architecture?"

## Done-Check
- [ ] Can draw client, load balancer, multiple app nodes, and database.
- [ ] Can explain vertical vs horizontal scaling trade-offs.
- [ ] Can define statelessness in plain technical terms.
- [ ] Verified live request distribution across container instances.

## Clean-Up
`scripts/fix.sh`
