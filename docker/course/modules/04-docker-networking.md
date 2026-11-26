# Module 4 — Docker Networking & Multi-Container Communication

Teach-skill content file. Format is described in `.claude/skills/teach-docker-class/SKILL.md`.  
Story Anchor: **The Shipping Container** (Internal Port Yard Roads, Customs Gates, and Harbor Radio DNS).

## Objectives
By the end of this module, candidates can:
1. Contrast Docker's main network drivers: `bridge`, `host`, and `none`.
2. Explain why **user-defined bridge networks** provide automatic **Container DNS** resolution (and why the default `bridge` does not).
3. Avoid the #1 beginner mistake: using `localhost` inside one container to reach another container.
4. Connect multiple containers (Python API + Redis) on an isolated network using both `docker network` CLI and `docker-compose.yml`.

---

### Beat 4.1 — Network Drivers & The Harbor Yard

- **Story Anchor (The Shipping Container):**
  A port has strict security zones:
  - **`bridge` (The Dockyard Road)**: Containers sit inside a private fenced yard. They can talk to each other across internal yard lanes, while the outside world can only reach them through approved **Customs Gates** (`-p 8000:8000`).
  - **`host` (No Fence)**: The container plugs directly into the host computer's network card (no port mapping needed, no network isolation—Linux only for true host mode).
  - **`none` (Quarantine Box)**: Zero network interfaces except loopback (`lo`). Completely air-gapped for sensitive batch jobs.

- **Say (Key Talking Points):**
  - **Network Drivers**:
    - `bridge` (default): Private virtual subnet (`172.17.0.0/16` or similar) with NAT to the outside world.
    - `host`: Shares the host's network namespace directly (useful for ultra-low-latency Linux networking, loses port isolation).
    - `none`: Disables all external networking.
  - **Inspecting Networks**: `docker network ls` and `docker network inspect <net>`.

- **Ask (Check Questions):**
  - Q: Which Docker network driver would you use to run an untrusted script that must have zero internet or LAN access? — A: `none` (`--network none`).

- **Done when:** Candidates can name the three single-host network drivers and when to use each.

---

### Beat 4.2 — Default Bridge vs User-Defined Bridge (Container DNS!)

- **Story Anchor (The Shipping Container):**
  In the old **default yard** (`bridge`), containers only know each other by temporary parking-spot numbers (IP addresses like `172.17.0.3`), which change every time a container restarts!
  When you build your own **User-Defined Yard** (`docker network create harbor-net`), Docker installs a **Harbor Radio Directory (Embedded DNS at `127.0.0.11`)**. Now the API container can simply call `redis:6379` by **container name**, and Docker automatically resolves it to the right IP!

- **Say (Key Talking Points):**
  - **Default `bridge` Limitations**:
    - No automatic DNS name resolution between containers (you can only reach peers by raw IP, which breaks on restart).
    - All unrelated containers on the default bridge can see each other.
  - **User-Defined Bridge (`docker network create harbor-net`)**:
    - **Automatic DNS**: Containers on the same user-defined network resolve each other by **container name** (or Compose **service name**), e.g., `redis://redis:6379/0` or `postgresql://db:5432/hr`.
    - **Network Isolation**: Containers on `harbor-net` cannot be reached by containers on `other-net`.
  - **The `localhost` Trap**:
    - Inside `harbor-api`, `localhost` (or `127.0.0.1`) means **inside `harbor-api` itself**—NOT your laptop and NOT `harbor-redis`!
    - Always use the target **container/service name** (e.g., `redis`, not `localhost`) when one container calls another.

