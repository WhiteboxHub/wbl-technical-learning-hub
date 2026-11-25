# Class-Day Quickstart (5-Minute Pre-Flight)

1. **Start Docker Desktop** and confirm it responds:
   ```bash
   docker info >/dev/null && echo "Docker OK"
   ```
2. **Pre-pull base images** (avoids slow classroom Wi-Fi):
   ```bash
   docker pull python:3.12-slim
   docker pull redis:7-alpine
   docker pull nginx:alpine
   docker pull alpine
   ```
3. **Run one-command setup & smoke test**:
   ```bash
   ./scripts/setup.sh
   docker compose exec api pytest -q
   ./scripts/setup.sh --stop
   ```
4. **Open workspace** `wbl-technical-learning-hub/docker` in your AI assistant and type `set up the class` followed by `teach module 1`.
