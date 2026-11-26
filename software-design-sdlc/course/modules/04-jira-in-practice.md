# Module 4 — Jira in Practice: Agile Project Execution

Teach-skill content file. Format is described in `.claude/skills/teach-sdlc-class/SKILL.md`.  
Story Anchor: **Building a House** (The Digital Jobsite Board: Epics, Subcontractor Work Orders, Sprints & Burndown Tracking).  

## Objectives
By the end of this module, candidates can:
1. Explain Jira's core purpose, enterprise architecture, and deployment setup (Jira Cloud vs Jira Data Center).
2. Configure Admin credentials, user roles (Tester, Developer, PM), and create Agile projects (Scrum vs Kanban).
3. Master the Jira issue hierarchy and types: Epic $\rightarrow$ User Story $\rightarrow$ Task / Subtask $\rightarrow$ Bug.
4. Manage and groom the Product Backlog, assign story points, and establish a Sprint Backlog.
5. Create, configure, and launch a time-boxed Sprint (1–4 weeks) with a defined Sprint Goal.
6. Conduct a Daily Standup on the Active Sprint Board, updating ticket statuses across custom workflows.
7. Analyze and interpret Agile reports: Burndown charts, Velocity charts, Cumulative Flow Diagrams (CFDs), and Dashboards.

---

### Beat 4.1 — Introduction to Jira & Deployment Setup (Cloud-First Architecture)

- **Story Anchor (Building a House):**
  On a large jobsite with 40 subcontractors (framers, roofers, plumbers, electricians), you can't manage work with sticky notes on the back of a truck. The general contractor installs a digital jobsite whiteboard in the construction trailer. Every worker taps their badge, sees their tasks for the morning, marks when inspections pass, and the contractor instantly sees whether the foundation framing is on schedule. In software engineering, **Jira** is that centralized digital jobsite.

- **Say (Key Talking Points):**
  - **What is Jira?**: Developed by Atlassian, Jira is the world's leading project management and issue-tracking software. It provides a centralized platform for planning, tracking, managing, and reporting on agile software delivery.
  - **Why Use Jira?**:
    - *Agile Project Management*: Native support for both Scrum (sprint-based) and Kanban (continuous flow) frameworks.
    - *Custom Workflows*: Tailor lifecycle statuses and transitions for different teams and projects.
    - *Issue Tracking*: Granular tracking of epics, stories, tasks, subtasks, and bugs in one place.
    - *Reports & Dashboards*: Real-time visibility into team velocity, sprint burndown, and bottlenecks.
    - *Traceability*: Connects directly to Git repositories (GitHub, Bitbucket, GitLab) to link commits and pull requests to tickets.
  - **Jira Setup Models (Enterprise Architecture)**:
    - **Jira Cloud (Modern Standard)**: Atlassian-managed multi-tenant SaaS. Instant browser provisioning, automatic weekly feature updates, zero server patch maintenance, and native Atlassian Cloud integrations (Bitbucket, Confluence).
    - **Jira Data Center (Enterprise On-Premises)**: Self-managed multi-node clustered architecture deployed on enterprise virtual private clouds (AWS/Azure) for heavily regulated compliance environments requiring custom data residency.
  - **Account Setup & Free Cloud Tier Provisioning**:
    - Sign up at `https://www.atlassian.com/software/jira/free` (100% free for up to 10 users, no credit card needed).
    - Choose a site name: `https://<your-subdomain>.atlassian.net`.
    - Create a Scrum project with key `HOUSE` (Smart House Construction & Management).
    - **Configure the `In Review` Column**: Jira's default Scrum board ships with `To Do`, `In Progress`, and `Done`. In **Board settings** (or `+ Create column` on the **Board**), add an **`In Review`** column/status between `In Progress` and `Done`.
    - In Jira Cloud, navigate to **Project Settings > Access / People** to assign team roles:
      - *Project Manager / Product Owner*: Backlog prioritization, release versioning, and sprint lifecycle control.
      - *Developer*: Code implementation, branch creation, ticket movement from In Progress to In Review.
      - *Tester (QA)*: Defect authoring, acceptance criteria verification, and signoff to Done.
  - **Using the Live Jira Dashboard (No Local HTML Files)**:
    - In the top bar, click **Dashboards > Create Dashboard**.
    - Add real reporting gadgets: **Sprint Health**, **Sprint Burndown**, and **Assigned to Me**.
    - This gives candidates a production-grade live dashboard URL (`https://<domain>.atlassian.net/jira/dashboards`) to showcase in technical interviews.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Open Jira Cloud in the web browser and walk through workspace navigation:
  1. Access the Atlassian home dashboard (`https://<domain>.atlassian.net`) and select **Jira Software**.
  2. Create a new Software Development project using the **Scrum** template.
  3. Navigate to **Project Settings > People** and invite team members, mapping each to Developer, Tester, or Product Owner roles.
  **Point out:**
  - Notice that Jira Cloud requires zero local command line installation or container management; it is a turnkey SaaS product.
  - Role permissions ensure that developers cannot arbitrarily change sprint dates and QA controls sign-off transitions.
  - The project template automatically provisions a Scrum Backlog, Active Sprint Board, and Agile Reports.

