# Instructor Steps: How to Start and Run the Class

Course: Generative AI, Prompt Engineering, Embeddings, Vector Databases, RAG & Evaluation (Week 3 AM).
Taught with an AI co-pilot (Claude Code) and an enterprise HR policy RAG demo system.
Project folder: `wbl-technical-learning-hub/genai-course`.
Reference guides: `docs/instructor-guide.md` and `docs/class-day-quickstart.md`.

---

## 1. Before Class

1. **Open the course folder in a new session.** In Claude Code, open `genai-course` and start a **new session** so skills load properly.
2. **Start Docker Desktop** and confirm it is running.
3. **Configure OpenAI Credentials.** Verify `.env` has a valid `OPENAI_API_KEY=sk-...`.
4. **Prepare presentation windows.**
   - Screen 1: Slide talking points from `course/modules/NN-*.md`.
   - Screen 2: Streamlit Visual UI at `http://localhost:3000`.

---

## 2. Starting the Class

1. Say **"set up the class"** (triggers skill `setup-genai-class`). It verifies Docker, ports 3000/8000/8001, seeds the 5 HR documents, and runs the smoke test.
2. Say **"teach module N"**, e.g., `teach module 1`.
3. The co-pilot confirms stack health, presents a brief lesson roadmap, and asks: **"Is your screen shared?"**
4. Answer "yes" if screen sharing so student answers are kept concealed until you call `answer`.

---

## 3. Start Commands by Module

| Module | Topic | Live Stack Components | Primary Interface |
|---|---|---|---|
| **Module 1** | Transformers & Attention | API `:8000` + UI `:3000` | Tokenizer UI (`/01_tokenizer`) & Terminal curl |
| **Module 2** | LLM APIs & Prompts | API `:8000` | Terminal curl (`/generate`, temperature tests) |
| **Module 3** | Embeddings & Vector DBs | API `:8000` + ChromaDB `:8001` + UI `:3000` | Embeddings UI (`/02_embeddings`) & `/retrieve` |
| **Module 4** | RAG End-to-End | Full Stack (`:8000`, `:8001`, `:3000`) | Chunker UI (`/03_chunker`) & RAG Chat UI (`/04_rag_chat`) |
| **Module 5** | Fine-Tuning & Evaluation | API `:8000` + `api/finetuning/` scripts | Terminal evaluation demo (`/evaluate`) & code walkthrough |

---

## 4. During Class

The co-pilot guides you one beat at a time:
- **Slide cue**: Identifies what to present.
- **Say**: 3–5 bulleted talking points.
- **Demo**: Executes live curls or prompts you to open the Streamlit UI.
- **Ask**: Conceptual questions to pose to the class.

### Verbal Controls
`next` · `back` · `repeat` · `skip` · `answer [n]` · `more` · `status` · `take over` · `jump N.M` · `end`

---

## 5. At the End of Each Module

1. Say `end`. The co-pilot:
   - Summarizes covered and skipped beats.
   - Presents the student hands-on exercise.
   - Conducts the Done-check assessment.
   - Appends a teaching log to `.class/progress.md`.
2. Clean up any modified or injected test data with `scripts/fix.sh`.

---

## 6. If Something Goes Wrong

| Problem | Immediate Fix |
|---|---|
| Docker daemon offline | Open Docker Desktop, wait for green icon, say "set up the class" again |
| Missing API key error | Add key to `.env` and restart: `docker compose restart api` |
| Retrieval returns corrupted or empty data | Reseed vector database: `scripts/setup.sh --reset` |
| Port conflict on 3000/8000/8001 | Stop conflicting local servers, then run `scripts/setup.sh` |
| Injected fault still active | Run `scripts/fix.sh` to restore baseline configuration |

---

## 7. For Candidates (Students)

Provide candidates with `docs/student-guide.md`.
- Before class, they run: **"set up my environment"** (skill `setup-candidate`).
- After class, they run: **"quiz me"** or **"help with the exercise"** (skill `practice-genai`).
