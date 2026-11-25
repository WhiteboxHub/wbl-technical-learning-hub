# Module 3 — Embeddings and Vector Databases

Teach-skill content file. Format is described in `.claude/skills/teach-genai-class/SKILL.md`.
Deck: no slides yet. **NEW slide** = teach from the "Say" points and the demo.
Stack: RAG API at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 75–90 minutes with demos and questions.
Story anchor: **The library that shelves books by meaning, not by title — neighbours are books about similar things.**

## Objectives
By the end, candidates can explain embeddings as semantic coordinates, calculate and interpret cosine similarity scores, select and tune document chunking strategies, and query ChromaDB using semantic search and metadata filtering.

---

### Beat 3.1 — Embeddings: meaning as coordinates
- **Slides:** NEW slide: "Embeddings: mapping language into high-dimensional geometry"
- **Say:**
  - Words with similar meanings should be close together in mathematical space.
  - An embedding model (like `text-embedding-3-small`) takes text and outputs a vector of 1,536 floating-point numbers.
  - Unlike generative models (which predict tokens), embedding models encode the entire semantic essence of a sentence into static coordinates.
  - "PTO policy" and "vacation time" will have nearly identical vector directions, even though they share zero letters or words.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/embed -H "Content-Type: application/json" -d '{"texts": ["vacation policy", "paid time off", "corporate VPN setup"]}' | python3 -m json.tool | grep -E "dimensions|model"
  ```
  **Point out:** The model returns 1,536 floats for each text. We cannot visually see 1,536 dimensions, but we can compute angles between them.
- **Ask:**
  - Q: How does an embedding model differ from GPT-4o? — A: GPT-4o generates text; an embedding model outputs a static numerical vector representing semantic meaning.
  - Q: What does dimension count (e.g. 1536 vs 3072) represent? — A: The width of the vector space; higher dimensions can encode finer distinctions at the cost of more storage and memory.
- **Done when:** candidates describe embeddings as coordinates representing meaning.

---

### Beat 3.2 — Cosine similarity: measuring distance in vector space
- **Slides:** NEW slide: "Cosine similarity: dot products of normalized vectors"
- **Say:**
  - How do we know if two vectors mean the same thing? We measure the angle ($\theta$) between them.
  - **Cosine Similarity**: $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$.
  - Ranges from $-1.0$ (opposite directions) to $1.0$ (identical direction).
  - In normalized text embeddings:
    - $\ge 0.85$: Strong semantic match (nearly identical concept).
    - $0.60 - 0.84$: Related topics.
    - $< 0.30$: Unrelated (used as our abstention threshold).
  - Cosine similarity is magnitude-invariant: length of text doesn't distort the angle.
- **Demo (run: instructor):**
  Show page `02_embeddings` in the Streamlit UI (`http://localhost:3000`). Show live comparison of "How much vacation?" vs "PTO policy" ($0.88$) vs "VPN setup" ($0.29$).
- **Ask:**
  - Q: Why is cosine similarity preferred over Euclidean distance for text? — A: Cosine measures direction rather than magnitude, so document length differences don't penalize similarity.
  - Q: If two sentences both discuss financial fraud but take opposite stances, is cosine similarity high or low? — A: High; embedding models group by topic rather than logical polarity.
- **Done when:** candidates can predict whether a similarity score indicates a match.

---

