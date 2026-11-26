# Software Design, Architecture, SDLC & Agile (Jira) — Course Table of Contents

This document outlines the 5 comprehensive modules comprising the course. Topics cover 100% of the concepts across Software Architecture, Application Lifecycle Management (SDLC), and Agile / Jira.

**Story Anchor**: **Building a House** (Blueprints, Foundations, General Contractors, Subcontractors, City Permits, Inspections, and Iterative Renovations).

---

## Curriculum Structure
- **Module 1: Software Architecture & System Design** (Competency: Architecture & Distributed Systems): Client-Server, 3-Tier/N-Tier, MVC, Distributed Computing, Shared DB / Stored Procedures, Batch, P2P (Super-Peers), Plugins, Search, Cloud (IaaS/PaaS/SaaS) (Output: Architectural Blueprinting & Trade-off Matrix).
- **Module 2: SDLC Models & Application Lifecycle Management** (Competency: Lifecycle Governance & ALM): ALM 10 Roles, Waterfall, V-Model, Evolutionary Prototyping, RAD, Incremental, Spiral (Risk-Driven), Agile Methods (FDD, DSDM, ASD, XP, RUP, Adaptive), Tailored SDLC (Output: SDLC Model Selection & Risk Assessment Case Study).
- **Module 3: Agile Methodology & Scrum / Kanban** (Competency: Agile Delivery Frameworks): Agile Manifesto (4 Values, 12 Principles, Benefits), Iron Triangle, 4 Frameworks (Scrum, Kanban, SAFe, XP), Scrum (Roles, Ceremonies, Artifacts), Kanban (WIP), INVEST Stories, Points, DoR/DoD (Output: Drafting INVEST User Stories & Estimation Poker).
- **Module 4: Jira in Practice: Agile Project Execution** (Competency: Project Management Tooling): Jira Setup (Cloud-First Architecture), Roles, 5 Issue Types (Epic, Story, Task, Subtask, Bug), Backlog grooming, Sprints, Standups, Workflows, Reports (Burndown, Velocity, CFD, Dashboards) (Output: Building a Full Jira Project & Active Sprint Board).
- **Module 5: Capstone: Architectural Blueprint to Jira** (Competency: Integrated Course Synthesis): End-to-end translation from System Architecture to an Active Sprint with Burndown Tracking (Output: Live Sprint Simulation & Architecture Defense).

---

## Detailed Module Syllabi

### Module 1: Software Architecture & System Design
- **1.1 Client-Server Model**: Definition of Client vs Server, asymmetric relationship, always-on server daemons, request/response lifecycle, statelessness.
- **1.2 Three-Tier & N-Tier Architecture vs MVC**: Physical and logical separation (Presentation Tier, Application Logic Tier, Data Tier). Linear flow vs MVC triangular pattern; security boundaries and permission control.
- **1.3 Distributed Computing & Coordination Patterns**: Heterogeneous environments, network links of varying latencies, unpredictable failures, tight vs loose coupling. Distributed coordination patterns: Shared Relational DBMS, Stored Procedures on database servers, and Dynamic Table-Driven Logic.
- **1.4 Batch-Sequential Processing vs Pipes & Filters**: High-volume offline file processing, strict sequential stages (`Input -> Validate -> Process -> Report`). Contrast with concurrent Pipes and Filters. Enterprise use cases: Compilers, data pipelines, legacy mainframes.
- **1.5 Specialized Architectures**:
  - *Peer-to-Peer (P2P)*: Equal nodes acting as client and server simultaneously, collective bandwidth/storage/compute, centralized indexing vs decentralized discovery, super-peers (super-nodes) in star-like topologies.
  - *Plugin Architecture (Microkernel Pattern)*: Extensible software design, modular dynamic loading via `.dll` or OSGi interfaces (Notepad++, Eclipse IDE).
  - *Search-Oriented Software Architecture*: Search engine as the primary architectural integration layer (Elasticsearch/Meilisearch) replacing SQL joins with inverted index keyword search.
