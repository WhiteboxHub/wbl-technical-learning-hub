# System Design Student Guide & Reference

Welcome to the **System Design** track. This guide contains everything you need to prepare your machine, master the 5-step design method, and practice after class.

---

## 1. Laptop Setup (Before Class)
Run the following in your terminal to ensure you have the required tools:
```bash
docker --version
curl --version
python --version
```
If you are using Claude Code / Antigravity, open this folder and say: **"set up my environment"** (skill `setup-candidate`).

---

## 2. The 5-Step System Design Method

Whenever you are asked to design any system in an interview or project, follow these 5 steps in order:

```
[ Step 1: Requirements & Scope ]
   ↓ (Clarify functional features, non-functional latency/availability, and out-of-scope)
[ Step 2: Capacity Estimations ]
   ↓ (Calculate QPS, peak traffic, storage per year, network bandwidth)
[ Step 3: High-Level Architecture ]
   ↓ (Draw Client -> DNS -> Load Balancer -> App Servers -> Cache -> DB -> Queue)
[ Step 4: Identify Bottlenecks ]
   ↓ (Where does the city jam first? DB read saturation? Write spikes? SPOF?)
[ Step 5: Defend Trade-offs ]
   ↓ (Name the cost of every lever: cache staleness, replication lag, ops overhead)
```

---

## 3. Back-of-the-Envelope Math Cheat Sheet

### Time Constants
- **1 Day = 86,400 seconds ≈ 100,000 seconds ($10^5$ seconds)**
- 1 Million requests per day = $1,000,000 / 100,000 = \mathbf{10\text{ requests/sec (QPS)}}$
- 10 Million requests per day = $\mathbf{100\text{ QPS}}$
- 100 Million requests per day = $\mathbf{1,000\text{ QPS}}$
- **Peak QPS**: Assume $2\times$ to $5\times$ average QPS.

### Powers of 2 & Data Storage
- $2^{10} = 1,024 \approx \mathbf{1\text{ KB}}$ (Kilobyte)
- $2^{20} = 1,048,576 \approx \mathbf{1\text{ MB}}$ (Megabyte)
- $2^{30} \approx \mathbf{1\text{ GB}}$ (Gigabyte)
- $2^{40} \approx \mathbf{1\text{ TB}}$ (Terabyte)
- $2^{50} \approx \mathbf{1\text{ PB}}$ (Petabyte)

### Latency Numbers to Know
| Operation | Latency | Story Comparison |
|---|---|---|
| L1 CPU Cache | 1 ns | Eye blink |
| RAM Access | 100 ns | Reach into pocket |
| Read 1 MB from NVMe SSD | 100 μs | Walk down the hall |
| Read 1 MB from Network DB | 10 ms | Drive across town |
| Intercontinental Roundtrip | 150 ms | Flight to Europe |

---

## 4. The Core Levers Summary

| Lever | Story Metaphor | What Problem It Solves | The Price / Trade-off You Must Name |
|---|---|---|---|
| **Load Balancer** | Traffic Controller | Distributes traffic across app nodes; removes single node bottlenecks | Added network hop; must configure health checks and session affinity |
| **Stateless Replicas** | Identical Market Stalls | Scales compute horizontally to meet request volume | State must be pushed out to DB/cache; cannot store user data in RAM |
| **Cache (Redis)** | Corner Shop | Cuts read latency to ~2ms; offloads 80%+ of database reads | Cache staleness; cache invalidation complexity; memory cost |
| **Message Queue** | Delivery Depot | Absorbs traffic spikes (peak shaving); decouples slow background jobs | Eventual consistency; messages may arrive out of order or duplicate |
| **Read Replicas** | Extra Ledger Copies | Scales read queries across multiple DB read nodes | Replication lag; reading your own writes immediately may show old data |

---

## 5. Evening Practice with AI Tutor
After class, open this directory and prompt:
- `"quiz me"` — Takes a 5-question oral quiz on the day's topics with hidden answers until you try.
- `"review my system design"` — Submit your 1-page design for critique by a virtual Senior Engineer.
- `"explain [topic]"` — Re-teaches any concept using *The Growing City* story.
