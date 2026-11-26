# Module 3 — Agile Methodology & Scrum / Kanban Framework

Teach-skill content file. Format is described in `.claude/skills/teach-sdlc-class/SKILL.md`.  
Story Anchor: **Building a House** (The Jobsite Crew, Tradespeople, Daily 7:30 AM Tailgate Standups & Visual Jobsite Boards).  

## Objectives
By the end of this module, candidates can:
1. Recite and explain the 4 Core Values, 12 Principles, and 4 major benefits of the Agile Manifesto.
2. Differentiate the Iron Triangle of Constraints in Waterfall vs Agile.
3. Distinguish the 4 Agile Frameworks: Scrum, Kanban, SAFe (Scaled Agile Framework), and XP (Extreme Programming).
4. Master the Scrum Framework: 3 Roles, 4 Ceremonies, and 3 Artifacts.
5. Explain Kanban principles: flow management, bottleneck removal, WIP limits, and contrast Scrum vs Kanban.
6. Author INVEST-compliant User Stories with Given-When-Then acceptance criteria.
7. Estimate relative effort using Fibonacci Story Points, and track progress using Velocity and Burndown charts.

---

### Beat 3.1 — What is Agile? 4 Core Values, 12 Principles & Core Benefits

- **Story Anchor (Building a House):**
  In traditional construction, the builder hands the homeowner a 300-page contract. If the homeowner realizes during drywalling that the nursery needs a closet door on the other wall, the contractor points at page 142 and says: *"Contract negotiation is closed. Sign a $10,000 penalty change-order or live without the closet."*
  In Agile home building, the contractor invites the homeowner to the jobsite every Friday afternoon. When they walk through the framed nursery together, the contractor says: *"We haven't hung the drywall yet—let's move the door frame right now before we finish the electrical wiring!"* Customer collaboration and responding to change triumph over rigid contracts.

- **Say (Key Talking Points):**
  - **What is Agile?**: An iterative and incremental approach to project management and software development that delivers value to customers faster and with fewer obstacles.
  - **Core Focus**: Collaboration, adaptability, and continuous customer satisfaction.
  - **Historical Genesis (Snowbird, Utah 2001)**: 17 software leaders (representing XP, Scrum, DSDM, Pragmatic Programming) drafted the **Agile Manifesto** to replace bureaucratic, document-heavy processes.
  - **The 4 Core Values**:
    1. **Individuals and interactions** over processes and tools.
    2. **Working software** over comprehensive documentation.
    3. **Customer collaboration** over contract negotiation.
    4. **Responding to change** over following a plan.
    *(Key Nuance: While there is value in the items on the right, we value the items on the left more).*
  - **The 12 Agile Principles (Core Pillars)**:
    1. Highest priority is customer satisfaction through early and continuous delivery of valuable software.
    2. Welcome changing requirements, even late in development, for customer competitive advantage.
    3. Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale.
    4. Business stakeholders and developers must collaborate daily throughout the project.
    5. Build projects around motivated individuals; provide support, trust, and autonomy.
    6. Face-to-face conversation is the most efficient and effective method of conveying information.
    7. Working software is the primary measure of progress.
    8. Agile processes promote sustainable development—maintaining a constant, unhurried pace indefinitely.
    9. Continuous attention to technical excellence and good design enhances agility.
    10. Simplicity—the art of maximizing the amount of work *not done*—is essential.
    11. The best architectures, requirements, and designs emerge from self-organizing teams.
    12. Team reflects at regular intervals on how to become more effective, then tunes and adjusts behavior accordingly.
  - **The 4 Core Benefits of Agile**:
    1. *Faster delivery of value*: Early working increments reach customers in weeks.
    2. *Improved collaboration*: Daily sync between business, developers, and QA removes silos.
    3. *Better adaptability*: Changes are welcomed and incorporated into upcoming sprints.
    4. *Enhanced product quality*: Frequent testing and continuous integration catch bugs early.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a scenario where a competitor launches a new feature mid-quarter:
  1. Traditional Waterfall reaction: *"The change request must be submitted to the change control board, reviewed in 6 months, and scheduled for Release 2.0 next year."* (The business loses market share).
  2. Agile response: The Product Owner brings the new requirement to the next bi-weekly Sprint Planning. The team estimates it, swaps out lower-priority backlog items, and ships the working feature to customers 14 days later.
  **Point out:**
  - Notice Principle 2: "Welcome changing requirements, even late in development. Agile processes harness change for the customer's competitive advantage."
  - Agile does not mean chaotic changes mid-sprint; changes enter the backlog and are prioritized for the next sprint boundary.
  - Progress is measured by working, tested software delivered to users, not by percent-completed specification documents.

