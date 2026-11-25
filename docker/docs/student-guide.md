# Student Guide — Docker & Containerising Python APIs

Welcome! In this 2-hour hands-on session, you'll learn how Docker works by running and debugging a real Python **FastAPI** app (**Cargo Manifest API**) paired with **Redis**—right on your own laptop.

You don't need any prior Docker experience. Everything is built around one simple analogy: **The Shipping Container**.

---

## 1. Why Docker? (In Plain English)
Have you ever seen code work on your laptop, then fail on a teammate's computer because they have a different Python version, missing libraries, or a different OS?

Docker solves that by packing your app **together with** its exact Python runtime, dependencies, and setup into a portable box called a **Container**. If it runs in the box on your laptop, it runs the same way anywhere else.

### What You Will Learn Today
| # | Module | By the end, you will be able to… |
|---|---|---|
| 1 | **Images & Containers** | explain the difference between a template (Image) and a running app (Container), and start/stop/inspect them |
| 2 | **Dockerfile & Builds** | read and write a `Dockerfile`, speed up builds with layer caching, and avoid running as `root` |
| 3 | **Volumes & Persistence** | keep your database safe even when a container is deleted and recreated |
| 4 | **Networking & Compose** | let two containers (`api` and `redis`) talk to each other by name, and run the whole stack with one command |
| 5 | **Capstone & Debugging** | run automated tests inside a container and figure out why a broken container isn't working |

---

## 2. Before Class: Get Your Laptop Ready (5 Minutes)
You only need two things:
- **Docker Desktop** (macOS / Windows) or **Docker Engine + Compose v2** (Linux): https://www.docker.com/products/docker-desktop/
- A terminal with `curl` (built into macOS/Linux; on Windows, use **WSL2** or **Git Bash**)

### Quick Setup
1. Open **Docker Desktop** and wait until it says **Running**.
2. Open your terminal in the `docker/` folder and check that Docker responds:
   ```bash
   docker --version
   docker compose version
   ```
