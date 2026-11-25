# Generative AI, Prompt Engineering & RAG — Course Table of Contents (Week 3 AM)

5 modules covering the mechanics of Transformers, Large Language Models, Prompt Engineering, Embeddings, ChromaDB Vector Database, RAG pipelines, and Evaluation.
Running example: **Meridian Solutions HR Policy Assistant**. Environment: Docker Compose.

---

## Curriculum Overview

| # | Module | Core Topics | Live Demos | Hands-on Labs |
|---|---|---|---|---|
| **1** | Transformers & Attention | Architecture, Self-Attention formula, BPE tokenization, Context limits | Terminal BPE curl + Streamlit Tokenizer UI (`:3000/01_tokenizer`) | Calculate BPE subwords, inspect token IDs, identify context limits |
| **2** | LLM APIs & Prompts | Chat completions, Temperature, Top-p, System prompts, Few-shot, JSON schemas | API curl completions, Structured JSON mode tests | Write strict enterprise system prompts, enforce JSON output |
| **3** | Embeddings & Vector DBs | Vector embeddings, Cosine distance math, ChromaDB collections & indexing | Embeddings UI (`:3000/02_embeddings`), ChromaDB queries | Calculate vector cosine similarities, search top-k nearest neighbors |
| **4** | RAG End-to-End | Chunking strategies, Ingestion, Grounded generation, Abstention, Citations | Chunker UI (`:3000/03_chunker`), RAG Chat UI (`:3000/04_rag_chat`) | Build RAG pipeline: ingest HR doc $\to$ retrieve $\to$ synthesize with citations |
| **5** | Fine-Tuning & Evaluation | RAG vs Fine-tuning decision matrix, PEFT/LoRA walkthrough, LLM-as-a-judge | Evaluation UI (`:8501/05_evaluation`), Benchmark report | Walk through LoRA script, evaluate faithfulness and relevance scores |

---

## 1. Transformers & Attention
1. **The Transformer Revolution:** RNN/LSTM bottlenecks, sequential vs parallel processing, the 2017 "Attention Is All You Need" breakthrough.
2. **Self-Attention Mechanics:** Query ($Q$), Key ($K$), Value ($V$) vectors, the scaled dot-product formula $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$.
3. **Multi-Head Attention:** Attending to information from different representation subspaces simultaneously.
4. **Tokenization & Byte-Pair Encoding (BPE):** Characters vs subwords vs words, how BPE builds vocabularies, handling code and emojis.
5. **Context Windows & Limits:** Context limits ($8k$ vs $128k$), the "Lost-in-the-Middle" phenomenon, quadratic computational scaling $O(N^2)$.

---

## 2. LLM APIs & Prompt Engineering
1. **Chat Completions API:** Roles (system, user, assistant), API request structure, stateless HTTP conversations.
2. **Sampling & Generation Control:** Temperature ($0.0$ to $2.0$), Top-$p$ (nucleus sampling), frequency and presence penalties.
3. **System Prompts & Persona:** Setting behavioral bounds, enterprise tone, role definitions, and negative constraints.
4. **In-Context Learning:** Zero-shot vs Few-shot prompting, selecting representative few-shot exemplars.
5. **Chain-of-Thought & Reasoning:** Eliciting step-by-step reasoning for logic and multi-step math tasks.
6. **Structured Output & JSON Mode:** Enforcing machine-readable output with Pydantic and JSON Schema.

---

## 3. Embeddings & Vector Databases
1. **What is an Embedding?:** Mapping text to dense continuous vector space, capture of semantic meaning.
2. **Vector Math & Distance Metrics:** Dot product, Euclidean distance, Cosine similarity: $\cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$.
3. **Embedding Models:** OpenAI `text-embedding-3-small` (1536-dim) vs `large` (3072-dim), normalization.
4. **Vector Databases vs Relational Databases:** Exact keyword matching vs Approximate Nearest Neighbor (ANN) search, HNSW indexing.
5. **ChromaDB Architecture:** Containerized vector database, collections, document upserting, metadata filtering.

---

## 4. RAG End-to-End
1. **Why RAG?:** Overcoming LLM knowledge cutoffs, hallucination mitigation, private data access without retraining.
2. **Document Chunking Strategies:** Fixed character splitting, Recursive character splitting (respecting paragraphs/sentences), Semantic sentence splitting.
3. **The Ingestion Pipeline:** Document parsing $\to$ chunking $\to$ embedding $\to$ indexing in ChromaDB.
4. **Semantic Retrieval:** Query embedding $\to$ cosine similarity search $\to$ metadata filtering $\to$ top-$k$ context assembly.
5. **Grounded Synthesis & Citations:** Structuring context blocks, prompting for numbered citations (`[1]`, `[2]`), source traceability.
6. **Abstention & Guardrails:** Establishing similarity thresholds (e.g. $< 0.30$), out-of-domain query detection, preventing hallucinations.

---

## 5. Fine-Tuning & Evaluation
1. **RAG vs Fine-Tuning Matrix:** When to use RAG (knowledge retrieval, dynamic facts) vs Fine-Tuning (style, tone, specialized format).
2. **PEFT & LoRA Fundamentals:** Full parameter fine-tuning vs Parameter-Efficient Fine-Tuning, Low-Rank Adaptation weight decomposition $W = W_0 + B \cdot A$.
3. **Preparing Fine-Tuning Datasets:** Instruction-response JSONL pairs, formatting, validation splits.
4. **LoRA Training Walkthrough:** Reference implementation with Hugging Face transformers, PEFT, and Phi-2.
5. **LLM Evaluation Frameworks:** Traditional metrics (BLEU, ROUGE) vs LLM-as-a-judge.
6. **Core RAG Evaluation Dimensions:** Faithfulness (groundedness in context) and Answer Relevance (directness of response).
