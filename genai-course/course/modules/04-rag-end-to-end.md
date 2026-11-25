# Module 4 — RAG End-to-End

Teach-skill content file. Format is described in `.claude/skills/teach-genai-class/SKILL.md`.
Deck: no slides yet. **NEW slide** = teach from the "Say" points and the demo.
Stack: RAG API at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 90 minutes with demos and questions.
Story anchor: **The open-book exam: the model may look things up — your job is the library, the index, and the rules.**

## Objectives
By the end, candidates can trace the full RAG pipeline from ingest to citation, implement grounding constraints and abstention rules, evaluate retrieval and generation quality, and diagnose end-to-end failure modes.

---

### Beat 4.1 — The full RAG architecture
- **Slides:** NEW slide: "RAG architecture: offline indexing + online retrieval-generation"
- **Say:**
  - RAG bridges the gap between private enterprise knowledge and generative models.
  - Two decoupled pipelines:
    1. **Offline Ingestion Pipeline**: Raw Documents $\to$ Chunking $\to$ Embedding $\to$ Vector Store.
    2. **Online Query Pipeline**: User Query $\to$ Query Embed $\to$ Vector Search $\to$ Context Assembly $\to$ Prompt Synthesis $\to$ LLM Generation $\to$ Grounded Answer with Citations.
  - The model operates in an "open-book exam": it is given the reference excerpts directly in its prompt.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "How many weeks of primary caregiver leave does Meridian offer?"}' | python3 -m json.tool
  ```
  **Point out:** The output contains `answer`, `sources: ["pto-and-leave-policy"]`, `abstained: false`, and `retrieved_chunks`.
- **Ask:**
  - Q: Why is RAG called "Retrieval-Augmented Generation"? — A: Because the generative model's prompt is augmented with retrieved evidence before generating an answer.
  - Q: What are the two distinct pipelines in a RAG system? — A: Ingestion (indexing) and Querying (retrieval + generation).
- **Done when:** candidates can draw and explain the two RAG pipelines from memory.

---

### Beat 4.2 — Document ingestion in practice
- **Slides:** NEW slide: "The ingestion pipeline: parsing, chunking, and metadata tagging"
- **Say:**
  - Real enterprise documents are messy: headers, markdown tables, footnotes.
  - Ingestion must strip junk, detect document boundaries, and tag every chunk with essential metadata: `document_id`, `created_at`, `version`, `access_tier`.
  - In our API, `POST /ingest` accepts raw text and metadata, splits it via recursive chunking, embeds all chunks in a batch, and stores them in ChromaDB.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d '{"document_id": "equipment-policy", "text": "Meridian provides all engineers with a 16-inch MacBook Pro M3 Max and a $500 home monitor allowance.", "metadata": {"dept": "IT", "year": "2024"}}' | python3 -m json.tool
  ```
  **Point out:** Returns `chunks_stored: 1` and `document_id: "equipment-policy"`. The new policy is immediately searchable.
- **Ask:**
  - Q: Why attach metadata at ingestion rather than after retrieval? — A: Metadata must be indexed alongside vectors so queries can be filtered before similarity calculation.
  - Q: What happens if you re-ingest an updated document with the same document_id? — A: Our `upsert` replaces existing chunks, preventing duplicate old policy answers.
- **Done when:** candidates can ingest a document with custom metadata via the API.

---

### Beat 4.3 — Query embedding and top-K retrieval
- **Slides:** NEW slide: "Top-K retrieval: precision vs recall"
- **Say:**
  - The query is embedded using the exact same embedding model used during ingestion.
  - We ask ChromaDB for the Top-$K$ closest chunks ($K=3$ or $K=5$).
  - **Trade-off**:
    - Too small $K$ ($K=1$): Risk missing secondary context needed for complete answers.
    - Too large $K$ ($K=10$): Fills context window with low-relevance noise, confuses model, increases cost.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/retrieve -H "Content-Type: application/json" -d '{"query": "What is the gym stipend amount?", "n_results": 3}' | python3 -m json.tool
  ```
  **Point out:** Shows the top 3 chunks with their similarity scores. Chunk 1 has the $50/month gym stipend from `benefits-and-healthcare.md` with high similarity (~0.85).
- **Ask:**
  - Q: What does $K$ stand for in Top-K? — A: The number of top candidate chunks returned by the vector database.
  - Q: If the top chunk has a similarity of 0.20, what does that indicate? — A: The query has virtually no relevant documents in the database.
- **Done when:** candidates can tune $K$ and explain its impact on answer quality.

---

### Beat 4.4 — Grounding and citation enforcement
- **Slides:** NEW slide: "Prompt synthesis: enforcing citations and verifiable claims"
- **Say:**
  - Simply pasting context into an LLM prompt is not enough. You must instruct the model how to cite sources.
  - In `api/app/rag.py`, context chunks are formatted as numbered blocks: `[1] (source: pto-policy) text...`
  - The system prompt instructs the model: *"Cite your sources using bracketed numbers [1], [2]. Never state facts not present in the context."*
  - This allows automated parsing of citations and human verification.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What health insurance plans are available at Meridian?"}' | python3 -m json.tool
  ```
  **Point out:** The generated answer explicitly references `[1]` and mentions BlueShield HMO, PPO, and HDHP. The API extracts `sources: ["benefits-and-healthcare"]`.
