# Module 2 — SDLC Models & Application Lifecycle Management (ALM)

Teach-skill content file. Format is described in `.claude/skills/teach-sdlc-class/SKILL.md`.  
Story Anchor: **Building a House** (Construction Contracts, Building Codes, Turnkey High-Rises vs Modular Home Additions).  

## Objectives
By the end of this module, candidates can:
1. Explain the complete Application Lifecycle Management (ALM) framework, the 10 cross-functional roles, and their modern evolution (SDET, DevOps/SRE, DevSecOps).
2. Evaluate the Waterfall model: sequential phase-gating, strengths, deficiencies (big-bang integration), and where it remains mandatory in the modern world.
3. Master the V-Shaped model: parallel verification and validation mapping, Shift-Left testing, and the modern Test Pyramid.
4. Contrast Structured Evolutionary Prototyping (MVPs and avoiding the "Code-and-Fix" trap), Rapid Application Development (RAD time-boxing), and Incremental SDLC.
5. Master the Spiral Model: its 4 quadrants, risk-driven philosophy, and modern architectural spikes / POCs.
6. Master Agile SDLC methods: Feature Driven Development (FDD `<action> <result> <object>`), Dynamic Systems Development Method (DSDM 80/20 rule & Ambassador users), and Extreme Programming (XP engineering practices).
7. Defend and architect a Tailored Hybrid SDLC model for real-world enterprise projects.

---

### Beat 2.1 — What is SDLC & The Application Lifecycle Management (ALM) Process

- **Story Anchor (Building a House):**
  Building a home isn't just hammering nails into wood. It starts months earlier when a family decides they need more space (Business need), consults a bank for financing (Funding), commissions an architect for blueprints (Design), obtains city zoning permits (Compliance), hires plumbers and electricians (Development), calls city inspectors to sign off on plumbing pressure (QA/Testing), and moves in to maintain the roof and furnace for the next 30 years (Operations & Maintenance). 
  **SDLC** is the construction phase; **ALM** is the entire lifecycle from initial dream to demolition day.

- **Say (Key Talking Points):**
  - **Definition of Computer Software**: A collection of computer programs, procedures, data structures, and associated documentation providing instructions for telling computer hardware what to do and how to do it.
  - **SDLC (Software Development Life Cycle)**: A structured framework describing the sequence of activities, phases, deliverables, and quality gates performed during software creation.
  - **ALM (Application Lifecycle Management)**: The continuous governance, engineering, operational maintenance, and decommissioning framework. ALM spans three broad dimensions:
    ```
                      ┌────────────────────────────────────────────────────────┐
                      │          Application Lifecycle Management (ALM)        │
                      │  (Governance, Portfolio, Compliance, Budget, SLAs)     │
                      └──────────────────────────┬─────────────────────────────┘
                                                 │
          ┌──────────────────────────────────────┴──────────────────────────────────────┐
          │                                                                             │
          ▼                                                                             ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ Requirements │──►│ Architecture │──►│ Implementation│──►│ Testing & QA │──►│ Operations & │
    │  & Analysis  │   │   & Design   │   │   (Coding)   │   │ (Verification)│  │ Maintenance  │
    └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
          ▲                                                                             │
          └────────────────────────── Continuous Feedback Loop ─────────────────────────┘
    ```
    1. *Governance*: Portfolio decision-making, business value justification, regulatory compliance, and budget/resource management.
    2. *Development*: Requirements engineering, architectural modeling, coding, and automated verification (the traditional SDLC).
    3. *Operations & Maintenance*: CI/CD deployment, server monitoring, incident response, performance optimization, and eventual system retirement.
  - **The Defect Cost Escalation Curve (The Economic Rationale)**:
    - **Requirements / Architecture ($1x - Lowest)**: Update a bullet point in a spec or erase a line on a whiteboard.
    - **Development / Local Coding ($5x)**: Engineer rewrites local unit test and refactors function in pull request.
    - **Automated Testing / CI ($15x)**: Pull request blocked, ticket reassigned, branch re-tested.
    - **Production Post-Release ($30x - 100x)**: Emergency hotfix war room, database rollback, data loss, client SLA penalty.

- **Modern Enterprise Real-World Context**:
  - Today, ALM is automated through **CI/CD pipelines, DevSecOps, and Cloud Observability**.
  - Code changes commit to Git, automatically trigger unit tests and static security analysis (SAST), deploy to ephemeral preview environments, and stream live metrics to monitoring dashboards (Datadog, Prometheus).

- **Scenario Walkthrough: The $100x Production Bug Incident (run: instructor):**
  Trace the cost escalation of an architectural flaw in a residential smart door lock system:
  - *Phase 1 (Requirements/Design)*: The architect notices no offline fallback is specified if home WiFi drops. Fix: Erase diagram, add local Bluetooth fallback protocol. Cost: $100 (1 hour whiteboard review).
  - *Phase 2 (Implementation)*: Developer discovers the omission during coding. Fix: Refactor local lock firmware. Cost: $500 (1 day developer effort).
  - *Phase 3 (QA Testing)*: Tester catches the bug in the staging test lab. Fix: Re-open ticket, re-code firmware, re-run automated regression suite. Cost: $1,500.
  - *Phase 4 (Production Release)*: 10,000 homes deploy the lock; a regional internet outage locks residents out of their houses at night. Emergency locksmiths dispatched, PR crisis, recall issued, class-action lawsuit. Cost: $100,000+ (100x to 1000x design cost).
  **Point out:**
  - Emphasize that quality assurance and architectural rigor during early ALM phases exist for pure risk and cost mitigation.