- **1.6 Cloud Computing Service Models**:
  - *SaaS (Software as a Service)*: Turnkey browser software for SMEs, pay-per-use, zero maintenance (Salesforce.com, emailcloud, Jira Cloud).
  - *PaaS (Platform as a Service)*: Managed execution runtimes, databases, and automated scaling (Google App Engine, Mosso, AWS S3).
  - *IaaS (Infrastructure as a Service)*: Raw compute, full OS root access, virtual firewalls, routers, load balancing (AWS EC2, Flexiscale).
- **1.7 Monolithic vs Microservices Architecture**:
  - *Monolith vs Microservices*: Single deployable unit vs independently deployable bounded-context services.
  - *Core Microservices Rules*: Bounded contexts, Database-per-Service (no shared DB anti-pattern), API Gateway, synchronous REST/gRPC vs asynchronous event-driven messaging, independent scaling & fault isolation, and when to start with a Modular Monolith.

---

### Module 2: SDLC Models & Application Lifecycle Management (ALM)
- **2.1 ALM Process & Foundations**: Definition of software, SDLC framework, the ALM umbrella (Governance, Development, Operations & Maintenance), defect cost escalation curve.
- **2.2 The 10 Core Roles in ALM**: Business Manager, Project Manager (PM), PMO Decision Makers, Business Analyst (BA), Software Architect, User Experience (UX) Design Team, Database Administrators (DBAs), Developers, Testers (QA), and Operations & Maintenance Staff (DevOps/SRE).
- **2.3 The Waterfall Model**: Linear sequential stages (Requirements, Design, Implementation, Testing, Maintenance), requirements freezing, strengths (structure, milestone clarity), critical deficiencies (big-bang integration, inflexible), appropriate use cases (stable requirements, porting).
- **2.4 The V-Shaped SDLC Model**: Parallel Verification vs Validation mapping across 5 tiers (Requirements <-> Acceptance, Analysis <-> System Integration, Architecture <-> Integration, Detailed Design <-> Unit Testing, Apex Coding); when to use for safety-critical reliability (medical, avionics).
- **2.5 Structured Evolutionary Prototyping Model**: 7-step lifecycle, user demonstrations & corrective loops, strengths (visible progress, user learning), weaknesses (code-and-fix trap, premature delivery pressure), when to use (unstable requirements, novel UIs).
- **2.6 Rapid Application Development (RAD) & Incremental SDLC**:
  - *RAD*: 4 phases (Requirements Planning, User Description, Construction time-box "Do until done", Cutover), productivity tools (WYSIWYG), strengths, weaknesses, when to use.
  - *Incremental Model*: Partial implementations, prioritized releases, divide-and-conquer, strengths (early customer value), weaknesses (requires excellent upfront architecture), when to use.
- **2.7 The Spiral Model (Barry Boehm)**: Risk-driven engineering, 4 quadrants (Objectives/Constraints, Risk Analysis & Prototyping, Development & Verification, Next cycle planning); strengths (early risk resolution), weaknesses (high complexity/overhead), when to use.
- **2.8 Agile SDLC Frameworks & Tailoring**:
  - History (Snowbird 2001), speed up/bypass phases.
  - *Feature Driven Development (FDD)*: 5 steps, client-valued feature template (`<action> <result> <object>`, e.g. "Calculate total sale").
  - *Dynamic Systems Development Method (DSDM)*: 80/20 Pareto rule, Ambassador users, 9 principles, 5 lifecycle phases.
  - *Adaptive SDLC*: Project initiation, time-boxing, optimal cycle planning, task review.
  - *Other Methods*: ASD, Crystal Clear, Extreme Programming (XP), Rational Unified Process (RUP).
  - *Tailored SDLC Models*: Customizing and combining models to project risk and organizational constraints.

---

