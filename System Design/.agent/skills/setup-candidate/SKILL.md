---
name: setup-candidate
description: Pre-class local environment verification for candidates taking the System Design course. Use when a student says "set up my environment", "check my laptop", or prepares for class. Validates Docker, curl, Python, terminal tools, and clones/verifies the course directory.
---

# Candidate Setup Guide

You help candidates verify that their laptop is fully configured before class begins.

## What is Verified
1. **Terminal**: Bash / Git Bash / Zsh working.
2. **Curl**: `curl --version` functional.
3. **Python**: Python 3.10+ installed and available (`python --version` or `python3 --version`).
4. **Docker Desktop**: Docker daemon running (`docker ps`).
5. **Network / Ports**: Port 8080 and 8000 free for local lab containers.

## Procedure
1. Ask the candidate which OS they are on (Windows WSL2/Git Bash, macOS, Linux).
2. Run or instruct them to run:
   ```bash
   docker --version && curl --version && python --version
   ```
3. Test container capability:
   ```bash
   docker run --rm hello-world
   ```
4. If anything fails, provide exact, platform-specific fixes (e.g., enabling WSL2 backend in Docker Desktop settings on Windows).
5. Confirm candidate has created their `candidate-state.md` progress file.
