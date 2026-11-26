# Module 5 — Capstone: Architectural Blueprint to Jira

Teach-skill content file. Format is described in `.claude/skills/teach-sdlc-class/SKILL.md`.  
Story Anchor: **Building a House** (From Full Architectural Blueprints to an Active, Tracked Jira Construction Sprint).  

## Objectives
This capstone synthesizes all four preceding modules:
1. Translating business requirements into a **System Architecture Blueprint** (3-Tier, Client-Server, Cloud Services).
2. Selecting and defending a **Tailored SDLC Model** for multi-component delivery.
3. Defining **Scrum Roles, Ceremonies, DoR, and DoD**.
4. Constructing a complete, production-ready **Jira Project Backlog** (Epics, INVEST User Stories, Acceptance Criteria, Story Points, Subtasks).
5. Executing a **Simulated Sprint & Daily Standup**, resolving an unexpected blocker, and analyzing Burndown velocity metrics.

---

### Capstone Scenario: The "Apex Smart-Home Management System"
A residential construction startup, **"Apex Modular Homes"**, is building next-generation modular homes. Each home features smart IoT environmental controls (thermostat, smart locks, solar power monitoring) and a homeowner mobile/web portal. Your candidates act as Lead Architects and Project Leads designing and delivering the full system.

---

### Beat 5.1 — Capstone System Architecture Blueprint & Threat Model

- **Story Anchor (Building a House):**
  Before ordering lumber or digging a foundation, the master architect draws blueprints defining the living areas (Presentation Tier), the behind-the-wall utility manifold (Logic Tier), and municipal hookups (Data Tier). In our smart house, door locks and thermostats must never connect directly to the public internet or raw SQL database.
- **Say (Key Talking Points):**
  - **Tier 1 (Presentation)**: Mobile App & Web Browser Client. Uses secure token authentication.
  - **Tier 2 (Logic / Application)**: Application backend services and microservices routing through an API Gateway. Enforces business validation and security authorization.
  - **Tier 3 (Data Persistence)**: Relational database for accounts/billing + Time-series database for IoT sensor telemetry.
  - **Cloud Model Classification**:
    - *IaaS*: Virtual private cloud (VPC), firewalls, and custom edge routing.
    - *PaaS*: Container runtimes, managed PostgreSQL, and Redis caching.
    - *SaaS*: Stripe payment processing, Jira project tracking.
- **Demo / Blueprint Boundary Review (run: instructor):**
  Review the complete 3-Tier architectural blueprint:
  1. Presentation Tier (Mobile App & Web Portal): Handles user authentication UI and telemetry dashboards.
  2. Application Logic Tier: Orchestrates automation rules, validates permissions, and enforces business logic.
  3. Data Tier: PostgreSQL database on private VPC subnet.
  **Point out:**
  - The Presentation tier cannot bypass the Logic tier to query PostgreSQL directly.
  - Client credentials never touch the database tier.
- **Ask (Check Questions):**
  - Q: Why should IoT smart locks authenticate via the Logic Tier API rather than connecting directly to the PostgreSQL database? — A: Direct database connections expose database credentials, bypass business validation/auditing, and create high coupling and severe security vulnerabilities.
  - Q: In cloud computing models, why is our Jira workspace classified as SaaS while our container runtime is PaaS? — A: Jira is turnkey end-user software delivered over the web (zero infrastructure management); container runtimes are application platforms where we deploy our own code.
- **Done when:** Candidates can draw the 3-tier architecture diagram and classify each service into IaaS, PaaS, or SaaS.

---

### Beat 5.2 — SDLC Model Selection & ALM Team Mapping

- **Story Anchor (Building a House):**
  Building a custom luxury home requires different strategies for different rooms. The structural foundation and physical door-lock deadbolts require zero-defect upfront engineering (Waterfall / V-Model). However, interior paint colors, kitchen tile layouts, and smart speaker routines can be iterated sprint-by-sprint with the homeowner (Agile Scrum).
- **Say (Key Talking Points):**
  - **The Hybrid Defense**:
    - *Physical Firmware & Door Locks*: Safety-critical, regulated domain. Use **V-Shaped SDLC** with rigorous verification (unit tests, static analysis) and validation (penetration tests, physical door-jam stress tests).
    - *Homeowner Mobile App & Web Portal*: Volatile, consumer-facing requirements. Use **Agile Scrum** in 2-week sprints with continuous homeowner feedback.
  - **Mapping the 10 ALM Roles**:
    - Product Owner: Voice of the homeowner, prioritizes feature backlogs.
    - Scrum Master: Shields the team, removes impediments, ensures agile ceremonies run on time.
    - System Architect: Enforces 3-tier decoupling and API interface contracts.
    - Full-Stack / Mobile Developers: Implement user stories and technical subtasks.
    - QA / SDET Engineers: Build automated regression suites, Shift-Left verification checklists.
    - DevOps / SRE: Maintain Docker containers, CI/CD deployment pipelines, and database reliability.