- **Ask (Check Questions):**
  - Q: What is the core difference between SDLC and ALM? — A: SDLC focuses specifically on the development phases of software; ALM is the broader lifecycle covering business justification, governance, development, operations, and eventual retirement.
  - Q: Why is skipping the design or requirements phase almost always more expensive than completing it? — A: Fixing a bug or misunderstanding in production costs 30x to 100x more than catching it during requirements or design.

- **Done when:** Candidates can define SDLC and ALM and explain the cost of late-stage defect discovery.

---

### Beat 2.2 — The 10 Core Roles in the ALM Process & Modern Evolution

- **Story Anchor (Building a House):**
  A house cannot be built by a single carpenter working alone. You need:
  - The Homeowner / Investor (funds the house).
  - The General Contractor (keeps work on schedule and within budget).
  - The City Permitting Office / PMO (makes sure it fits neighborhood portfolio plans).
  - The Interior Space Planner / BA (figures out what the family really needs).
  - The Structural Architect (draws the engineering blueprints).
  - The Decorator & Ergonomist / UX (places switches and counters where people naturally reach).
  - The Master Plumber & Electrician / DBAs (connects and tunes critical infrastructure lines).
  - The Carpenters & Bricklayers / Developers (write the physical walls into existence).
  - The City Building Inspector / Testers (tests pipes and verifies building codes before walls close).
  - The Property Maintenance Crew / Ops (services HVAC, cleans gutters, and keeps the house running).

- **Say (Key Talking Points):**
  Modern software engineering is an integrated, cross-functional team sport:
  1. **Business Manager**: Decides when development activity starts based on market analysis and expected return on investment (ROI).
  2. **Project Manager (PM)**: Manages project schedules, tracks milestones, mitigates risks, and controls budgets.
  3. **PMO Decision Makers (Project Management Office)**: Evaluates how the new initiative impacts or expands the company’s broader project portfolio and allocates organizational resources.
  4. **Business Analyst (BA)**: Elicits, analyzes, and documents detailed stakeholder requirements, translates business problems into technical user stories, and bridges business and tech.
  5. **Architect**: Draws the initial blueprint of the technical solution, selecting system topology, technology stacks, non-functional requirements (scalability, security), and service interfaces.
  6. **User Experience (UX) Design Team**: Conducts user research, builds design systems, creates interactive wireframes, and ensures intuitive usability.
  7. **Database Administrators (DBAs)**: Tunes schemas, indexing, query optimization, high-availability clusters, backup SLAs, and guarantees data integrity.
  8. **Developers (Software Engineers)**: Build the application by turning architecture blueprints and business specifications into clean, modular, testable source code.
  9. **Testers (Quality Assurance)**: Engaged from the very first written requirement through deployment, designing test plans, automated suites, performance testing, and validating compliance.
  10. **Operations and Maintenance Staff (DevOps/SRE)**: Takes custody of finished applications, manages cloud infrastructure, handles production releases, monitors uptime, and supports systems until retirement.

- **Modern Enterprise Real-World Evolution**:
  - **Business Analyst (BA) -> Product Manager (PM)**: Discovers customer problems, manages backlog ROI, defines acceptance criteria.
  - **Tester (QA) -> SDET (Software Development Engineer in Test)**: Writes automated test frameworks running inside CI/CD.
  - **Operations Staff -> DevOps & SRE (Site Reliability Engineer)**: Uses Infrastructure-as-Code (Terraform, Kubernetes) to maintain 99.99% uptime.
  - **Security Auditor -> DevSecOps Engineer**: Integrates automated security scanners into Git pull requests.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a real-world production incident on the Smart House platform to show the 10 roles in action:
  1. A security vulnerability is reported: The PM and PMO evaluate priority and allocate team bandwidth.
  2. The BA translates the security flaw into a user story with testable acceptance criteria.
  3. The Architect reviews the API token schema change, while the DBA audits indexing on the auth table.
  4. The Developer writes the fix; the SDET runs automated regression tests in the CI pipeline.
  5. The DevOps/SRE deploys the canary build to AWS; the Support/Ops team monitors telemetry and alert boards.
  **Point out:**
  - Notice how every role owns a distinct phase of the application lifecycle without working in isolated silos.
  - QA/SDET is engaged right at the requirements stage to design test scenarios, not tacked on at the end.
  - Operations has evolved into automated DevOps/SRE managing infrastructure as code.

- **Ask (Check Questions):**
  - Q: At what stage in the ALM process should the QA/Testing team become involved? — A: From the very beginning during requirements analysis (to design test cases and ensure requirements are testable), NOT just at the end after coding is finished!
  - Q: How has the traditional Operations role evolved in modern cloud engineering? — A: Operations has evolved into DevOps and SRE, using code (Terraform, Docker, Kubernetes) to automate infrastructure provisioning, CI/CD, and 99.99% system reliability.

- **Done when:** Candidates can name at least 6 ALM roles, describe their distinct responsibilities, and explain the modern evolution to SDET and DevOps/SRE.

---

### Beat 2.3 — The Waterfall Model: Linear Sequential Engineering

