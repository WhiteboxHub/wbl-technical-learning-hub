# Module 1 — Images, Containers & The Shipping Container Revolution

Teach-skill content file. Format is described in `.claude/skills/teach-docker-class/SKILL.md`.  
Story Anchor: **The Shipping Container** (Break-bulk chaos vs standardized intermodal steel boxes, ship blueprints, and ports).

## Objectives
By the end of this module, candidates can:
1. Explain what Docker is, why it exists, and how its client-daemon architecture (`docker` CLI $\rightarrow$ `dockerd` $\rightarrow$ `containerd` / Registry) works.
2. Explain why containers solved the "it works on my machine" problem using the intermodal shipping container analogy.
3. Contrast Virtual Machines (full OS per app) with Docker Containers (shared host kernel, isolated user space).
4. Distinguish a Docker **Image** (read-only layered blueprint) from a **Container** (writable running instance).
5. Manage the full container lifecycle using core Docker CLI commands (`pull`, `run`, `ps`, `logs`, `exec`, `stop`, `rm`, `rmi`).
6. Run containers in detached mode (`-d`) and publish ports (`-p host:container`) to reach a containerized service from the host.

---

### Beat 1.1 — Introduction to Docker & How Docker Works

- **Story Anchor (The Shipping Container):**
  Before we load any cargo or read any blueprints, we need to understand the **port authority and crane system** itself. **Docker** is the global shipping platform: you give orders at the port office (**Docker CLI**), the harbor master (**Docker Daemon `dockerd`**) coordinates the cranes (**`containerd` / `runc`**), and blueprints are fetched from the central warehouse (**Docker Registry**). Without the port system, standardized shipping boxes cannot move.

- **Say (Key Talking Points):**
  - **What is Docker?**: An open platform for developing, shipping, and running applications inside lightweight, isolated **containers**. Instead of manually installing Python, Postgres, Redis, and OS libraries on every machine, you package and run them consistently everywhere.
  - **Where Docker Fits in the SDLC**: Developers build and test locally in the exact same environment that CI/CD tests and production servers run—eliminating environment drift across dev, staging, and prod.
  - **Docker Architecture (Client-Server)**:
    - **Docker CLI (`docker`)**: The command-line client you type into. It does *not* run containers itself—it sends REST API requests to the daemon.
    - **Docker Daemon (`dockerd`)**: The background engine managing images, containers, networks, and volumes (delegating low-level container execution to `containerd` and `runc`).
    - **Docker Registry (e.g., Docker Hub)**: The remote catalog where pre-built images (`python`, `redis`, `nginx`, `postgres`) are stored and pulled from.
  - **Docker Engine vs. Docker Desktop**:
    - On **Linux**, Docker Engine runs natively on the Linux kernel.
    - On **macOS and Windows**, Docker Desktop runs a lightweight Linux VM under the hood because containers rely on **Linux kernel** features (namespaces and cgroups).

- **Demo / Command Trace (run: instructor):**
  Verify the Docker client and daemon are both alive and inspect the engine:
  ```bash
  docker --version
  docker compose version
  docker info
  ```
  **Point out:**
  - `docker --version` only checks the CLI client; `docker info` actually talks to the **Docker Daemon** (if Docker Desktop is stopped, `docker info` fails!).
  - Notice `OSType: linux` and `Server Version` in `docker info`—even on macOS or Windows, Docker runs containers inside a Linux kernel.

- **Ask (Check Questions):**
  - Q: When you type `docker ps` in your terminal, does the `docker` CLI inspect containers directly, or talk to something else? — A: It acts as a **client** sending an API request to the **Docker Daemon (`dockerd`)**.
  - Q: Why does Docker Desktop on macOS/Windows run a lightweight Linux VM behind the scenes? — A: Because Docker containers use **Linux kernel** isolation features (namespaces and cgroups), which macOS and Windows kernels don't natively provide.

- **Done when:** Candidates can explain what Docker is, name the 3 core parts of Docker's architecture (CLI, Daemon, Registry), and verify their local Docker engine with `docker info`.

---

### Beat 1.2 — Why Containers? Break-Bulk Chaos vs The Shipping Container

