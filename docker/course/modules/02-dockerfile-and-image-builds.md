# Module 2 — Dockerfile & Building Custom Images

Teach-skill content file. Format is described in `.claude/skills/teach-docker-class/SKILL.md`.  
Story Anchor: **The Shipping Container** (The Shipyard Packing Specification — packing your own Python Cargo Manifest API into a standardized box).

## Objectives
By the end of this module, candidates can:
1. Read and write a `Dockerfile` using core instructions (`FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE`, `USER`, `CMD`, `ENTRYPOINT`).
2. Explain Docker's **layer cache** and order instructions so dependency installs are cached across code edits.
3. Use `.dockerignore` to keep build contexts fast, lean, and free of secrets or host artifacts.
4. Apply production best practices: slim base images, non-root users, and multi-stage builds.

---

### Beat 2.1 — Anatomy of a `Dockerfile`

- **Story Anchor (The Shipping Container):**
  If an **Image** is the stamped container blueprint, the **`Dockerfile`** is the **step-by-step packing manifest** given to the shipyard. Every line in the `Dockerfile` adds a new layer onto the box: start with a standard steel shell (`FROM`), set the work floor (`WORKDIR`), load the tools (`COPY requirements.txt` + `RUN pip install`), pack the cargo (`COPY app`), label the hatch (`EXPOSE`), and write the startup instruction (`CMD`).

- **Say (Key Talking Points):**
  - **`FROM <image>:<tag>`**: Every `Dockerfile` starts from a base image (e.g., `python:3.12-slim`).
  - **`WORKDIR /srv`**: Sets the working directory inside the image for all subsequent `COPY`, `RUN`, and `CMD` instructions (creates it if missing).
  - **`COPY <src> <dest>` vs `ADD`**: Always prefer `COPY` for local files. `ADD` has hidden magic (auto-extracts tarballs, fetches URLs) that makes builds unpredictable.
  - **`RUN <command>`**: Executes at **build time** and commits the filesystem result as a new image layer (e.g., `RUN pip install --no-cache-dir -r requirements.txt`).
  - **`ENV KEY=VAL`**: Sets persistent environment variables available at both build time and runtime.
  - **`EXPOSE 8000`**: **Documents** which port the app listens on inside the container. It does *not* publish the port to the host (you still need `-p` or `ports:` in Compose).
  - **`CMD` vs `ENTRYPOINT`**:
    - `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` sets the default command executed when the container starts (easily overridden at `docker run`).
    - `ENTRYPOINT` sets the fixed executable; arguments passed to `docker run` are appended to it.
    - Always use **exec form** (JSON array `["cmd", "arg"]`) so your app runs as PID 1 and receives `SIGTERM` cleanly!

- **Demo / File Walkthrough (run: instructor):**
  Open and walk through `api/Dockerfile` line by line:
  ```dockerfile
  FROM python:3.12-slim
  ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \
      MANIFEST_DB_PATH=/data/manifest.db
  WORKDIR /srv
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY app ./app
  COPY tests ./tests
  ```
  **Point out:**
  - `PYTHONUNBUFFERED=1` ensures Python prints logs immediately so `docker logs` works in real time.
  - `--host 0.0.0.0` in `CMD` is mandatory: if `uvicorn` binds to `127.0.0.1` inside the container, host port forwarding (`-p 8000:8000`) cannot reach it!

- **Ask (Check Questions):**
  - Q: What happens if you run `uvicorn app.main:app --host 127.0.0.1 --port 8000` inside a container with `-p 8000:8000`? — A: Requests from the host will fail (`Connection reset by peer` / empty reply) because `127.0.0.1` inside the container only listens to the container's own loopback interface, not the bridge network interface.
  - Q: Does `EXPOSE 8000` automatically make port 8000 reachable on `localhost:8000`? — A: No! `EXPOSE` is metadata/documentation. Only `-p 8000:8000` publishes the port.

- **Done when:** Candidates can explain every instruction in `api/Dockerfile` and why `--host 0.0.0.0` is required.

---

### Beat 2.2 — Layer Caching & `.dockerignore`

- **Story Anchor (The Shipping Container):**
  Imagine repacking a 20-ton shipping container because you changed one label on the top crate. If you packed the heavy machinery (Python dependencies) *after* the top crate (your source code), you'd have to unload and reload the heavy machinery every single time! Instead, pack the heavy, rarely changing items at the bottom, and put your frequently changing app code on top.