- **Ask (Check Questions):**
  - Q: Why do the vast majority of modern engineering organizations choose Jira Cloud over self-hosted deployments? — A: Jira Cloud is a turnkey SaaS platform with zero server patching, automated uptime, instant browser access, and direct integration with cloud Git repositories.
  - Q: Why is configuring distinct project roles (Developer, QA Tester, PO) important in Jira? — A: To enforce workflow permission schemes (e.g. only QA or PO can transition tickets to Done) and assign appropriate access boundaries.

- **Done when:** Candidates can define Jira's purpose, compare Cloud vs Data Center setup, and explain role configuration.

---

### Beat 4.2 — Jira Issue Types & Hierarchy (Epic, Story, Task, Subtask, Bug)

- **Story Anchor (Building a House):**
  Look at how work is broken down on a construction site:
  1. **Epic**: "Construct the Kitchen & Dining Wing" (Takes 6 weeks, multiple trades).
  2. **Story**: "As a homeowner, I want hot running water in the kitchen sink so that I can wash dishes." (Valuable end-user slice).
  3. **Task**: "Deliver 100 feet of copper PEX piping to jobsite." (Technical chore).
  4. **Subtask**: "Rough-in pipe manifold behind wall" (Assigned to Plumber A) and "Pressure-test water line at 60 PSI" (Assigned to Inspector B).
  5. **Bug**: "Sink shutoff valve drips when hot water is active." (Defect in working software).

- **Say (Key Talking Points):**
  - **The 5 Core Issue Types & Concrete Examples**:
    1. **Epic**: A large body of strategic work that can be broken down into smaller tasks and user stories, typically spanning multiple sprints.
       - *Example*: *"Build a User Management System"* or *"Construct House Climate Control Infrastructure"*.
    2. **Story**: A user-focused feature or requirement representing a vertical slice of end-user functionality.
       - *Example*: *"As a user, I want to log in using my credentials so that I can access my account."*
       - *Attributes*: Summary, Description, Acceptance Criteria, Story Points (e.g. 5 points).
    3. **Task**: A general technical work item, often unrelated to direct user-facing stories.
       - *Example*: *"Set up the database schema"* or *"Configure Nginx reverse proxy SSL certificate"*.
    4. **Subtask**: A granular, detailed piece of work within a parent issue (Story or Task) to distribute labor between developers and QA testers.
       - *Development Subtask*: *"Implement Login API endpoint"* or *"Write unit tests for the login API"*.
       - *QA Subtask*: *"Test Login Functionality & edge cases on mobile"*.
    5. **Bug**: A defect, error, or regression in the product that deviates from acceptance criteria.
       - *Example*: *"Login button is not responsive on mobile browsers"* or *"Door lock timeout returns 500 error"*.
  - **Hierarchy Rule**: Subtasks must always roll up to a parent Story or Task; Stories and Tasks roll up into an Epic.

