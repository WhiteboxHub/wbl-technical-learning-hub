# Software Design, Architecture, SDLC and Agile (JIRA) — Course Repo

Running story anchor: **Building a House** (from architectural blueprints and foundations to framing, modular additions, permits, subcontractor standups, and Jira-managed construction sprints).

## Overview
This course provides foundational mastery in:
1. **Software Architecture & System Design Patterns** (Client-Server, 3-Tier/N-Tier, MVC, Distributed Systems, Batch-Sequential, P2P, Plugin, Search-Oriented, Cloud SaaS/PaaS/IaaS, and **Monolithic vs Microservices Architecture**).
2. **SDLC Frameworks & Application Lifecycle Management (ALM)** (ALM Roles, Waterfall, V-Model, Spiral, RAD, Iterative/Incremental, Agile SDLC, FDD, DSDM, Tailored SDLC).
3. **Agile Methodology & Scrum/Kanban Frameworks** (Manifesto & 12 Principles, Scrum Roles & Ceremonies, Kanban WIP Limits, User Stories, Story Points, DoR/DoD, Velocity & Burndown).
4. **Jira in Practice** (Epics, Stories, Tasks/Subtasks, Sprints, Agile Boards, Workflows, Dashboards, and Reporting).
5. **Capstone End-to-End Lab** (Translating an architectural design into a fully estimated, sprint-ready Jira project).

---

## Quick Navigation & Guides
- [Class-day quick start](docs/class-day-quickstart.md) — Pre-flight checklist before class starts
- [Instructor Guide](docs/instructor-guide.md) — Step-by-step facilitation, pacing, teaching with the Claude/AGY agent co-pilot
- [Student Guide](docs/student-guide.md) — Student setup, agile cheatsheet, architecture reference, and hands-on exercises
- [Instructor Steps](instructor-steps.md) — Exact vocal beats, commands, and teaching script
- [Course Table of Contents](docs/course-toc.md) — Comprehensive syllabus mapping topics to modules

---

## Getting Started

In chat with your AI assistant, type:
```text
set up the class
```
When verified, type `teach module 1` to begin.

- **Story Anchor**: Building a House
- **Hands-on Tooling**: Real Atlassian Jira Cloud in Web Browser (No local HTML files or mock dashboards)
  - Free sign-up: [https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free) (Up to 10 users free forever, no credit card required)
  - Project Template: **Scrum** project named `Smart House Construction & Management` (Key: `HOUSE`)
  - Live Dashboard: `https://<your-subdomain>.atlassian.net/jira/dashboards`
  - Zero-Docker / Zero Local Servers: No local containers or backend servers are required. All hands-on Agile/Scrum execution runs directly in live Atlassian Jira Cloud.
- **AI Teaching Co-Pilot**: Type `teach module 1` in chat to begin (skills in `.claude/skills/` and `.agents/skills/`)

---

## The Story Anchor: Building a House
Throughout this course, abstract software and project management concepts are mapped to building a house:
- **Architectural Blueprints** $\rightarrow$ Software Architecture (Load-bearing walls, foundations, plumbing & electrical tiers).
- **Client-Server & 3-Tier** $\rightarrow$ The homeowner (Client), the living spaces/appliances (Presentation & Business Logic), and municipal water/power grids (Data Tier).
- **Waterfall vs Agile** $\rightarrow$ Rigid monolithic skyscraper construction (fixed plans, no changes allowed) vs modern modular home building (iterative room additions, early move-in, continuous homeowner feedback).
- **ALM Roles** $\rightarrow$ Homeowner (Business Manager), Architect (Software Architect), General Contractor (Project Manager / Scrum Master), Plumbers/Electricians/Carpenters (Developers/DBAs), Building Inspector (QA Tester), Property Maintenance (DevOps/Operations).
- **Jira Hierarchy** $\rightarrow$
  - **Epic**: Construct the Kitchen / Master Suite / Electrical Infrastructure.
  - **Story**: As a homeowner, I want hot water running in the kitchen sink so that I can wash dishes.
  - **Task / Subtask**: Run PEX hot water lines (Dev), pressure-test pipes for leaks (QA).
  - **Sprint**: 2-week construction cycle with daily morning subcontractor tailgate standup.
  - **Definition of Done (DoD)**: Inspected by building inspector, water flowing at 50 PSI, clean inspection certificate signed.

---

