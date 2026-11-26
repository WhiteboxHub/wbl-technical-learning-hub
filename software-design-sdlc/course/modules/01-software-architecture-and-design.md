# Module 1 — Software Architecture & System Design

Teach-skill content file. Format is described in `.claude/skills/teach-sdlc-class/SKILL.md`.  
Story Anchor: **Building a House** (Blueprints, Foundations, Load-Bearing Walls, In-Wall Utilities & Modular Outlets).  

## Objectives
By the end of this module, candidates can:
1. Articulate the Client-Server model, the request-response lifecycle, and connection states.
2. Design and explain linear 3-Tier and N-Tier architectures, contrasting them with MVC.
3. Explain distributed computing challenges: network latency, partial failures, and tight vs loose coupling.
4. Distinguish specialized architectural patterns: Batch-Sequential vs Pipes & Filters, Peer-to-Peer (P2P), Plugin Architecture, and Search-Oriented Architecture.
5. Accurately categorize cloud computing models: Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS).
6. Contrast **Monolithic** vs **Microservices Architecture** (bounded contexts, database-per-service, API Gateway, sync vs async communication, and when to start with a modular monolith).

---

### Beat 1.1 — Client-Server Model: The Request-Response Foundation

- **Story Anchor (Building a House):**
  Imagine you are in your kitchen and you turn on the water tap. You (the homeowner) are the **Client** initiating a demand for water. The municipal water pumping station miles away is the **Server**—it runs 24 hours a day, 7 days a week, waiting passively under pressure. The water pipe is the **Network Connection**. The server does not randomly push water into your living room unannounced; it only responds when you open the valve. In software, clients ask; servers listen and answer.

- **Say (Key Talking Points):**
  - **The Asymmetric Relationship**: Client-Server is a distributed computing paradigm dividing workloads between service requesters (**Clients**) and service providers (**Servers**). Communication is always initiated by the client.
  - **Server Lifecycle & Availability**: A server is an always-on daemon bound to a well-known network IP and Port (e.g., standard HTTP Port 80, HTTPS Port 443). It passively listens in the background for incoming client connection requests.
  - **Statelessness**: In standard HTTP client-server architecture, each request is completely independent. The server retains no memory of previous requests unless explicit session state or security tokens (like JWTs) are passed in the headers.
  - **Enterprise Examples**: Web browsers requesting web pages from cloud servers, mobile apps querying backend application services, application services querying a centralized database.
  - **Multi-Role Nodes**: A single computer or program can act as both client and server simultaneously. For example, a backend application server acts as a *server* to the frontend browser, but acts as a *client* when making database queries to PostgreSQL.

- **Demo / Conceptual Trace (run: instructor):**
  Trace the conceptual client-server exchange between a resident's mobile app and backend services:
  - **Client Request**:
    The mobile client initiates the connection, sending an action, destination host, authentication token, and requested format.
  - **Server Response**:
    The backend server verifies permissions, queries the database, and returns a success status with the user profile payload in JSON format.
  **Point out:**
  - Notice that communication is strictly client-initiated; the server does not push unsolicited data in basic client-server protocols.
  - The server daemon waits passively on its listening port until the client initiates the connection.

- **Ask (Check Questions):**
  - Q: In a client-server architecture, can a server initiate a standard HTTP response without a client request? — A: No; in standard client-server protocols, the client must initiate the request. (Note: WebSockets or Webhooks create two-way or reverse client-server connections).
  - Q: Why is a database like PostgreSQL considered a server? Who are its clients? — A: PostgreSQL runs continuously listening on port 5432 waiting for SQL queries; its clients are backend application services and DBA tools.

- **Done when:** Candidates can explain the Client-Server relationship in their own words and state who initiates the connection.

---

### Beat 1.2 — Three-Tier & N-Tier Architecture vs MVC

