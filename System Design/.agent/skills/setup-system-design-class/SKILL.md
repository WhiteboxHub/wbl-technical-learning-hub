---
name: setup-system-design-class
description: Pre-flight check and automated stack launcher for instructors teaching the System Design course. Use when the instructor says "set up the class", "start system design stack", "check environment", or before starting Module 1. Checks Docker Desktop, port availability (8080, 8000, 6379), brings up containers, runs the 10-check smoke test, and outputs a READY summary.
---

# Setup System Design Class

You verify prerequisites and start the System Design training stack for the instructor.

## What this skill does
1. Confirms Docker Desktop is running.
2. Checks that required ports (`8000`, `8080`, `6379`) are free or held by this stack.
3. Launches the Docker Compose stack (`scripts/setup.sh`).
4. Runs `scripts/smoke.sh` to verify API, Gateway, Redis cache, and Worker queues.
5. Prints the **READY** summary and hands over to `teach-system-design-class`.

## Procedure

### Step 1: Check Docker
Run `docker info`. If it fails:
> "Docker Desktop is not running. Please start Docker Desktop and wait until it indicates 'running', then ask me to set up the class again."

### Step 2: Check Ports
Verify ports 8000, 8080, and 6379:
- If occupied by another unrelated process, notify the instructor with the PID and process name. Never kill a process without explicit confirmation.

### Step 3: Launch Stack
Run:
```bash
./scripts/setup.sh
```
Wait for the health check to pass.

### Step 4: Smoke Test
`scripts/setup.sh` runs `scripts/smoke.sh` automatically. Confirm:
- Health check (:8000 and :8080) -> OK
- URL shorten write -> OK (201 Created)
- Cache MISS -> OK
- Cache HIT -> OK
- Async Queue write -> OK (202 Accepted)
- Worker processing -> OK
- Rate limiting -> OK (429)

### Step 5: Ready Announcement
Output the ready block:
```
==========================================================
 [READY] System Design Environment is Live!
 - Gateway / Load Balancer: http://localhost:8080
 - App Node:                http://localhost:8000
 - Redis Cache & Queues:   localhost:6379
 - System Metrics:         http://localhost:8080/api/metrics
==========================================================
Instructor command to begin: "teach module 1"
```
