# Module 3 — Volumes, Bind Mounts & Persistent Data

Teach-skill content file. Format is described in `.claude/skills/teach-docker-class/SKILL.md`.  
Story Anchor: **The Shipping Container** (Ephemeral steel boxes vs Bonded Port Warehouses and Dockside Loading Bays).

## Objectives
By the end of this module, candidates can:
1. Explain why container filesystems are **ephemeral** and what happens to data when a container is removed.
2. Create and attach **Named Volumes** (`docker volume create`, `-v name:/path`) to persist database/API state across container recreations.
3. Use **Bind Mounts** (`-v $(pwd)/app:/srv/app`) for live local development without rebuilding images on every edit.
4. Distinguish Named Volumes, Bind Mounts, and `tmpfs` mounts, and manage volume lifecycles (`ls`, `inspect`, `rm`, `prune`).

---

### Beat 3.1 — The Ephemeral Container Problem

- **Story Anchor (The Shipping Container):**
  Shipping containers are **disposable/interchangeable**. When a ship docks for maintenance or you upgrade to a newer steel box (`docker rm` + `docker run`), the old box is scrapped. If you stored the entire port's cargo ledger *inside* the container's writable layer instead of in a **bonded port warehouse**, scrapping the box destroys your ledger forever!

- **Say (Key Talking Points):**
  - **Ephemeral by Design**: Every file written inside a container (e.g., `/data/manifest.db`) lives in that container's thin **writable layer**.
  - **The Trap**: `docker stop` keeps the writable layer, so data appears safe during a restart. **As soon as you run `docker rm` (or `docker compose down` + rebuild), the writable layer is deleted permanently.**
  - **Golden Rule**: Containers should be **stateless and replaceable**. State (databases, uploads, logs) must live **outside** the container's writable layer in a **Volume**.

- **Demo / Failure Trace (run: instructor):**
  Demonstrate data loss without a volume:
  1. Run `docker run -d --name ephemeral-api -p 8000:8000 cargo-api:1.0`
  2. `POST /containers` to create a shipment record.
  3. `docker rm -f ephemeral-api`
  4. Start a fresh container `docker run -d --name ephemeral-api -p 8000:8000 cargo-api:1.0` and `GET /containers` — the list is empty (`[]`)!
  **Point out:**
  - The SQLite database `/data/manifest.db` was created inside the old container's writable layer and vanished with `docker rm`.

- **Ask (Check Questions):**
  - Q: If you run `docker stop` and `docker start` on a container without a volume, is the data lost? What about `docker rm` + `docker run`? — A: `stop`/`start` preserves the container's writable layer; `rm` + `run` creates a brand-new container and permanently destroys the old data.

- **Done when:** Candidates can explain why containers must be treated as ephemeral and why databases never store data only in the container writable layer.

---

### Beat 3.2 — Named Volumes (Port Warehouses)

- **Story Anchor (The Shipping Container):**
  A **Named Volume** is a **Docker-managed bonded warehouse** on the dock. You give it a name (`cargo-data`) and hook a pipe from the warehouse to `/data` inside your container. Even if you scrap the container and roll in a brand-new v2 container, you reconnect it to `cargo-data` and every record is still there!

- **Say (Key Talking Points):**
  - **What is a Named Volume?** Storage managed entirely by Docker on the host (e.g., `/var/lib/docker/volumes/cargo-data/_data` on Linux). Works identically on macOS, Windows, and Linux.
  - **Why Doesn't a New Container Create a New Volume? (Named vs. Anonymous Volumes):**
    - If you pass `-v /data` **without a name** (an *anonymous volume*), Docker generates a random ID each time—so a new container gets a brand-new empty volume.
    - When you pass **the same name** (`-v cargo-data:/data`), Docker checks if `cargo-data` already exists. If it does, Docker **re-attaches the existing volume** instead of creating a new one!
    - **Real-World Use:** When you upgrade your API from `cargo-api:1.0` to `cargo-api:2.0` (or rebuild with `docker compose up --build -d`), the old container is replaced, **the same `cargo-data` volume is re-attached**, and 100% of your database records survive. You can also mount the same named volume into a second container (e.g., a backup job).
  - **CLI Syntax**:
    - `docker volume create cargo-data` (optional—`docker run -v cargo-data:/data` auto-creates it if missing).
    - Attach: `docker run -d --name api-v1 -p 8000:8000 -v cargo-data:/data cargo-api:1.0`.
    - Modern `--mount` syntax (more explicit): `--mount type=volume,src=cargo-data,dst=/data`.
  - **Lifecycle Commands**: `docker volume ls`, `docker volume inspect cargo-data`, `docker volume rm cargo-data`, `docker volume prune`.
  - **Warning**: `docker compose down` keeps named volumes; `docker compose down -v` **deletes** them!

