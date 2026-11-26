# Student Guide: Software Design, Architecture, SDLC & Agile (Jira)

Welcome to the **Software Design, Architecture, SDLC and Agile (Jira)** course. You will learn system architecture and agile engineering execution by designing, tracking, and interacting with a live **Smart House Construction & Management System** in Atlassian Jira Cloud in your browser.

Running Story Anchor: **Building a House** (From architectural blueprints and foundations to framing, utility tiers, subcontractor daily standups, and Jira-managed sprints).

---

## 1. What You Will Learn
- **Module 1: Software Architecture & System Design**: Distinguish Client-Server, design linear 3-Tier systems, compare to MVC, and evaluate Cloud IaaS/PaaS/SaaS (Story Anchor: Blueprint, Foundation, Behind-the-wall Utilities & Modular Outlets).
- **Module 2: SDLC Models & ALM Frameworks**: Map the 10 cross-functional ALM roles, compare Waterfall, V-Model, Spiral, and RAD, and tailor an SDLC to project risks (Story Anchor: Turnkey Skyscraper Contracts vs Modular Room Additions).
- **Module 3: Agile Methodology & Scrum / Kanban**: Apply the 4 Agile values & 12 principles, run Scrum ceremonies, apply Kanban WIP limits, and size stories with Fibonacci Story Points (Story Anchor: Subcontractor Crew, Daily 7:30 AM Jobsite Standups & Work Boards).
- **Module 4: Jira in Practice: Agile Project Execution**: Navigate Jira issue hierarchy (Epic $\rightarrow$ Story $\rightarrow$ Task/Subtask $\rightarrow$ Bug), manage Backlogs, start Sprints, and analyze Burndown charts (Story Anchor: Digital Jobsite Board, Framing Sprint, & Punch-list Tracking).
- **Module 5: Capstone: Architectural Blueprint to Jira**: Translate a system architecture blueprint into a complete, estimated, sprint-ready Jira project and simulate execution (Story Anchor: End-to-End Blueprint to Finished Move-in Readiness).

---

## 2. Get Your Laptop Ready: Setting Up Real Atlassian Jira Cloud

Instead of running any local code or mock servers, this course is **100% cloud-first** and uses **live, production Atlassian Jira Cloud** directly in your web browser.

No local coding environment, no local backend servers, and no Docker setup are required on your laptop. All hands-on engineering execution takes place in Jira.

You need:
- A modern web browser (Chrome, Edge, or Firefox)
- An **Atlassian Jira Cloud Free Account** (Free forever for up to 10 users, no credit card required)

### Step-by-Step: How to Create Your Free Jira Cloud Account & Project

1. **Sign Up for the Free Tier**:
   - Go to: [https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free)
   - Click **Get it free** under Jira Software.
   - Sign up using your Google account or email address.

2. **Claim Your Personal Jira Site URL**:
   - Atlassian will ask you to name your site.
   - Enter a unique subdomain, for example: `https://yourname-wbl.atlassian.net` (or `https://yourname-smarthouse.atlassian.net`).
   - Click **Agree and sign up**. Atlassian will provision your cloud instance in ~30 seconds.

3. **Create the Smart House Scrum Project & `In Review` Column**:
   - On the onboarding screen, choose **Software Development**.
   - Select the **Scrum** project template (recommended: Company-managed or Team-managed).
   - Enter the project details:
     - **Project Name**: `Smart House Construction & Management`
     - **Project Key**: `HOUSE`
   - Click **Create Project**. Your live Jira board and backlog are now active!
   - **Add `In Review` Column**: Jira's default Scrum board ships with `To Do`, `In Progress`, and `Done`. On the **Board**, click **`+ Create column`** (or **Board settings**) and add an **`In Review`** column/status between `In Progress` and `Done`.

4. **Access and Use the Real Live Jira Dashboard**:
   - In the top navigation bar of Jira, click **Dashboards** $\rightarrow$ **View all dashboards** or **Create dashboard**.
   - Name your dashboard: `Smart House Executive Dashboard`.
   - Click **Add gadget** on the right side to add live reporting tools:
     - **Sprint Health Gadget**: Shows active sprint progress, percentage completed, and blockers.
     - **Sprint Burndown Gadget**: Automatically graphs your daily burndown curve as tickets move to Done.
     - **Assigned to Me**: Lists tasks currently assigned to you.
     - **Two-Dimensional Filter Statistics**: Shows ticket counts by Assignee or Priority.
   - Your permanent live dashboard URL:
     `https://<your-subdomain>.atlassian.net/jira/dashboards`

