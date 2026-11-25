# Docker & Containerising Python APIs — Course Table of Contents

5 hands-on modules covering  Docker curriculum.  
**Story Anchor**: **The Shipping Container** (Intermodal Steel Boxes, Shipyard Packing Manifests, Bonded Warehouses, Harbor Yards & Customs Gates).

---

## Curriculum Map
1. **Module 1: Introduction to Docker, Images & Containers** — What Docker is, CLI/Daemon/Registry architecture, break-bulk vs containers, VMs vs containers, Image layers vs Container writable layer, lifecycle CLI (`run`, `ps`, `logs`, `exec`, `stop`, `rm`, `rmi`), `-d` and `-p host:container`.
2. **Module 2: Dockerfile & Building Custom Images** — `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `EXPOSE`, `USER`, `CMD` vs `ENTRYPOINT`; layer caching (`requirements.txt` before `app/`); `.dockerignore`; `python:3.12-slim`, non-root users, and multi-stage builds.
3. **Module 3: Volumes, Bind Mounts & Persistent Data** — Ephemeral container problem; Named Volumes (`cargo-data:/data`); Bind Mounts for hot reload; `tmpfs` and `:ro` mounts; `docker volume` CLI and `down` vs `down -v`.
4. **Module 4: Docker Networking & Multi-Container Communication** — `bridge`, `host`, `none`; default bridge vs user-defined bridge Container DNS; escaping the `localhost` trap; `docker-compose.yml` (`api` + `redis` + `harbor-net`).
5. **Module 5: Capstone — Containerise the Python API End-to-End** — Full Cargo Manifest FastAPI stack verification (`pytest`, `smoke.sh`), 4-case Docker incident triage, and live feature extension lab.
