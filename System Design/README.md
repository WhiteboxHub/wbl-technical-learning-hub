# System Design — Scaling, Load Balancing, Caching & Queues

Running example: **The Growing City URL Shortener & Scaling Platform**.  
Story anchor: **The Growing City** (Load balancer = traffic controller, cache = corner shop, queue = depot, microservices = specialised shops, monolith = one central market hall).

---

## 🚦 START HERE

| Role | Start File | What It Explains |
|---|---|---|
| **Instructors** | [**`INSTRUCTOR-START-HERE.md`**](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/INSTRUCTOR-START-HERE.md) | Classroom setup, running live beats with AI co-pilot, managing hidden answer keys, running incident triage demos, and post-class wrap-up. |
| **Candidates / Learners** | [**`CANDIDATE-START-HERE.md`**](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/CANDIDATE-START-HERE.md) | Laptop setup, navigating exercises, 5-step system design template, back-of-the-envelope math cheat sheet, and 2-hour evening AI tutor routine. |

---

## 🧭 Repository Structure

```
System Design/
├── INSTRUCTOR-START-HERE.md   # Primary guide for instructors
├── CANDIDATE-START-HERE.md    # Primary guide for candidates
├── README.md                  # This file
│
├── .agent/skills/             # Universal agent skills (Antigravity, Claude Code, Codex, Cursor)
│   ├── setup-system-design-class/  # Automates Docker, port, and smoke testing
│   ├── teach-system-design-class/  # In-class beat-by-beat teaching engine
│   ├── setup-candidate/            # Pre-class candidate workstation verification
│   └── practice-system-design/     # Post-class student tutor & hint ladder
│
├── prompts/                   # Platform-neutral master prompts (ChatGPT, Gemini, Claude Web, Grok)
│   ├── tutor-agent.md
│   ├── practice-agent.md
│   ├── coding-review-agent.md
│   ├── quiz-assessment-agent.md
│   └── candidate-state-template.md # Student memory file template
│
├── course/modules/            # 8 complete beat-by-beat lesson scripts
│   ├── 01-client-server-and-statelessness.md
│   ├── 02-load-balancing-and-routing.md
│   ├── 03-caching-and-staleness.md
│   ├── 04-message-queues-and-async-processing.md
│   ├── 05-database-scaling-and-storage.md
│   ├── 06-monolith-vs-microservices.md
│   ├── 07-repeatable-system-design-method.md
│   └── 08-capstone-system-design-studio.md
│
├── docs/                      # Reference documents & guides
│   ├── class-day-quickstart.md     # 5-minute pre-class cheat sheet
│   ├── instructor-guide.md         # Pedagogical guide & story anchors
│   ├── student-guide.md            # Reference sheets & math formulas
│   └── course-toc.md               # Complete syllabus breakdown
│
├── api/                       # Stateless URL Shortener service (FastAPI)
├── worker/                    # Asynchronous Queue Worker (The Depot)
├── gateway/                   # Nginx Reverse Proxy & Load Balancer (:8080)
├── scripts/                   # Automated orchestration & incident injection scripts
│   ├── setup.sh & smoke.sh         # Stack lifecycle & 10-point assertion test
│   ├── load-test.sh                # Live concurrency & latency test
│   ├── break.sh                    # Injects 4 live production failure modes
│   └── fix.sh                      # Cleans faults and restores healthy baseline
└── docker-compose*.yml        # Composable Docker deployment manifests
```

---

## ⚡ Quick Start: Start the Stack
Requires Docker Desktop running.

```bash
# Start standard single-node baseline stack + smoke test
scripts/setup.sh

# Or start in scaled mode (3 stateless replicas behind Nginx load balancer)
scripts/setup.sh --scale

# Or start with no-cache to simulate database bottleneck under load
scripts/setup.sh --nocache
```

### Key Service Endpoints
- **Gateway / Load Balancer**: http://localhost:8080
- **Direct App Node**: http://localhost:8000
- **Health Check & Node ID**: http://localhost:8080/health
- **Short URL Redirection**: `GET http://localhost:8080/r/{short_code}`
- **Create Short URL**: `POST http://localhost:8080/api/shorten`
- **URL Statistics**: `GET http://localhost:8080/api/stats/{short_code}`
- **System Telemetry / Metrics**: http://localhost:8080/api/metrics
- **Redis Cache & Queues**: `localhost:6379`

### Run Tests & Verification
```bash
# Execute smoke test (10 automated system assertions)
./scripts/smoke.sh

# Execute load test (measures cache hit vs miss & replica distribution)
./scripts/load-test.sh http://localhost:8080/r/wbl 50

# Reset to clean seed data
./scripts/setup.sh --reset
```
