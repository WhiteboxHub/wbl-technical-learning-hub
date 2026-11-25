# Class-Day Quick Start: System Design

5-minute checklist for instructors before teaching.

## 1. 10 Minutes Before Class
- [ ] Docker Desktop is running.
- [ ] Open terminal in `wbl-technical-learning-hub/System Design`.
- [ ] Start new session in your agent tool so `.claude/skills/` load.
- [ ] Run: `scripts/setup.sh` (or prompt: `"set up the class"`).
- [ ] Verify smoke test output displays 10 `OK` checks.

## 2. 5 Minutes Before Class
- [ ] Open shared whiteboard tool (Excalidraw, Miro, or physical board) with pre-drawn *Growing City* village template:
  - Client (Resident)
  - Road (Network)
  - Market Hall (Monolith App)
  - Central Ledger (Database)
- [ ] Decide on screen-sharing mode (agent hides answers by default).

## 3. Class Start
1. Type: `teach module 1`
2. Deliver the story anchor: *The Growing City*.
3. Use prompt controls: `next`, `repeat`, `answer`, `status`, `end`.

## 4. Emergency Troubleshooting
- **Docker not running**: Start Docker Desktop, wait for icon to turn green, run `scripts/setup.sh`.
- **Port 8080/8000 in use**: Run `netstat -ano | findstr :8080` and stop conflicting local service.
- **Demo output unexpected**: Run `scripts/setup.sh --reset`.
- **Stack stuck**: Run `scripts/setup.sh --stop`, then `scripts/setup.sh`.