- **Ask (Check Questions):**
  - Q: Does the Agile Manifesto mean developers should produce zero documentation? — A: No; it means working, valuable software takes precedence over endless bureaucratic manuals that become obsolete before software ships.
  - Q: Name two primary benefits an organization gains by adopting Agile over Waterfall. — A: Faster delivery of value to market and superior adaptability to changing customer requirements.

- **Done when:** Candidates can recite the 4 values, summarize the core principles, and explain the business benefits of Agile.

---

### Beat 3.2 — Agile vs Waterfall & The 4 Agile Frameworks (Scrum, Kanban, SAFe, XP)

- **Story Anchor (Building a House):**
  - **Waterfall (Fixed Scope Skyscraper)**: You commit upfront to building a 4,000 sq ft house with 5 bedrooms, an Olympic swimming pool, and Italian marble floors. If lumber prices double and labor strikes occur, your budget skyrockets and the deadline pushes back by 2 years, but the scope never changes.
  - **Agile (Fixed Cadence Modular Home)**: You have a fixed budget of $400,000 and must move in within 6 months. In Agile, the team fixes time (2-week sprints) and team size (cost), and adjusts **scope** based on priority: finish the kitchen and master bed first, and if time runs short, defer the swimming pool to next summer.

- **Say (Key Talking Points):**
  - **Agile vs Waterfall Comparison**:
    - *Waterfall*: Linear and sequential. Each phase (requirements, design, implementation, testing, deployment) must be completed before moving to the next. High upfront risk; customer preview only at the end.
    - *Agile*: Iterative and incremental. Work is divided into small cycles or sprints (typically 1–4 weeks), allowing for continuous customer feedback, quality validation, and scope flexibility.
  - **The Inverted Triangle of Constraints**:
    - *Waterfall*: Fixed Scope $\rightarrow$ Estimated Cost & Time.
    - *Agile*: Fixed Time (Sprints) & Cost (Team size) $\rightarrow$ Variable/Prioritized Scope.
  - **The 4 Major Agile Frameworks**:
    1. **Scrum**: Focuses on fixed-length sprints (1–4 weeks), clear cross-functional roles (Product Owner, Scrum Master, Developers), and formal ceremonies.
    2. **Kanban**: A visual approach emphasizing continuous flow, eliminating bottlenecks, and strictly limiting Work-in-Progress (WIP).
    3. **SAFe (Scaled Agile Framework)**: Designed for scaling Agile across massive enterprises with hundreds of developers, synchronizing multiple Scrum teams via "Agile Release Trains" (ARTs).
    4. **XP (Extreme Programming)**: Highly focused on disciplined engineering practices: Pair Programming, Test-Driven Development (TDD), Continuous Integration (CI), and automated refactoring.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through the "Iron Triangle of Constraints" trade-off during a mobile app redesign:
  1. **Waterfall Scenario**: Scope is fixed at 50 screens. Development runs late. The deadline is fixed. To hit the date, quality is compromised (testing is slashed) and costs balloon (unsustainable overtime).
  2. **Agile Scenario**: The team has a fixed 2-week sprint and a fixed team of 5 engineers. The Product Owner prioritizes the top 15 critical user journeys. The team delivers a flawless, tested MVP on time. The remaining 35 screens are prioritized across subsequent sprints.
  **Point out:**
  - In Waterfall, Scope is fixed, forcing Cost and Schedule to absorb all variance.
  - In Agile, Schedule (Sprint cadence) and Cost (Team size) are fixed, allowing Scope to be prioritized based on real customer value.
  - Extreme Programming (XP) practices like TDD and CI ensure code quality remains non-negotiable regardless of scope adjustments.

- **Ask (Check Questions):**
  - Q: How does the Agile "Iron Triangle" differ from the traditional Waterfall triangle? — A: In Waterfall, scope is fixed while time and cost flex; in Agile, time (sprint duration) and cost (team size) are fixed while scope is prioritized.
  - Q: Which Agile framework is primarily focused on software engineering practices like Test-Driven Development (TDD) and Pair Programming? — A: Extreme Programming (XP).
  - Q: What framework is used when an enterprise has 500+ engineers organized into dozens of Agile teams? — A: Scaled Agile Framework (SAFe).

- **Done when:** Candidates can contrast Agile vs Waterfall and distinguish Scrum, Kanban, SAFe, and XP.

---

### Beat 3.3 — The Scrum Framework: Roles, Ceremonies & Artifacts