- **Story Anchor (Building a House):**
  Waterfall is like building a 50-story concrete skyscraper. 
  Step 1: Geological survey. Step 2: Excavate foundation. Step 3: Pour concrete. Step 4: Steel framing. Step 5: Glass curtain walls. 
  Every phase must be 100% finished before the next starts. 
  If the client walks onto the 40th floor in month 18 and says: *"Actually, I want a 10-story atrium with an indoor waterfall right in the center!"*, you cannot do it—the structural pillars are already frozen in concrete! 
  Waterfall gives great scheduling predictability, but zero flexibility to changing minds.

- **Say (Key Talking Points):**
  - **Sequential Phase-Gating**: Work cascades downward in strict, discrete stages:
    1. *Requirements Analysis*: Defines needed information, function, behavior, performance, and interfaces.
    2. *Design*: Data structures, software architecture, interface representations, algorithmic details.
    3. *Implementation (Coding)*: Source code development, database setup, user documentation, and initial unit verification.
    4. *Testing & Integration*: Big-bang system integration, verification against requirements specifications.
    5. *Maintenance & Operations*: Defect fixes, environment patching, and support.
  - **Requirements Freezing**: Deliverables created for each phase are considered frozen before the next begins.
  - **Key Strengths**:
    - Easy to understand, simple to manage with well-understood milestones.
    - Provides structure for inexperienced staff.
    - Sets requirements stability; good for management tracking and fixed-price contracts.
    - Works well when quality and predictability are prioritized over cost and schedule flexibility.
  - **Critical Deficiencies**:
    - All requirements must be known and locked upfront.
    - Deliverables are frozen, inhibiting flexibility and adaptation to customer feedback.
    - Gives a false impression of progress (writing 500 pages of requirements does not mean 50% of the working system is delivered!).
    - **Integration is one big bang at the end**: Different modules developed in silos collide at the end, exposing architectural mismatches when schedule time has expired.
    - Little opportunity for customers to preview the system until it is practically finished.

- **Modern Enterprise Real-World Context**:
  - *Is Waterfall dead?* **No!** While pure Waterfall failed for fast-moving web apps, it remains strictly mandated in:
    1. **Medical Devices & Healthcare**: FDA Class III medical devices (pacemakers, surgical robots) where requirements cannot change on a whim.
    2. **Aerospace & Defense**: Flight control avionics (FAA DO-178C certification) where fatal crashes result from unverified code changes.
    3. **Automotive Firmware**: ISO 26262 automotive safety integrity levels (ASIL D) for anti-lock braking and autonomous driving modules.
    4. **Hardware-Dependent Systems**: When software is burned into ASIC microchips or silicon that cannot be patched over the air.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through the catastrophic cost of a late change request in a Waterfall avionics project:
  1. Month 1-6: Flight navigation system requirements frozen and signed off.
  2. Month 7-18: Architectural design, code implementation, and hardware assembly completed in silos.
  3. Month 19 (Testing / Big-Bang Integration): The flight computer is integrated with cockpit sensor hardware for the first time. The team discovers a timing synchronization mismatch.
  4. Rework requires redesigning circuit boards, rewriting core firmware, and re-submitting FAA compliance filings, costing \$1.8M and 14 months of delay.
  **Point out:**
  - In Waterfall, big-bang integration at the end surfaces all interface and timing mismatches when they are most expensive to fix.
  - Because each phase was signed off and frozen, rolling back to redesign the architecture breaks schedules and budgets.
  - Waterfall succeeds only when specifications are physically frozen and fully known upfront (e.g. ASIC microchips, space flight).

- **Ask (Check Questions):**
  - Q: Why is "big-bang integration" considered the biggest risk in Waterfall? — A: Because different components developed in silos are integrated only at the end; architectural incompatibilities and interface bugs surface when there is no time left to fix them.
  - Q: In what modern industries is Waterfall still preferred over pure Agile? — A: Safety-critical regulated domains: medical devices, avionics, automotive braking firmware, and defense hardware.

- **Done when:** Candidates can draw the Waterfall phases and articulate its pros, cons, and appropriate modern domains.

---

### Beat 2.4 — The V-Shaped Model: Parallel Verification & Validation

- **Story Anchor (Building a House):**
  In the V-Model, you never design a part of the house without simultaneously writing the inspection checklist for that specific part:
  - When the architect writes the **Foundation Specs**, the city inspector writes the **Foundation Inspection Checklist**.
  - When the plumber maps the **In-Wall Pipes**, they write the **60-PSI Pressure Test Checklist**.
  - When workers lay the pipes, they immediately run the pressure test checklist before closing the drywall!
  The design descends down the left side of the "V"; the testing ascends up the right side.