5. **Using Jira Throughout the Course**:
   - In **Module 3**: You write User Stories with INVEST criteria and estimate Fibonacci story points.
   - In **Module 4**: You enter those stories into your live Jira Backlog, organize them into Epics, and launch **Sprint 1**.
   - In **Module 5**: You conduct simulated daily standups on your live Active Board, move cards from To Do $\rightarrow$ In Progress $\rightarrow$ Done, and analyze your real Sprint Burndown chart.

---

## 3. Core Jira Hierarchy at a Glance
Running Project Anchor: **Building a House (The Smart House Construction Project)**

- **Epics** *(Jira assigns sequential numeric keys like `HOUSE-1`, `HOUSE-2`, `HOUSE-3` in creation order)*:
  - **Foundation & Structural Architecture**
  - **Plumbing, Electrical & Utility Tiers** (3-Tier Infrastructure)
  - **Smart Home Automation & IoT Security**
- **User Stories** *(example backlog items you will create in Module 4, with **Parent** set to the Epics above)*:
  - *Poured Concrete Foundation with Structural Rebar* (5 pts)
  - *Dual-Zone PEX Hot & Cold Water Distribution System* (8 pts)
  - *Biometric & Remote Mobile Door Lock Control* (5 pts)
  - *Smart Thermostat Eco-Schedule Integration* (3 pts)
- **Subtasks**: Discrete Dev & QA technical execution steps rolling up to each parent story.
- **Sprint 1**: 2-week active iteration committed to delivering foundational structure and beta door lock control.

Target Practice Data (Create in Jira during Module 4): 3 Epics, 4 User Stories, 1 active Sprint.

---

## 4. Cheat Sheets

### Architecture Cheat Sheet (Module 1)
- **Client-Server**: Asymmetric distributed relationship. Client initiates request; server listens and responds.
- **3-Tier Linear Separation**:
  - *Presentation Tier*: User interface (HTML/JS, mobile app).
  - *Application/Logic Tier*: Business validation, calculation, authentication rules.
  - *Data Tier*: Relational database (PostgreSQL).
  - *Golden Rule*: Presentation tier NEVER connects directly to Data tier.
- **Cloud Models**:
  - **IaaS**: Raw infrastructure (VMs, OS control) $\rightarrow$ *Empty plot of land with utility hooks*.
  - **PaaS**: Managed platform/runtime $\rightarrow$ *Unfurnished apartment with maintained plumbing/power*.
  - **SaaS**: Hosted turnkey application via browser $\rightarrow$ *Furnished hotel room*.

### SDLC & ALM Models Cheat Sheet (Module 2)
- **ALM 3 Pillars**: Governance, Development, Operations & Maintenance.
- **The 10 Roles & Modern Evolution**:
  - *Business Manager* (funding/ROI), *Project Manager* (schedule/budget), *PMO* (portfolio alignment), *Business Analyst* (requirements), *Architect* (system blueprint), *UX Team* (usability/design system), *DBAs* (data integrity/indexing), *Developers* (code implementation).
  - *Testers $\rightarrow$ SDETs*: Test automation (Playwright, PyTest) integrated in CI/CD.
  - *Operations $\rightarrow$ DevOps & SREs*: Infrastructure as Code (Terraform, Kubernetes) and high availability.
- **Waterfall**: Sequential gated delivery (`Requirements -> Design -> Code -> QA -> Deploy`). Frozen upfront specs. Inflexible, big-bang integration risk. Mandatory for FDA medical devices, avionics, automotive ASIL D firmware.
- **V-Model & Shift-Left Testing**: Parallel planning of development and test gates:
  - *Requirements* $\longleftrightarrow$ Acceptance Testing.
  - *Architecture* $\longleftrightarrow$ Integration/System Testing.
  - *Detailed Design* $\longleftrightarrow$ Unit Testing.
  - *Golden Distinction*: **Verification** (*"Building the product right?"*) vs **Validation** (*"Building the right product?"*).
- **Structured Evolutionary Prototyping**: 7-step iterative demonstration loop. Evolved into modern **MVPs**. Beware the **"Code-and-Fix" trap** (prematurely shipping hacky demos without security or unit tests).
- **Rapid Application Development (RAD)**: 4 phases (Requirements Planning, User Description, Construction time-box "Do until done", Cutover). Evolved into modern sprint time-boxing.
- **Incremental Model**: Phased operational builds adding functionality release by release. Evolved into modern feature-flagged SaaS canary deployments.
- **Spiral Model (Barry Boehm)**: Mandatory 4-quadrant risk analysis in every cycle. Evolved into modern **Architectural Spikes** and Proof-of-Concepts (POCs) before sprint commitments.
- **Agile SDLC Methods**:
  - *FDD (Feature Driven Development)*: `<action> <result> <object>` (matches modern REST API endpoint design).
  - *DSDM*: **80/20 Pareto rule** (ship the 20% delivering 80% value) & Ambassador Users (Design Partners).
  - *Extreme Programming (XP)*: TDD, Pair Programming, Continuous Integration, Refactoring.