- **Story Anchor (Building a House):**
  - **The 3 Roles**:
    1. *Product Owner*: The Homeowner (decides what gets built, prioritizes the kitchen over the hot tub, accepts finished rooms).
    2. *Scrum Master*: The Jobsite Superintendent (removes obstacles, clears permits, protects the workers from outside interference).
    3. *Development Team*: The Skilled Subcontractors (plumbers, electricians, carpenters building the house).
  - **The 4 Ceremonies**:
    1. *Sprint Planning*: Monday morning blueprint huddle to pick the next 2 weeks of construction.
    2. *Daily Standup*: 15-minute 7:30 AM tailgate meeting with coffee on the jobsite.
    3. *Sprint Review*: Homeowner walkthrough of the completed master bathroom.
    4. *Sprint Retrospective*: Friday evening crew meeting to discuss why the drywall delivery was late and how to improve next week.
  - **The 3 Artifacts**:
    1. *Product Backlog*: The master wishlist of all rooms and fixtures.
    2. *Sprint Backlog*: The specific lumber and pipes committed for the next 2 weeks.
    3. *Increment*: The finished, inspected, livable master bathroom.

- **Say (Key Talking Points):**
  - **What is Scrum?**: A lightweight Agile framework designed for managing complex projects through iterative cycles called **Sprints** (typically 1–4 weeks; 2 weeks is the enterprise standard).
  - **Key Roles in Scrum**:
    1. **Product Owner (PO)**: Manages and prioritizes the Product Backlog, defines user stories, maximizes business value, and accepts/rejects deliverables.
    2. **Scrum Master (SM)**: Facilitates the team, coaches adherence to Scrum practices, removes blockers/impediments, and shields engineers from external interruptions.
    3. **Development Team**: 3–9 cross-functional engineers (developers, testers, designers) who self-organize to build the product increment.
  - **Key Ceremonies**:
    1. **Sprint Planning**: Time-boxed session where the team establishes a **Sprint Goal** and selects prioritized items from the Product Backlog into the Sprint Backlog.
    2. **Daily Standup (Daily Scrum)**: 15-minute daily sync to track progress where each member answers:
       - What did I complete yesterday?
       - What will I work on today?
       - Are there any blockers or impediments in my way?
    3. **Sprint Review**: Inspect the working increment with stakeholders and gather feedback.
    4. **Sprint Retrospective**: Reflect on team dynamics, processes, and tools to identify continuous improvements for the next sprint.
  - **Scrum Artifacts**:
    1. **Product Backlog**: Prioritized list of all features, technical debt, and bugs for the entire project.
    2. **Sprint Backlog**: Forecast of items chosen for the current sprint + technical delivery plan.
    3. **Increment**: The usable, tested sum of all completed backlog items meeting the Definition of Done.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Trace the 2-week Scrum cycle on the Smart House team:
  1. **Monday (Sprint Planning)**: PO presents the Sprint Goal ("Biometric Lock Integration"). The team pulls 5 user stories (26 story points) into the Sprint Backlog.
  2. **Daily (15-min Standup)**: Each engineer answers the 3 questions. When Developer Alex reports a blocker ("Waiting on door lock OAuth API keys"), the Scrum Master immediately steps in to resolve it.
  3. **Second Friday (Sprint Review)**: The team demos working biometric lock unlocking on a live mobile simulator to the executive stakeholders.
  4. **Second Friday (Sprint Retrospective)**: The team identifies that API mock responses saved 3 days of development, and votes to adopt API mocking for all future hardware integrations.
  **Point out:**
  - The Scrum Master does not manage tasks or write code; their primary responsibility is clearing blockers and protecting team focus.
  - Daily standups are strictly time-boxed to 15 minutes and focus on coordination, not detailed problem-solving.
  - The Sprint Retrospective produces actionable process improvements that take effect in the very next sprint.

- **Ask (Check Questions):**
  - Q: Who is the only person authorized to change the priority of items in the Product Backlog? — A: The Product Owner (PO).
  - Q: What is the strictly enforced time limit for a Daily Standup, and what 3 questions are answered? — A: 15 minutes; 1. What did you do yesterday? 2. What will you do today? 3. Any blockers?
  - Q: What is the main purpose of the Sprint Retrospective? — A: Team self-inspection and continuous process improvement for the next sprint.

- **Done when:** Candidates can list and define all 3 roles, 4 ceremonies, and 3 artifacts without hesitation.

---

### Beat 3.4 — Kanban Methodology: Flow, Visualizing Work & WIP Limits