- **Say (Key Talking Points):**
  - **The V-Model Concept**: A direct variant of Waterfall emphasizing parallel planning for Verification and Validation:
    - Testing is not an afterthought squeezed at the end; test design begins concurrently with the corresponding development phase.
  - **The Left-to-Right Mapping Diagram**:
    ```
      Requirements & Planning  ────────────────────────►  System & Acceptance Testing
              \                                                     /
          Product Analysis     ────────────────────────►  System Integration Testing
                  \                                             /
              Architecture     ────────────────────────►  Component Integration Testing
                      \                                     /
                    Design     ────────────────────────►  Unit Testing
                            \                             /
                              ─────►  Apex: Coding  ─────►
    ```
    - *Project & Requirements Planning* $\longleftrightarrow$ **System & Acceptance Testing**: Complete specification $\rightarrow$ test entire software system in operational environment with real users.
    - *Product Requirements Analysis* $\longleftrightarrow$ **System Integration Testing**: Complete specification $\rightarrow$ verify all integrated subsystems function together.
    - *Architecture / High-Level Design* $\longleftrightarrow$ **Component Integration Testing**: Define software functions and component contracts $\rightarrow$ verify interfaces between modules.
    - *Detailed Design* $\longleftrightarrow$ **Unit Testing**: Develop specific algorithms and data models $\rightarrow$ verify individual functions and classes in isolation.
    - *Apex of the V: Coding*: Production of source code.
  - **Verification vs Validation (The Golden Interview Distinction)**:
    - **Verification**: *"Are we building the product right?"* (Checking code against specifications, designs, algorithms, and architectural standards).
    - **Validation**: *"Are we building the right product?"* (Checking software against actual customer business needs, user workflows, and operational usability).
  - **Strengths**: Emphasizes early planning for V&V, increases probability of high-quality delivery, simple and disciplined tracking.
  - **Weaknesses**: Does not easily handle concurrent events, lacks early working software iterations, rigid change management.
  - **When to Use V-Model**: Systems requiring **high reliability and safety** (hospital patient monitoring, air traffic control, nuclear plant controllers, automotive braking systems).

- **Modern Enterprise Real-World Context**:
  - The V-Model is the foundation of **Shift-Left Testing**: writing test specifications *before* or *in parallel with* code rather than waiting for manual QA at the end.
  - In modern engineering, the right side of the V is realized as the **Test Pyramid**:
    - *Base*: Thousands of fast, automated **Unit Tests** (0.01s).
    - *Middle*: Hundreds of **Integration Tests** testing API contracts and database queries (0.5s).
    - *Apex*: Targeted **End-to-End (E2E) Acceptance Tests** testing user journeys in headless browsers (5s).

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through the V-Model parallel traceability matrix for a medical insulin infusion pump:
  1. **Phase 1 (Requirements Planning)**: The team writes requirement REQ-101 ("Maximum bolus delivery: 5.0 units"). Concurrently, the QA lead writes Acceptance Test Plan ATP-101 to verify bolus caps under all battery states.
  2. **Phase 2 (Architectural Design)**: The architect specifies the motor controller interface. Concurrently, integration test engineers author Component Integration tests for the motor API.
  3. **Phase 3 (Coding & Verification Ascent)**: Developers write the motor firmware; the team executes unit tests, then ascends through integration tests, and finally executes ATP-101 with real pump hardware.
  **Point out:**
  - Notice the 1-to-1 horizontal linkage across the "V": testing plans are created in parallel with design, not after code exists.
  - Verification confirms the motor driver matches the technical blueprint specifications.
  - Validation confirms the insulin pump safely delivers the exact physician-prescribed dosage to the patient.

- **Ask (Check Questions):**
  - Q: In the V-Model, when is the Acceptance Test Plan created? — A: During the Requirements Planning phase at the very beginning of the project.
  - Q: What is the fundamental difference between Verification and Validation? — A: Verification checks conformance to technical specs; Validation ensures the software meets real user business needs.
  - Q: How does the modern concept of "Shift-Left Testing" relate to the V-Model? — A: Shift-Left moves testing activities (test case design, automated unit/integration checks) to the earliest stages of development, exactly as prescribed by the V-Model's parallel planning.

- **Done when:** Candidates can draw the V-Model, pair the development stages with testing stages, and define Verification vs Validation.

---

### Beat 2.5 — Structured Evolutionary Prototyping Model: MVPs & The Code-and-Fix Trap

- **Story Anchor (Building a House):**
  Before building a multi-million-dollar custom mansion, the builder constructs a full-scale 3D physical model or stages an interactive walk-through room with temporary foam walls. The homeowner walks through, touches the countertops, realizes the kitchen island is too cramped, and asks to widen the hallway. The builder modifies the foam model in real time. Once the family loves the layout, they order the real steel, concrete, and hardwood.

- **Say (Key Talking Points):**
  - **Core Concept**: Developers build an initial prototype during the requirements phase; the prototype is demonstrated to end users, who evaluate it and provide corrective feedback. Developers refine the prototype in an iterative loop until the user is satisfied, at which point the prototype code is engineered up to production standards.
  - **Step-by-Step Lifecycle**:
    1. Develop preliminary project plan.
    2. Create partial high-level paper model or wireframes.
    3. Generate partial requirements specification from the model.
    4. Build an interactive working prototype featuring basic and critical attributes (core database, key user interface screens, fundamental algorithmic functions).
    5. Demonstrate prototype to users; users evaluate problems and suggest improvements.
    6. **Iterative Loop**: Developers refine the prototype; repeat demonstrations until customer is satisfied.
    7. Hardening: Bring code up to production quality, security, and performance standards.
  - **Strengths**:
    - Customers can physically "see" and interact with system requirements as they are being gathered.
    - Developers learn domain nuances directly from customers.
    - Produces a significantly more accurate end product tailored to real human workflows.
    - Accommodates unexpected or evolving requirements with ease.
    - Provides flexible design and steady, visible signs of progress.
  - **Weaknesses**:
    - **Code-and-Fix Trap**: Strong tendency to abandon structured software engineering practices for messy, unmaintainable "quick-and-dirty" hacking.
    - Maintainability and architecture quality may be overlooked.
    - **Client Delivery Pressure**: Customers seeing a working UI may demand the prototype be deployed directly to production, unaware that security, scaling, and error handling are missing!
    - Process may continue indefinitely without closure (endless scope creep).
  - **When to Use**:
    - Requirements are unstable, ambiguous, or need extensive user clarification.
    - Developing complex, novel user interfaces.
    - Short-lived proof-of-concept demonstrations.
    - New, original development where no prior system exists.
    - During the analysis and design portions of object-oriented development.

