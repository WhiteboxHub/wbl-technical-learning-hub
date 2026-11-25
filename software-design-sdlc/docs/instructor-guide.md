# Instructor Guide: Software Design, Architecture, SDLC & Agile (Jira)

This guide provides instructors with pedagogical strategies, classroom facilitation advice, discussion prompts, and the core story anchor to run a world-class training session.

---

## 1. The Core Philosophy
Engineering fundamentals often fail when taught as dry definitions. Candidates memorize acronyms without understanding **why** an architecture or methodology exists.
Our teaching methodology hinges on two pillars:
1. **The Story Anchor ("Building a House")**: Every software architecture pattern and agile ceremony is mapped directly to physical home construction.
2. **The Socratic Beat Format**: Every beat presents the core concept anchor, deep talking points, a concrete scenario/exercise, check questions with answers, and an explicit exit criterion.

---

## 2. Tooling Architecture: Zero-Docker & Live Atlassian Jira Cloud
- **Zero Local Setup Friction**: Unlike courses that require running local backends, Docker containers, or local databases, this course is **100% cloud-first**. Candidates do not write or run any local API code or backend servers.
- **Enterprise Tooling**: All hands-on Agile, Scrum, and SDLC execution is conducted directly in live, free **Atlassian Jira Cloud** ([https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free)) in the web browser.