### Beat 3.3 — Chunking strategies: fixed, recursive, and sentence
- **Slides:** NEW slide: "Chunking: how you slice documents decides what you can find"
- **Say:**
  - You cannot embed a 100-page document into a single vector — the specifics get averaged out and lost.
  - Documents must be broken into **chunks**:
    - **Fixed Token Chunking**: Hard cuts every $N$ tokens. Fast, but chops sentences and tables in half.
    - **Sentence Chunking**: Splits on punctuation boundaries. Clean sentences, but variable lengths.
    - **Recursive Character Chunking**: Tries splitting on double newlines (paragraphs), then single newlines, then sentences, then spaces. Preserves document structure!
  - **Chunk Overlap**: Overlapping 10-15% between chunks ensures sentences spanning a boundary aren't severed from their context.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/chunk -H "Content-Type: application/json" -d '{"text": "Meridian provides 15 days of PTO. Accrual is 5 hours per pay period. Carryover is limited to 10 days.", "strategy": "fixed", "chunk_size": 10, "chunk_overlap": 2}' | python3 -m json.tool | grep -E "total_chunks|token_count"
  ```
  **Point out:** A tiny chunk size splits the policy into fragments. If chunk 1 has "15 days of PTO" and chunk 2 has "Carryover is limited to 10 days", a query about carryover might miss the PTO context.
- **Ask:**
  - Q: What happens if your chunks are too large (e.g. 2,000 tokens)? — A: The embedding averages too many concepts, and retrieved chunks dilute the prompt with irrelevant text.
  - Q: What happens if your chunks are too small (e.g. 20 tokens)? — A: Crucial surrounding context (like conditions or exceptions) is severed.
- **Done when:** candidates can explain the trade-offs of chunk size and overlap.

---

### Beat 3.4 — Vector databases and ChromaDB architecture
- **Slides:** NEW slide: "Vector DBs: indexing for fast Approximate Nearest Neighbors (ANN)"
- **Say:**
  - Comparing a query vector against 10 million vectors one by one ($O(N)$) is too slow for real-time web applications.
  - Vector databases use **Approximate Nearest Neighbor (ANN)** indexing algorithms, most commonly **HNSW** (Hierarchical Navigable Small World).
  - ANN trades a tiny bit of precision for orders-of-magnitude speed ($O(\log N)$).
  - In our stack, ChromaDB runs as a dedicated microservice on port `:8001`, storing document text, embeddings, and metadata.
- **Demo (run: agent):**
  ```bash
  curl -s http://localhost:8000/documents | python3 -m json.tool
  ```
  **Point out:** Shows the 5 seeded HR documents in ChromaDB (`employee-handbook`, `pto-and-leave-policy`, `benefits-and-healthcare`, `remote-work-policy`, `it-security-guidelines`).
- **Ask:**
  - Q: What does HNSW do inside ChromaDB? — A: Builds a multi-layer graph index for logarithmic-time nearest-neighbor retrieval.
  - Q: Why run ChromaDB in a separate container rather than in-memory in production? — A: Decouples vector indexing and storage from API web workers, allowing independent scaling.
- **Done when:** candidates can explain why brute-force vector search does not scale.

---

### Beat 3.5 — Semantic retrieval with metadata filtering
- **Slides:** NEW slide: "Hybrid retrieval: semantic search + metadata filters"
- **Say:**
  - Vector search finds meaning, but cannot enforce hard business rules (e.g., "only search documents updated in 2024", or "only search the IT security policy").
  - **Metadata Filtering**: Filtering on structured tags (`document_id`, `department`, `author`, `access_tier`) before or during vector ranking.
  - In enterprise systems, access control (RBAC) is enforced through metadata filters so users only retrieve documents they are cleared to read.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/retrieve -H "Content-Type: application/json" -d '{"query": "How many in-office days are required?", "n_results": 2}' | python3 -m json.tool | grep -E "document_id|score"
  curl -s -X POST http://localhost:8000/retrieve -H "Content-Type: application/json" -d '{"query": "How many in-office days are required?", "n_results": 2, "filter": {"document_id": "remote-work-policy"}}' | python3 -m json.tool | grep -E "document_id|score"
  ```
  **Point out:** Adding the filter guarantees all results originate strictly from the specified document.
- **Ask:**
  - Q: Why not just rely on semantic search to filter by department? — A: Semantic search is fuzzy; a question about "engineering tools" might match sales documents. Hard metadata guarantees isolation.
  - Q: What does ChromaDB's where clause do? — A: Filters the candidate chunks by metadata keys before returning the closest matches.
- **Done when:** candidates can execute a filtered semantic search request.

---

### Beat 3.6 — The poisoned retrieval fault (`break.sh`)
- **Slides:** NEW slide: "Retrieval quality is the ceiling on generation quality"
- **Say:**
  - If the vector database contains outdated, malicious, or conflicting text, the generator will faithfully generate incorrect answers.
  - The model does not know reality; it only knows the chunks placed in its prompt.
  - In this demo, we inject a false policy chunk claiming Meridian offers 0% 401(k) matching.
- **Demo (run: agent):**
  ```bash
  scripts/break.sh poisoned-retrieval
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What is the company 401(k) match?"}' | python3 -m json.tool | grep -E "answer|sources"
  scripts/fix.sh
  curl -s -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"query": "What is the company 401(k) match?"}' | python3 -m json.tool | grep -E "answer|sources"
  ```
  **Point out:** Under the fault, the model answers that there is 0% match because the poisoned chunk scored highest! After `scripts/fix.sh`, it returns the authentic 4% match.
- **Ask:**
  - Q: Did the LLM make a mistake during the poisoned retrieval demo? — A: No; the LLM followed its instructions perfectly. The retrieval pipeline served bad data.
  - Q: What is the primary defense against stale or conflicting documents in RAG? — A: Document lifecycle management, version metadata, and automatic deletion of superseded chunks.
- **Done when:** candidates explain that hallucination is an LLM failure, while bad retrieval is a data engineering failure.

---

### Beat 3.7 — Embedding model consistency
- **Slides:** NEW slide: "The cardinal rule: identical models for indexing and querying"
- **Say:**
  - Embeddings from different models live in completely different vector spaces.
  - You cannot query a collection indexed with `text-embedding-3-small` using `text-embedding-ada-002` or `cohere-embed`.
  - The vector coordinates will have no semantic correspondence, resulting in nonsense similarity scores.
- **Demo (run: agent):**
  Explain that `scripts/break.sh dim-mismatch` triggers this exact issue.
- **Ask:**
  - Q: What happens if an organization upgrades their embedding model to a newer version? — A: All existing documents must be re-embedded and re-indexed into a new collection.
- **Done when:** candidates explain why embedding models cannot be swapped without re-indexing.

---

## Exercise (candidates, ~25 min)
1. Ingest a new mini-policy using `POST /ingest` with `document_id: "intern-policy"`.
2. Test retrieval with 3 different queries.
3. Observe how the similarity scores vary as phrasing shifts.
4. Delete the document using `DELETE /documents/intern-policy` and verify retrieval drops to 0.

## Done-check
1. Define an embedding and state its dimension in `text-embedding-3-small`.
2. Explain how cosine similarity measures semantic closeness.
3. Compare fixed-size vs recursive chunking.
4. Explain what happens if an unauthorized chunk is retrieved in a RAG pipeline.

## Clean-up
`scripts/setup.sh --reset`