- **Modern Enterprise Real-World Context**:
  - Evolutionary prototyping is the grandfather of today's **MVP (Minimum Viable Product)** and clickable **Figma / UX design prototypes**.
  - *The Real-World Warning*: In startup culture, engineers often build a hacky "prototype" for an investor demo, and leadership insists on releasing it to real customers. Without refactoring, this creates massive **technical debt**, security vulnerabilities, and scalability crashes.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through an interactive prototyping cycle and the "Code-and-Fix" trap:
  1. **Prototype 1**: Engineers build a lightweight interactive web prototype with simulated JSON data to test resident energy dashboard visualizations.
  2. **User Evaluation**: Residents test the prototype and reveal they never use pie charts; they only want a single "Estimated Monthly Bill ($)" gauge.
  3. **The Trap**: Executive leadership loves the demo and demands: *"Ship this exact code to 50,000 customers tomorrow!"*
  4. **The Safe Path**: The engineering team explains that the prototype lacks authentication, database connection pools, and error handling. They engineer the validated UI design into production-grade microservices.
  **Point out:**
  - Evolutionary prototyping quickly discovers true customer needs before expensive backend engineering begins.
  - Never allow a rapid prototype to be deployed directly to production without production engineering (the Code-and-Fix trap).
  - Modern evolutionary prototyping maps directly to building interactive Figma prototypes and customer MVPs.

- **Ask (Check Questions):**
  - Q: What is the primary danger when a customer sees a working evolutionary prototype? — A: The customer may assume the system is finished and demand it be delivered immediately to production, unaware that backend security, scaling, and test coverage are missing.
  - Q: What is the "code-and-fix" trap in prototyping? — A: Abandoning disciplined architecture, tests, and clean code in favor of rapid, unmaintainable patches to satisfy short-term demo requests.

- **Done when:** Candidates can explain the 7 steps of Evolutionary Prototyping, its major risk (the code-and-fix trap), and its modern evolution into MVPs.

---

### Beat 2.6 — Rapid Application Development (RAD) & Incremental SDLC Models

- **Story Anchor (Building a House):**
  - **RAD**: Using prefabricated modular walls and snap-in cabinets. A team of builders works inside a strict 30-day "time-box" with power tools to assemble a turnkey home.
  - **Incremental**: Building a modular expandable home. In Year 1, build the core 1-bedroom home with kitchen and bathroom so the family moves in immediately (Increment 1). In Year 2, add the children's bedroom wing (Increment 2). In Year 3, add the 2-car garage (Increment 3).

- **Say (Key Talking Points):**
  - **Rapid Application Development (RAD)**:
    - Squeezes development into short, aggressive **time-boxes** (typically 60 to 90 days) using visual productivity tools, screen builders, and component reuse.
    - **The 4 Core Phases**:
      1. *Requirements Planning Phase*: Intensive workshop utilizing structured discussions of business problems.
      2. *User Description Phase*: Automated tools and modeling capture information directly from users.
      3. *Construction Phase*: High-productivity tools (code generators, screen builders) assemble the software inside a time-box ("Do until done").
      4. *Cutover Phase*: Final system installation, user acceptance testing (UAT), and user training.
    - *Strengths*: Reduced cycle time, improved productivity with smaller teams (lower costs), time-box mitigates schedule risk, focus moves from paperwork to working code (WYSIWYG).
    - *Weaknesses*: Requires total, rapid-fire commitment from both developers and customers; hard to use with legacy systems; requires modular architecture; risk of never achieving closure.
    - *When to Use*: Reasonably well-known requirements, dedicated user involvement throughout, project can be modularized and time-boxed, low technical risk, ultra-high performance not required.
  - **Incremental SDLC Model**:
    - Constructs a partial implementation of a total system, then slowly adds increased functionality across successive releases.
    - Prioritizes requirements and implements them in grouped increments: each subsequent release adds capability to the operational foundation.
    - *Strengths*: Develops high-risk or major functions first; each release delivers a working, operational product; customers get critical functionality early; divide-and-conquer task breakdown lowers initial capital cost.
    - *Weaknesses*: Requires exceptional upfront architecture and interface design so future increments plug in smoothly; total cost of the complete system is not lower.
    - *When to Use*: Early realization of business benefits is vital; requirements are mostly known upfront but evolve; lengthy development schedules; integrating new technology.