3. Start the course stack with one command:
   ```bash
   ./scripts/setup.sh
   ```
   *(If you're using Claude Code, you can also just say **"set up my environment"**.)*

   When it prints **`== READY`**, everything is working!
4. Open **http://localhost:8000/docs** in your browser to see the live interactive API page, or test it in your terminal:
   ```bash
   curl -s http://localhost:8000/health
   ```
   You should see:
   `{"status":"ok","port":"Port of Rotterdam","db_path":"/data/manifest.db","redis":"connected"}`

---

## 3. During Class: Useful Reset Commands
Don't be afraid to experiment or break things during the labs—you can reset in seconds:
- **Undo a broken lab or fault:** `./scripts/fix.sh`
- **Wipe test data and start fresh:** `./scripts/setup.sh --reset`
- **Stop everything when class ends (keeps your data):** `./scripts/setup.sh --stop`

---

## 4. The App You Are Running (Cargo Manifest API)
The API (`api/app/main.py`, `database.py`, `schemas.py`) tracks shipping containers in a SQLite database (`/data/manifest.db`) and uses Redis to count how many times the list endpoint is called.

Base URL: `http://localhost:8000`

| Method | Path | What it does |
|---|---|---|
| `GET` | `/health` | Checks if the API is alive and whether Redis is connected |
| `GET` | `/containers` | Lists all containers (filter with `?status_filter=docked\|in_transit\|customs_hold\|delivered`) |
| `POST` | `/containers` | Registers a new shipping container (`201 Created`, or `409 Conflict` if the code already exists) |
| `GET` | `/containers/{id}` | Gets one container by its ID |
| `PATCH` | `/containers/{id}` | Updates `cargo`, `destination_port`, `weight_kg`, or `status` |
| `DELETE` | `/containers/{id}` | Deletes a container (`204 No Content`) |
| `GET` | `/stats` | Shows total containers, total weight (kg), and Redis hit count |

### Try It with `curl`
```bash
# Check health
curl -s http://localhost:8000/health

# Add a shipping container
curl -s -X POST http://localhost:8000/containers \
  -H "Content-Type: application/json" \
  -d '{"container_code":"MSCU9876543","cargo":"Solar Panels","origin_port":"Shanghai","destination_port":"Rotterdam","weight_kg":21000,"status":"docked"}'

# List containers and check stats
curl -s http://localhost:8000/containers
curl -s http://localhost:8000/stats
```

---

## 5. The Shipping Container Cheat Sheet

| Concept | What It Means in Real Life | Example |
|---|---|---|
| **Image** | A read-only blueprint or snapshot (like a class) | `docker build -t cargo-api:1.0 ./api` |
| **Container** | A live running app created from an image (like an object) | `docker run -d --name api -p 8000:8000 cargo-api:1.0` |
| **Dockerfile** | Step-by-step recipe to build an image | `FROM`, `WORKDIR`, `COPY`, `RUN`, `USER`, `CMD` |
| **Named Volume** | A separate warehouse that keeps data even if the container is deleted | `-v cargo-data:/data` |
| **Bind Mount** | Sharing a folder from your laptop directly into the container | `-v "$(pwd)/api/app:/srv/app"` |
| **Network** | A private network where containers find each other by name (`redis`) | `docker network create harbor-net` |
| **Port Mapping** | Opening a door (`-p laptop_port:container_port`) so your browser can reach the app | `-p 8000:8000` |
| **Docker Compose** | One YAML file (`docker-compose.yml`) that starts all containers, volumes, and networks together | `docker compose up --build -d` |

---

## 6. Commands You'll Actually Use

```bash
# Check what's running & read logs
docker ps -a                            # See all containers (running and stopped)
docker logs -f harbor-api               # Watch live logs from the API
docker exec -it harbor-api bash         # Open a terminal inside the container

# Build & inspect images
docker images                           # List images on your laptop
docker compose build api                # Rebuild just the API image

# Volumes & Networks
docker volume ls                        # List saved data volumes
docker network inspect harbor-net       # See which containers are on the network

# Docker Compose (your daily workflow)
docker compose up --build -d            # Build and start everything in the background
docker compose ps                       # Check if services are Up and (healthy)
docker compose exec api pytest -q       # Run automated tests inside the container
docker compose down                     # Stop and remove containers (KEEPS your data)
docker compose down -v                  # Stop and DELETE your data volumes too
```

---

## 7. Quick Hands-On Labs (5–15 Minutes Each)

1. **Module 1 — Peek Inside the Box (5 min):**
   Run `docker compose ps` to confirm both `harbor-api` and `harbor-redis` are `Up (healthy)`. Then run `docker compose exec api whoami`—it should print `harbor` (a safe non-root user), not `root`.
2. **Module 2 — Feel the Speed of Layer Caching (5 min):**
   Add a `# test` comment to `api/app/main.py` and run `docker compose build api`. Notice that `pip install -r requirements.txt` says `CACHED` and finishes in ~1 second instead of re-downloading Python packages.
3. **Module 3 — Prove Your Data Survives (5 min):**
   Create a container with `POST /containers`. Run `docker compose down` (without `-v`), then `docker compose up -d`. Run `GET /containers`—your record is still there because `cargo-data` lives outside the container.
4. **Module 4 — Why `redis` Works Instead of `localhost` (5 min):**
   Run `docker compose exec api python -c "import socket; print(socket.gethostbyname('redis'))"` to see Docker's built-in DNS translate the service name `redis` into its internal container IP.
5. **Module 5 — Run Tests & Extend the API (15 min):**
   - Run `docker compose exec api pytest -q` and `./scripts/smoke.sh`.
   - Try adding a small filter or field in `api/app/main.py` + a test in `api/tests/test_main.py`, rebuild with `docker compose up --build -d`, and re-run `pytest -q`.

---

## 8. Common Problems & Quick Fixes

| What Happened | Why | What to Do |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop isn't open | Start Docker Desktop and wait until it says Running |
| `port is already allocated` (port `8000`) | Another app (often `http-course`) is already using port `8000` | Stop the other app (`docker compose down` in that folder) |
| `curl: (7) Failed to connect` | Stack is stopped, or the app is listening on `127.0.0.1` inside the container | Run `docker compose ps` and `docker compose logs api`; make sure `uvicorn` uses `--host 0.0.0.0` |
| `/health` shows `"redis": "unreachable"` | `REDIS_URL` points to `localhost` instead of `redis`, or Redis is down | Check `REDIS_URL=redis://redis:6379/0` in `docker-compose.yml` |
| `attempt to write a readonly database` | Volume was mounted `:ro` or `/data` permissions are wrong | Run `./scripts/fix.sh` or check `docker-compose.yml` has `cargo-data:/data` (no `:ro`) |
| All my saved containers disappeared | You ran `docker compose down -v` (the `-v` deletes volumes) | Use `docker compose down` without `-v` when you want to keep data |

---

## 9. Practice After Class
If you have Claude Code open in the `docker/` folder, you can practice anytime by saying:
- **"quiz me"** — practice questions one at a time with explanations
- **"help with the exercise"** — guided lab help that checks your live containers
- **"review my Dockerfile"** — feedback on your `Dockerfile` for speed, size, and security
- **"check my progress"** — see what you've mastered so far