- **Story Anchor (The Shipping Container):**
  Before 1956, global shipping used **break-bulk cargo**: sacks of coffee, barrels of oil, crates of machinery, and coils of wire were loaded piece by piece into a ship's hull. Every port needed custom cranes, different ropes, and days of manual labor. Fragile items got crushed; oil leaked onto coffee.
  In 1956, Malcom McLean introduced the **standardized intermodal shipping container**. Suddenly, a crane didn't care whether the steel box held microchips, bananas, or car parts—every box had the exact same corner castings, dimensions, and locking pins. One ship could carry thousands of isolated boxes safely side-by-side.
  In software, deploying raw Python/Node/Java apps directly onto a server is break-bulk chaos ("It works on my machine!"). A **Docker container** packages your app, its Python runtime, and its libraries into one standardized box that runs identically on your laptop, a teammate's Mac, or a cloud Linux server.

- **Say (Key Talking Points):**
  - **The "Works on My Machine" Problem**: Different OS versions, missing system libraries, conflicting Python versions (3.9 vs 3.12), and global package collisions break deployments.
  - **VMs vs Containers**:
    - **Virtual Machine (VM)**: Like building a fleet of completely separate tugboats, each with its own hull, engine room, and crew (Hypervisor + full Guest OS per app). Heavy (GBs), slow to boot (minutes).
    - **Container**: Like stacking standardized steel boxes onto **one** giant container ship. Every container shares the **host OS kernel** (the ship's hull and engine), while keeping its own isolated filesystem, processes, and network interface (Linux namespaces & cgroups). Lightweight (MBs), starts in milliseconds.
  - **Portability & Isolation**: Two containers on the same host can run Python 3.8 and Python 3.12 simultaneously without ever conflicting.

- **Demo / Conceptual Trace (run: instructor):**
  Run a quick sanity check to show Docker's speed and isolation:
  ```bash
  docker run --rm alpine echo "Hello from inside a shipping container!"
  ```
  **Point out:**
  - Notice how fast it starts (under a second) compared to booting a VM.
  - `--rm` automatically scraps the container as soon as the command finishes.

- **Ask (Check Questions):**
  - Q: What do all Docker containers running on the same Linux host share, and what keeps them isolated? — A: They share the **host OS kernel**, while Linux **namespaces** (isolation of PIDs, network, filesystem) and **cgroups** (CPU/memory limits) keep them separated.
  - Q: Why is a container much smaller and faster to start than a Virtual Machine? — A: A container does not bundle or boot a full Guest Operating System; it only packages the app and its user-space dependencies.

- **Done when:** Candidates can explain the shipping container analogy and contrast VMs vs containers in one sentence each.

---

### Beat 1.3 — Images vs Containers (Blueprint vs Running Box)

- **Story Anchor (The Shipping Container):**
  Think of a **Docker Image** as the **stamped packing specification & empty container template** stored in a port warehouse (**Registry**, like Docker Hub). It is **read-only**—you don't ship goods by modifying the master blueprint.
  When you dispatch a voyage, you stamp out a **Container** from that image. You can launch 1, 5, or 50 containers from the exact same image, just like loading 50 identical containers from the same blueprint.

- **Say (Key Talking Points):**
  - **Docker Image**: An immutable, read-only template composed of stacked filesystem **layers** (base OS + runtime + dependencies + app code).
  - **Docker Container**: A runnable instance of an image. Docker adds a thin **writable layer** (Copy-on-Write / UnionFS) on top of the read-only image layers.
  - **Registry**: A warehouse for storing and distributing images (e.g., Docker Hub `docker.io`, GitHub Container Registry `ghcr.io`, AWS ECR).
  - **Image Tags**: `python:3.12-slim` means repository `python`, tag `3.12-slim`. Never rely blindly on `:latest` in production—pin explicit versions!

- **Demo / Command Trace (run: instructor):**
  Pull an image and inspect local images:
  ```bash
  docker pull nginx:alpine
  docker images
  ```
  **Point out:**
  - `docker pull` downloads the read-only image layers from Docker Hub.
  - `docker images` shows `REPOSITORY`, `TAG`, `IMAGE ID`, `CREATED`, and `SIZE`. Notice nothing is running yet!

- **Ask (Check Questions):**
  - Q: If you start 3 containers from `nginx:alpine`, how many copies of the read-only image layers are stored on disk? — A: Only **one** shared set of read-only layers; each container only gets its own thin writable top layer.
  - Q: If you edit a file inside a running container and delete that container (`docker rm`), does the underlying image change? — A: No. Images are immutable; changes lived only in the container's writable layer.

- **Done when:** Candidates clearly distinguish an Image (immutable template) from a Container (running instance with a writable layer).

---

### Beat 1.4 — Container Lifecycle & Essential CLI

- **Story Anchor (The Shipping Container):**
  At a busy port, dockworkers need standard controls: load a box onto the dock (`run`), check which boxes are active (`ps`), read the shipping log (`logs`), open the inspection hatch (`exec`), halt operations (`stop`), and scrap old boxes (`rm`).

- **Say (Key Talking Points):**
  - **Core Lifecycle Commands**:
    - `docker run [options] <image> [cmd]`: Creates and starts a new container.
    - `docker ps` / `docker ps -a`: Lists running containers / **all** containers (including stopped/exited ones).
    - `docker logs [-f] <container>`: Streams `stdout`/`stderr` from the container's main process (PID 1).
    - `docker exec -it <container> sh` (or `bash`): Opens an interactive shell inside a *running* container for debugging.
    - `docker stop <container>`: Sends `SIGTERM` (graceful shutdown), then `SIGKILL` after timeout.
    - `docker rm <container>`: Removes a stopped container (use `-f` to force-remove a running one).
    - `docker rmi <image>`: Removes a local image (only after all containers using it are removed).
  - **PID 1 Rule**: A container stays alive **only as long as its main process (PID 1) is running**. When PID 1 exits, the container stops.

- **Demo / Command Trace (run: instructor):**
  Run a container, inspect it, exec into it, stop and remove it:
  ```bash
  docker run -d --name harbor-web -p 8080:80 nginx:alpine
  docker ps
  docker logs harbor-web
  docker exec -it harbor-web sh -c "ls -la /usr/share/nginx/html"
  docker stop harbor-web
  docker ps -a
  docker rm harbor-web
  ```
  **Point out:**
  - `docker ps` hides stopped containers; `docker ps -a` reveals them with `Exited (0)`.
  - `docker stop` does not delete the container—you still need `docker rm` (or `--rm` at `run` time).

- **Ask (Check Questions):**
  - Q: Why does `docker run -it ubuntu echo "hi"` exit immediately instead of staying running? — A: Because `echo "hi"` is PID 1; once it prints and exits, the container has no running main process and stops.
  - Q: What is the difference between `docker run` and `docker exec`? — A: `docker run` creates and starts a **new** container from an image; `docker exec` runs a command inside an **already running** container.

- **Done when:** Candidates can run, inspect logs, exec into, stop, and remove a container without assistance.

---

### Beat 1.5 — Detached Mode & Port Mapping (`-d`, `-p`)

- **Story Anchor (The Shipping Container):**
  A sealed shipping container has its own internal wiring. Nobody outside the box can plug into it unless the port authority opens a **customs gate** (`-p host_port:container_port`) connecting a dockside port number to the container's internal port.

- **Say (Key Talking Points):**
  - **Foreground vs Detached (`-d`)**: Without `-d`, `docker run` attaches your terminal to the container's stdout—pressing `Ctrl+C` or closing your terminal stops the container! With `-d`, the container runs in the background and returns its container ID.
  - **Port Mapping (`-p HOST:CONTAINER`)**:
    - Example: `-p 8080:80` forwards traffic arriving on `localhost:8080` of your laptop into port `80` inside the container.
    - You can run two `nginx` containers at once by mapping `-p 8081:80` and `-p 8082:80`—inside each container it's still port `80`, while on the host they don't collide!

- **Ask (Check Questions):**
  - Q: In `docker run -p 9000:8000 my-api`, which port do you open in your browser (`curl http://localhost:____`)? — A: `9000` (the host port on the left side of the colon).

- **Done when:** Candidates can map a host port to a container port and avoid host port collisions.

---

### End-of-Module 1 Lab: First Voyage
1. Pull `nginx:alpine` and run it detached as `dock-1` on host port `8081` (`-p 8081:80`).
2. Verify it responds with `curl -I http://localhost:8081`.
3. View its access logs with `docker logs dock-1`.
4. Exec into `dock-1` and inspect `/etc/nginx/conf.d/default.conf`.
5. Stop and remove `dock-1`, then confirm `docker ps -a` is clean.