- **Demo / Jira Board Hierarchy (run: instructor):**
  Open the project backlog in Jira Cloud:
  - Expand Epic **"Foundation & Structural Architecture"** (note: Jira assigns sequential numeric keys like `HOUSE-1`, `HOUSE-2` in creation order).
  - Show child User Story **"Poured Concrete Foundation with Rebar"**.
  - Expand that User Story to show its two decomposed subtasks:
    1. Dev Subtask: "Dig trenches and lay grade rebar grid"
    2. QA Subtask: "Perform pre-pour building code inspection"
  **Point out:**
  - Stories belong to Epics; Subtasks belong to Stories.
  - Subtasks cannot exist independently—they represent the distinct cross-functional steps required to satisfy the parent story's Definition of Done.

- **Ask (Check Questions):**
  - Q: What is the relationship between an Epic and a User Story? — A: An Epic is a large body of work spanning multiple sprints that is decomposed into smaller, estimable User Stories.
  - Q: Give an example of how a Story is divided into Dev and QA subtasks. — A: Story: "User Login"; Dev Subtask: "Implement user authentication in backend logic"; QA Subtask: "Verify invalid password error handling".

- **Done when:** Candidates can categorize any engineering item into Epic, Story, Task, Subtask, or Bug.

---

### Beat 4.3 — Backlog Grooming, Sprint Creation & Goals

- **Story Anchor (Building a House):**
  Before the framing crew arrives on Monday morning, the general contractor cleans up the jobsite materials list: they throw away obsolete requests, estimate how many bundles of 2x4 lumber are needed, and pull the exact materials into the staging trailer. That is **Backlog Grooming** and **Sprint Planning**.

- **Say (Key Talking Points):**
  - **Product Backlog vs Sprint Backlog**:
    - *Product Backlog*: The master repository of all user stories, technical tasks, epics, and bugs for the entire project. Maintained and prioritized exclusively by the Product Owner.
    - *Sprint Backlog*: The prioritized subset of the product backlog selected for the current sprint, based on team velocity and sprint goals.
  - **Backlog Refinement (Grooming)**:
    - Ongoing team collaboration to review upcoming backlog items, clarify acceptance criteria, break large stories into smaller ones, and assign story points.
  - **Step-by-Step: Creating a Sprint in Jira**:
    1. Navigate to the **Backlog view** in your Jira project.
    2. Click **Create Sprint** (Jira labels it e.g. "Sprint 1").
    3. Drag estimated user stories from the Product Backlog container into the newly created Sprint area.
    4. Click **Start Sprint** and configure:
       - **Duration**: Fixed time-box (typically 1 to 4 weeks; 2 weeks is industry standard).
       - **Start and End Dates**: Set official timeline.
       - **Sprint Goal**: A clear, goal-oriented business objective (e.g., *"Complete user authentication module and biometric door lock"*).
       - Click **Start Sprint**.
  - **The 4 Key Elements of a Sprint**:
    1. *Time-Boxed*: Fixed duration (usually 1–4 weeks), never extended if work falls behind.
    2. *Goal-Oriented*: Focused on delivering a specific, cohesive increment of value.
    3. *Team Collaboration*: Developers, testers, and stakeholders working together daily.
    4. *Review and Feedback*: Concludes with a Sprint Review and Sprint Retrospective for continuous improvement.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through Backlog Grooming and launching Sprint 1 in Jira Cloud:
  1. Navigate to the **Backlog view** in your Jira project.
  2. Review 4 unestimated candidate user stories with the team, confirming each story has clear acceptance criteria.
  3. Assign Fibonacci story points (3, 5, 8) to each story during backlog grooming.
  4. Click **Create Sprint**, drag the top 3 stories into the sprint container, and click **Start Sprint**.
  5. Set duration to 2 weeks and enter the Sprint Goal: *"Complete resident authentication API and biometric door lock integration"*.
  **Point out:**
  - Stories without acceptance criteria or estimates should remain in the backlog until refined (Definition of Ready).
  - The Sprint Goal provides a North Star for the team to make trade-offs if unforeseen obstacles emerge during the 2 weeks.
  - Once started, the sprint backlog items immediately populate the Active Sprint Board.

