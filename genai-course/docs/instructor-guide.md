# Instructor Guide — GenAI, Prompt Engineering & RAG (Week 3 AM)

Hands-on curriculum for teaching Transformers, Large Language Models, Tokenization, Prompt Engineering, Embeddings, Vector Databases, Retrieval-Augmented Generation (RAG), and LLM Evaluation. Taught with an AI co-pilot (Claude Code) and an interactive Meridian Solutions HR policy knowledge stack.

**In a hurry? See the [Class-day quick start](class-day-quickstart.md).**

**Status:** All 5 modules (Modules 1–5) are fully scripted with active terminal and visual UI demos. Setup, teaching co-pilot, and candidate practice skills are ready.

---

## 1. How the course works
- **You teach; the agent co-pilots.** The agent tracks the teaching plan, runs or hands over terminal and browser demos, holds the answer key, and records candidate progress.
- **One running domain throughout:** Meridian Solutions internal HR policies (Employee Handbook, PTO & Leave, Healthcare & Benefits, Remote Work, IT Security).
- **Interactive Multi-Tier Stack:**
  - **FastAPI API (`:8000`)**: Core endpoints for tokenization, embeddings, chunking, retrieval, generation, and LLM evaluation.
  - **ChromaDB Vector DB (`:8001`)**: Containerized vector database storing policy chunk embeddings.
  - **Streamlit Visual Explorer (`:3000`)**: Visual interactive exploration of token splitting, cosine similarity math, chunking strategies, and end-to-end RAG chat with live context and citation inspection.
- **Module Structure:** 5 modular lesson files in `course/modules/`, each structured with **Objectives**, ordered **Beats** (Slides, Say, Demo, Ask, Done-when), an **Exercise**, and a **Done-check**.

| # | Module | File | Core Topics | Live Demos |
|---|---|---|---|---|
| 1 | Transformers & Attention | `01-transformers-and-attention.md` | Architecture, Attention formula, BPE tokenization, Context windows | Terminal BPE curl + Streamlit Tokenizer UI (`:3000/01_tokenizer`) |
| 2 | LLM APIs & Prompts | `02-llm-apis-and-prompts.md` | Chat Completions, Temperature, Top-p, System prompts, Few-shot, JSON mode | Curl API calls, Structured output tests, In-flight playground |
| 3 | Embeddings & Vector DBs | `03-embeddings-and-vector-dbs.md` | Semantic embeddings, Cosine distance, Vector search, ChromaDB indexing | Vector math demo, ChromaDB querying, Streamlit Embeddings UI (`:3000/02_embeddings`) |
| 4 | RAG End-to-End | `04-rag-end-to-end.md` | Chunking strategies, Ingestion, Grounded generation, Abstention, Citations | Chunking UI (`:3000/03_chunker`), RAG Chat UI (`:3000/04_rag_chat`), Abstention curls |
| 5 | Fine-Tuning & Evaluation | `05-fine-tuning-and-evaluation.md` | RAG vs Fine-tuning decision matrix, LoRA/PEFT, LLM-as-a-judge, Faithfulness | Reference training script walkthrough, Live `/evaluate` judge call, Benchmark report |

---

## 2. Before your first class (one-time setup)
1. Install **Docker Desktop** and verify it is running.
2. Ensure you have an **OpenAI API Key** with active quota.
3. Open the `genai-course` folder in Claude Code (open a **new session** so `.claude/skills/` load automatically).
4. Copy `.env.example` to `.env` and set `OPENAI_API_KEY=sk-...`.
5. Say **"set up the class"** (triggers skill `setup-genai-class`). The script verifies Docker, checks ports (3000, 8000, 8001), seeds the vector store, runs the 10-check smoke test, and outputs **READY**.
6. Open your slides or presentation window. (Missing slides are flagged as `NEW slide: "..."` with ready-to-teach speaking bullets).

---

## 3. Running a class
To start teaching, say:
> **"teach module 1"** (or `teach module 2`, `teach module 3`, etc.)

The teaching co-pilot will:
1. Probe container health (`localhost:8000/health`) and verify ChromaDB connectivity.
2. Present a short 5-line module overview (objectives, beats count, estimated time).
3. Ask: **"Is your screen shared with candidates?"** If yes, answers to all check questions are strictly withheld until you say `answer`.
4. Walk each beat sequentially:
   - **Show:** Slide title or speaking points.
   - **Say:** 3–5 bulleted key concepts.
   - **Demo:** Executes curl commands or guides you to the Streamlit UI.
   - **Ask:** 1–3 conceptual check questions for the room.
   - **Wait:** Awaits your signal to advance.

### Instructor Controls (Natural language works too)
| Command | Action |
|---|---|
| `next` / `done` | Advance to the next beat |
| `back` | Return to previous beat |
| `repeat` | Re-execute the current demo |
| `skip` | Skip the beat and log it to `.class/progress.md` |
| `answer [n]` | Reveal the answer key for the question(s) |
| `more` | Provide an extra question, code snippet, or analogy |
| `status` | Display module progress, elapsed time, and completed beats |
| `take over` | Instructor demonstrates manually; agent pauses |
| `jump N.M` | Navigate directly to a specific beat (e.g. `jump 4.3`) |
| `end` | Conclude module, present candidate exercise, and run Done-check |

---

## 4. Troubleshooting Guide

| Problem | Root Cause | Solution |
|---|---|---|
| `scripts/setup.sh` returns exit 10 or 11 | Docker Desktop not running | Start Docker Desktop, wait for the daemon, and retry |
| `scripts/setup.sh` returns exit 16 | Missing `OPENAI_API_KEY` | Edit `.env` and provide a valid OpenAI secret key |
| Port 8000, 8001, or 3000 already in use | Another service is listening | Run `netstat -ano` / `lsof` to find the process or stop conflicting containers |
| Retrieval returns 0 results | ChromaDB collection unseeded | Run `scripts/setup.sh --reset` to clear the volume and re-seed |
| Streamlit UI displays connection error | FastAPI backend is restarting | Verify `docker compose ps`; test with `curl http://localhost:8000/health` |
| Candidates see answers on instructor screen | Shared screen mode was disabled | Say "screen is shared" to enable strict answer concealment |

---

## 5. Wrapping up a module
1. When you say `end`, the agent:
   - Summarizes completed vs skipped beats.
   - Hands over the **Exercise** prompt for candidates.
   - Runs the **Done-check** checklist to gauge room comprehension.
   - Records notes and candidate feedback into `.class/progress.md`.
2. Clean up temporary test data if needed using `scripts/fix.sh`.
3. To stop all containers after class:
   ```bash
   scripts/setup.sh --stop
   ```
