# Module 1 — Transformers and Attention

Teach-skill content file. Format is described in `.claude/skills/teach-genai-class/SKILL.md`.
Deck: no slides yet. **NEW slide** = teach from the "Say" points and the demo.
Stack: RAG API at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 75–90 minutes with demos and questions.
Story anchor: **The meeting where everyone listens to everyone else before speaking — and remembers who said what.**

## Objectives
By the end, candidates can explain what a token is, describe the attention mechanism (Q, K, V) in plain mechanics, explain context windows and their hard limits, and inspect token splits and costs using the tokenizer API.

---

### Beat 1.1 — What is a language model (the prediction machine)
- **Slides:** NEW slide: "Language models: next-token prediction at scale"
- **Say:**
  - LLMs do one thing at their core: predict the next token given all previous tokens.
  - Trained on hundreds of billions of words to minimize prediction surprise (cross-entropy loss).
  - It is **not reasoning, feeling, or understanding** — it is extremely high-dimensional statistical pattern completion.
  - Temperature controls how strictly or randomly the model samples from its probability distribution over the vocabulary.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/tokenize -H "Content-Type: application/json" -d '{"text": "The meeting starts at"}' | python3 -m json.tool
  ```
  **Point out:** The model operates on integer token IDs, not human characters or raw strings. "The meeting starts at" is converted into an array of numbers.
- **Ask:**
  - Q: Does an LLM understand grammar rules? — A: No; it has learned statistical likelihoods of which tokens follow which, which mimics grammar.
  - Q: What does temperature 0.0 do to next-token prediction? — A: Makes it pick the single highest probability token every step (greedy decoding).
- **Done when:** candidates can define next-token prediction without using words like "thinking" or "understanding".

---

### Beat 1.2 — Tokenization: the alphabet of LLMs
- **Slides:** NEW slide: "Tokens: the vocabulary of modern models"
- **Say:**
  - Characters are too fine-grained; full words are too sparse (infinite vocabulary for typos and languages).
  - Modern LLMs use **Byte-Pair Encoding (BPE)**: common character sequences merge into single tokens.
  - Token counts differ from word counts: on average in English, 1,000 words $\approx$ 1,333 tokens (~0.75 words/token).
  - Edge cases: capitalization, punctuation, numbers, and code drastically change token boundaries and inflate costs.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/tokenize -H "Content-Type: application/json" -d '{"text": "ChatGPT vs chatgpt"}' | python3 -m json.tool
  curl -s -X POST http://localhost:8000/tokenize -H "Content-Type: application/json" -d '{"text": "Priya Raman manages 12 specialists at Meridian Solutions."}' | python3 -m json.tool
  ```
  **Point out:** Capitalization changes token counts ("ChatGPT" vs "chatgpt"); rare names like "Priya" or compound words split into multiple subwords.
- **Ask:**
  - Q: Why are tokens used instead of whole words? — A: Fixed vocabulary size while handling unseen words, prefixes, and code without out-of-vocabulary errors.
  - Q: Why does verbose prompt formatting increase your API bill? — A: Providers bill by total token count (input tokens + output tokens).
- **Done when:** candidates can predict whether a string has more tokens than words.

---