- **Ask (Check Questions):**
  - Q: Who manages the Product Backlog, and how does it differ from the Sprint Backlog? — A: The Product Owner manages the Product Backlog (all project features); the Sprint Backlog is the subset committed by the team for the active sprint.
  - Q: Why should every sprint have an explicit Sprint Goal? — A: A Sprint Goal gives the team a unified focus, guiding trade-offs if scope adjustments are required during the sprint.

- **Done when:** Candidates can explain backlog grooming, sprint duration, and how to create a sprint with a goal.

---

### Beat 4.4 — The Active Sprint Board, Daily Standups & Workflows

- **Story Anchor (Building a House):**
  At 7:30 AM every morning, all subcontractors gather around the jobsite board in the trailer. 
  - Plumber says: *"Yesterday I ran the PEX lines. Today I'm pressure testing. Blocker: The city water main shutoff is locked."*
  - The contractor immediately steps in to get the city key. Cards physically move from "In Progress" to "Passed Inspection."

- **Say (Key Talking Points):**
  - **The Active Sprint Board**:
    - Displays committed sprint issues as cards across workflow columns.
    - Team members drag-and-drop cards across columns as work progresses.
  - **Custom Workflow Statuses & Transitions**:
    - JIRA issues follow a defined workflow with statuses and transitions:
      1. `To Do`: Work not yet started.
      2. `In Progress`: Work is actively being coded or engineered.
      3. `In Review / QA`: Task is being peer-reviewed or undergoing QA test verification.
      4. `Done`: Work is 100% complete, meeting the Definition of Done (DoD).
    - Workflows can be customized with transition rules (e.g. requiring code review approval before moving to QA).
  - **Conducting the 15-Minute Daily Standup**:
    - Strictly time-boxed meeting where team members sync on progress.
    - Walk the board from right to left (focus on cards closest to Done first!).
    - **The 3 Core Questions with Role Walkthroughs**:
      - *QA Tester*: *"Yesterday, I tested the login page. Today, I’ll test logout functionality and edge cases. No blockers."*
      - *Developer*: *"Yesterday, I implemented the lock API. Today, I’ll debug an authentication issue. Blocker: waiting on test database credentials."*
      - *Project Manager / Scrum Master*: *"Monitoring sprint progress, clearing the database credentials blocker, and coordinating with stakeholders."*

- **Demo / Active Board Transitions (run: instructor):**
  Open the active Scrum board in Jira Cloud:
  - Drag the **"Dual-Zone PEX Plumbing"** story card from `In Progress` to `In Review`.
  - Open the ticket to assign the QA Engineer and attach the 60-PSI pressure test report.
  **Point out:**
  - The ticket cannot jump directly from In Progress to Done—it must be peer-reviewed and tested by QA.
  - This preserves the Definition of Done (DoD) gatekeeper role on the board.

- **Ask (Check Questions):**
  - Q: What are the 4 common statuses in a standard Jira agile workflow? — A: To Do, In Progress, In Review, and Done.
  - Q: If a developer completes their code on Monday, why shouldn't they immediately move the ticket to "Done"? — A: It must transition to "In Review" or "QA" to be verified against the Definition of Done before being marked complete.

- **Done when:** Candidates can explain active board columns, workflow transitions, and daily standup execution.

---

### Beat 4.5 — Agile Tracking & Reporting (Burndown, Velocity, CFD & Dashboards)

- **Story Anchor (Building a House):**
  If your construction crew committed to framing 20 rooms in 2 weeks, you track daily progress on a chart. If by Day 7 you have framed zero rooms, your line is completely flat! The contractor knows immediately that lumber was delayed or framing crews didn't show up. You don't wait until Day 14 to discover you're behind schedule!

