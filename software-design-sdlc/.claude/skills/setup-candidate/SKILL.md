---
name: setup-candidate
description: Candidate (student) setup for the Software Design, Architecture, SDLC & Agile (Jira) course. Use when a candidate wants to get ready for class, says "set up my environment", or needs to verify their practice setup. Verifies the course folder, introduces all 5 modules, walks through Atlassian Jira Cloud setup, and initializes .practice/progress.md.
---

# Candidate Setup: Software Design, Architecture, SDLC & Agile (Jira)

Prepare the candidate for hands-on learning across all 5 modules and Atlassian Jira Cloud practice. Keep each step clear, concise, and explain *why* it is needed before moving to the next step.

Running project anchor: **Building a House (The Smart House Construction Project)**.

## Steps

1. **Set Up & Verify the Course Folder:**
   - Open a terminal inside the course folder and verify all modules, docs, and skills exist:
     ```bash
     cd wbl-technical-learning-hub/software-design-sdlc
     ls -la course/modules docs .claude/skills .agent/skills
     ```
   - Open this `software-design-sdlc/` folder directly in **Claude Code** or **Antigravity** and start a **fresh session** so the skills auto-load.
   - No Docker containers, local databases, or coding IDEs are required.

2. **Overview of All 5 Modules (What You Will Learn & Practice):**
   - **Module 1 — Software Architecture & System Design** (`01-software-architecture-and-design.md`): Client-Server, 3-Tier vs. MVC, Distributed Computing & Coupling, Batch-Sequential vs. Pipes & Filters, P2P/Plugin/Search-Oriented, Cloud (IaaS, PaaS, SaaS), Monolithic vs. Microservices.
   - **Module 2 — SDLC Models & ALM** (`02-sdlc-models-and-alm.md`): SDLC vs. ALM, 10 ALM Roles, Waterfall, V-Model, Prototyping & Code-and-Fix Trap, RAD & Incremental, Spiral Model, Agile Frameworks (FDD, DSDM, XP) & Tailored Hybrid SDLC.
   - **Module 3 — Agile, Scrum & Kanban** (`03-agile-and-scrum-framework.md`): Agile 4 Values & 12 Principles, Agile vs. Waterfall, Scrum/Kanban/SAFe/XP, Scrum Roles/Ceremonies/Artifacts, Kanban Flow & WIP Limits, INVEST User Stories, Fibonacci Story Points, DoR/DoD, Velocity.
   - **Module 4 — Jira in Practice** (`04-jira-in-practice.md`): Jira Cloud setup (`HOUSE`), Epics/Stories/Tasks/Subtasks/Bugs, Backlog Grooming & Sprint Creation, Active Sprint Board & Daily Standups, Burndown/Velocity/CFD & Dashboards.
   - **Module 5 — Capstone: Blueprint to Jira** (`05-capstone-system-design-to-jira.md`): End-to-end Smart Home architecture blueprint, Threat Model, SDLC & ALM mapping, INVEST Backlog, Sprint 1 planning, and Burndown defense.

3. **Set Up Browser & Live Atlassian Jira Cloud (For Modules 4–5):**
   - Confirm the candidate has a modern browser (Chrome, Edge, or Firefox), then walk them through creating their free practice project:
     1. **Go to Jira & Sign Up / Log In**:
        - Open [https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free) and click **Get it free** (free forever for up to 10 users, no credit card required).
        - Sign up or log in with Google or email.
     2. **Claim Your Jira Site URL**:
        - Enter a unique site name, e.g. `https://<your-name>-smarthouse.atlassian.net`, and click **Agree and sign up** (~30 seconds to provision).
     3. **Create the Scrum Project & `In Review` Column**:
        - Choose **Software Development** $\rightarrow$ **Scrum** template.
        - **Project Name**: `Smart House Construction & Management` | **Project Key**: `HOUSE`.
        - Click **Create Project**.
        - On the **Board**, click **`+ Create column`** (or **Board settings**) and add an **`In Review`** column/status between `In Progress` and `Done`.
     4. **Set Up Your Live Dashboard**:
        - In the top navigation bar, click **Dashboards** $\rightarrow$ **Create dashboard** (`Smart House Executive Dashboard`), click **Add gadget**, and add **Sprint Health** and **Sprint Burndown**.
        - Once your `HOUSE` project is ready, type `help with jira` to practice creating Epics, Stories, Subtasks, Bugs, and Sprints.

4. **Initialize Progress & Wrap Up:**
   - Create `.practice/progress.md` if it does not exist yet (tracking `Current Module`, `Remaining / Pending Topics`, `Weak Areas`, and `Interview Focus`).
   - Point them to `docs/student-guide.md` and show what they can type next:
     - `learn module 1` — Self-paced, beat-by-beat interactive lessons (resumes from `Remaining / Pending Topics`)
     - `help with the exercise` / `explain [concept]` — Guided help for Modules 1–5
     - `help with jira` — Guided practice creating Epics, INVEST Stories, Subtasks, Bugs, and Sprints in `HOUSE`
     - `quiz me` / `check my user story` — Concept checks and INVEST story reviews
     - `interview questions on module 1` / `mock interview` — Scenario-based interview practice