### Module 3: Agile Methodology & Scrum / Kanban Framework
- **3.1 Agile Foundations & Manifesto**:
  - History (Snowbird Utah 2001), 4 Core Values, 12 Agile Principles in full, 4 core benefits (speed, collaboration, adaptability, quality).
- **3.2 Agile vs Waterfall & The 4 Frameworks**:
  - Inverted Iron Triangle of Constraints (Fixed Time/Cost vs Flexible Scope).
  - The 4 Major Agile Frameworks: Scrum, Kanban, SAFe (Scaled Agile Framework), and XP (Extreme Programming - Pair Programming, TDD).
- **3.3 The Scrum Framework**:
  - *Roles*: Product Owner, Scrum Master, Development Team.
  - *Ceremonies*: Sprint Planning (Sprint Goal), Daily Standup (15-min, 3 questions), Sprint Review, Sprint Retrospective.
  - *Artifacts*: Product Backlog, Sprint Backlog, Potentially Shippable Increment.
- **3.4 Kanban Methodology**:
  - Toyota lean manufacturing origins, 4 Core Principles (visualize workflow, limit WIP, manage flow, continuous improvement).
  - Kanban Board structure (columns, cards, WIP limits).
  - Comprehensive Scrum vs Kanban comparison table.
- **3.5 Key Agile Practices**:
  - User Stories format (`As a... I want... so that...`), 6 INVEST criteria (Bill Wake).
  - Relative Story Points & Modified Fibonacci scale (`1, 2, 3, 5, 8, 13, 21`), Planning Poker.
  - Definition of Ready (DoR) vs Definition of Done (DoD).
  - Agile Tracking: Velocity Tracking and Burndown Charts.

---

### Module 4: Jira in Practice: Agile Project Execution
- **4.1 Introduction to Jira & Deployment Setup**:
  - Atlassian Jira purpose, enterprise capabilities, Cloud-first SaaS architecture vs enterprise Data Center.
  - Creating Admin credentials and configuring project roles (Developer, QA Tester, PM).
- **4.2 Jira Issue Types & Hierarchy**:
  - Detailed definitions and examples for the 5 issue types:
    - *Epic*: Strategic initiative ("Build a User Management System").
    - *Story*: End-user value ("As a user, I want to log in using credentials").
    - *Task*: Technical chore ("Set up database schema").
    - *Subtask*: Granular labor split ("Implement Login API", "Test Login Functionality").
    - *Bug*: Defect ("Login button unresponsive on mobile").
- **4.3 Backlog Grooming, Sprint Creation & Goals**:
  - Product Backlog vs Sprint Backlog, refinement process, creating a sprint in Jira, time-boxing (1–4 weeks), establishing a cohesive Sprint Goal.
- **4.4 The Active Sprint Board & Daily Standups**:
  - Board columns (To Do, In Progress, In Review, Done), drag-and-drop workflow transitions.
  - 15-minute Daily Standup role walkthroughs (QA Tester, Developer, Project Manager).
  - Custom workflows, statuses, transitions, and resolutions.
- **4.5 Agile Tracking & Reporting**:
  - Burndown Chart analysis (ideal line, flat lines, scope spikes).
  - Velocity Chart (capacity forecasting).
  - Sprint Reports and Cumulative Flow Diagrams (CFD) for bottleneck detection.
  - Custom Dashboards with chart gadgets.

---

### Module 5: Capstone: Architectural Blueprint to Jira
- **The "Apex Smart-Home Construction & Management System"**:
  - Step 1: System Architecture Blueprint (3-Tier, Client-Server, IaaS/PaaS/SaaS classification).
  - Step 2: SDLC Selection & ALM Team Role Mapping (Hybrid Agile + V-Model).
  - Step 3: Jira Project Creation & Backlog Authoring (3 Epics, 4 INVEST Stories, Given-When-Then acceptance criteria, Story points, Dev & QA subtasks).
  - Step 4: Sprint Planning & Execution Simulation (Sprint Goal, Daily Standup blocker handling, burndown tracking).
  - Evaluation rubric for presentations.
