# Student Guide — GenAI, Prompt Engineering & RAG (Week 3 AM)

Welcome to the Generative AI and RAG course! You will learn the mechanics of modern Large Language Models (LLMs) and build production-grade Retrieval-Augmented Generation systems by sending real API requests and inspecting vector databases on your own laptop.

---

## 1. What you will learn
| # | Module | You will be able to… |
|---|---|---|
| 1 | Transformers & Attention | Calculate token counts with BPE, explain how Self-Attention calculates word relationships, and identify context window boundaries. |
| 2 | LLM APIs & Prompts | Control LLM temperature and top-p, write robust system instructions, apply few-shot prompting, and enforce structured JSON schemas. |
| 3 | Embeddings & Vector DBs | Generate 1536-dimensional embeddings, calculate cosine similarity between sentences, and query ChromaDB for nearest-neighbor documents. |
| 4 | RAG End-to-End | Build an end-to-end RAG pipeline: document chunking, semantic retrieval, grounded synthesis with citations, and hallucination abstention. |
| 5 | Fine-Tuning & Evaluation | Decide when to fine-tune vs use RAG, explain PEFT/LoRA parameter reduction, and score LLM outputs with LLM-as-a-judge evaluation. |

The running domain throughout this course is **Meridian Solutions**, an enterprise HR knowledge system with policies on PTO, healthcare, remote work, IT security, and employee standards.

---

## 2. Get your laptop ready (before class)
### Prerequisites
- **Docker Desktop** installed and running: https://www.docker.com/products/docker-desktop/
- **Claude Code** (CLI or desktop app)
- A terminal with `curl` (macOS/Linux terminal, or WSL2 / Git Bash on Windows)
- A modern web browser (Chrome, Edge, Firefox)
- An **OpenAI API Key** with active credit/quota

### Step-by-Step Setup
1. Open the `genai-course` folder in Claude Code (start a **new session**).
2. Copy `.env.example` to `.env` and fill in your API key:
   ```bash
   cp .env.example .env
   # Open .env and set: OPENAI_API_KEY=sk-...
   ```
3. Say:
   > **"set up my environment"** (runs skill `setup-candidate`)
4. The helper will run prerequisite checks, start the containers, and run the smoke test.
5. Once it reports **READY**, verify your first RAG query:
   ```bash
   curl -s -X POST http://localhost:8000/retrieve \
     -H "Content-Type: application/json" \
     -d '{"query": "How many days of PTO do employees receive?", "n_results": 2}'
   ```
6. Open the visual explorers in your browser:
   - **Streamlit Visual Explorer**: http://localhost:8501 (or http://localhost:3000)
   - **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
   - **ChromaDB Vector Store**: http://localhost:8001

---

## 3. During class
- Follow along with the instructor’s slides and run the curl requests in your own terminal.
- Use the **Streamlit Visual UI** (`http://localhost:3000`) to visualize how text is converted to token IDs, how chunking splits documents, and how vectors cluster in semantic space.
- Feel free to experiment! If you corrupt the vector database or want to reset to clean baseline data, run:
  ```bash
  scripts/setup.sh --reset
  ```
- To shut down the environment when class is over:
  ```bash
  scripts/setup.sh --stop
  ```

---

## 4. API Reference Cheat Sheet
Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Sample Request |
|---|---|---|---|
| `GET` | `/health` | Stack liveness and service status | `curl http://localhost:8000/health` |
| `POST` | `/tokenize` | Subword tokenization and token IDs | `curl -X POST http://localhost:8000/tokenize -d '{"text":"Hello world"}'` |
| `POST` | `/embed` | Generate 1536-dim text embeddings | `curl -X POST http://localhost:8000/embed -d '{"texts":["Sample text"]}'` |
| `POST` | `/chunk` | Split text (fixed, recursive, sentence) | `curl -X POST http://localhost:8000/chunk -d '{"text":"...","chunk_size":100}'` |
| `GET` | `/documents` | List indexed HR policy documents | `curl http://localhost:8000/documents` |
| `POST` | `/retrieve` | Vector similarity search in ChromaDB | `curl -X POST http://localhost:8000/retrieve -d '{"query":"PTO","n_results":2}'` |
| `POST` | `/generate` | Grounded RAG synthesis with citations | `curl -X POST http://localhost:8000/generate -d '{"query":"What is the 401k match?"}'` |
| `POST` | `/evaluate` | LLM-as-a-judge faithfulness scoring | `curl -X POST http://localhost:8000/evaluate -d '{"question":"...","answer":"...","contexts":["..."]}'` |

---

## 5. After-Class Self Practice
Need to review or practice on your own? In Claude Code, you can say:
- **"quiz me on module 2"**: The AI coach asks you questions one at a time and evaluates your answers.
- **"help with the exercise"**: The coach provides guided, 4-rung progressive hints without spoiling the solution.
- **"explain embeddings"**: Generates a concrete, intuitive explanation with a runnable curl demo.