- **Story Anchor (Building a House):**
  Think about how a modern house is plumbed and wired. 
  - **Tier 1 (Presentation Tier)**: The kitchen faucet, light switches, and dimmer knobs that you touch.
  - **Tier 2 (Logic / Application Tier)**: The behind-the-drywall plumbing manifold, water heater thermostat, and circuit breaker panel. This tier enforces rules: it prevents water from exceeding 120°F and trips the breaker if an overload occurs.
  - **Tier 3 (Data Tier)**: The underground high-voltage electrical grid and municipal water reservoir.
  *Why keep them separate?* If you want to replace your kitchen faucet with a modern gold finish (Presentation change), you shouldn't have to rebuild the city water reservoir (Database)! And more importantly, you never connect your kitchen sink directly to high-voltage power lines—the Logic tier protects the Data tier.

- **Say (Key Talking Points):**
  - **Definition of 3-Tier Architecture**: Physical and logical separation of a software system into three independent layers:
    1. **Presentation Tier (Client/UI)**: Mobile app, browser frontend, or CLI client. Displays information and captures user input.
    2. **Application / Business Logic Tier (Server/API)**: Backend application services and microservices. Enforces business rules, data validation, access permissions, calculations, and orchestrates workflows.
    3. **Data Tier (Persistence)**: Relational databases (PostgreSQL), NoSQL, or data warehouses. Persists raw structured records.
  - **3-Tier vs N-Tier Expansion**:
    - *3-Tier*: The foundational baseline (Presentation, Logic, Data).
    - *N-Tier*: In enterprise systems, the middle tier expands into $N$ specialized, decoupled layers: an **API Gateway Tier** (routing/rate limiting), a **Caching Tier** (Redis for high-speed in-memory reads), a **Messaging/Queueing Tier** (RabbitMQ/Kafka for asynchronous task decoupling), and an **Identity/Auth Tier** (OAuth2/SSO).
  - **Strict Linear Flow**: 3-Tier architecture is strictly **linear**: `Presentation <---> Application Logic <---> Data`. The Presentation Tier is **NEVER** permitted to communicate directly with the Data Tier!
  - **Why Direct DB Access from Clients is Catastrophic**: Exposing database credentials in frontend JavaScript, inability to enforce business validation, SQL injection vulnerability, and total loss of access control.
  - **3-Tier vs MVC**: MVC (Model-View-Controller) is an internal software design pattern often operating *within* a single tier (e.g. View and Controller inside a frontend or monolithic app, forming a triangle). 3-Tier represents a physical network and process boundary separation.
  - **Benefits**: Modular maintainability, independent horizontal scaling (scale API servers without scaling DB), security isolation, and permission boundaries.

- **Demo / Architectural Boundary Trace (run: instructor):**
  Walk through the physical and logical decoupling of the 3-Tier model:
  1. **Presentation Tier (Client UI)**: Mobile app (iOS/Android) or Web frontend. Communicates strictly over HTTPS/REST with the Application Tier. Holds zero database credentials.
  2. **Application / Business Logic Tier (Server API)**: Application microservices. Validates inputs, authenticates tokens, evaluates business rules, and initiates queries to the Data Tier.
  3. **Data Tier (Persistence)**: Relational database (PostgreSQL). Resides on an isolated private subnet, accessible exclusively by the Application Tier.
  **Point out:**
  - The communication flow is strictly linear: `Presentation <-> Logic <-> Data`.
  - Direct client-to-database connections violate security boundaries: they expose credentials in client bundles, allow raw SQL injection, and bypass all business validation.

- **Ask (Check Questions):**
  - Q: Why is 3-Tier architecture described as linear rather than triangular like MVC? — A: Because the Presentation Tier must pass through the Application Logic Tier to access data; it can never bypass the middle layer.
  - Q: If traffic suddenly spikes by 10x on the resident mobile app, how does 3-Tier architecture help? — A: You can scale up multiple instances of the Application Logic API behind a load balancer without needing to duplicate the entire database layer.

- **Done when:** Candidates can draw a 3-Tier diagram, explain what belongs in each tier, and justify why UI clients must never connect directly to databases.

---

### Beat 1.3 — Distributed Computing & Coupling

- **Story Anchor (Building a House):**
  Imagine building a house where the refrigerator, stove, and light bulbs are all hard-soldered into one giant block of copper wire. If the refrigerator compressor burns out, the entire house goes pitch black! That is **Tight Coupling**.
  In a modern house, we use standard wall outlets. The refrigerator plugs in; if it breaks, you unplug it and your living room lights keep working. That is **Loose Coupling**. 
  In distributed computing, our software runs on different machines across networks. If one service slows down or reboots, loosely coupled systems keep the rest of the house running.