- **Modern Enterprise Real-World Context**:
  - **Time-boxing**: The concept of the "time-box" introduced by RAD is the fundamental building block of modern 2-week Agile Scrum sprints.
  - **Incremental in SaaS**: Modern SaaS products (Netflix, Stripe, Spotify) operate on continuous incremental delivery: deploying small, decoupled feature increments multiple times a day behind **feature flags** (canary deployments) rather than releasing one giant monolithic update once a year.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a 60-day RAD time-box vs an Incremental delivery roadmap:
  1. **RAD 60-Day Time-Box**: A logistics portal must go live before peak holiday shipping. The scope includes 10 candidate features. At Day 45, features 1 through 7 are complete, but features 8-10 are behind. The team drops features 8-10 to hit the hard 60-day deadline (scope flexes, schedule holds).
  2. **Incremental Delivery**: Increment 1 delivers basic package scanning. Increment 2 delivers automated route optimization. Increment 3 delivers real-time SMS delivery tracking.
  **Point out:**
  - In RAD, the time-box is non-negotiable; scope adjusts to meet the deadline.
  - In the Incremental model, every release delivers a functioning, fully tested subsystem that generates early business value.
  - RAD's time-box is the direct conceptual ancestor of modern 2-week Agile Scrum sprints.

- **Ask (Check Questions):**
  - Q: What does the term "time-box" mean in Rapid Application Development (RAD)? — A: A fixed window of time (e.g. 60 days) where team members build as much functionality as possible; deadline and budget are fixed, scope is adjusted.
  - Q: Why does the Incremental Model require exceptional architectural design at the very beginning? — A: Because well-defined module interfaces are required so future increments can cleanly integrate into code written months earlier.

- **Done when:** Candidates can describe the 4 phases of RAD and explain how Incremental development delivers early customer value.

---

### Beat 2.7 — The Spiral Model: Risk-Driven Engineering & Spikes

- **Story Anchor (Building a House):**
  Building a home on a steep, unstable cliffside overlooking the ocean. 
  Before buying framing lumber, you evaluate the catastrophic risk of a landslide. 
  - *Spiral 1*: Soil drill tests and geological simulations. (Risk resolved: bedrock is 20 feet down). 
  - *Spiral 2*: Pour concrete retaining pilings and test stability. (Risk resolved: foundation is rock solid). 
  - *Spiral 3*: Construct the lower living levels. 
  At every turn of the spiral, you evaluate whether the project is safe to continue or whether you should stop before spending another million dollars.

- **Say (Key Talking Points):**
  - **Origins (Barry Boehm, 1986)**: The Spiral Model introduces **explicit, continuous risk assessment** into the software lifecycle, combining the structured phase-gating of Waterfall with the iterative prototyping of RAD.
  - **The 4 Quadrants in Each Cycle**:
    ```
                       Quadrant 1:                       Quadrant 2:
                  Determine Objectives,              Identify & Resolve
                 Alternatives, Constraints                 Risks
                                    \                  /
                                     \                /
                                      \              /
                                       ──────────────
                                      /              \
                                     /                \
                                    /                  \
                        Quadrant 4:                      Quadrant 3:
                         Plan Next                   Develop & Verify
                           Cycle                    Next-Level Product
    ```
    1. *Quadrant 1: Determine Objectives, Alternatives & Constraints*: Define goals, performance benchmarks, and design choices.
    2. *Quadrant 2: Identify and Resolve Risks*: Perform deep risk analysis, build prototypes, simulate workloads, and benchmark critical algorithms.
    3. *Quadrant 3: Develop and Verify Next-Level Product*: Build the software increment, run integration and unit testing.
    4. *Quadrant 4: Plan Next Cycle*: Review results with stakeholders and plan the subsequent iteration of the spiral.
  - **Strengths**:
    - Early indication of insurmountable risks without spending the entire project budget.
    - Critical high-risk functions and architectural bottlenecks are resolved first.
    - Users see prototypes early and are tied into all lifecycle steps.
    - Cumulative financial costs are assessed frequently.
  - **Weaknesses**:
    - Highly complex model requiring specialized risk-assessment expertise.
    - Excessive overhead and planning time for small or low-risk projects.
    - The spiral can continue indefinitely if risk thresholds are not strictly defined.
  - **When to Use Spiral Model**:
    - Medium-to-high risk, large-scale projects.
    - When costs and risk evaluation are critical to organizational survival.
    - Users are unsure of their exact needs and requirements are highly complex.
    - Breakthrough, research-oriented systems or completely new product lines.

- **Modern Enterprise Real-World Context**:
  - In modern Agile engineering, the Spiral philosophy lives on as **Architectural Spikes** and **Proof-of-Concept (POC) cycles**:
    - If a team doesn't know whether a new third-party payment gateway or database will scale to 50,000 requests/sec, they don't commit it to a feature sprint.
    - They dedicate a 1-week **Spike** (risk analysis & prototype) to benchmark it. If it fails, they terminate the approach early (**Fail-Fast Principle**) before burning hundreds of thousands of dollars in team sprint cycles.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a 4-quadrant Spiral cycle and an architectural spike:
  1. **Quadrant 1 (Objectives)**: The smart home platform must ingest 100,000 sensor telemetry events per second.
  2. **Quadrant 2 (Risk Analysis & Prototype)**: The primary risk is database write lock contention. The team runs a 1-week benchmark spike comparing direct PostgreSQL writes against an in-memory queue.
  3. **Quadrant 3 (Develop & Verify)**: Benchmarks reveal PostgreSQL locks at 12,000 events/sec; the in-memory queue handles 150,000 events/sec. The team implements the queue buffer.
  4. **Quadrant 4 (Plan Next Cycle)**: Stakeholders review benchmark data and approve proceeding to the next spiral (device authentication and schema validation).
  **Point out:**
  - Notice how the project would have failed in late integration if the team had not evaluated the write-bottleneck risk in Quadrant 2.
  - Modern Agile teams implement the Spiral philosophy through 1-week "Architectural Spikes" to resolve technical unknowns before sprint planning.
  - The spiral allows early termination ("fail-fast") if an insurmountable technical or financial risk is detected.