- **Demo / Command Trace (run: instructor):**
  Wire `redis` and `cargo-api` manually on a user-defined network:
  ```bash
  docker network create harbor-net
  docker run -d --name redis --network harbor-net redis:7-alpine
  docker run -d --name api --network harbor-net -p 8000:8000 \
    -e REDIS_URL="redis://redis:6379/0" \
    -v cargo-data:/data \
    cargo-api:1.0
  curl -s http://localhost:8000/health
  ```
  **Point out:**
  - Notice `redis` has **no `-p 6379:6379`**! It is **not** exposed to the host internet/laptop—only `api` inside `harbor-net` can reach `redis:6379`.
  - `/health` reports `"redis": "connected"` because `api` resolved `redis` via Docker's embedded DNS.
  - Clean up: `docker rm -f api redis && docker network rm harbor-net`.

- **Ask (Check Questions):**
  - Q: Why does `REDIS_URL=redis://localhost:6379/0` fail inside the `api` container even when Redis is running on the same Docker host? — A: Because `localhost` inside the `api` container refers to the `api` container's own loopback interface, not the Redis container. It must use the container/service name (`redis://redis:6379/0`) on a shared user-defined bridge network.
  - Q: Why didn't we publish `-p 6379:6379` on the Redis container? — A: Only the `api` container needs to talk to Redis; keeping Redis off host ports reduces attack surface and prevents port conflicts.

- **Done when:** Candidates can create a user-defined bridge network, attach two containers, and explain why container DNS replaces `localhost`.

---

### Beat 4.3 — Multi-Container Orchestration with `docker-compose.yml`

- **Story Anchor (The Shipping Container):**
  Instead of shouting 15 `docker run`, `docker volume create`, and `docker network create` commands to dockworkers every morning, you hand them **one master manifest (`docker-compose.yml`)** that defines the entire port—containers, volumes, networks, environment variables, and startup order—in a single declarative file.

- **Say (Key Talking Points):**
  - **What Docker Compose Does**: Reads `docker-compose.yml`, automatically creates a user-defined bridge network (`harbor-net`), creates named volumes (`cargo-data`, `redis-data`), builds images if needed, and starts services in dependency order (`depends_on` + `condition: service_healthy`).
  - **Why `service_healthy` Matters**: Plain `depends_on: [redis]` only waits for the Redis container to *start*, not for `redis-server` to finish booting and accept TCP connections. Adding `condition: service_healthy` makes `api` wait until `redis-cli ping` succeeds.
  - **Essential Compose Commands**:
    - `docker compose up --build -d`: Build images and start all services in background.
    - `docker compose ps`: Check service status and healthchecks.
    - `docker compose logs -f api`: Tail logs for a specific service.
    - `docker compose exec api pytest -q`: Run tests inside the running service.
    - `docker compose down` (keeps volumes) vs `docker compose down -v` (wipes volumes).

- **Demo / File Walkthrough (run: instructor):**
  Walk through `docker-compose.yml` in the repo root and bring the stack up:
  ```bash
  docker compose up --build -d
  docker compose ps
  ./scripts/smoke.sh
  ```
  **Point out:**
  - `depends_on: redis: condition: service_healthy` ensures `api` waits until `redis-cli ping` succeeds before starting.
  - Both `api` and `redis` attach to `harbor-net`, and `api` talks to `redis://redis:6379/0`.

- **Ask (Check Questions):**
  - Q: In `docker-compose.yml`, if `api` needs to connect to `redis`, what hostname does `api` use? — A: `redis` (the service name defined under `services:`).

- **Done when:** Candidates can read `docker-compose.yml` and start/inspect/stop a multi-container stack.

---

### End-of-Module 4 Lab: Network Isolation & DNS Check
1. Bring up the stack with `docker compose up --build -d`.
2. Verify `GET /health` shows `"redis": "connected"`.
3. Call `GET /containers` twice, then `GET /stats` to confirm `list_endpoint_hits` increments in Redis.
4. Exec into `api` (`docker compose exec api sh`) and verify `python -c "import socket; print(socket.gethostbyname('redis'))"` resolves `redis` to an internal bridge IP.
5. Stop the stack with `docker compose down` (preserving volumes).
