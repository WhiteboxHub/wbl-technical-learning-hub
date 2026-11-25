# INSTRUCTOR START HERE: System Design Course Runbook

Welcome! This document is the **single point of orientation for any instructor** teaching the **System Design** track in the Whitebox Learning Agentic AI Engineering Program.

Whether you are using **Antigravity, Claude Code, OpenAI Codex, Cursor**, or terminal CLI, this guide explains exactly how to navigate this folder, operate the stack, and teach with your AI co-pilot.

---

## 1. Quick Navigation: Where Everything Lives

```
System Design/
├── INSTRUCTOR-START-HERE.md   # ← You are here: Master instructor manual
├── CANDIDATE-START-HERE.md    # Candidate orientation manual
├── README.md                  # Stack overview and quick-start summary
│
├── .agent/skills/             # AI Co-pilot skills (compatible with ALL coding agents)
│   ├── setup-system-design-class/  # Automates Docker, port, and smoke testing
│   ├── teach-system-design-class/  # In-class beat-by-beat teaching engine
│   ├── setup-candidate/            # Pre-class candidate workstation verification
│   └── practice-system-design/     # Post-class student tutor & hint ladder
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
│   ├── instructor-guide.md         # Full pedagogical details & story anchors
│   ├── student-guide.md            # Student manual, math formulas & design template
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
└── prompts/                   # Universal platform-neutral prompts (for ChatGPT, Gemini, etc.)
```

---

## 2. How to Use the AI Co-Pilot with Any Coding Agent

All AI skills are located in [`.agent/skills/`](file:///c:/Users/AI%20ML%20PC%20Ajmeer/Desktop/Course%20Restructure/wbl-technical-learning-hub/System%20Design/.agent/skills/). They follow the open Agent Skill specification and work seamlessly in:
* **Antigravity (Google DeepMind)**
* **Claude Code (Anthropic)**
* **OpenAI Codex / ChatGPT CLI**
* **Cursor / Windsurf / Copilot Workspace**

### Step 1: Open the Folder
In your coding agent, open this folder:
```bash
wbl-technical-learning-hub/System Design
```
*Note: Always open this specific folder so `.agent/skills/` are loaded at session start.*

### Step 2: Set Up the Environment
In your agent chat, type:
> **"set up the class"** (or run `./scripts/setup.sh` in the terminal)

The agent executes `setup-system-design-class`:
1. Validates that Docker Desktop is active.
2. Checks that ports `8080`, `8000`, and `6379` are free.
3. Launches the containers and runs `scripts/smoke.sh` (10 automated verifications).
4. Outputs **`[READY]`** with active URLs.

### Step 3: Begin Teaching
In your agent chat, type:
> **"teach module 1"** (or module 2, 3... 8)

The agent executes `teach-system-design-class`:
1. Displays the module overview, time estimate, and key live demos.
2. Asks: **"Is your screen shared with candidates?"**
   - **Important**: If screen sharing is on, the agent **strictly hides all answers** until you ask for them, preventing answer leaks.
3. Walks the module **beat by beat**.

---

## 3. In-Class Voice / Text Controls

During class, the instructor talks to the room and draws on the board. The AI co-pilot waits for your command at every beat:

| You Say | What the Agent Does |
|---|---|
| `next` | Moves to the next beat (gives talking points, slide cue, demo) |
| `back` | Steps back to the previous beat |
| `repeat` | Re-executes the live demo commands |
| `answer` / `answer 1` | Reveals the hidden answer to the question asked |
| `take over` | Pauses agent execution while you sketch or lecture manually |
| `status` | Reports elapsed time, beats completed, and beats remaining |
| `jump 3.2` | Jumps directly to beat 3.2 |
| `end` | Wraps up the module, hands over the candidate exercise, and runs the exit check |

---

## 4. Class Flow: The Three Acts & The Story Anchor

Every System Design class is built on the **Storytelling Rule**:
> **Tell them what you are going to tell them. Tell them. Tell them what you told them.**

### The Story Anchor: *The Growing City*
Anchor every technical concept back to this metaphor:
- **Client** = City resident ordering goods.
- **Network** = Road subject to traffic jams and roadworks.
- **Monolith** = Central Market Hall (everything under one roof).
- **Load Balancer** = Traffic Controller at the roundabout directing cars down parallel streets.
- **Stateless Replicas** = Multiple identical market stalls.
- **Cache (Redis)** = Corner Shop keeping daily milk/bread near homes so trips to the warehouse are rare.
- **Message Queue** = Delivery Depot taking order tickets (`202 Accepted`) during the morning rush.
- **Database** = The Central Bank Ledger where all transactions must be recorded.
- **Microservices** = Specialized boutique shops across the city.

---

## 5. Module 8 Capstone: Running the Break-It Incident Workshop

In Module 8, you test candidate intuition using `scripts/break.sh`. The room must diagnose each fault from evidence (curl status codes, headers, and logs) before you fix it:

1. **Inject Cache Crash**:
   ```bash
   ./scripts/break.sh redis-down
   ```
   - *Symptom*: Requests to `/r/wbl` still succeed, but latency increases and returns `X-Cache: MISS`. App logs show Redis connection errors.
   - *Teaching Point*: Graceful degradation vs. sudden database overload.

2. **Inject Database Bottleneck**:
   ```bash
   ./scripts/break.sh db-bottleneck
   ```
   - *Symptom*: Direct DB queries take >1500ms; gateway times out or clients lag.
   - *Teaching Point*: Why adding more app servers does not fix stateful lock contention.

3. **Inject Rate Limiting**:
   ```bash
   ./scripts/break.sh rate-limit
   ```
   - *Symptom*: 1st request succeeds, subsequent requests return `429 Too Many Requests` with `Retry-After`.
   - *Teaching Point*: Edge protection and client exponential backoff.

4. **Inject Stalled Workers**:
   ```bash
   ./scripts/break.sh queue-backlog
   ```
   - *Symptom*: Async shorten returns `202 Accepted`, but URLs take minutes to appear; queue length metric grows.
   - *Teaching Point*: Backpressure and decoupling.

*Always restore baseline between faults:*
```bash
./scripts/fix.sh
```

---

## 6. Post-Class Wrap-up
1. Say `end` to your agent co-pilot.
2. Hand over the **Exercise** text to the room.
3. The agent logs session progress, student sticking points, and timing in `.class/progress.md`.
4. Run `./scripts/fix.sh` to ensure the environment is ready for the next session.