- **Ask (Check Questions):**
  - Q: What makes the Spiral Model uniquely different from Waterfall, V-Model, or RAD? — A: Its mandatory, explicit risk analysis quadrant executed during every single cycle of the project.
  - Q: How is the Spiral Model's risk-driven approach used in modern Agile engineering? — A: Through time-boxed "Spikes" and Proof-of-Concepts (POCs) that benchmark high-risk technical unknowns before committing them to production backlogs.

- **Done when:** Candidates can draw the 4 quadrants of the Spiral Model and explain why it is risk-driven.

---

### Beat 2.8 — Agile SDLC Frameworks (FDD, DSDM, XP) & Tailored Hybrid SDLC

- **Story Anchor (Building a House):**
  - **Tailored SDLC in Home Building**: If you are building a custom home with an indoor swimming pool:
    - You build the swimming pool foundation and waterproof concrete basin using **Waterfall / V-Model** (zero room for error, frozen engineering specs, rigorous water pressure verification).
    - You build the interior kitchen cabinets, living room layout, and smart lighting using **Agile Sprints** (iterative, homeowner selects countertops and paint colors after seeing the sunlight in the room).
  No smart contractor uses one single rigid methodology for every part of the build!

- **Say (Key Talking Points):**
  - **Agile SDLC Overview**:
    - In 2001, 17 software pioneers met in Snowbird, Utah to forge common ground against heavyweight bureaucratic processes, signing the **Agile Manifesto**.
    - Key operational traits: Speed up or bypass formal lifecycle phases, reduce unnecessary scope, focus on time-critical delivery, and empower cross-functional teams.
  - **Specific Agile Frameworks**:
    1. **Adaptive Software Development (ASD)**: Continuous cycle of Speculate $\rightarrow$ Collaborate $\rightarrow$ Learn; designed for rapidly changing environments.
    2. **Feature Driven Development (FDD)**:
       - Highly structured, client-centric 5-step process:
         1. *Develop overall model* (class and sequence diagrams with chief architect and domain experts).
         2. *Build features list* (decomposed into Business Activities within Subject Areas; features sized under 2 weeks using the strict template: `<action> <result> <object>`, e.g., *"Calculate the total of a sale"*).
         3. *Plan by feature*.
         4. *Design by feature*.
         5. *Build by feature*.
    3. **Dynamic Systems Development Method (DSDM)**:
       - Formal framework for RAD and short time-frames governed by the **80/20 Pareto principle**: 80% of business value can be delivered with 20% of system complexity in a relatively short timeframe.
       - *Core Principles*: Active user involvement is imperative (**Ambassador Users** embedded with developers), teams empowered to make decisions, frequent delivery, fitness for business purpose, reversible changes, integrated testing.
       - *5-Phase Lifecycle*: Feasibility Study $\rightarrow$ Business Study (prioritized requirements) $\rightarrow$ Functional Model Iteration (risk & timebox plan) $\rightarrow$ Design and Build Iteration $\rightarrow$ Implementation.
    4. **Adaptive SDLC**: Combines RAD speed with software engineering discipline. Steps: Project initiation $\rightarrow$ Determine project time-box $\rightarrow$ Determine optimal cycles & time-box for each $\rightarrow$ Write cycle objective statements $\rightarrow$ Assign primary components $\rightarrow$ Develop task list $\rightarrow$ Review cycle success $\rightarrow$ Plan next cycle.
    5. **Other Agile Methods**:
       - *Crystal Clear*: Highly flexible, people-centric, lightweight communications.
       - *Extreme Programming (XP)*: The engineering engine of Agile (Pair Programming, Test-Driven Development [TDD], Continuous Integration, Refactoring).
       - *Rational Unified Process (RUP)*: Use-case driven, architecture-centric, iterative 4-phase framework (Inception, Elaboration, Construction, Transition).
  - **Tailored SDLC Models (The Modern Hybrid Standard)**:
    - **One model does not fit all projects**: If no single off-the-shelf methodology fits a project, choose a close model and customize it:
      - *Example 1*: A project has high risk, but full Spiral overhead is too costly $\rightarrow$ Start with Spiral, pare down non-critical reviews.
      - *Example 2*: A project must deliver frequent increments, but failure carries severe liability $\rightarrow$ Combine the **Incremental Model with the V-Shaped Model** (each increment is verified through rigorous V&V gates).
      - *Modern Enterprise Hybrid Standard*: Upfront Discovery, Architecture spikes, and regulatory compliance modeling $\longleftrightarrow$ executed via 2-week Scrum/Kanban sprints with continuous CI/CD automated gates.