### Beat 1.3 — Context windows and working memory
- **Slides:** NEW slide: "Context windows: the hard ceiling on working memory"
- **Say:**
  - Context window = maximum number of tokens an LLM can attend to in a single forward pass (input + generated output combined).
  - `gpt-4o-mini` has a 128,000 token window; smaller models often have 8,192 or 16,384 tokens.
  - When text exceeds the context window, **information is truncated or rejected**.
  - A 128k context does not mean you should dump 100-page manuals into every query — cost increases linearly, latency increases, and recall suffers ("lost in the middle").
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/tokenize -H "Content-Type: application/json" -d '{"text": "Policy query test", "model": "gpt-4o-mini"}' | python3 -m json.tool
  ```
  **Point out:** The API returns `context_limit: 128000` and `truncated: false`. If a payload approaches the limit, warnings fire before an OpenAI crash.
- **Ask:**
  - Q: What happens when an input prompt exceeds the model's context limit? — A: The API rejects the call with an error, or cuts off earlier tokens.
  - Q: Why not use a 128k context for every single customer question? — A: High latency, high cost, and degraded precision on specific facts.
- **Done when:** candidates explain the context window as a hard operational boundary.

---

### Beat 1.4 — Attention: the meeting room story
- **Slides:** NEW slide: "Self-Attention: Q, K, V mechanics"
- **Say:**
  - The story anchor: Imagine a meeting where nobody speaks until everyone has listened to what everyone else has to say.
  - In an RNN, words were processed sequentially (early words faded). Attention allows every word to attend to every other word simultaneously.
  - **Query ($Q$)**: "What am I looking for?" (the question each token asks).
  - **Key ($K$)**: "What do I offer / what is my label?" (how tokens advertise their content).
  - **Value ($V$)**: "What is my actual content / message?"
  - Match $Q$ with all $K$ via dot product $\to$ softmax $\to$ weights. Multiply weights by $V$ $\to$ new context-rich representation.
- **Demo (run: instructor):**
  Open the whiteboard or Streamlit Tokenizer. Walk through the sentence: "The bank of the river" vs "The bank approved the loan". Show how "bank" attends to "river" in sentence 1 and "loan" in sentence 2, resolving ambiguity.
- **Ask:**
  - Q: What does the dot product of Q and K measure? — A: The relevance or affinity between two tokens.
  - Q: Why is positional encoding added to tokens before attention? — A: Attention is order-blind without it; "dog bites man" would look identical to "man bites dog".
- **Done when:** candidates can state the role of Q, K, and V in one sentence each.

---

### Beat 1.5 — Multi-head attention and the Transformer block
- **Slides:** NEW slide: "Multi-head attention: specialized parallel perspectives"
- **Say:**
  - Rather than computing one set of attention weights, models run multiple "heads" in parallel (e.g., 8, 16, or 32 heads).
  - One head attends to grammatical syntax (subject-verb agreement). Another attends to semantic pronouns ("she" $\to$ "Priya"). Another attends to negations ("not", "never").
  - The Transformer block stacks: Multi-Head Attention $\to$ Add & Norm (residual connection) $\to$ Feed-Forward Network $\to$ Add & Norm.
  - Stacking 32 or 96 of these layers creates deep representational power.
- **Ask:**
  - Q: Why have multiple attention heads? — A: To capture different types of linguistic and semantic relationships simultaneously.
  - Q: What do residual (Add & Norm) connections prevent? — A: Vanishing gradients during backpropagation through deep layers.
- **Done when:** candidates can draw or describe the four main components of a Transformer block.

---

### Beat 1.6 — Pretraining, SFT, and RLHF
- **Slides:** NEW slide: "The 3 stages of modern LLMs: Pretraining → SFT → RLHF"
- **Say:**
  - **Stage 1 (Pretraining)**: Raw next-token prediction on 15+ trillion tokens. Builds knowledge and language structure.
  - **Stage 2 (Supervised Fine-Tuning - SFT)**: Trained on high-quality Question/Answer pairs so the model learns to answer questions rather than just continue text.
  - **Stage 3 (RLHF / DPO)**: Reinforcement Learning from Human Feedback aligns answers with safety, honesty, and helpfulness.
  - In Week 3, every API we call is already an instruction-tuned, aligned model.
- **Ask:**
  - Q: What happens if you prompt a raw base pretrained model with "How many vacation days do I get?" — A: It might generate more questions like "How many sick days? How do I apply?" instead of answering.
  - Q: What does SFT teach the base model? — A: The instruction-following conversation format.
- **Done when:** candidates can describe why base models need instruction tuning before being used in applications.

---

### Beat 1.7 — Hallucinations and the need for grounding
- **Slides:** NEW slide: "Where LLMs fail: hallucinations and temporal cutoff"
- **Say:**
  - LLMs have no internal database or factual verification engine — they produce fluent, plausible-sounding text.
  - **Hallucination**: Generating an authoritative-sounding statement that is factually incorrect.
  - Training data has a fixed knowledge cutoff; private corporate documents (like Meridian HR policies) were never in the training set.
  - This is the foundation for Week 3: We don't ask the LLM to memorize our policies; we build **RAG** to feed the exact policy chunks into the prompt context at runtime.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/tokenize -H "Content-Type: application/json" -d '{"text": "Meridian Solutions PTO carryover policy limits"}' | python3 -m json.tool
  ```
  **Point out:** The tokenizer can process the words, but the raw model has never seen Meridian's confidential intranet.
- **Ask:**
  - Q: Why can't we just rely on GPT-4's pretrained weights to know company vacation policy? — A: Company documents are private, proprietary, and change regularly.
  - Q: How does RAG solve hallucination? — A: It retrieves ground-truth document excerpts and constrains the model to answer only from those sources.
- **Done when:** candidates can articulate why enterprise AI requires external retrieval rather than relying on model memory.

---

## Exercise (candidates, ~25 min)
1. Open the Streamlit Tokenizer at `http://localhost:3000` (or use `POST /tokenize`).
2. Test how token counts change when tokenizing:
   - A normal sentence from `employee-handbook.md`.
   - The same sentence with ALL CAPS.
   - A code block with indentation.
3. Calculate the character-to-token ratio for each and record the differences in your notes.
4. Verify what happens when tokenizing an empty string (`""`) or very long repetition.

## Done-check
1. Explain what a token is and how it differs from a word.
2. State what $Q$, $K$, and $V$ do in attention mechanics.
3. Name the context window size of `gpt-4o-mini` and what occurs when exceeded.
4. Define hallucination and explain why private corporate data cannot be answered from pretraining.

## Clean-up
`scripts/setup.sh --reset`