- **Story Anchor (Building a House):**
  Imagine 5 different subcontractor crews trying to work in a tiny 8x10 bathroom at the same exact time: the plumber is soldering pipes, the electrician is pulling wires, the tile installer is laying mortar, and the painter is spraying the ceiling! They bump into each other, knock over tools, and nothing gets done. 
  A smart contractor puts a **WIP Limit of 1** on the bathroom: the plumber finishes completely, leaves, then the electrician enters, then the tiler. 
  Kanban limits work in progress so work flows smoothly without traffic jams.

- **Say (Key Talking Points):**
  - **What is Kanban?**: A method focused on visualizing work, improving flow, and reducing bottlenecks, originally derived from Toyota’s lean manufacturing system.
  - **The 4 Core Kanban Principles**:
    1. *Visualize workflow*: Represent work items as cards moving across distinct column stages (e.g. To Do, In Progress, In Review, Done).
    2. *Limit Work-in-Progress (WIP)*: Restrict the maximum number of tasks allowed in any active column to prevent team overload.
    3. *Manage flow effectively*: Monitor lead time and cycle time to minimize delays and keep work flowing continuously.
    4. *Continuous improvement (Kaizen)*: Constantly inspect bottlenecks and incrementally improve processes.
  - **The Kanban Board**:
    - Columns represent workflow stages.
    - Cards represent individual tasks or work items.
    - **WIP Limits** prevent multitasking: "Stop Starting, Start Finishing!" When a column hits its limit, developers cannot pull new tickets—they must swarm to unblock downstream cards.
  - **Scrum vs Kanban Comparison**:
    - **Cadence**: Scrum uses fixed time-boxed iterations (1–4 week Sprints); Kanban uses continuous pull and continuous delivery.
    - **Roles**: Scrum prescribes Product Owner, Scrum Master, and Dev Team; Kanban prescribes no rigid roles.
    - **Planning**: Scrum uses batch planning at Sprint Planning; Kanban uses on-demand replenishment from backlog.
    - **Changes**: Scrum protects scope during the active sprint; Kanban allows changes to the backlog at any time.
    - **Primary Metric**: Scrum tracks Velocity (Story points per sprint); Kanban tracks Cycle Time and Lead Time.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Open the Kanban Board in Jira Cloud and demonstrate active workflow flow and WIP limits:
  1. Observe the board columns: `To Do`, `In Progress` (WIP Limit: 3), `In Review` (WIP Limit: 2), and `Done`.
  2. Attempt to drag a 4th card into `In Progress`: Jira warns or highlights the column indicating WIP limit violation.
  3. Rather than starting new work, engineers swarm on the 2 cards currently in `In Review` to test, approve, and move them to `Done`.
  **Point out:**
  - WIP limits enforce the core Lean rule: "Stop starting, start finishing!"
  - By capping work-in-progress, cycle time decreases and throughput of finished features increases.
  - Bottlenecks become instantly visible visually across the board when cards bunch up behind a congested column.

- **Ask (Check Questions):**
  - Q: What is the primary operational difference between Scrum and Kanban? — A: Scrum operates in fixed time-boxed sprints; Kanban operates on continuous pull without sprint boundaries.
  - Q: How do Work-in-Progress (WIP) limits improve team throughput? — A: They eliminate context-switching and multitasking bottlenecks, forcing team members to finish in-flight work before pulling new tasks.

- **Done when:** Candidates can recite the 4 Kanban principles and contrast Scrum vs Kanban.

---

### Beat 3.5 — Key Agile Practices: User Stories, Story Points, DoR/DoD & Velocity

- **Story Anchor (Building a House):**
  - **User Story**: Don't say "Buy 20 feet of copper." Say: *"As a homeowner, I want hot water running in the master shower so that I can take a warm bath after work."* The value is the warm bath, not the copper pipe!
  - **Story Points**: How long does it take to paint a wall? If it's a smooth bedroom wall, that's a 2-point job. If it's a 30-foot cathedral ceiling over a staircase on scaffolding, that's an 8-point job! You don't estimate in hours because an expert painter takes 2 hours while an apprentice takes 6 hours, but **both agree the cathedral ceiling is 4x more complex than the bedroom wall!**

