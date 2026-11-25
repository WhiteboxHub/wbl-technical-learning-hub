# Generative AI, RAG & LLMs — Course Repo (Week 3 AM)

Hands-on training curriculum for Generative AI, Attention Mechanisms, Tokenization, Prompt Engineering, Embeddings, ChromaDB Vector Database, Retrieval-Augmented Generation (RAG), and LLM Evaluation.

Running example throughout the course: **Meridian Solutions Enterprise HR Policy Assistant** (comprehensive policies for PTO, Healthcare Benefits, Remote Work, IT Security, and Employee Conduct).

---

## Guides
- [Class-day Quick Start](docs/class-day-quickstart.md) — 5-minute instructor launch checklist
- [Instructor Guide](docs/instructor-guide.md) — complete curriculum architecture, beat mechanics, and co-pilot controls
- [Student Guide](docs/student-guide.md) — laptop setup, API reference table, and Module 1 cheat sheet
- [Instructor Steps](instructor-steps.md) — quick cheat sheet for class delivery

---

## Start the Stack
Requires **Docker Desktop** running and an `OPENAI_API_KEY` in `.env`.

```bash
# 1. Configure credentials
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY=sk-...

# 2. Start stack and run smoke test
scripts/setup.sh
```

### Stack Endpoints
- **RAG Backend API**: http://localhost:8000
- **Interactive API Documentation (Swagger)**: http://localhost:8000/docs
- **ChromaDB Vector Database**: http://localhost:8001
- **Streamlit Visual Explorer**: http://localhost:8501 (or http://localhost:3000)
  - *Tokenizer Visualizer*: http://localhost:8501/01_tokenizer
  - *Embeddings & Cosine Math*: http://localhost:8501/02_embeddings
  - *Chunking Strategies*: http://localhost:8501/03_chunker
  - *Interactive RAG Chat*: http://localhost:8501/04_rag_chat
  - *LLM Evaluation & Fine-Tuning*: http://localhost:8501/05_evaluation

### Run Tests & Verification
```bash
# Run pytest test suite in the API container
docker compose run --rm api pytest -q

# Run end-to-end smoke test
scripts/smoke.sh

# Reset vector database to clean seed data
scripts/setup.sh --reset

# Stop all containers
scripts/setup.sh --stop
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness check, ChromaDB heartbeat, and OpenAI key status |
| `POST` | `/tokenize` | BPE subword tokenization with token IDs, offsets, and context limits |
| `POST` | `/embed` | Generates 1536-dimensional embeddings (`text-embedding-3-small`) |
| `POST` | `/chunk` | Splits documents using `fixed`, `recursive`, or `sentence` strategies |
| `POST` | `/ingest` | Chunks, embeds, and stores documents into ChromaDB |
| `POST` | `/retrieve` | Queries ChromaDB for top-$k$ nearest neighbors by cosine similarity |
| `POST` | `/generate` | Grounded RAG synthesis with context citations and abstention check |
| `GET` | `/documents` | Lists all indexed policy documents in the vector store |
| `DELETE` | `/documents/{id}` | Deletes a document and its chunks from ChromaDB |
| `POST` | `/evaluate` | LLM-as-a-judge scoring for faithfulness, relevance, and groundedness |

---

## Repository Layout
```
genai-course/
├── .claude/skills/
│   ├── teach-genai-class/SKILL.md    # Instructor beat-by-beat teaching co-pilot
│   ├── setup-genai-class/SKILL.md    # Instructor 1-command environment setup
│   ├── setup-candidate/SKILL.md      # Student onboarding and first RAG query
│   └── practice-genai/SKILL.md       # Student tutor (quiz, hints, concepts)
├── api/
│   ├── app/
│   │   ├── main.py                   # FastAPI application & route declarations
│   │   ├── tokenizer.py              # tiktoken BPE tokenization handler
│   │   ├── embeddings.py             # OpenAI vector embeddings & cosine similarity
│   │   ├── chunker.py                # Fixed, recursive, and sentence chunkers
│   │   ├── vector_store.py           # ChromaDB client, upsert, and query logic
│   │   ├── rag.py                    # RAG retrieval, synthesis, citations, abstention
│   │   ├── evaluator.py              # LLM-as-a-judge faithfulness evaluator
│   │   ├── seed.py                   # Auto-ingestion of HR policy documents
│   │   └── database.py               # In-memory document tracker for UI
│   ├── finetuning/
│   │   ├── prepare_dataset.py        # Generates instruction QA training dataset
│   │   ├── train_lora.py             # PEFT/LoRA fine-tuning walkthrough (Phi-2)
│   │   └── evaluate.py               # Benchmark comparison: base vs fine-tuned
│   ├── tests/
│   │   └── test_rag.py               # Pytest suite with mocked completions
│   ├── Dockerfile                    # API container definition
│   └── requirements.txt              # FastAPI, tiktoken, openai, chromadb, pytest
├── course/modules/
│   ├── 01-transformers-and-attention.md
│   ├── 02-llm-apis-and-prompts.md
│   ├── 03-embeddings-and-vector-dbs.md
│   ├── 04-rag-end-to-end.md
│   └── 05-fine-tuning-and-evaluation.md
├── data/hr_documents/                # Seed policy documents (PTO, benefits, remote, etc.)
├── docs/
│   ├── instructor-guide.md           # Comprehensive curriculum and teaching guide
│   ├── student-guide.md              # Student onboarding and reference guide
│   └── class-day-quickstart.md       # 5-minute instructor checklist
├── postman/
│   └── genai.postman_collection.json # Postman collection for all API endpoints
├── scripts/
│   ├── setup.sh                      # Pre-checks, container boot, smoke test
│   ├── smoke.sh                      # 10-point status and functionality test
│   ├── break.sh                      # Fault injector (poisoned docs, chunk shredding)
│   └── fix.sh                        # Restores healthy baseline stack
├── ui/
│   ├── pages/
│   │   ├── 01_tokenizer.py           # Subword tokenizer visualization page
│   │   ├── 02_embeddings.py          # Vector embedding similarity visualizer
│   │   ├── 03_chunker.py             # Chunking strategies comparison page
│   │   ├── 04_rag_chat.py            # Interactive RAG chat with citations
│   │   └── 05_evaluation.py          # LLM-as-a-judge evaluation & fine-tuning hub
│   ├── app.py                        # Streamlit homepage and system health
│   ├── Dockerfile                    # Streamlit UI container definition
│   └── requirements.txt              # Streamlit, requests, plotly, pandas
├── docker-compose.yml                # API (:8000), ChromaDB (:8001), UI (:8501, :3000)
├── docker-compose.finetune.yml       # Optional LoRA training override
├── instructor-steps.md               # Quick cheat sheet for instructors
├── .env.example                      # Configuration template
├── .gitignore                        # Git ignore rules
└── README.md                         # Course repository documentation
```
