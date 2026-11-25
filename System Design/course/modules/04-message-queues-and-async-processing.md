# Module 4: Message Queues and Asynchronous Decoupling

Story anchor: **The Growing City**. During the holiday rush, thousands of residents show up at the postal counter at 9:00 AM. The clerk cannot process 5,000 parcels in an hour. Instead of locking the door, the clerk places orders in a **delivery depot queue**. Customers get a claim ticket (202 Accepted) and leave; depot workers process the parcels steadily in the background.

## Objectives
By the end of this module, candidates can:
1. Distinguish synchronous (blocking) from asynchronous (non-blocking) processing.
2. Explain how message queues provide **peak shaving** (buffering traffic bursts).
3. Understand the Producer-Consumer pattern and worker pool scaling.
4. Explain message delivery semantics (At-least-once, At-most-once) and the necessity of idempotent consumers.

## Stack Requirements
- Running stack: `scripts/setup.sh`
- Redis `:6379`, Worker service, API `:8000`.

---

### Beat 4.1 — Synchronous Bottlenecks vs. Asynchronous Decoupling
- **Slides:** Diagram: Synchronous RPC (Client waits) vs Asynchronous Queue (Client unblocked).
- **Say:**
  - In a synchronous system, the client waits until every database write, third-party API call, and email notification completes before receiving an HTTP response.
  - If any downstream component is slow or down, the user request times out or crashes.
  - In an asynchronous system, the API validates the input, enqueues a job, and returns an immediate response (`202 Accepted`).
  - Workers consume the queue at their own sustainable pace.
- **Demo (run: agent):**
  ```bash
  # Send an asynchronous shorten request
  curl -i -X POST http://localhost:8080/api/shorten \
    -H "Content-Type: application/json" \
    -d '{"url":"https://github.com","custom_code":"gh-async","async_queue":true}'
  ```
  - **Point out:** The HTTP status code `202 Accepted` and `"queued": true`. The client is unblocked in milliseconds.
- **Ask:**
  - Q: Why is synchronous processing dangerous for operations like sending emails or generating PDF reports?
  - A: It ties up web server threads waiting for slow external services; if the service hangs, client requests pile up and exhaust server connections.
- **Done when:** Candidates can explain synchronous blocking vs asynchronous buffering.

---

### Beat 4.2 — Peak Shaving & Backpressure
- **Slides:** Graph: Traffic Spike vs Constant Worker Consumption Rate.
- **Say:**
  - **Peak Shaving (Load Leveling)**:
    - Flash sale: 10,000 orders/minute arrive for 5 minutes.
    - Database can only safely process 1,000 orders/minute.
    - Without a queue: DB locks up, crashes, drops connections.
    - With a queue: 50,000 orders sit safely in the queue; workers drain them at 1,000/min over 50 minutes.
  - **Backpressure**: The queue acts as a shock absorber. When the backlog grows, we can scale up worker containers independently without changing the API tier.
- **Demo (run: agent):**
  ```bash
  # Inspect Redis queue lengths
  docker compose exec -T redis redis-cli LLEN "analytics:queue"
  docker compose exec -T redis redis-cli LLEN "shorten:queue"
  ```
  - **Point out:** The queue length metrics in Redis. As traffic arrives, the queue absorbs spikes without dropping data.
- **Ask:**
  - Q: What happens to user latency during peak shaving?
  - A: The initial request is fast (`202 Accepted`), but the eventual completion of the background task takes longer until workers drain the queue.
- **Done when:** Candidates explain how queues prevent database collapse during flash traffic spikes.

---

### Beat 4.3 — Idempotency and Consumer Failure
- **Slides:** Diagram: Producer -> Queue -> Worker -> Crash -> Retry.
- **Say:**
  - In distributed systems, networks fail. Workers crash halfway through processing an order.
  - Most queues offer **At-Least-Once Delivery**: A message may be delivered more than once if an acknowledgment is lost.
  - Therefore, workers **must be idempotent**: Processing the same message twice must have the same outcome as processing it once (e.g., using unique transaction IDs).
- **Demo (run: agent):**
  ```bash
  # View worker logs processing analytics and shorten events
  docker compose logs worker --tail=10
  ```
  - **Point out:** The worker polling Redis, pulling tasks, and updating the database with idempotent upsert queries.
- **Ask:**
  - Q: If a message is delivered twice to a payment worker, what prevents double charging?
  - A: Idempotency keys/checks: The worker checks if the transaction ID was already settled before charging again.
- **Done when:** Candidates define at-least-once delivery and explain why consumers must be idempotent.

---

## Exercise (~15 min)
1. Trigger 20 click events by querying `http://localhost:8080/r/wbl`.
2. Inspect the analytics queue and database stats: `curl -s http://localhost:8080/api/stats/wbl`
3. Notice that click count increments asynchronously via the worker without adding latency to the redirect.

## Done-Check
- [ ] Understands the difference between synchronous blocking and asynchronous queues.
- [ ] Can draw and explain the producer-consumer pattern.
- [ ] Can define peak shaving and why shock absorbers protect databases.
- [ ] Explains at-least-once delivery and consumer idempotency.

## Clean-Up
`scripts/fix.sh`