- **Say (Key Talking Points):**
  - **What is Distributed Computing?**: A collection of autonomous computational systems connected through network links that coordinate by passing messages.
  - **The Fallacies of Distributed Computing**:
    1. The network is reliable (it isn't—packets drop).
    2. Latency is zero (network calls take milliseconds; memory takes nanoseconds).
    3. Bandwidth is infinite.
    4. The network is secure.
  - **Tight Coupling vs Loose Coupling**:
    - *Tight Coupling*: Components require intimate knowledge of each other’s internal implementations and memory spaces. If Service A crashes, Service B immediately crashes.
    - *Loose Coupling*: Components interact via standardized contracts (REST APIs, JSON schemas, message queues). Service B can handle Service A being temporarily offline via retries and fallbacks.
  - **Heterogeneous Environments**: In real enterprises, distributed systems run across different operating systems (Linux servers, iOS mobile devices, Windows desktops) using different languages (Python, Go, JavaScript) unified by standard network protocols.
  - **Shared Data & Distributed Coordination Patterns**:
    - In distributed architectures, communication and coordination between parallel processes typically fall into proven patterns:
      1. *Shared Relational Database*: Multiple distributed workers or backend services coordinate and communicate by reading and writing to a shared relational database.
      2. *Stored Procedures on Database Servers*: Business logic and validation routines precompiled and executed directly inside the database engine to minimize network round-trips for high-throughput batch operations.
      3. *Dynamic Table-Driven Logic*: Routing rules, permissions, and configuration stored dynamically in database tables rather than hardcoded in application code, allowing behavior changes without rebuilding or redeploying code.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through a distributed network boundary and simulated database downtime:
  1. A client app sends a telemetry payload to the API server over HTTPS.
  2. The database connection drops due to network partition or DB failover.
  3. Instead of crashing the entire system (tight coupling), the API catches the timeout and returns `HTTP 503 Service Unavailable` with a structured JSON retry contract (`{"retry_after": 15}`).
  **Point out:**
  - Notice that the client and server do not share memory; they communicate across network boundaries via contracts.
  - In a tightly coupled system, the API process would freeze and terminate abruptly.
  - In a loosely coupled system, components degrade gracefully and isolate failures.

- **Ask (Check Questions):**
  - Q: What is the main danger of tight coupling in a distributed system? — A: Cascading failures: a bug or outage in one component propagates and takes down the entire system.
  - Q: Name two unavoidable real-world network realities that distributed systems must handle. — A: Network latency (delays), packet loss/timeouts, and partial network partitions.

- **Done when:** Candidates can contrast tight vs loose coupling and explain why distributed systems require resilience.

---

### Beat 1.4 — Batch-Sequential Processing vs Pipes & Filters

- **Story Anchor (Building a House):**
  Think of two ways to haul construction debris away from a jobsite:
  - **Batch-Sequential**: You fill an entire 20-ton dumpster with drywall over 3 days. When completely full, the flatbed truck drives it to the landfill, dumps it, and drives back. Step 2 cannot begin until Step 1 is 100% finished.
  - **Pipes & Filters (Streaming)**: Workers place drywall scraps on a motorized conveyor belt that continuously rolls out the window and drops pieces into a moving wood chipper. The waste is processed concurrently in a continuous stream.
  In software, month-end utility billing is Batch-Sequential; real-time smart sensor alerts are Streaming/Pipes-and-Filters.

- **Say (Key Talking Points):**
  - **Batch-Sequential Processing**: An architectural style designed for high-volume, offline data operations. Data is collected into files or batches and processed in discrete, sequential stages:
    `Input Dataset -> Validation Stage -> Transformation/Processing -> Report Generation`.
  - **Subset of Data Flow Architectures**:
    - Both Batch-Sequential and Pipes-and-Filters belong to the broader family of **Data Flow Architectures** (systems where computation is driven by data flowing through a series of transformations).
    - *Key Difference*: **Pipes and Filters executes in parallel** (concurrent streaming between filters), whereas **Batch-Sequential does NOT execute in parallel** (each stage must run to completion, transform data, and write to a new file before the next stage can touch it).
  - **Strict Stage Boundaries**: Each stage in a batch-sequential architecture must run to completion and write its entire intermediate result before the subsequent stage can begin.
  - **Common Enterprise Use Cases**:
    - **Legacy Mainframe Systems**: High-throughput nightly financial batch jobs.
    - **Compilers**: Lexical analysis $\rightarrow$ Syntax parsing $\rightarrow$ Semantic analysis $\rightarrow$ Code generation.
    - **Compression Pipelines**: Multi-stage data compression (e.g. video encoding, gzip chunking) where raw streams are transformed through sequential compression algorithms.
    - **Utility Billing**: Nightly smart-meter energy consumption aggregation.
    - **Payroll**: End-of-month employee payroll processing.

- **Demo / Scenario Walkthrough (run: instructor):**
  Trace the 4 discrete offline stages of an enterprise utility billing batch run:
  1. `Stage 1 (Ingest)`: Read offline smart-meter telemetry records accumulated over 30 days.
  2. `Stage 2 (Validate)`: Filter out negative or corrupted sensor readings; quarantine invalid records.
  3. `Stage 3 (Transform & Aggregate)`: Calculate total kWh consumption per household and apply peak/off-peak rate formulas.
  4. `Stage 4 (Report & Emit)`: Generate finalized monthly invoice statements and ledger entries.
  **Point out:**
  - Stage 3 never touches raw input; it strictly operates on the validated intermediate output of Stage 2.
  - Unlike streaming, if Stage 2 fails, Stage 3 never begins, protecting downstream systems from dirty data.

- **Ask (Check Questions):**
  - Q: Why is Batch-Sequential processing generally unsuited for interactive user web applications? — A: Because users expect sub-second responses; batch processing runs offline over large datasets and takes minutes or hours.
  - Q: What happens if a batch-sequential job fails halfway through Stage 2? — A: Stage 3 never starts; the failure is isolated and the batch can be retried from the beginning of Stage 2.

- **Done when:** Candidates can describe the 4 stages of a batch pipeline (`Input -> Validate -> Process -> Report`) and contrast it with streaming.

---

### Beat 1.5 — Specialized Architectures: Peer-to-Peer, Plugin, and Search-Oriented

- **Story Anchor (Building a House):**
  - **Peer-to-Peer (P2P)**: A neighborhood block party where every homeowner brings a dish and shares tools. No single person owns the kitchen; everyone gives and takes equally.
  - **Plugin Architecture**: The modular electrical breaker panel or smart home hub. You can plug in a brand-new solar inverter or hot tub breaker module tomorrow without rewiring the home.
  - **Search-Oriented Architecture**: Instead of sorting through 500 paper building blueprints in filing cabinets, you install an instant digital barcode scanner that pulls up the exact plumbing schematic in 0.2 seconds.

- **Say (Key Talking Points):**
  - **Peer-to-Peer (P2P) Architecture**:
    - Equal nodes (peers) acting as both clients and servers simultaneously.
    - Instead of relying on a centralized server infrastructure, P2P harnesses the collective connectivity, bandwidth, computing power, and storage space of all participants in the network.
    - *Centralized Indexing vs Decentralized Discovery*: Some P2P networks employ a central coordination server solely to assist with peer lookups, while file transfers occur directly between peers.
    - *Super-Peers (Super-Nodes)*: Many enterprise P2P architectures leverage stronger nodes with higher bandwidth and uptime as super-peers; client-peers connect to a single super-peer in a star-like network topology.
  - **Plugin Architecture (Microkernel Extensible Pattern)**:
    - Designed specifically for extensible software where third parties or modules can add functionality dynamically without modifying or recompiling the core application.
    - *Enterprise Examples*:
      - **Notepad++**: Placing a compiled `.dll` file into the `plugins/` directory instantly injects new capabilities (e.g. hex editors, snippet insertion, color-pickers, syntax linters).
      - **Eclipse IDE Plug-in Architecture**: Modular OSGi bundles providing language servers, debuggers, and builders on top of a lean core runtime.
  - **Search-Oriented Software Architecture**:
    - The search engine (Elasticsearch, Meilisearch, Solr) acts as the **primary integration component of the architectural layer**, rather than traditional relational databases.
    - Replaces SQL query joins with high-performance keyword search over distributed inverted indices, delivering instant full-text retrieval, fuzzy search, and faceting over massive datasets.

- **Scenario Walkthrough / System Inspection (run: instructor):**
  Walk through the architectural trade-offs across 3 specialized systems:
  1. *BitTorrent (P2P with Super-Peers)*: A newly released 10GB game update is seeded by a few nodes; as 50,000 players download it, their machines immediately act as uploaders, multiplying aggregate network bandwidth.
  2. *Notepad++ / VS Code (Plugin Microkernel)*: The core editor binary is a lean 15MB executable; third parties build Python linters, Git lenses, and Markdown renderers as external modules loaded via standardized dynamic interfaces without touching core code.
  3. *Amazon / E-Commerce (Search-Oriented)*: A shopper searches "cordless drill under $100"; the query hits an Elasticsearch inverted index cluster in 15ms instead of executing an expensive multi-table `JOIN` with full-table scans across 20 million relational DB rows.
  **Point out:**
  - Notice how P2P eliminates the central bandwidth bottleneck.
  - Notice how Plugins isolate stability: a crashing third-party plugin cannot corrupt the microkernel.
  - Notice how Search-Oriented architectures offload query spikes from primary relational transactional ledgers.

- **Ask (Check Questions):**
  - Q: How do super-peers improve performance in a Peer-to-Peer network? — A: Stronger nodes with high bandwidth and uptime act as local indexing and proxy hubs, organizing edge client-peers into efficient star clusters.
  - Q: How does a Plugin architecture allow software to be extended without modifying its source code? — A: The core system exposes standardized interfaces and dynamic plugin directories (like `.dll` files in Notepad++ or OSGi in Eclipse) loaded at runtime.
  - Q: Why would an e-commerce site use a Search-Oriented architecture instead of querying PostgreSQL directly for product search? — A: Search engines use inverted indices optimized for instantaneous keyword search, ranking, and faceting across millions of records, offloading heavy search traffic from the relational database.

- **Done when:** Candidates can explain the architectural advantages of P2P, Plugin, and Search-Oriented designs.

---

### Beat 1.6 — Cloud Computing Service Models: IaaS, PaaS, and SaaS

- **Story Anchor (Building a House):**
  How do you want to live in a house?
  1. **IaaS (Infrastructure as a Service)**: You buy an empty, zoned piece of land with municipal water and electrical hookups. You must bring the foundation, framing, plumbing, drywall, furniture, and maintenance. *Maximum control, maximum work.*
  2. **PaaS (Platform as a Service)**: You rent an unfurnished apartment. The landlord built the foundation, walls, plumbing, and air conditioning. You bring your own furniture and move in. *Balanced control, lower maintenance.*
  3. **SaaS (Software as a Service)**: You check into a luxury hotel room. The bed is made, Wi-Fi is connected, breakfast is downstairs, and room service cleans up. You just walk in and live. *Zero maintenance, instant utility, fixed layout.*

- **Say (Key Talking Points):**
  - **Cloud Architecture Overview**: A paradigm for linking computational resources (applications, compute, storage, and networking) on demand over network links to achieve business outcomes for service consumers and other applications.
  - **The Shared Responsibility Model**: Responsibilities shift across the 3 layers:
  - **SaaS (Software as a Service)**:
    - Complete turnkey application delivered to end users directly through a web browser.
    - Increasingly popular with SMEs (Small & Medium Enterprises) because there is zero hardware or software to manage, install, or patch.
    - *Key Characteristics*: Pay-per-use subscription pricing, instant horizontal scalability, high built-in security and reliability, and integration via REST APIs.
    - *Enterprise Examples*: **Salesforce.com**, **emailcloud**, Jira Cloud, Google Workspace, Slack.
  - **PaaS (Platform as a Service)**:
    - Provides pre-configured development and deployment environments (managed runtime, execution engine, managed database, automated scaling).
    - Why PaaS? Building and maintaining custom infrastructure is expensive, estimating traffic demand is not an exact science, and operating system / middleware patch management consumes massive engineering cycles.
    - *Key Services Delivered*: Managed storage, automated relational/NoSQL databases, load balancing, and runtime scaling.
    - *Enterprise Examples*: **Google App Engine**, **Mosso**, **AWS S3** (managed object storage platform), AWS Elastic Beanstalk, Heroku.
  - **IaaS (Infrastructure as a Service)**:
    - Delivers raw, virtualized computing resources over the internet.
    - *Access Provided*: Full operating system (OS) root/administrator access, customizable virtual firewalls, network routers, and software-defined load balancers.
    - *Enterprise Examples*: **AWS EC2**, **Flexiscale**, Google Cloud Compute Engine, Microsoft Azure VMs.

- **Live Demo / Scenario Walkthrough (run: instructor):**
  Walk through the three cloud deployment tiers using the Smart House enterprise platform:
  1. **IaaS Layer**: An AWS EC2 virtual server running Ubuntu Linux with custom firewall rules and private subnets where the backend team manages OS patches and network routing.
  2. **PaaS Layer**: An AWS RDS managed database and S3 bucket where cloud engineers store resident documents without ever patching the underlying database engine or disk hardware.
  3. **SaaS Layer**: Jira Cloud where the software development team logs tickets, tracks sprints, and reviews velocity reports completely inside the web browser.
  **Point out:**
  - In IaaS, you have root access and own everything from the operating system up.
  - In PaaS, the cloud provider manages the OS, runtime, and hardware; you own only your code and data.
  - In SaaS, the provider manages the entire stack; you consume the application as an end-user service.

- **Ask (Check Questions):**
  - Q: Why is SaaS particularly popular with Small and Medium Enterprises (SMEs)? — A: No hardware or software to manage, pay-per-use subscription pricing, instant scalability, and zero server maintenance overhead.
  - Q: What level of control does an engineer receive with IaaS compared to PaaS? — A: IaaS grants full root OS access, virtual firewall, and router control; PaaS manages the OS and runtime, letting the engineer focus purely on code and data.
  - Q: Where does Jira Cloud fit in the cloud service hierarchy? What about AWS EC2 and AWS S3? — A: Jira Cloud is SaaS (turnkey browser app); AWS EC2 is IaaS (raw compute with full OS control); AWS S3 is PaaS (managed storage platform).

- **Done when:** Candidates can accurately categorize any cloud tool or provider into IaaS, PaaS, or SaaS using the housing analogy.

---

### Beat 1.7 — Monolithic vs Microservices Architecture

- **Story Anchor (Building a House):**
  Compare two ways to build a growing smart-home community:
  - **Monolith**: One giant 40-room mansion sharing a single main breaker panel, one water heater, and one shared kitchen. It is fast and simple to build at first, but if a pipe bursts in the guest wing, you may have to shut off water to the whole mansion—and 50 contractors trip over each other in the same hallway.
  - **Microservices**: A planned neighborhood of specialized, self-contained units—a Security Gatehouse (Auth/Gateway), a Smart Lock Service, a Billing Service, and a Telemetry Service. Each unit has its **own utility meter and private storage room (Database-per-Service)**, communicates through a **central street/intercom (API Gateway & Event Bus)**, and can be renovated or scaled independently without shutting down the neighborhood.

- **Say (Key Talking Points):**
  - **Monolithic Architecture**: Single deployable unit containing Presentation, Business Logic, and Data Access together. Simple to develop, test, and deploy early on ("Monolith-First" is often right for small teams), but scales only as a whole and couples release cycles.
  - **Microservices Architecture**: Decomposes a system into small, independently deployable services organized around **Business Capabilities / Bounded Contexts** (e.g., Residents, Billing, Smart Locks, Telemetry).
  - **Core Microservices Principles**:
    1. **Single Responsibility & Bounded Context**: Each service owns one domain capability.
    2. **Database-per-Service (No Shared DB Anti-Pattern)**: Service A must NEVER query Service B's database tables directly; it must call Service B's API or subscribe to its domain events.
    3. **API Gateway**: Single entry point handling routing, authentication, rate limiting, and TLS termination so clients don't call 20 internal services directly.
    4. **Sync vs Async Communication**: Use synchronous request/response (REST/gRPC) only when an immediate answer is required; use asynchronous messaging/events (queues/brokers) to decouple services and prevent cascading failures.
    5. **Independent Scaling & Failure Isolation**: Scale the high-traffic Telemetry Service to 10 instances without scaling Billing; if Billing restarts, door locks still unlock.
  - **Trade-offs & When NOT to Use Microservices**: Microservices introduce distributed systems complexity—network latency, partial failures, eventual consistency, distributed tracing, and operational overhead. Small teams with unclear domain boundaries should start with a **Modular Monolith**.

- **Live Demo / Conceptual Trace (run: instructor):**
  Trace a resident unlocking their Smart Front Door in a Microservices Architecture:
  1. Mobile App sends request to the **API Gateway** (validates identity token and rate limits).
  2. API Gateway routes to **Door Lock Service** (owns its own Lock State DB).
  3. Door Lock Service unlocks the door and publishes a `DoorUnlocked` event to the **Message Broker** (async).
  4. **Notification Service** and **Audit Log Service** consume the event independently—even if the Notification Service is temporarily down, the door still unlocks!
  **Point out:**
  - Notice **no shared database**: Notification Service does not read the Door Lock database; it reacts to events or calls an API.
  - Notice **fault isolation**: A slow downstream service does not block the critical door-unlock path.

- **Ask (Check Questions):**
  - Q: Why is "Database-per-Service" a golden rule in microservices? What breaks if two microservices read and write the same database tables? — A: Sharing a database creates tight coupling: a schema change in one service breaks the other, locks contend, and services can no longer be deployed or scaled independently.
  - Q: When is a Modular Monolith a better choice than Microservices? — A: Early-stage products, small teams, or domains with unclear boundaries—where network hops, distributed transactions, and operational overhead slow delivery down.

- **Done when:** Candidates can contrast Monolith vs Microservices, explain Database-per-Service and API Gateway, and name at least two trade-offs of microservices.

---

## Exercise: The Smart Home Architectural Blueprint
**Scenario**: You are the Lead Architect for Apex Smart Homes. You must design the system architecture for a neighborhood of 500 connected homes.
1. **Draw the 3-Tier Diagram**:
   - Identify the Presentation Tier (Mobile app & Wall touchscreens).
   - Identify the Logic Tier (Application orchestrator & business validation rules).
   - Identify the Data Tier (PostgreSQL user accounts & telemetry storage).
2. **Microservices Decomposition**:
   - Split the Logic & Data tiers into 3–4 bounded-context microservices (e.g., Auth/Resident Service, Door Lock Service, Telemetry Service, Billing Service) behind an **API Gateway**.
   - Specify which service owns which database (Database-per-Service) and which interactions should be **synchronous** vs **asynchronous events**.
3. **Specialized Architecture**:
   - Recommend whether nightly power usage billing should use **Batch-Sequential** or **Interactive REST**.
   - Explain how smart door lock sensors connect to the central hub.
4. **Cloud Strategy**:
   - Classify where the components will run across IaaS, PaaS, and SaaS.

## Done-Check
- [ ] Can define Client and Server and explain who initiates communication.
- [ ] Can draw and explain the 3 tiers in a 3-Tier architecture and why it is linear.
- [ ] Can explain how tight coupling causes cascading failures in distributed systems.
- [ ] Can explain the 4 stages of Batch-Sequential processing (`Input -> Validate -> Process -> Report`).
- [ ] Can explain IaaS, PaaS, and SaaS using the empty lot, apartment, and hotel analogy.
- [ ] Can contrast Monolithic vs Microservices architecture, explain Database-per-Service, and justify sync vs async communication.

---

## Post-Class Practice & Dynamic Interview Preparation
When reviewing this module after class or preparing for technical interviews, use your AI practice coach to dynamically generate fresh, real-world architectural scenarios:
- In chat, type: **`interview questions on module 1`** or **`give me a senior architecture interview challenge`**.
- The AI coach dynamically generates random, interview-grade production scenarios (failure modes, edge cases, system trade-offs) and evaluates your architectural defense in real time.
