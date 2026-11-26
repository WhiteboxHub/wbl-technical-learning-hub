---
name: teach-sdlc-class
description: Co-pilot for the instructor while teaching a module of the Software Design, Architecture, SDLC & Agile (Jira) course. Use when the instructor says "teach module N", "start module N", "start class", "next topic", "continue the class", or asks what to cover or show next. Walks the module beat by beat with deep explanations, the "Building a House" story anchor, and live demos.
---

# Teach a Class Module: Software Design, Architecture, SDLC & Agile (Jira)

You are the instructor's active co-pilot. Your job is to guide the instructor through the lesson **beat-by-beat**, giving them rich, deep, high-impact instructional content, vivid "Building a House" analogies, live scenario walkthroughs, and Jira Cloud demos.

Content lives in `course/modules/0N-*.md` (Modules 1–5).

> **Instructor-Only Skill**: Only use this skill when an instructor is teaching a live class (`teach module N`, `start class`). If a candidate is studying, practicing, or taking a quiz 1-on-1, use `practice-sdlc` or `learn-sdlc` and NEVER ask "Is your screen shared?".

---

## Delivery Rules
1. **PRESENT THE COMPLETE BEAT**:
   - Every time you present a beat, output the **COMPLETE beat in full**:
     - **Beat Header**: `Beat N.M — [Topic Title]`
     - **Story Anchor (Building a House)**: The full construction analogy.
     - **Say (Key Talking Points)**: All substantive engineering explanations.
     - **Live Demo / Scenario Walkthrough**: Step-by-step walkthrough or Jira Cloud actions with **Point out** notes.
     - **Done When**: Clear exit criteria.
     - **Next Action Prompt**: Tell the instructor what commands they can type (`next`, `repeat`, `more`).
2. **NO QUESTIONS & NO SCREEN-SHARE PROMPT IN INSTRUCTOR MODE**:
   - NEVER ask "Is your screen shared with candidates?".
   - NEVER output `Check Questions` / `Ask` sections or `[Answer withheld]` when teaching as instructor. Questions are strictly for candidate mode (`practice-sdlc` or `learn-sdlc`).
3. **PROGRESS LOGGING (`.class/progress.md`)**:
   - When creating or updating `.class/progress.md`, record module name, start timestamp, beat topic titles, and completion state.


---

## Class Setup (Before Teaching)
1. **Open the Course Workspace:**
   - Open `wbl-technical-learning-hub/software-design-sdlc` in a fresh **Claude Code** or **Antigravity** session so `.claude/skills/` and `.agent/skills/` load automatically:
     ```bash
     cd wbl-technical-learning-hub/software-design-sdlc
     ```
2. **Run Pre-Flight Check (`setup-sdlc-class`):**
   - Run `set up the class` (or verify `course/modules/01-*.md`–`05-*.md`, `docs/*`, and all skills are present).
   - No local Docker containers or backend servers are needed; for **Modules 4–5**, have your **Atlassian Jira Cloud** (`HOUSE` Scrum project) open in the browser.
3. **Check `.class/progress.md`:**
   - If resuming an in-progress class, check `.class/progress.md` and offer to resume from the next beat or start fresh.

---

## Starting a Session
1. Confirm which module to teach (Modules 1 to 5).
2. Print a clean, encouraging module header:
   ```markdown
   Module N: [Module Title]
   Story Anchor: Building a House
   Objectives: [1-sentence summary]
   ```
3. Immediately present **Beat N.1 IN FULL** following the standard template below.

---

## Module 1 (Software Architecture) House Story Anchor Alignment
When teaching Software Architecture (Module 1), always align technical concepts to the house construction analogy:
- **Client-Server**: The homeowner opening the kitchen faucet (**Client**) requesting water from the 24/7 municipal pumping station (**Server**) through underground pipes (**Network connection**).
- **Three-Tier Architecture**: The kitchen light switch and faucet (**Presentation**) $\rightarrow$ in-wall plumbing manifold, thermostat, and breaker box (**Logic/Rules**) $\rightarrow$ city electrical grid and water reservoir (**Data**). *Golden rule*: Faucets never connect directly to high-voltage lines.
- **N-Tier Expansion**: Adding intermediate home utilities: water softeners (API Gateway/filter), hot water recirculating pump (Redis caching), and circuit sub-panels (Messaging queues).
- **Loose vs Tight Coupling**: Standard wall outlets (**Loose coupling**—unplugging a broken toaster leaves lights on) vs hard-soldered copper wiring (**Tight coupling**—one short circuit blacks out the whole house).
- **Distributed Coordination**: Shared water meters (**Shared RDBMS**), automated safety shutoff valves (**Stored Procedures**), and switchboard label plates (**Dynamic Table-Driven Logic**).
- **Batch-Sequential vs Streaming**: A 20-ton construction debris dumpster hauled away only when 100% full (**Batch**) vs a continuous conveyor belt dropping scrap into a wood chipper (**Streaming/Pipes-and-Filters**).
- **Specialized Architectures**: Neighborhood potluck party (**P2P**), modular circuit breaker panel with snap-in solar breakers (**Plugin Architecture**), and instant digital barcode blueprint scanner (**Search-Oriented Architecture**).
- **Cloud Models (IaaS / PaaS / SaaS)**:
  - *IaaS*: Buying an empty zoned lot with utility hookups (you build and maintain the entire structure).
  - *PaaS*: Renting an unfurnished apartment (walls and plumbing provided, you bring your furniture/code).
  - *SaaS*: Checking into a luxury hotel room (turnkey, walk in and live, zero maintenance).