- **Demo / Model Synthesis (run: instructor):**
  Review the tailored hybrid SDLC architecture:
  - Safety-critical IoT lock firmware $\rightarrow$ V-Model with formal verification checklists and penetration testing.
  - Resident mobile portal $\rightarrow$ Agile Scrum with 2-week iterations and customer feedback loops.
  **Point out:**
  - How modern enterprise teams blend predictive rigor for regulated core systems with iterative speed for customer-facing interfaces.
- **Ask (Check Questions):**
  - Q: Why would using 100% pure Waterfall for the mobile app lead to project failure? — A: User requirements and UI preferences change rapidly; Waterfall defers testing and user feedback until the end, resulting in high risk of building the wrong product.
- **Done when:** Candidates can defend the tailored hybrid model and assign ALM responsibilities to each team member.

---

### Beat 5.3 — Jira Project Creation & INVEST Backlog Authoring

- **Story Anchor (Building a House):**
  In the construction trailer, the contractor creates three master project folders: **"Foundation & Structural Architecture"**, **"Plumbing, Electrical & Utility Tiers"**, and **"Smart Home Automation & IoT Security"** (Epics). Under Smart Home Automation, the lead writes work orders for door locks and thermostats (Stories), each with an inspection checklist (Acceptance criteria) and trade requirements (Subtasks).
- **Say (Key Talking Points):**
  - **Jira Issue Hierarchy**:
    - **Epic**: High-level strategic initiative spanning multiple sprints (e.g. `Access Control & Security Management`).
    - **Story**: User-centric deliverable delivering standalone business value (`As a homeowner, I want to remotely unlock my front door...`).
    - **Task / Subtask**: Technical implementation chore (Dev API endpoint, QA test script).
    - **Bug**: Defect found during sprint testing.
  - **INVEST Criteria Checklist**: Independent, Negotiable, Valuable, Estimable, Small, Testable.
  - **Given-When-Then Acceptance Criteria**: Standard Gherkin format removing ambiguity between Dev and QA.
- **Demo / Jira Story Creation (run: instructor):**
  Author an INVEST-compliant user story in Jira Cloud:
  - Project: Smart House Construction
  - **Parent**: Epic **Foundation & Structural Architecture**
  - Issue Type: Story
  - Summary: "Homeowner remote door unlock via mobile app"
  - Description: "As a homeowner, I want to remotely unlock my front door via smartphone so that I can let family inside when away."
  - Acceptance Criteria: Given resident authenticates with MFA, When user taps unlock, Then door deadbolt disengages within 1.5 seconds.
  - Story Points: 5
  **Point out:**
  - The story delivers standalone end-user value and carries clear, testable acceptance criteria.
- **Ask (Check Questions):**
  - Q: Why is "Install PostgreSQL 16 database" a Task rather than a User Story? — A: It provides no direct customer-facing business value on its own; a story must deliver value to an end-user role (`As a... I want... So that...`).
- **Done when:** Candidates author at least 3 INVEST user stories with acceptance criteria and Fibonacci story points.

---

### Beat 5.4 — Sprint 1 Planning & Daily Standup Blocker Simulation

- **Story Anchor (Building a House):**
  It is 7:30 AM on Monday morning. The general contractor circles the crew in their trucks for a 15-minute tailgate standup. The plumber says: *"I laid the hot water pipe manifold yesterday, but the city water main shutoff is locked with a master padlock."* The contractor immediately steps in to call city hall, freeing the plumber to work on indoor piping while the blocker is cleared.
- **Say (Key Talking Points):**
  - **Sprint Cadence & Goal**: 2-week timebox. Sprint Goal: *"Enable secure remote door unlock and telemetry logging for beta homeowners."*
  - **The 3 Daily Standup Questions**:
    1. What did I accomplish yesterday that helped the team meet the Sprint Goal?
    2. What will I work on today to help the team meet the Sprint Goal?
    3. What impediments or blockers are in my way?
  - **Role of the Scrum Master**: The Scrum Master does NOT manage tasks—they aggressively remove external impediments and protect the team from sprint scope changes.