### Step-by-Step: Creating & Using the Jira Account in Class
Guide both yourself (before class) and candidates (before Module 4) through these exact steps:
1. **Create / Log In to Free Jira Cloud**:
   - Go to [https://www.atlassian.com/software/jira/free](https://www.atlassian.com/software/jira/free) and click **Get it free** (up to 10 users free forever, no credit card required).
   - Sign up or log in with Google or email.
   - Claim a unique site URL (e.g., `https://<your-name>-smarthouse.atlassian.net`) and click **Agree and sign up**.
2. **Create the Scrum Project & `In Review` Board Column**:
   - Select **Software Development** $\rightarrow$ **Scrum** template.
   - **Project Name**: `Smart House Construction & Management` | **Project Key**: `HOUSE`.
   - Click **Create Project**.
   - On the **Board** (default columns are `To Do`, `In Progress`, `Done`), click **`+ Create column`** (or **Board settings**) and add an **`In Review`** column/status between `In Progress` and `Done`.
3. **Demo & Practice Steps Inside Jira (Modules 4 & 5)**:
   - **Epics**: Create 3 Epics: **Foundation & Structural Architecture**, **Plumbing, Electrical & Utility Tiers**, and **Smart Home Automation & IoT Security** (Jira assigns sequential keys like `HOUSE-1`, `HOUSE-2`, `HOUSE-3`).
   - **Backlog & Stories**: Add 4 INVEST User Stories with **Parent** set to those Epics, Given-When-Then acceptance criteria, and Fibonacci **Story Points** (`1, 2, 3, 5, 8`).
   - **Subtasks & Bugs**: Open a Story to add separate Dev and QA **Subtasks**, and log 1 sample **Bug**.
   - **Sprint 1 & Board**: Click **Create sprint**, pull ~18 points into **Sprint 1**, set a **Sprint Goal**, click **Start sprint** (2 weeks), and walk cards across `To Do` $\rightarrow$ `In Progress` $\rightarrow$ `In Review` $\rightarrow$ `Done`.
   - **Dashboards & Reports**: Go to **Dashboards** $\rightarrow$ **Create dashboard** (`Smart House Executive Dashboard`) $\rightarrow$ **Add gadget** $\rightarrow$ add **Sprint Health** and **Sprint Burndown** (`https://<your-subdomain>.atlassian.net/jira/dashboards`).

---

## 3. Course Structure & Core Activities

The course is organized into 5 cohesive modules covering architectural blueprints through Jira execution:

- **Module 1: Software Architecture & System Design**: Blueprint trade-off debate (3-Tier vs MVC vs P2P).
- **Module 2: SDLC Models & ALM Process**: Case study: Selecting SDLC for 3 real-world scenarios.
- **Module 3: Agile, Scrum & Kanban**: Story writing workshop & Planning Poker estimation.
- **Module 4: Jira in Practice**: Hands-on Jira project setup, board config, & sprint run.
- **Module 5: Capstone: Blueprint to Active Sprint**: End-to-end team project & mock standup walkthrough.

---

## 5. Teaching the Story Anchor: Building a House

Use this mapping consistently throughout every module:

### Architecture & System Design (Module 1)
- **Client-Server Foundation**: Opening the kitchen faucet (**Client**) requesting water from the 24/7 municipal pumping station (**Server**) through underground pipes (**Network**). Clients demand; servers listen and answer.
- **3-Tier Separation**:
  - *Presentation Tier*: The living room walls, paint, light switches, faucets.
  - *Logic / Application Tier*: The behind-the-drywall plumbing manifold, water heater thermostat, circuit breaker panel.
  - *Data Tier*: The municipal power plant and water reservoir.
  - *Why separate them?* If you replace your kitchen faucet with a modern gold finish (Presentation change), you shouldn't have to rebuild the city water reservoir (Database)! Faucets must never tap directly into high-voltage mains.
- **Coupling**: Standard wall outlets (**Loose coupling**—unplugging a broken toaster leaves the lights on) vs hard-soldered copper wiring (**Tight coupling**—one short circuit blacks out the house).
- **Processing**: 20-ton dumpster hauled away only when 100% full (**Batch-Sequential**) vs continuous conveyor belt dropping scrap into a wood chipper (**Streaming / Pipes & Filters**).
- **Specialized Architectures**: Neighborhood potluck party (**P2P**), modular circuit breaker panel with snap-in solar breakers (**Plugin Architecture**), instant blueprint digital barcode scanner (**Search-Oriented Architecture**).
- **Cloud Models**: Empty zoned lot (**IaaS**), unfurnished apartment (**PaaS**), luxury turnkey hotel room (**SaaS**).

### SDLC Models & ALM Process (Module 2)
- **SDLC vs ALM**: SDLC is the physical construction phase (framing, plumbing, inspections); ALM is the entire 30-year lifecycle from home financing and permits through HVAC maintenance and demolition.
- **The 10 ALM Roles**: Homeowner (Business Manager), General Contractor (PM), Permitting Board (PMO), Space Planner (BA), Blueprint Architect, Ergonomist (UX), Master Plumbers/Electricians (DBAs), Carpenters (Developers), City Inspectors (QA/Testers), and Property Maintenance Crew (DevOps/Ops).
- **Waterfall**: Building a 50-story concrete skyscraper. Structural columns and blueprints are frozen upfront; changing your mind on floor 40 is impossible. Great for predictable fixed-scope contracts, fatal for evolving user needs. Mandatory in FDA/FAA/ISO 26262.
- **V-Model & Shift-Left**: Parallel blueprints and inspection checklists. When the architect writes foundation specs, the inspector writes the foundation inspection checklist; pipes are pressure-tested immediately before drywalling.
- **Evolutionary Prototyping**: Walking through a temporary foam/cardboard scale model to refine room layout before pouring concrete. Beware the dangerous **"Code-and-Fix" Trap** of living in the foam house!
- **Rapid Application Development (RAD)**: Pre-fabricated modular walls assembled with power tools inside an aggressive 30-day time-box ("Do until done").
- **Incremental SDLC**: Building a modular expandable home. Move into the 1-bedroom starter core in Year 1 (Increment 1), add the guest bedroom wing in Year 2 (Increment 2).
- **Spiral Model (Barry Boehm)**: Building a cliffside mansion over an unstable ocean fault line. Before buying lumber, you drill soil cores (Spiral 1), build retaining walls (Spiral 2), and constantly reassess risk before spending another dollar (modern Architectural Spikes/POCs).
- **Tailored Hybrid SDLC**: Building custom luxury homes: build the pool foundation with Waterfall/V-Model (zero room for error), but build interior lighting and kitchen cabinets with Agile Sprints.

### Agile Methodology, Scrum & Kanban (Module 3)
- **Agile Manifesto**: 300-page rigid contract with $10k change-order fees vs walking through framed rooms every Friday afternoon to adjust closet doors before drywall closes. Customer collaboration over contract negotiation.
- **Iron Triangle Inverted**: Fixed-scope skyscraper (cost and schedule blow out) vs fixed-cadence modular home (fixed 2-week sprints and fixed crew budget, prioritizing living spaces first and deferring luxury pools).
- **The 3 Scrum Roles**: Homeowner (**Product Owner** — prioritizes rooms and accepts finished deliverables), Jobsite Superintendent (**Scrum Master** — clears city permits, removes blockers, shields trades from interruptions), and Skilled Trades (**Development Team** — plumbers, electricians, framers).
- **The 4 Ceremonies**: Monday morning blueprint huddle (**Sprint Planning**), 15-minute 7:30 AM tailgate standup with coffee (**Daily Standup**), homeowner room walkthrough (**Sprint Review**), and Friday evening crew retrospective on delivery delays (**Sprint Retrospective**).
- **The 3 Artifacts**: Master home wishlist (**Product Backlog**), 2-week committed framing materials (**Sprint Backlog**), and the finished, inspected, livable master bathroom (**Increment meeting DoD**).
- **Kanban & WIP Limits**: 5 subcontractors crowding into an 8x10 bathroom at once (plumber, electrician, tiler, painter) creating gridlock vs enforcing a **WIP Limit of 1** so work flows smoothly without traffic jams.
- **User Stories & Story Points**:
  - *User Story*: Don't say "Buy 20 feet of copper." Say: *"As a homeowner, I want hot running water in the master shower so that I can take a warm bath."*
  - *Story Points*: Painting a flat bedroom wall (**2 points**) vs a 30-foot cathedral ceiling on scaffolding (**8 points**). Both agree the cathedral ceiling is 4x more complex, regardless of individual painter speed.

### Jira in Practice & Project Tracking (Module 4)
- **Central Digital Jobsite**: Replacing lost paper sticky notes on truck hoods with a central digital touchscreen in the construction trailer where trades badge in, see their tasks, and log passed inspections.
- **Issue Hierarchy**: Strategic wing construction (**Epic**: "Kitchen & Dining Wing") $\rightarrow$ End-user requirement (**Story**: "Hot running water in sink") $\rightarrow$ Technical task (**Task**: "Deliver 100ft PEX") $\rightarrow$ Trade assignments (**Dev Subtask**: "Rough-in manifold", **QA Subtask**: "Pressure test at 60 PSI") $\rightarrow$ Defect (**Bug**: "Sink shutoff valve drips").
- **Backlog Grooming & Sprint Launch**: Contractor cleaning the trailer lumber list on Monday morning, pulling the exact 2x4s into the staging trailer, setting the **Sprint Goal** (*"Dry-in the roof before winter rain"*), and launching the 2-week iteration.
- **Active Board & Daily Standup**: Subcontractors walking the board right-to-left at 7:30 AM; unblocking the plumber whose municipal water shutoff was locked so cards move safely to Done.
- **Burndown & Velocity**: Tracking daily completed rooms on a chalkboard; spotting a flat line on Day 7 to fix delays immediately rather than discovering failure on Day 14.

### Capstone Synthesis (Module 5)
- **Apex Smart-Home Project**: Candidates act as Lead Architects and Project Leads designing and building a neighborhood of connected smart homes:
  1. Blueprinting the 3-Tier utilities and cloud infrastructure.
  2. Selecting the hybrid SDLC model (Waterfall for hardware firmware + Agile for resident app).
  3. Staffing the ALM trade roles.
  4. Authoring INVEST user stories and Fibonacci estimates in Jira.
  5. Running a live Daily Standup, resolving an unexpected delayed city inspector permit blocker, and inspecting burndown velocity.

---

## 6. Facilitation Tips & Common Pitfalls

1. **Avoid Tool-First Thinking in Jira**:
   - Don't let students get lost in Jira configuration menus before they understand **why** an Epic needs User Stories, or what acceptance criteria are. Always enforce: *Concept first, Jira click second*.
2. **Story Points vs Hours**:
   - Students frequently equate 1 story point to 1 hour or 1 day. Intervene immediately! Explain that a story point measures **relative effort, complexity, and uncertainty** (like sizing T-shirts: Small, Medium, Large).
3. **Waterfall Bashing**:
   - Emphasize that Waterfall is not "bad" or "dead." For mission-critical embedded software (pacemakers, rocket avionics, nuclear power systems), rigorous upfront specifications and V-model validation are essential. Agile shines where requirements are emergent and user feedback is rapid.