- **Say (Key Talking Points):**
  - **User Story Definition & Format**:
    - Short, simple descriptions of a feature from the end-user’s perspective:
      `As a <type of user>, I want <some capability> so that <business benefit>.`
  - **The 6 INVEST Criteria (Bill Wake)**:
    - **I - Independent**: Can be built and released independently without tight coupling.
    - **N - Negotiable**: Captures intent, not a frozen contract; open to discussion.
    - **V - Valuable**: Delivers measurable value to end-users or customers.
    - **E - Estimable**: Clear enough for engineers to size with confidence.
    - **S - Small**: Sized to fit comfortably within a single sprint (typically 1–8 points).
    - **T - Testable**: Accompanied by verifiable acceptance criteria (Given-When-Then).
  - **Story Points & Relative Estimation**:
    - Measure task **complexity, effort, and uncertainty** using story points rather than time/hours.
    - Decouples estimation from individual developer speed (junior vs senior).
    - Uses the Modified Fibonacci Scale: `1, 2, 3, 5, 8, 13, 21`.
  - **Definition of Ready (DoR) vs Definition of Done (DoD)**:
    - **DoR**: Criteria required before a task can enter a sprint (clear user story, acceptance criteria defined, dependencies resolved, estimated).
    - **DoD**: Criteria required before considering a task complete (code reviewed, unit tests passing, QA verified, deployed to staging/production).
  - **Agile Tracking Metrics**:
    - **Velocity Tracking**: Measures the amount of work (total story points) completed by a team in a sprint; used to forecast future capacity.
    - **Burndown Charts**: Track sprint progress by visualizing remaining work (story points) over time.

- **Demo / Story Workshop (run: instructor):**
  Critique two candidate user stories to demonstrate INVEST quality enforcement:
  - **Non-Compliant Story (Fails INVEST)**:
    - *Title*: "Build the lock now"
    - *Critique*: Fails 'V' (Valuable)—no user role or business benefit specified; fails 'T' (Testable)—no acceptance criteria; fails 'E' (Estimable)—vague technical chore.
  - **Compliant INVEST Story**:
    - *Title*: "Master Bedroom Lighting Dimmer"
    - *Format*: "As a homeowner, I want automated lighting dimmers so that energy consumption drops and room ambiance is customizable."
    - *Acceptance Criteria (Given-When-Then)*:
      - Given the bedroom smart switch is connected to the home network
      - When the homeowner slides the brightness control to 40%
      - Then the fixture dims within 500ms and power draw is recorded
    - *Estimate*: 3 Story Points (Fibonacci scale)
  **Point out:**
  - The essential difference between a technical chore and an outcome delivering real business value.
  - How Given-When-Then criteria remove ambiguity between the Product Owner and the QA team.

- **Ask (Check Questions):**
  - Q: Why do Agile teams estimate in relative Story Points rather than calendar hours? — A: Story points account for inherent complexity and uncertainty, avoiding false precision and removing bias between junior and senior developer speeds.
  - Q: What is the difference between the Definition of Ready (DoR) and the Definition of Done (DoD)? — A: DoR is the exit gate from the backlog into a sprint; DoD is the quality checklist required before an item is marked complete.
  - Q: What does team Velocity represent? — A: The average number of story points successfully completed per sprint.

- **Done when:** Candidates can author an INVEST user story, explain story points, and contrast DoR vs DoD.

---

## Exercise: Story Writing & Planning Poker Workshop
1. **Author a User Story**: Feature: *"Smart Thermostat Remote Control."*
   - Write using the standard template: `As a... I want... so that...`
   - Include 3 Given-When-Then acceptance criteria.
2. **Estimate Points**: Conduct Planning Poker using Fibonacci scale (1, 2, 3, 5, 8). Justify your score based on complexity and risk.
3. **Break into Subtasks**: Split the story into 1 Developer subtask and 1 QA subtask.

## Done-Check
- [ ] Can recite the 4 values and 4 core benefits of the Agile Manifesto.
- [ ] Can contrast Waterfall vs Agile and distinguish Scrum, Kanban, SAFe, and XP.
- [ ] Can name the 3 Scrum roles, 4 ceremonies, and 3 artifacts.
- [ ] Can explain how Kanban WIP limits reduce bottlenecks.
- [ ] Can write an INVEST user story with Given-When-Then criteria.
- [ ] Can explain why Story Points measure relative complexity, not hours.

---

## Post-Class Practice & Dynamic Interview Preparation
When reviewing this module after class or preparing for technical interviews, use your AI practice coach to dynamically generate fresh, real-world Agile execution scenarios:
- In chat, type: **`interview questions on module 3`** or **`give me an agile leadership interview challenge`**.
- The AI coach dynamically generates random, interview-grade scenarios (mid-sprint scope changes, Iron Triangle trade-offs, Kanban CFD bottlenecks, story sizing disputes) and evaluates your leadership approach in real time.