- **Demo / Standup Board Simulation (run: instructor):**
  In Jira Cloud, advance a story from To Do to In Progress and simulate a blocker:
  - Drag the **"Poured Concrete Foundation with Rebar"** story card into `In Progress`.
  - In the morning standup, the team identifies a blocker (city inspector permit delayed).
  - Right-click card $\rightarrow$ **Add Flag (Impediment)** in Jira.
  **Point out:**
  - The card turns yellow/flagged on the active board, alerting the Scrum Master to clear the impediment immediately.
- **Ask (Check Questions):**
  - Q: During a daily standup, a developer starts a 20-minute debate on database indexing algorithms. What should the Scrum Master do? — A: Call "table it for after standup" (the 16th minute meeting / parking lot) to keep the standup under 15 minutes.
- **Done when:** Candidates run a mock 15-minute daily standup, log a blocker, and advance cards on the sprint board.

---

### Beat 5.5 — Burndown Analysis & Capstone Architecture Defense

- **Story Anchor (Building a House):**
  At the end of the 2-week sprint, the contractor and homeowner walk through the master bedroom. The homeowner turns on the faucet—hot water flows, the city inspector signs the permit, and the DoD is passed. On the trailer wall, the burndown line drops to zero points.
- **Say (Key Talking Points):**
  - **Sprint Burndown Mechanics**: X-axis = sprint working days (Day 1 to 10); Y-axis = remaining committed story points.
  - **Interpreting Burndown Curves**:
    - *Ideal Guideline*: Straight diagonal line from total sprint commitment to 0.
    - *Flat Line (Days 3–6)*: Indicates blocked tasks or scope creep.
    - *Steep Cliff on Day 10*: Indicates mini-waterfall (QA testing held until the last day).
  - **Definition of Done (DoD) Verification**: Code reviewed by 2 peers, automated unit/integration tests passing, documentation updated, verified by QA in staging environment.
- **Demo / Burndown & Velocity Review (run: instructor):**
  Open Jira Reports to analyze sprint performance:
  - Inspect the Sprint 1 Burndown chart to see completed story points vs remaining commitment.
  - Review the team Velocity report showing historical completed velocity across sprints.
  **Point out:**
  - As stories meet the Definition of Done and move to `Done`, remaining points decrease toward zero.
  - Velocity establishes the empirical capacity baseline for sizing the subsequent sprint.
- **Ask (Check Questions):**
  - Q: If a burndown chart remains flat for 5 days, what should the team investigate? — A: Subtasks are blocked, stories were sized too large (>8 points), or developers are multitasking across too many items (violating WIP limits).
  - Q: What is the difference between velocity and productivity? — A: Velocity measures predictable capacity of story points delivered per sprint; it is relative to team sizing and must never be used to compare different teams.
- **Done when:** Candidates can explain the burndown curve, verify DoD compliance, and defend their complete architectural design.

---

## Evaluation Rubric
- **Architecture Blueprint**:
  - *Excellent (3 pts)*: Clean 3-tier separation, proper cloud models, clear client-server protocols.
  - *Adequate (2 pts)*: Basic diagram, minor tier confusion.
  - *Needs Work (1 pt)*: No tier separation or cloud classification.
- **User Stories & INVEST**:
  - *Excellent (3 pts)*: Follows "As a / I want / So that", clear business benefit, rigorous acceptance criteria.
  - *Adequate (2 pts)*: Basic user stories, missing detailed criteria.
  - *Needs Work (1 pt)*: Vague technical tasks disguised as stories.
- **Story Estimation**:
  - *Excellent (3 pts)*: Fibonacci sizing justified by complexity and risk.
  - *Adequate (2 pts)*: Numbers assigned arbitrarily without discussion.
  - *Needs Work (1 pt)*: Missing story points or estimating in hours.
- **Jira Structure**:
  - *Excellent (3 pts)*: Flawless Epic -> Story -> Subtask hierarchy.
  - *Adequate (2 pts)*: Minor confusion between Tasks and Stories.
  - *Needs Work (1 pt)*: All flat tasks, no Epics or Subtasks.
- **Sprint Simulation**:
  - *Excellent (3 pts)*: Clear goal, active board management, standup blocker resolved.
  - *Adequate (2 pts)*: Sprint started, but weak goal or poor board updates.
  - *Needs Work (1 pt)*: Sprint not properly initialized.

---

## Post-Class Practice & Dynamic Interview Preparation
When preparing for technical interviews or defending your capstone design, use your AI practice coach to dynamically generate end-to-end synthesis challenges:
- In chat, type: **`interview questions on module 5`** or **`mock interview me on capstone architecture`**.
- The AI coach dynamically generates random, interview-grade scenarios testing your ability to bridge high-level system blueprints to agile sprint delivery and manage real-world dependency blockers.