- **Demo / Command Trace (run: instructor):**
  Prove persistence across container replacement:
  ```bash
  docker volume create cargo-data
  docker run -d --name api-v1 -p 8000:8000 -v cargo-data:/data cargo-api:1.0
  # POST a container record, then destroy api-v1
  docker rm -f api-v1
  # Launch a brand-new container attached to the same volume
  docker run -d --name api-v2 -p 8000:8000 -v cargo-data:/data cargo-api:1.0
  curl -s http://localhost:8000/containers
  ```
  **Point out:**
  - The record created by `api-v1` is immediately returned by `api-v2`!
  - Note on permissions: Because `api/Dockerfile` created `/data` owned by user `harbor`, Docker initializes the empty named volume with `harbor`'s ownership.

- **Ask (Check Questions):**
  - Q: If you delete `api-v1` and start `api-v2` with `-v cargo-data:/data`, does Docker create a new empty volume? — A: No! Because the volume has the same name (`cargo-data`), Docker re-attaches the existing volume so `api-v2` keeps all the old data. (Only an unnamed *anonymous* volume `-v /data` would create a new one.)
  - Q: What is the difference between `docker compose down` and `docker compose down -v`? — A: `down` stops and removes containers and networks but **preserves** named volumes; `down -v` also **deletes** the named volumes and all persisted data.

- **Done when:** Candidates can attach a named volume to `/data` and verify data survives `docker rm -f`.

---

### Beat 3.3 — Bind Mounts & `tmpfs` (Dockside Live Loading)

- **Story Anchor (The Shipping Container):**
  A **Bind Mount** is like backing a delivery truck directly up to the open door of a shipping container at the dockyard: whatever file you edit on your laptop (`./api/app`) is **instantly** visible inside `/srv/app` in the container without repacking the box (`docker build`).
  A **`tmpfs` mount** is a scratchpad in volatile RAM—fast, never written to disk, and wiped the instant the container stops (great for temporary secrets or session caches).

- **Say (Key Talking Points):**
  - **Named Volume vs Bind Mount vs `tmpfs`**:
    | Type | Managed By | Host Path Required? | Primary Use Case |
    |---|---|---|---|
    | **Named Volume** | Docker | No (just a name) | Databases, persistent app state, production |
    | **Bind Mount** | You (Host OS) | Yes (absolute path, e.g. `$(pwd)/api/app:/srv/app`) | Local dev hot-reload, injecting config files (`:ro`) |
    | **`tmpfs`** | Kernel RAM | No | Sensitive temp tokens, high-speed scratch space |
  - **Read-Only Mounts (`:ro`)**: Append `:ro` (e.g., `-v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro`) so a container can read host config but never corrupt it.
  - **Watch Out for Overwriting**: Mounting a bind mount onto `/srv` hides whatever was in `/srv` in the image (don't overwrite `site-packages` if your venv is inside `/srv`—mount only `./api/app:/srv/app`!).

- **Demo / Command Trace (run: instructor):**
  Run uvicorn with `--reload` using a bind mount for live local dev:
  ```bash
  docker run -d --name api-dev -p 8000:8000 \
    -v "$(pwd)/api/app:/srv/app" \
    -v cargo-data:/data \
    cargo-api:1.0 \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
  **Point out:**
  - Notice we combined **both** a bind mount (`/srv/app` for live code reload) and a named volume (`/data` for persistent SQLite data) in one container!

- **Ask (Check Questions):**
  - Q: When should you use a Bind Mount vs a Named Volume? — A: Use **Bind Mounts** in development when you need direct host access (live code reload, local config files); use **Named Volumes** for persistent database/application state managed by Docker.
  - Q: What does `:ro` do at the end of `-v ./config.yml:/app/config.yml:ro`? — A: Mounts the file as **read-only** inside the container so the container process cannot modify or delete it.

- **Done when:** Candidates can choose the right mount type for databases, live code reload, and read-only configs.

---

### End-of-Module 3 Lab: Persistent Cargo Manifest
1. Create a named volume `harbor-lab-vol`.
2. Run `cargo-api:1.0` attached to `harbor-lab-vol:/data`.
3. Use `curl` to `POST` two shipping containers to `http://localhost:8000/containers`.
4. Force-remove the running container (`docker rm -f ...`).
5. Start a new container attached to `harbor-lab-vol:/data` and confirm `GET /containers` still returns both records.
6. Clean up the container and remove `harbor-lab-vol` with `docker volume rm`.