- **The Master SDLC Comparison Matrix (Interview Reference)**:
  - **Waterfall**: Sequential phase-gates; frozen upfront requirements; involvement at beginning and end; risk of big-bang integration collapse; best for regulated medical, defense, avionics, ASICs.
  - **V-Model**: Parallel verification and validation; rigid specifications; customer signoff and UAT; slow to adapt to changes; best for safety-critical reliability systems.
  - **Prototyping**: User-facing discovery; evolving demo feedback; continuous co-design; risk of the Code-and-Fix trap; best for novel user interfaces, POCs, and MVPs.
  - **RAD**: Rapid time-boxing (WYSIWYG); moderately stable requirements; high customer involvement throughout; risk of never achieving closure; best for low-risk business tools and internal portals.
  - **Incremental**: Phased functional delivery; defined upfront, built in stages; customer evaluates each release; risk of poor architecture between increments; best for SaaS feature releases.
  - **Spiral**: Continuous risk reduction; complex emergent requirements; high customer involvement at every cycle; high complexity and overhead; best for breakthrough R&D and high-cost capital projects.
  - **Agile (Scrum)**: Empirical inspect and adapt; flexible prioritized backlog; weekly sprint feedback; risk of scope creep without strong PO; best for customer web/mobile apps and SaaS products.
  - **Tailored Hybrid**: Pragmatic risk and speed balance; tiered requirements (frozen core + agile UI); customer embedded throughout; best for enterprise banking, healthcare portals, and IoT.

- **Modern Enterprise Real-World Context**:
  - **FDD in Modern Software**: The `<action> <result> <object>` template matches modern software feature specifications: `"Calculate the total sales invoice"` or `"Validate user authentication credentials"`.
  - **DSDM in Modern Startups**: The 80/20 rule prevents over-engineering: build the 20% of features that 80% of users actually touch. Ambassador Users are modern **Design Partners / Beta Advisory Boards**.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a real-world Tailored Hybrid SDLC for a digital healthcare mobile app:
  1. **Phase 1 (Waterfall / V-Model Gate)**: HIPAA compliance rules, patient data privacy encryption specs, and medical regulatory validation tests are formally documented and frozen upfront.
  2. **Phase 2 (Agile Scrum Sprints)**: The mobile UI, doctor appointment scheduling screens, and notification reminders are built in bi-weekly sprints with continuous patient feedback.
  3. **Phase 3 (Continuous CI/CD Testing Gate)**: Every pull request automatically runs unit and integration test suites before automated deployment to staging.
  **Point out:**
  - Modern enterprise engineering avoids religious adherence to a single methodology.
  - Regulatory, safety, and security foundations use disciplined V-Model phase-gating.
  - Customer-facing interfaces and business workflows use adaptive Agile Scrum iterations.

- **Ask (Check Questions):**
  - Q: What is the standard template used in Feature Driven Development (FDD) to define a feature? — A: `<action> <result> <object>` (e.g. "Calculate the total of a sale").
  - Q: What does DSDM mean by the 80/20 rule, and who are Ambassador Users? — A: 80% of business requirements can be delivered in a short timeframe with 20% complexity; Ambassador Users are real business users embedded directly in development teams with decision-making power.
  - Q: Why do the majority of real-world enterprise software companies use a Tailored Hybrid SDLC rather than pure textbook Scrum or pure Waterfall? — A: Because enterprise software must balance upfront architectural planning, regulatory compliance, and security with the speed, adaptability, and frequent customer feedback of iterative sprints.

- **Done when:** Candidates can explain FDD, DSDM, Adaptive SDLC, and defend a tailored hybrid SDLC model using the comparison matrix.

---

## Exercise: SDLC Model Selection & Tailoring Workshop
**Scenario**: You are the Lead Systems Architect and Consulting Director. Review three enterprise client RFPs and defend your SDLC selection and tailoring strategy:
1. **Client A**: A medical robotics startup building automated insulin delivery pumps. A software crash or dosage calculation defect can be lethal.
2. **Client B**: A high-growth e-commerce retailer needing an AI-powered personalized gift recommendation engine live for Black Friday.
3. **Client C**: An enterprise insurance corporation replacing a 30-year-old COBOL mainframe claims system. Claims logic is fixed, but modern web interfaces and automated testing are required across 12 product lines.

## Done-Check
- [ ] Can name all 10 ALM roles and explain their modern evolution (SDET, DevOps/SRE, DevSecOps).
- [ ] Can draw and contrast Waterfall vs V-Model (Verification vs Validation).
- [ ] Can explain the 7 steps of Evolutionary Prototyping and the danger of the "Code-and-Fix" trap.
- [ ] Can describe RAD's 4 phases and explain time-boxing.
- [ ] Can explain the 4 quadrants of the risk-driven Spiral Model and how modern Spikes apply it.
- [ ] Can write an FDD feature using `<action> <result> <object>`.
- [ ] Can explain DSDM's 80/20 rule and the role of Ambassador Users.
- [ ] Can defend why and how to tailor an SDLC model for a real-world enterprise project using the comparison matrix.

---

## Post-Class Practice & Dynamic Interview Preparation
When reviewing this module after class or preparing for technical interviews, use your AI practice coach to dynamically generate fresh, real-world SDLC and ALM governance scenarios:
- In chat, type: **`interview questions on module 2`** or **`give me an SDLC governance interview challenge`**.
- The AI coach dynamically generates random, interview-grade scenarios (regulated compliance, shift-left testing, prototyping vs technical debt, risk-driven spikes) and evaluates your strategy in real time.