- **Say (Key Talking Points):**
  - **How Layer Caching Works**: Docker executes `Dockerfile` top-to-bottom. Each instruction produces a cached layer. If an instruction's inputs haven't changed, Docker reuses the cached layer (`CACHED`). Once **one** layer invalidates, **every layer below it** must be rebuilt.
  - **The Golden Rule for Python Dockerfiles**:
    - **Bad**: `COPY . .` followed by `RUN pip install -r requirements.txt` (every single code edit forces `pip install` to re-download all packages!).
    - **Good**: `COPY requirements.txt .` -> `RUN pip install --no-cache-dir -r requirements.txt` -> `COPY app ./app`. Now editing `app/main.py` reuses the cached `pip install` layer and rebuilds in <1 second!
  - **Build Context & `.dockerignore`**:
    - When you run `docker build ./api`, Docker sends the entire `./api` directory (the **build context**) to the Docker daemon.
    - Without `.dockerignore`, you accidentally copy `.venv/`, `__pycache__/`, `.git/`, `.env`, or `*.db` into the build context—slowing builds and risking secret leaks.

- **Demo / Command Trace (run: instructor):**
  Build the API image, then observe cache hits:
  ```bash
  docker build -t cargo-api:v1 ./api
  docker history cargo-api:v1
  ```
  **Point out:**
  - `docker history` shows every layer and its size.
  - Re-running `docker build -t cargo-api:v1 ./api` finishes almost instantly because all layers are `CACHED`.

- **Ask (Check Questions):**
  - Q: Why do we copy `requirements.txt` and run `pip install` *before* `COPY app ./app`? — A: So that changing Python source files in `app/` does not invalidate the `pip install` cache layer.
  - Q: Name two things that should always be in `.dockerignore` for a Python project. — A: `.venv/` (or `venv/`), `__pycache__/`, `.git/`, `.env` (secrets), `*.db`.

- **Done when:** Candidates can diagnose a slow Dockerfile with `COPY . .` before `pip install` and fix it.

---

### Beat 2.3 — Lean Images, Non-Root Users & Multi-Stage Builds

- **Story Anchor (The Shipping Container):**
  You don't ship the welding torches, cranes, and scaffolding inside the finished shipping container! You use heavy tools in the shipyard to build the cargo, then seal only the finished product into a lightweight, locked box.

- **Say (Key Talking Points):**
  - **Choosing a Base Image**:
    - `python:3.12` (~1 GB): Full Debian + compilers (`gcc`, `git`, etc.). Too bloated for production.
    - `python:3.12-slim` (~130 MB): Minimal Debian, fast, compatible with Python binary wheels. **Recommended default for Python APIs.**
    - `python:3.12-alpine` (~50 MB): Uses `musl` libc instead of `glibc`—many Python packages with C extensions have no prebuilt `musl` wheels and take minutes to compile.
  - **Non-Root User (`USER harbor`)**: By default, containers run as `root` (UID 0). If an attacker exploits a vulnerability in your web framework while running as `root`, they gain `root` inside the container (and potentially on mounted volumes). Creating a dedicated non-root user (`harbor`) limits the blast radius.
  - **Multi-Stage Builds**: Use a `builder` stage (`FROM python:3.12 AS builder`) to compile wheels or frontend assets, then `COPY --from=builder` only the compiled artifacts into a clean `python:3.12-slim` final stage.

- **Ask (Check Questions):**
  - Q: Why is `python:3.12-slim` usually preferred over `python:3.12-alpine` for Python APIs? — A: `alpine` uses `musl` libc, which often lacks prebuilt Python wheels (`manylinux`) and forces slow C compilation; `slim` uses `glibc` while staying small.
  - Q: Why should a production `Dockerfile` include a `USER` instruction? — A: To follow the principle of least privilege so the application process does not run as `root` inside the container.

- **Done when:** Candidates can justify `python:3.12-slim`, non-root `USER`, and multi-stage builds.

---

### End-of-Module 2 Lab: Build & Run the Cargo Manifest API
1. Inspect `api/Dockerfile` and `api/.dockerignore`.
2. Build the image: `docker build -t cargo-api:1.0 ./api`.
3. Run it: `docker run -d --name api-test -p 8000:8000 cargo-api:1.0`.
4. Verify `/health` and `/docs` (Swagger UI) at `http://localhost:8000/docs`.
5. Run the unit tests inside the container: `docker exec api-test pytest -q`.
6. Stop and remove `api-test`.
