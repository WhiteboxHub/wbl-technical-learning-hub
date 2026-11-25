# Instructor Steps: How to Start and Teach the Software Design & SDLC Course

Course: **Software Design, Architecture, SDLC, Agile & Jira**  
Anchor Story: **Building a House**  
Project Folder: `wbl-technical-learning-hub/software-design-sdlc`  
Reference Curriculum: Software Architecture, SDLC Models, Agile Methodology & Jira  

---

## 1. Before Class (Instructor Checklist)
1. **Open the correct workspace**:
   - In Claude Code / Antigravity, open `wbl-technical-learning-hub/software-design-sdlc`.
   - Start a fresh session so the native skills load properly (`.claude/skills/` for Claude Code, `.agents/skills/` for Antigravity / Gemini CLI).
2. **Verify Environment (Zero-Docker / Cloud-First)**:
   - In chat, type: `set up the class` or `verify setup` to verify all 5 modules, 5 skills, and documentation.
   - Note: No local Docker containers or backend servers are needed. All hands-on Agile/Scrum execution runs in live Atlassian Jira Cloud in the web browser.

---

## 2. Starting the Class with the AI Co-Pilot
1. Type: **`setup sdlc class`** or **`set up the class`**
   - The agent verifies modules, prompts, documentation, and skills readiness.
2. Type: **`teach module N`** (e.g., `teach module 1` or `teach module 3`).
3. The AI agent asks:
   > *"Is your screen shared with candidates?"*
   - If **Yes**, the agent holds back quiz answers and spoilers until you say `answer`.
   - If **No**, you will see talking points and answers together on your private screen.

---

## 3. Teaching Commands Reference
The AI co-pilot works one beat at a time. It prompts you with core concept titles, key talking points, real-world house analogies, interactive whiteboard/lab exercises, and Socratic check questions.

- `next`: Advance to the next beat (presents full beat in depth)
- `back`: Return to the previous beat
- `repeat`: Re-explain the current concept or re-run the demonstration
- `skip`: Skip the current beat and log it in `.class/progress.md`
- `answer` / `answer [n]`: Reveal the answer to the question asked
- `more`: Provide an additional real-world scenario or house analogy
- `status`: Show current progress, time elapsed, and completed beats
- `take over`: Pause AI co-pilot while the instructor leads an open debate or exercise
- `jump N.M`: Jump directly to a specific beat (e.g., `jump 2.3` or `jump 4.2`)
- `end`: Conclude the module, present the hands-on lab exercise, and record the done-check

---

## 4. Module Teaching Overview

### Module 1: Software Architecture & System Design
- **Anchor**: Building a House (Foundation, Load-bearing structure, Electrical/Plumbing tiers, Modular room extensions).
- **Key beats**: Client-Server, 3-Tier vs MVC, Distributed Computing, Batch-Sequential, P2P, Plugin Architecture, Search-Oriented, Cloud SaaS/PaaS/IaaS.
- **Core takeaway**: Architecture is making fundamental structural choices that are expensive to change later.

### Module 2: SDLC Models & Application Lifecycle Management
- **Anchor**: Construction Contracts & Project Timelines (Fixed-bid turnkey vs iterative build).
- **Key beats**: What is SDLC & ALM, The 10 ALM Roles, Waterfall Model & Strengths/Deficiencies, V-Shaped Model & Verification/Validation, Incremental/Spiral/RAD, Agile SDLC & 12 Principles, FDD & DSDM, Tailoring SDLC.
- **Core takeaway**: Match the development methodology to requirements volatility and risk profile.

### Module 3: Agile Methodology & Scrum / Kanban Framework
- **Anchor**: The Jobsite Crew (Subcontractors, daily morning huddles, visual Kanban boards).
- **Key beats**: Agile Manifesto 4 Values & 12 Principles, Agile vs Waterfall, Scrum Roles, Ceremonies & Artifacts, Kanban Principles & WIP Limits, User Stories, Story Points, DoR & DoD, Burndown & Velocity.
- **Core takeaway**: Agile is a mindset of continuous value delivery and rapid feedback loops, not just meetings.

### Module 4: Jira in Practice
- **Anchor**: The Contractor's Work Board (From blueprints to task boards and progress tracking).
- **Key beats**: What is Jira & Setup, Issue Hierarchy: Epic $\rightarrow$ Story $\rightarrow$ Task/Subtask $\rightarrow$ Bug, Sprint Creation & Goal Setting, Daily Standups & Board Management, Product vs Sprint Backlog, Workflows & Dashboards.
- **Core takeaway**: Jira translates user requirements into prioritized, trackable, and verifiable increments of work.

### Module 5: Capstone Lab
- **Hands-on Synthesis**: Candidates receive an architectural specification for a "Smart Home Management System" and build out the full Jira project from scratch (Epics, Stories with acceptance criteria, Story Points, Sprint Backlog, and mock Daily Standup simulation).

---

## 5. End of Module Protocol
1. Say `end` to conclude.
2. Present the candidate lab assignment from the module file.
3. Conduct the **Done-Check** (verify every student meets the exit criteria).
4. Review student entries in `.class/progress.md`.