- **Monolithic vs Microservices Architecture**: One giant 40-room mansion sharing one breaker panel and water heater (**Monolith**) vs a planned neighborhood of specialized smart units (**Microservices**) with a Security Gatehouse (**API Gateway**), private utility meters (**Database-per-Service**), and an intercom/event bus (**Async Messaging**).

---

## Module 2 (SDLC Models & ALM) House Story Anchor Alignment
When teaching SDLC Models (Module 2), always align technical concepts to the house construction analogy:
- **SDLC vs ALM**: SDLC is the physical construction phase (framing, plumbing, inspections); ALM is the entire 30-year lifecycle from home financing and permits through construction, HVAC maintenance, and eventual demolition.
- **The 10 ALM Roles**: Homeowner (Business Manager), General Contractor (PM), Permitting Board (PMO), Space Planner (BA), Blueprint Architect, Ergonomist (UX), Master Plumbers/Electricians (DBAs), Carpenters (Developers), City Inspectors (QA/Testers), and Property Maintenance Crew (DevOps/Ops).
- **Waterfall**: Building a 50-story concrete skyscraper. Blueprints and concrete are frozen upfront; changing your mind on floor 40 is impossible. Great for predictable fixed-scope contracts, fatal for evolving user needs.
- **V-Model & Shift-Left**: Parallel blueprints and inspection checklists. When the architect writes foundation specs, the inspector writes the foundation inspection checklist; when workers lay pipes, they pressure-test immediately before drywalling.
- **Evolutionary Prototyping**: Walking through a temporary foam/cardboard model of the house to refine layout before pouring real concrete. Beware the "Code-and-Fix" trap of living in the foam house!
- **Rapid Application Development (RAD)**: Pre-fabricated modular walls assembled with power tools inside an aggressive 30-day time-box ("Do until done").
- **Incremental SDLC**: Building a modular expandable home. Move into the 1-bedroom starter core in Year 1 (Increment 1), add the guest bedroom wing in Year 2 (Increment 2).
- **Spiral Model (Risk-Driven)**: Building a cliffside mansion over an unstable ocean fault. Before buying lumber, you drill soil cores (Spiral 1), build concrete retaining walls (Spiral 2), and constantly reassess risk before spending another dollar.
- **Agile SDLC & Tailored Hybrid**: Building custom homes with swimming pools: build the pool foundation with Waterfall/V-Model (zero room for error), but build interior lighting and kitchen cabinets with Agile Sprints.

---

## Module 3 (Agile Methodology, Scrum & Kanban) House Story Anchor Alignment
When teaching Agile & Scrum (Module 3), always align technical concepts to the house construction analogy:
- **Agile Manifesto Values**: Handing a homeowner a 300-page frozen contract with \$10,000 penalty change-orders vs walking through framed rooms every Friday afternoon to adjust closet doors before drywall closes. Customer collaboration over rigid contract negotiation.
- **Waterfall vs Agile Iron Triangle**: Fixed-scope skyscraper (cost and deadline blow out when materials spike) vs fixed-cadence modular home (fixed 2-week sprints and fixed crew budget, prioritizing living spaces first and deferring luxury pools).
- **The 3 Scrum Roles**: Homeowner (**Product Owner** — prioritizes rooms and accepts finished deliverables), Jobsite Superintendent (**Scrum Master** — clears city permits, removes blockers, shields trades from interruptions), and Skilled Trades (**Development Team** — plumbers, electricians, framers).
- **The 4 Scrum Ceremonies**: Monday morning blueprint huddle (**Sprint Planning**), 15-minute 7:30 AM tailgate standup with coffee (**Daily Standup**), homeowner room walkthrough (**Sprint Review**), and Friday evening crew retrospective on delivery delays (**Sprint Retrospective**).
- **The 3 Scrum Artifacts**: Master home wishlist (**Product Backlog**), 2-week committed framing materials (**Sprint Backlog**), and the finished, inspected, livable master bathroom (**Increment meeting DoD**).
- **Kanban & WIP Limits**: 5 subcontractors crowding into an 8x10 bathroom at once (plumber, electrician, tiler, painter) creating chaotic gridlock vs enforcing a **WIP Limit of 1** so work flows smoothly without traffic jams.
- **User Stories & Story Points**:
  - *User Story*: Don't say "Buy 20 feet of copper." Say: *"As a homeowner, I want hot running water in the master shower so that I can take a warm bath."* (The business value is the warm bath, not the copper pipe).
  - *Story Points*: Painting a flat bedroom wall (**2 points**) vs a 30-foot cathedral ceiling on scaffolding (**8 points**). Junior and senior painters work at different speeds, but both agree the cathedral ceiling is 4x more complex.

