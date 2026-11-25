# CANDIDATE START HERE: System Design Learning Guide

Welcome to the **System Design Track** (Scaling, Load Balancing, Caching, Queues, Microservices & The 5-Step Method)!

This document is your **complete guide to navigating this folder**, setting up your local machine, running live experiments, and using your AI tutors every evening.

---

## 1. How This Folder is Structured

```
System Design/
├── CANDIDATE-START-HERE.md    # ← You are here: Your personal study roadmap
├── README.md                  # Stack overview and quick-start guide
│
├── docs/                      # Your Core References
│   ├── student-guide.md       # Cheat sheets: Math constants, latency rules, 5-step template
│   └── course-toc.md          # Syllabus breakdown for Modules 1 to 8
│
├── course/modules/            # Module reading & end-of-module exercises
│   ├── 01-client-server-and-statelessness.md
│   ├── 02-load-balancing-and-routing.md
│   ├── 03-caching-and-staleness.md
│   ├── 04-message-queues-and-async-processing.md
│   ├── 05-database-scaling-and-storage.md
│   ├── 06-monolith-vs-microservices.md
│   ├── 07-repeatable-system-design-method.md
│   └── 08-capstone-system-design-studio.md
│
├── .agent/skills/             # AI Agents that coach you on your machine
│   ├── setup-candidate/       # Pre-flight laptop check
│   └── practice-system-design/# Quiz coach, design reviewer, hint ladder
│
├── prompts/                   # Universal Master Prompts for ChatGPT, Claude, Gemini, Grok
│   ├── candidate-state-template.md # ← Copy this to candidate-state.md (Your personal progress file)
│   ├── tutor-agent.md
│   ├── practice-agent.md
│   ├── coding-review-agent.md
│   └── quiz-assessment-agent.md
│
├── scripts/                   # Runnable system design tools
│   ├── setup.sh               # Starts local URL Shortener & Redis cluster
│   ├── load-test.sh           # Simulates concurrent traffic to test cache & scaling
│   └── smoke.sh               # 10-point health check
└── api/ & worker/ & gateway/  # The live codebase you inspect and scale
```

---

## 2. Laptop Setup (Day 0)

Before class begins, ensure your machine has the required tools:
1. **Docker Desktop** installed and running.
2. **Terminal** (Git Bash / WSL2 on Windows, Terminal on macOS/Linux).
3. **Curl** (`curl --version`).
4. **Python 3.10+** (`python --version`).

### Automated Setup Verification
Open this folder in your coding agent (Antigravity, Claude Code, Cursor) and type:
> **"set up my environment"**

Or run in your terminal:
```bash
./scripts/setup.sh
```
When it finishes with `[READY]`, your machine is fully verified!

---

## 3. Your Personal Memory: `candidate-state.md`

Agents forget everything when a chat ends. Your **`candidate-state.md`** is the memory you carry everywhere.
1. Copy the template from [`prompts/candidate-state-template.md`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/candidate-state-template.md) into your root as `candidate-state.md`.
2. Fill in your name, current module, and level band (`Ready`, `Catch-up`, `Stretch`).
3. Paste or attach this file at the start of every session with your AI tutor.
4. At the end of every session, save the updated state block back into your file.

---

## 4. The 2-Hour Evening Routine

Every evening after class, complete the structured 5-step loop:

```
[ Step 1: Tutor Review (30 min) ]
   ↓ Prompt: "Tutor: explain [topic] using The Growing City story, then check me with 2 questions."
[ Step 2: Hands-On Practice (45 min) ]
   ↓ Prompt: "Practice Agent: give me today's scenario task. One task at a time; check my evidence."
[ Step 3: Design Review & Code (30 min) ]
   ↓ Prompt: "Review Agent: review my 1-page design / code. Hints before solutions, always."
[ Step 4: Closed-Book Quiz (15 min) ]
   ↓ Prompt: "Quiz Agent: quiz me on today's topics only. 10 questions, one at a time, no answers until end."
[ Step 5: Daily Report (5 min) ]
   ↓ Send the generated Daily Report block to your instructor tonight.
```

---

## 5. Working with AI on Any Platform

You can use the 4 AI agents on any platform you prefer:

### Option A: Inside Your Coding Agent (Antigravity, Claude Code, Cursor)
Since this repository includes [`.agent/skills/`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/.agent/skills/), simply say:
- `"quiz me"` $\rightarrow$ starts the closed-book oral exam.
- `"review my system design"` $\rightarrow$ critiques your 1-page photo-sharing or URL shortener design.
- `"explain [topic]"` $\rightarrow$ re-teaches the concept with the story anchor.

### Option B: On ChatGPT, Gemini, Claude Web, or Grok
1. Open [`prompts/README.md`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/README.md).
2. Copy the relevant master prompt ([`tutor-agent.md`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/tutor-agent.md), [`practice-agent.md`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/prompts/practice-agent.md), etc.) into your Custom GPT, Project, or chat session.
3. Attach `docs/student-guide.md` and your `candidate-state.md`.

---

## 6. Running Local System Design Experiments

Don't just memorize theory—run it live on your laptop:

### 1. Test Cache Acceleration (Corner Shop)
```bash
# 1st read: Cache MISS (queries DB, takes ~5-15ms)
curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"

# 2nd read: Cache HIT (served from Redis RAM, takes <2ms)
curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"
```

### 2. Test Horizontal Load Balancing across 3 Replicas
```bash
# Start in scaled mode
./scripts/setup.sh --scale

# Run 30 requests and see the Traffic Controller (Nginx) balance load
./scripts/load-test.sh http://localhost:8080/health 30
```

### 3. See What Happens When the Database Jams
```bash
# Start with no cache to simulate DB lock contention
./scripts/setup.sh --nocache

# Observe response latency increase by 200ms+
curl -sI http://localhost:8080/r/wbl | grep -E "X-Cache|X-Response-Time"

# Restore healthy baseline
./scripts/fix.sh
```

---

## 7. The Program Exit Gate: What "Done" Looks Like

At the end of this course, you will demonstrate:
1. **The 5-Step Method**: Write a one-page architecture for a **Photo-Sharing App (1M users)** covering functional scope, QPS/storage calculations, high-level sketch, bottlenecks, and defended trade-offs.
2. **Live Request Walkthrough**: Walk one request through client, load balancer, stateless app, cache, database, and background queue out loud.
3. **Incident Diagnosis**: Look at HTTP status codes and response headers to diagnose a cache outage (`redis-down`) vs. database lock bottleneck (`db-bottleneck`).
