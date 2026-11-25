# Module 5 — Capstone: Containerise the Python API End-to-End

Teach-skill content file. Format is described in `.claude/skills/teach-docker-class/SKILL.md`.  
Story Anchor: **The Shipping Container** (Full Shipyard Certification — packing, wiring, inspecting, and troubleshooting the Python Cargo Manifest API).

## Objectives
By the end of this capstone module, candidates can:
1. Containerise a Python FastAPI service from scratch with an optimized `Dockerfile` and `.dockerignore`.
2. Wire persistent storage (named volume) and multi-container networking (custom bridge + Redis) via `docker-compose.yml`.
3. Execute automated tests (`pytest`) and live smoke checks against the containerised stack.
4. Diagnose and fix the 4 most common Docker production/dev failures.

---

### Beat 5.1 — Full-Stack Architecture Review

- **Story Anchor (The Shipping Container):**
  Let's inspect the complete harbor we built today:
  - **Cargo Manifest API (`api`)**: A Python FastAPI container (`api/app/main.py`, `database.py`, `schemas.py`) built from `api/Dockerfile` (`python:3.12-slim`, non-root user `harbor`, `HEALTHCHECK`, `uvicorn` on `0.0.0.0:8000`).
  - **Customs Gate (`-p 8000:8000`)**: The only port published to the host.
  - **Bonded Warehouse (`cargo-data:/data`)**: Named volume persisting `/data/manifest.db` across container upgrades.
  - **Harbor Yard (`harbor-net`)**: User-defined bridge network enabling `api` to reach `redis:6379` by DNS without exposing Redis to the outside world.

- **Say (Key Talking Points):**
  - Every piece from Modules 1–4 comes together in one reproducible stack:
    1. **Image & Dockerfile** (Module 1–2): `api/Dockerfile` + `api/.dockerignore`.
    2. **Volumes** (Module 3): `cargo-data` + `redis-data` named volumes.
    3. **Networking** (Module 4): `harbor-net` bridge + `service_healthy` dependency.

- **Ask (Check Questions):**
  - Q: If you update `api/app/main.py` and run `docker compose up --build -d`, what happens to your existing containers in `/data/manifest.db`? — A: They are preserved! `cargo-data` is a named volume mounted at `/data`, independent of the rebuilt `api` container.

- **Done when:** Candidates can trace a request from `curl localhost:8000/containers` through port mapping, FastAPI, SQLite on `cargo-data`, and Redis on `harbor-net`.

---

### Beat 5.2 — Verification: Tests & Smoke Check

- **Demo / Verification (run: instructor):**
  Run the full verification suite:
  ```bash
  docker compose up --build -d
  docker compose exec api pytest -q
  ./scripts/smoke.sh
  ```
  **Point out:**
  - `pytest -q` runs inside the exact container image that runs in production—no "works on my laptop virtualenv" surprises.
  - `scripts/smoke.sh` verifies live HTTP endpoints end-to-end.

- **Ask (Check Questions):**
  - Q: Why do we run `docker compose exec api pytest -q` inside the container instead of only running `pytest` on our host laptop? — A: Running inside the container tests against the exact Python version, installed dependencies, and environment variables packaged in the image, eliminating "works on my laptop virtualenv" drift.

- **Done when:** All `pytest` tests and `scripts/smoke.sh` pass against the running stack.

---

### Beat 5.3 — Docker Incident Triage (4 Classic Failures)

- **Say (Key Talking Points):**
  Walk through how to diagnose the 4 most common Docker issues:
  1. **Port Already in Use (`Bind for 0.0.0.0:8000 failed: port is already allocated`)**:
     - Cause: Another container or local process is already bound to host port `8000`.
     - Fix: `docker ps` to find the culprit, stop it, or map a different host port (`-p 8001:8000`).
  2. **Connection Refused / Empty Reply from Server**:
     - Cause: App inside container bound to `127.0.0.1` instead of `0.0.0.0`, or container exited immediately.
     - Fix: Check `docker ps -a` and `docker logs <name>`; ensure `--host 0.0.0.0`.
  3. **Container A Cannot Reach Container B (`Connection refused` / DNS failure)**:
     - Cause: Code used `localhost` instead of service name, or containers are on different networks (or default `bridge`).
     - Fix: Put both on a user-defined bridge network and use the service/container name (`redis`, not `localhost`).
  4. **Data Disappeared After `docker compose down -v` or `docker rm`**:
     - Cause: No named volume mounted, or `-v` flag deleted the volume.
     - Fix: Always declare `volumes:` for stateful paths (`/data`, `/var/lib/postgresql/data`) and avoid `-v` unless intentionally resetting.

- **Ask (Check Questions):**
  - Q: A teammate says "My FastAPI container is `Up` in `docker ps`, and `uvicorn` logs say `Uvicorn running on http://127.0.0.1:8000`, but `curl http://localhost:8000/health` fails from my laptop." What is the exact bug? — A: `uvicorn` is listening on `127.0.0.1` (loopback) inside the container instead of `0.0.0.0`, so Docker's port forwarder cannot reach it.

- **Done when:** Candidates can diagnose all 4 failure modes from symptoms alone.

---

### End-of-Module 5 Capstone Assignment: Ship Your Own Feature
1. Add a new field or endpoint to `api/app/main.py` (for example, `GET /health` returning an `environment` field from `APP_ENV`, or filtering `GET /containers?origin_port=Shenzhen`).
2. Add a `pytest` test for your change in `api/tests/test_main.py`.
3. Rebuild and restart with `docker compose up --build -d` (verify `requirements.txt` layer stays `CACHED`!).
4. Run `docker compose exec api pytest -q` and `./scripts/smoke.sh`.
5. Confirm previously created container records in `cargo-data` survived the rebuild.