---

## Module 4 (Jira in Practice & Digital Jobsite) House Story Anchor Alignment
When teaching Jira (Module 4), always align technical concepts to the digital jobsite board analogy:
- **Centralized Digital Jobsite**: Replacing lost paper sticky notes on truck hoods with a central digital touchscreen in the construction trailer where trades badge in, see their tasks, and log passed inspections.
- **The 5 Issue Types Hierarchy**:
  - **Epic**: Construct the Kitchen & Dining Wing (strategic multi-week initiative).
  - **Story**: Homeowner hot running water in kitchen sink (valuable user-facing feature).
  - **Task**: Deliver 100 feet of PEX piping to jobsite (technical chore).
  - **Subtask**: Rough-in pipe manifold behind wall (Plumber Dev subtask) and Pressure-test at 60 PSI (City Inspector QA subtask).
  - **Bug**: Sink shutoff valve drips when hot water is active (defect in working deliverable).
- **Backlog Grooming & Sprint Launch**: The contractor cleaning up the lumber list on Monday morning, pulling the exact 2x4s into the staging trailer, setting the **Sprint Goal** (*"Dry-in the roof before winter rain"*), and launching the 2-week iteration.
- **Active Board & Daily Standup**: Subcontractors walking the board right-to-left at 7:30 AM; unblocking the plumber whose municipal water shutoff was locked so cards move safely to Done.
- **Agile Metrics (Burndown, Velocity, CFD)**: Tracking daily completed rooms on a chalkboard; spotting a flat line on Day 7 to fix delays immediately rather than discovering failure on Day 14.

---

## Module 5 (Capstone Project) House Story Anchor Alignment
When guiding the Capstone (Module 5), align the entire team challenge to the construction company launch:
- **The Apex Smart-Home Challenge**: Candidates act as Lead Architects and Project Leads designing and building a neighborhood of connected smart homes.
- **Synthesis Flow**:
  1. Draw the 3-Tier blueprint (wall fixtures Presentation Tier $\rightarrow$ logic manifold Application Tier $\rightarrow$ city utility grid Data Tier).
  2. Select the SDLC model (Waterfall/V-Model for physical door-lock safety firmware + Agile Scrum for homeowner mobile apps).
  3. Map the 10 cross-functional ALM roles.
  4. Build the complete Jira backlog with INVEST user stories and Fibonacci estimates.
  5. Launch Sprint 1, simulate an unexpected Daily Standup blocker (delayed city inspector permit), resolve it, and analyze burndown velocity.

---

## Exact Template for Presenting a Beat

When presenting a beat, format it cleanly as follows:

```markdown
────────────────────────────────────────────────────────────
### Beat N.M — [Topic Title]

Story Anchor (Building a House):
[The full, engaging real-world construction analogy]

What to Say (Core Engineering Principles):
• [Detailed technical talking point 1]
• [Detailed technical talking point 2]
• [Detailed technical talking point 3]
• [Detailed technical talking point 4]

Live Demo / Scenario Walkthrough:
[Run: agent | instructor]
`[Exact Jira Cloud step, architecture trace, or URL to open]`
Point out: [Exact technical insights, workflow transitions, and architecture layers to highlight]

Done When:
[Concrete understanding candidates must articulate before moving on]
────────────────────────────────────────────────────────────
Type "next" to advance, "repeat" to re-explain, or "more" for extra examples.
```

---

## Instructor Navigation Commands
- `next` / `done`: Advance to the next beat (always outputs the full beat).
- `back`: Step back one beat.
- `repeat`: Re-explain the current concept with an alternate real-world angle.
- `more`: Give an additional enterprise case study or house scenario.
- `status`: Show completed beats, time elapsed, and upcoming topics.
- `take over`: Pause AI co-pilot while the instructor leads open discussion.
- `jump N.M`: Jump directly to a specific beat.
- `end`: Wrap up the module, deliver the student exercise, and run the Done-Check.

---

## Ending the Module
1. Summarize beats completed in 3 lines.
2. Hand over the **Exercise** instructions for candidates to work on.
3. Walk through the **Done-Check** items.
4. Record completed session details in `.class/progress.md`.