## Course Modules
- **Module 01: Software Architecture & System Design**: Client-Server, 3-Tier/N-Tier, Distributed Systems, Cloud & **Microservices** (Story Anchor: Blueprints, Foundation, N-Tier Utilities, Modular Plugins & Smart-Home Microservice Units).
- **Module 02: SDLC Models & ALM Frameworks**: ALM Lifecycles, Waterfall, V-Model, Spiral, RAD, & Agile (Story Anchor: The Construction Process: Rigid Blueprints vs Iterative Builds).
- **Module 03: Agile Methodology & Scrum / Kanban**: Agile Manifesto, Scrum Roles & Ceremonies, Kanban & INVEST (Story Anchor: The Self-Organizing Subcontractor Crew & Daily Jobsite Standups).
- **Module 04: Jira in Practice: Hands-on Execution**: Jira Project Hierarchy, Backlogs, Sprints, & Burndown Metrics (Story Anchor: Digital Jobsite Board: Epics, Stories, Sprints, & Burndown Charts).
- **Module 05: Capstone: Architectural Blueprint to Jira**: Full Course Capstone Synthesis (Story Anchor: Blueprint to Delivery: Full System Design into Backlog & Sprint).

---

## Post-Class Self-Study & Technical Interview Preparation
This repository is a self-contained learning lab for candidates after class completes. Candidates can return in the evening, on weekends, or during job interview preparation to practice with the AI coach:
- **`interview questions on module N`**: Starts a senior-level technical interview round on that module.
- **`mock interview`**: Comprehensive multi-topic interview across Architecture, SDLC, Scrum, and Jira.
- **`quiz me on module N`**: Socratic check questions with progressive hints.
- **`check my user story`**: Audits user stories against the 6 INVEST principles and Given-When-Then criteria.
- **`help with the exercise`**: Step-by-step guidance for end-of-module architecture blueprints and Jira sprints.

---

## Repository Layout (In Recommended Reading & Execution Order)
```
software-design-sdlc/
├── README.md                          # [1. START HERE] Course overview, story anchor, Jira Cloud setup
├── instructor-steps.md                # [2. INSTRUCTOR FLOW] Beat-by-beat live delivery commands
│
├── docs/                              # [3. GUIDES & SYLLABUS]
│   ├── class-day-quickstart.md        #   3a. 5-minute pre-flight checklist
│   ├── course-toc.md                  #   3b. Complete syllabus (Modules 1–5)
│   ├── instructor-guide.md            #   3c. Facilitation & pedagogy guide
│   └── student-guide.md               #   3d. Student cheatsheets & step-by-step Jira Cloud guide
│
├── course/                            # [4. CURRICULUM CONTENT (MODULES 01–05)]
│   ├── course-backlog.md              #   Course roadmap & backlog
│   └── modules/
│       ├── 01-software-architecture-and-design.md   # Architecture, 3-Tier, Cloud & Microservices
│       ├── 02-sdlc-models-and-alm.md                # ALM 10 Roles, Waterfall, V-Model, Spiral, Agile
│       ├── 03-agile-and-scrum-framework.md          # Scrum, Kanban, INVEST, Story Points
│       ├── 04-jira-in-practice.md                   # Jira Cloud Epics, Stories, Sprints & Reports
│       └── 05-capstone-system-design-to-jira.md     # End-to-End Blueprint to Active Jira Sprint
│
├── .claude/skills/                    # [5a. CLAUDE CODE — Auto-discovered skills]
│   ├── setup-sdlc-class/              #   Instructor pre-flight check
│   ├── teach-sdlc-class/              #   Live beat-by-beat co-pilot
│   ├── setup-candidate/               #   Candidate Jira Cloud onboarding & login steps
│   └── practice-sdlc/                 #   Candidate coach, mock interviews & Jira walkthrough
│
└── .agents/skills/                    # [6b. GOOGLE ANTIGRAVITY / GEMINI CLI — Auto-discovered skills]
    ├── setup-sdlc-class/              #   Instructor pre-flight check  (mirror of .claude/skills/)
    ├── teach-sdlc-class/              #   Live beat-by-beat co-pilot   (mirror of .claude/skills/)
    ├── setup-candidate/               #   Candidate Jira Cloud onboarding (mirror of .claude/skills/)
    └── practice-sdlc/                 #   Candidate coach & mock interviews (mirror of .claude/skills/)
```

> **Multi-Agent Ecosystem**: Skills are mirrored under both `.claude/skills/` (Claude Code auto-discovery) and `.agents/skills/` (Google Antigravity / Gemini CLI auto-discovery). Both sets are identical in content — if you update a skill, edit it in `.claude/skills/` then re-copy to `.agents/skills/` to keep them in sync.