- **Say (Key Talking Points):**
  - **Tracking Progress in Jira**:
    1. **Burndown Chart**:
       - Tracks work completed vs remaining work (story points) over the sprint timeline.
       - *Ideal Guideline*: A diagonal line burning down to zero on the final day.
       - *Flat Line*: Reveals hidden blockers, delayed reviews, or oversized stories.
       - *Spike Upward*: Indicates scope creep (new stories injected into an active sprint).
    2. **Velocity Chart**:
       - Measures the team's historical productivity by comparing committed vs completed story points across past sprints.
       - Essential for reliable sprint capacity planning.
    3. **Sprint Report**:
       - Comprehensive post-sprint summary showing stories completed, incomplete stories pushed back to the backlog, and any issues added after sprint start.
    4. **Cumulative Flow Diagram (CFD)**:
       - Visualizes the total number of work items across all workflow stages over time.
       - A widening band indicates an emerging bottleneck in that stage (e.g. widening "In Review" band means QA is overloaded).
    5. **Custom Dashboards**:
       - Centralized visibility for teams and executive stakeholders.
       - Configurable widgets: Burndown gadgets, Assigned to Me filters, Pie charts by issue type, and sprint health summaries.

- **Demo / Burndown & Velocity Reports (run: instructor):**
  Navigate to **Reports -> Burndown Chart** in Jira Cloud:
  **Point out:**
  - X-axis represents the working days in the 2-week sprint; Y-axis represents remaining story points.
  - The gray guideline indicates the ideal burndown rate.
  - The red/green actual line shows day-to-day progress.
  - A flat line indicates blocked tickets or team multitasking; a sharp drop at the end indicates batch-testing anti-patterns.

- **Ask (Check Questions):**
  - Q: What does a widening band in a Cumulative Flow Diagram (CFD) indicate? — A: A bottleneck in that specific workflow stage (e.g. tickets accumulating faster than they are being processed).
  - Q: If a Burndown Chart shows an unexpected vertical jump on Day 4, what happened? — A: Scope was added to the sprint after it started.
  - Q: How does a Velocity Chart help a team during Sprint Planning? — A: It provides empirical evidence of the team's average completed story points per sprint, preventing over-commitment.

- **Done when:** Candidates can read a Burndown chart, explain Velocity, and describe Jira Dashboards.

---

## Exercise: Hands-On Jira Construction Board
1. **Create Your Epics & Starter Story** (if not already created):
   - In **Backlog** (or **Timeline**), create the 3 Epics: **Foundation & Structural Architecture**, **Plumbing, Electrical & Utility Tiers**, and **Smart Home Automation & IoT Security**.
   - Ensure your **Board** has the `In Review` column between `In Progress` and `Done`.
2. **Author a New Story**: In the **Backlog**, click **Create Issue**:
   - Issue Type: Story
   - Summary: *"Smart Water Meter Leak Detection"*
   - Description: *"As a homeowner, I want real-time pipe leak alerts so that water damage is prevented."* (plus Given-When-Then acceptance criteria)
   - Story Points: 3
   - **Parent**: Epic **Smart Home Automation & IoT Security**
3. **Start a Sprint & Advance a Story**:
   - Click **Create sprint**, drag your story into **Sprint 1**, set a **Sprint Goal**, and click **Start sprint**.
   - Open the **Board**, move your story to `In Progress`, and assign it to yourself.
4. **Inspect the Metrics**: Check **Reports** (Sprint Burndown) or your **Dashboard** to observe how the active sprint health and remaining work appear.

## Done-Check
- [ ] Understands Jira's core purpose, deployment options (Cloud-First SaaS vs Data Center), and role setup.
- [ ] Understands the 5 Jira issue types (Epic, Story, Task, Subtask, Bug) with real examples.
- [ ] Knows how to groom a backlog, set sprint duration, and define a Sprint Goal.
- [ ] Can navigate an active sprint board and manage workflow transitions.
- [ ] Can interpret a Burndown chart, Velocity chart, and Cumulative Flow Diagram.

---

## Post-Class Practice & Dynamic Interview Preparation
When reviewing this module after class or preparing for technical interviews, use your AI practice coach to dynamically generate fresh, real-world Jira project execution scenarios:
- In chat, type: **`interview questions on module 4`** or **`give me a jira management interview challenge`**.
- The AI coach dynamically generates random, interview-grade scenarios (issue hierarchy decomposition, burndown anti-patterns, workflow validators, velocity forecasting) and evaluates your practical execution in real time.
