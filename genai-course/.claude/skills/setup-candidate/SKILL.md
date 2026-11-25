---
name: setup-candidate
description: Candidate (student) setup for the Generative AI & RAG course (Week 3 AM). Use when a candidate wants to get their laptop ready for class, says "set up my environment", "I can't get the RAG API running", or needs to reset their practice stack. Walks them through Docker & OPENAI_API_KEY, starts the stack, and makes their first RAG query.
---

# Candidate Setup

Guides a learner from a fresh laptop to their first successful RAG retrieval and synthesis call. Be friendly, patient, and concrete; explain each step in one simple sentence.

## Steps

1. **Check Prerequisites:**
   - Docker Desktop installed and running.
   - Terminal (macOS/Linux terminal, or WSL2/Git Bash on Windows).
   - Valid `OPENAI_API_KEY` in `.env` (copy from `.env.example`).
2. **Run `scripts/setup.sh`:**
   Explain that the first run builds the FastAPI and Streamlit images and starts ChromaDB.
3. **Handle Errors if Needed:**

| Exit | Candidate guidance |
|---|---|
| 10 | "Docker is not installed. Download Docker Desktop from docker.com/products/docker-desktop/ and install it." |
| 11 | "Docker is installed but closed. Please open Docker Desktop and wait until the green light shows, then retry." |
| 12 | "Port 8000, 8001, or 3000 is occupied by another application. Free the port or stop that app." |
| 13 / 14 | Review container logs: `docker compose logs api`. Ensure OpenAI API key has sufficient quota. |
| 16 | "Missing OpenAI API key. Copy `.env.example` to `.env` and paste your key in `OPENAI_API_KEY=sk-...`" |

4. **First RAG Query Together:**
   Once setup outputs **READY**, guide the candidate through their first live curl request:
   ```bash
   curl -s -X POST http://localhost:8000/retrieve \
     -H "Content-Type: application/json" \
     -d '{"query": "How many days of PTO do I get each year?", "top_k": 2}'
   ```
   Point out:
   - The retrieved document excerpt from `pto-and-leave-policy.md`.
   - The cosine similarity score.
   - The chunk metadata.
5. **Open Visual UI:**
   Direct them to `http://localhost:3000` in their browser to explore the Tokenizer, Chunker, and RAG Chat interfaces visually.
6. **Wrap Up:**
   Remind them they can reset the database at any time using `scripts/setup.sh --reset` and stop using `scripts/setup.sh --stop`.

## Rules
- Never solve problems silently; explain what happened and why.
- Never print or share real API keys.
- Keep the scope strictly to local workstation environment setup.