- **Ask:**
  - Q: Why is citation enforcement critical in regulated industries (healthcare, legal, HR)? — A: Answers must be audited; users need to know which policy document authorizes the answer.
  - Q: Can an LLM generate a citation to a chunk it didn't use? — A: Yes, which is why automated evaluation (checking faithfulness) is necessary.
- **Done when:** candidates can explain how bracketed citations enable auditability.

---

### Beat 4.5 — The abstention rule: knowing when to say "I don't know"
- **Slides:** NEW slide: "Abstention: the most valuable answer in enterprise AI"
- **Say:**
  - In consumer chat, an LLM making up a creative guess is harmless. In enterprise HR or medical systems, it can cause legal liability or employee distress.
  - **Abstention**: If the similarity score of the top chunk is below our threshold ($0.30$), the system **refuses to answer**.
  - It returns `abstained: true` and directs the user to contact the Human Resources team directly.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What is the company stock option vesting cliff for SpaceX?"}' | python3 -m json.tool
  ```
  **Point out:** Returns `abstained: true` and the polite fallback message: *"I cannot find information about this topic in the Meridian Solutions HR documents."*
- **Ask:**
  - Q: Why is an abstention better than a plausible guess? — A: An abstention has zero error cost and routes to a human; a hallucination creates false assumptions.
  - Q: What threshold does our system use to trigger abstention? — A: Similarity score $< 0.30$.
- **Done when:** candidates can demonstrate a working abstention trigger on out-of-domain questions.

---

### Beat 4.6 — The hallucination trap fault (`break.sh`)
- **Slides:** NEW slide: "What happens when you disable abstention"
- **Say:**
  - Let's see what happens when developers remove the abstention guardrail and force the model to answer anyway.
- **Demo (run: agent):**
  ```bash
  scripts/break.sh hallucination-trap
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What is the corporate pet policy for bringing dogs to the office?"}' | python3 -m json.tool
  scripts/fix.sh
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What is the corporate pet policy for bringing dogs to the office?"}' | python3 -m json.tool
  ```
  **Point out:** Under `hallucination-trap`, the model takes loosely related chunks (like code of conduct) and hallucinates a detailed pet policy! Once restored, it abstains cleanly.
- **Ask:**
  - Q: Why did the model hallucinate when abstention was turned off? — A: Because the prompt forced it to answer from weak, irrelevant chunks.
- **Done when:** candidates explain why score-based abstention is a mandatory production guardrail.

---

### Beat 4.7 — RAG evaluation: faithfulness and relevance
- **Slides:** NEW slide: "Evaluating RAG: Faithfulness vs Answer Relevance"
- **Say:**
  - How do you grade thousands of RAG queries automatically?
  - Two primary RAG evaluation metrics:
    1. **Faithfulness**: Is the answer completely grounded in the retrieved chunks? (Score 0.0 to 1.0). Catches hallucinations.
    2. **Answer Relevance**: Did the answer address the user's specific question? (Score 0.0 to 1.0). Catches evasion.
  - In our API, `POST /evaluate` uses an LLM-as-judge with a strict prompt to compute these scores.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/evaluate -H "Content-Type: application/json" -d '{
    "question": "How many days of sick leave do employees get?",
    "answer": "Employees receive 10 dedicated paid sick days per year.",
    "contexts": ["Meridian provides 10 dedicated paid Sick Days (80 hours) per year, allocated on January 1st."]
  }' | python3 -m json.tool
  ```
  **Point out:** Returns `faithfulness: 1.0`, `relevance: 1.0`, and reasoning explaining that the claim matches the context text.
- **Ask:**
  - Q: If faithfulness is 1.0 but relevance is 0.2, what happened? — A: The model repeated facts from the document that had nothing to do with what the user asked.
  - Q: If relevance is 1.0 but faithfulness is 0.1, what happened? — A: The model answered the question directly, but made up the facts out of thin air.
- **Done when:** candidates can interpret faithfulness and relevance scores.

---

### Beat 4.8 — RAG failure modes and debugging runbook
- **Slides:** NEW slide: "The RAG triage runbook: where did it fail?"
- **Say:**
  - When a RAG answer is wrong, where do you look first?
  - **Triage hierarchy**:
    1. Check `retrieved_chunks` and their scores. Did the right chunk get retrieved? If NO $\to$ Chunking, embedding, or query issue.
    2. If the right chunk WAS retrieved $\to$ Inspect the prompt and model temperature. Did the generator ignore the chunk or hallucinate?
    3. If the answer is correct but ungrounded $\to$ Missing citations.
- **Ask:**
  - Q: If an answer is fluent but factually incorrect, is it usually a generation or a retrieval problem? — A: Check retrieval first; 80% of RAG failures originate from the retrieval stage.
- **Done when:** candidates can diagnose an incorrect RAG answer using the triage runbook.

---

## Exercise (candidates, ~25 min)
1. Run 3 questions through the RAG Chat UI:
   - One direct policy question (e.g. PTO carryover).
   - One multi-document question (e.g. benefits and sick leave).
   - One off-topic question to trigger abstention.
2. Inspect the retrieved chunks in the UI for each.
3. Call `POST /evaluate` on your first answer and verify that both faithfulness and relevance score $\ge 0.9$.

## Done-check
1. Describe the offline and online stages of RAG.
2. Explain the purpose and mechanism of abstention.
3. Demonstrate a query with working citations.
4. Distinguish between faithfulness and answer relevance.

## Clean-up
`scripts/setup.sh --reset`
