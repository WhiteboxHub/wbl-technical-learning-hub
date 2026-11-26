# Docker & Containerising Python APIs — Course Repo

Running story anchor: **The Shipping Container** (standardized intermodal steel boxes, shipyard packing manifests, bonded port warehouses, and harbor yard networking).

## Overview
This Thursday module repo provides hands-on mastery in:
1. **Images & Containers** — VMs vs Containers, UnionFS layers, registries, and core Docker CLI lifecycle.
2. **Dockerfile & Image Builds** — Writing production `Dockerfile`s, layer caching, `.dockerignore`, slim base images, and non-root users.
3. **Volumes & Persistence** — Ephemeral container layers vs Named Volumes, Bind Mounts, and `tmpfs`.
4. **Docker Networking** — `bridge` / `host` / `none`, user-defined bridge Container DNS, escaping the `localhost` trap, and `docker compose`.
5. **Capstone: Containerise the Python API** — Packaging, persisting, networking, testing, and troubleshooting the **Cargo Manifest FastAPI** service.

---

## Quick Navigation & Guides
- [Class-day quick start](docs/class-day-quickstart.md) — 5-minute pre-flight checklist
- [Instructor Guide](docs/instructor-guide.md) — Facilitation, pacing, and teaching with the AI co-pilot
- [Student Guide](docs/student-guide.md) — Laptop setup, Docker CLI cheatsheet, and hands-on labs
- [Instructor Steps](instructor-steps.md) — Exact vocal beats, commands, and teaching script
- [Course Table of Contents](docs/course-toc.md) — Full 5-module syllabus

---

## Start the Stack
Requires Docker Desktop (or Docker Engine + Compose v2) running.

```bash
./scripts/setup.sh
```

Or manually:
```bash
docker compose up --build -d
./scripts/smoke.sh
```

- **Cargo Manifest API**: http://localhost:8000/containers
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Stats**: http://localhost:8000/stats
- **Run API Tests in Container**: `docker compose exec api pytest -q`
- **Stop (keep data)**: `docker compose down`
- **Reset (wipe volumes)**: `docker compose down -v && docker compose up --build -d`

---

## Endpoints (Cargo Manifest API)
| Method | Path | Notes |
|---|---|---|
| `GET` | `/health` | Liveness + DB path + Redis connectivity |
| `GET` | `/containers` | List all containers (`?status_filter=docked\|in_transit\|customs_hold\|delivered`) |
| `POST` | `/containers` | Register a shipping container (`201 Created`, `409 Conflict` on duplicate code) |
| `GET` | `/containers/{id}` | Fetch single container by ID |
| `PATCH` | `/containers/{id}` | Update cargo, destination, weight, or status |
| `DELETE` | `/containers/{id}` | Remove container (`204 No Content`) |
| `GET` | `/stats` | Total containers, total weight (kg), and Redis-tracked list hits |

---

## The Story Anchor: The Shipping Container
- **Break-Bulk Chaos** $\rightarrow$ Deploying raw apps directly onto servers ("It works on my machine!").
- **ISO Shipping Container** $\rightarrow$ Standardized **Docker Container** sharing the ship's hull/OS kernel while isolating cargo.
- **Stamped Blueprint** $\rightarrow$ Read-only **Docker Image** stored in a port warehouse (**Registry**).
- **Shipyard Packing Manifest** $\rightarrow$ **`Dockerfile`** (ordered for layer caching + `.dockerignore`).
- **Bonded Port Warehouse** $\rightarrow$ **Named Volume** (`cargo-data:/data`) that survives scrapping the box.
- **Dockside Truck Loading** $\rightarrow$ **Bind Mount** (`./api/app:/srv/app`) for live local code reload.
- **Harbor Yard & Radio DNS** $\rightarrow$ User-defined **Bridge Network** (`harbor-net`) where `api` reaches `redis:6379` by name.
- **Customs Gate** $\rightarrow$ **Port Publishing** (`-p 8000:8000`) exposing only approved doors to the host.

---

## Repository Layout
```text
docker/
├── README.md                          # Course overview, quick start, story anchor
├── instructor-steps.md                # Beat-by-beat teaching flow with AI co-pilot
├── docker-compose.yml                 # Multi-container stack: api + redis + harbor-net + volumes
├── api/
│   ├── Dockerfile                     # Production-ready Python 3.12-slim Dockerfile
│   ├── .dockerignore                  # Excludes __pycache__, .venv, .git, *.db
│   ├── requirements.txt               # FastAPI, Uvicorn, Pydantic, Redis, Pytest
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py                    # Cargo Manifest FastAPI service
│   └── tests/
│       └── test_main.py               # Pytest suite
├── scripts/
│   └── smoke.sh                       # End-to-end curl smoke check
├── docs/
│   ├── class-day-quickstart.md        # 5-minute pre-flight checklist
│   ├── course-toc.md                  # Syllabus & module map
│   ├── instructor-guide.md            # Facilitation & troubleshooting
│   └── student-guide.md               # Docker CLI cheatsheet & labs
├── course/
│   └── modules/
│       ├── 01-images-and-containers.md
│       ├── 02-dockerfile-and-image-builds.md
│       ├── 03-volumes-and-persistence.md
│       ├── 04-docker-networking.md
│       └── 05-containerise-the-python-api-capstone.md
└── .claude/
    └── skills/                        # Native CLI teaching & coaching skills
        ├── setup-docker-class/
        ├── teach-docker-class/
        ├── practice-docker/
        └── setup-candidate/
```