- **Tailored Hybrid SDLC**: Real-world standard: combining upfront architectural modeling and compliance gates with 2-week Agile execution and automated CI/CD pipelines.

### Agile & Jira Cheat Sheet (Modules 3 & 4)
- **4 Values of Agile Manifesto**:
  1. Individuals and interactions over processes and tools.
  2. Working software over comprehensive documentation.
  3. Customer collaboration over contract negotiation.
  4. Responding to change over following a plan.
- **User Story INVEST Criteria**:
  - **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall, **T**estable.
  - Standard format: `As a [role], I want [action] so that [benefit].`
- **Scrum Ceremonies**:
  - Sprint Planning (What to build & Sprint Goal).
  - Daily Standup (15-min sync: yesterday, today, blockers).
  - Sprint Review (Live demo to stakeholders).
  - Sprint Retrospective (Team process improvement).
- **Jira Issue Hierarchy**:
  `Epic (Quarterly Initiative) -> User Story (Deliverable Value) -> Subtask (Dev/QA implementation) -> Bug (Defect)`.

---

## 5. Post-Class Self-Study & Technical Interview Preparation

This repository is designed as your complete, independent learning workbench after class completes. Whether you are reviewing in the evening, studying on weekends, or preparing for senior engineering interviews, you can run realistic practice drills directly in this workspace.

### How to Practice Independently in Chat
Simply open this repository and message your AI practice coach:
- **Mock Interviews**: Type **`interview questions on module 1`** (or 2, 3, 4, 5) or **`mock interview`** to be tested on production scenarios, failure modes, and architectural trade-offs.
- **Socratic Concept Checks**: Type **`quiz me`** to drill fundamental principles with progressive hints.
- **User Story Review**: Type **`check my user story`** and paste your draft. The coach audits it against the 6 INVEST principles and Given-When-Then criteria.
- **Exercise Guidance**: Type **`help with the exercise`** to get scaffolded hints without spoiling solutions.
- **Concept Deep-Dives**: Type **`explain [topic]`** for a detailed architectural breakdown.

### Top 10 Architectural & Agile Interview Traps to Avoid
1. **The Direct Database Access Trap**: Never suggest mobile or web frontends should connect directly to databases. Always articulate connection pooling (PgBouncer), process-per-connection RAM limits, and zero-trust API gateway boundaries.
2. **The Hand-Wavy Scale Trap**: Don't say "we'll just autoscale". Explain client-side jittered backoff, asynchronous message streaming buffers (Kafka), and bulk database write batching.
3. **The NAT/Firewall Amnesia Trap**: In IoT, remember that cloud servers cannot initiate inbound TCP connections to edge devices behind carrier NAT. Devices must maintain long-lived outbound connections (MQTT/WebSockets) or receive OS push notifications (APNs/FCM).
4. **The Agile Dogma Trap**: Never claim "Waterfall is dead" or "Agile is always better". Defend why regulated safety-critical systems (FDA medical devices, FAA avionics, automotive ASIL D) legally require predictive V-Model verification matrices.
5. **The Prototype in Production Trap**: Always warn against the "Code-and-Fix" trap when business leaders want to ship MVP prototypes. Explain missing non-functional requirements (security, pooling, telemetry, error handling).
6. **The Story Points as Hours Trap**: Story points measure relative complexity, effort, and uncertainty—never calendar hours. Points prevent false precision and decouple sizing from developer seniority.
7. **The Phantom Velocity Trap**: Sprints where cards are moved to Done without meeting the Definition of Done (e.g. missing automated tests) create fake velocity that surfaces as production bugs.
8. **The Mid-Sprint Scope Chaos Trap**: Scrum protects team focus during the active sprint. If an executive requests changes, the request goes to the Product Backlog for the next sprint, or the Product Owner terminates the sprint if the goal is obsolete.
9. **The Monolithic Burndown Cliff**: If a burndown stays flat and drops on the last day, stories are too large or testing is batched at the end. Split stories into vertical slices under 5-8 points.
10. **The Horizontal Sprint Trap**: In Sprint 1, avoid writing "database only" or "infrastructure only" horizontal layers. Always deliver a "thin vertical slice" (e.g. resident login) proving end-to-end integration across UI, API, DB, and CI/CD.
