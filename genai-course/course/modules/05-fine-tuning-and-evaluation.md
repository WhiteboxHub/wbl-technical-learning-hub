# Module 5 — Fine-Tuning and LLM Evaluation

Teach-skill content file. Format is described in `.claude/skills/teach-genai-class/SKILL.md`.
Deck: no slides yet. **NEW slide** = teach from the "Say" points and the demo.
Stack: RAG API at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 90 minutes with demos and questions.
Story anchor: **The apprenticeship and the exam board: one shapes behaviour, the other proves it.**

## Objectives
By the end, candidates can apply the Prompt vs RAG vs Fine-Tuning decision matrix, explain Parameter-Efficient Fine-Tuning (PEFT/LoRA) mechanics, inspect training dataset formats (JSONL), and build a regression evaluation suite for production models.

---

### Beat 5.1 — The enterprise decision matrix: Prompt vs RAG vs Fine-Tune
- **Slides:** NEW slide: "Prompt vs RAG vs Fine-Tune: the decision that saves budgets"
- **Say:**
  - The single most common mistake in enterprise AI is jumping to fine-tuning when prompt engineering or RAG is what is needed.
  - **Prompt Engineering**: Fast (minutes), zero training cost. Best for format control, tone, role-playing, and few-shot classification.
  - **RAG (Retrieval-Augmented Generation)**: Best for factual enterprise knowledge that updates frequently (policies, manuals, tickets). Prevents hallucinations.
  - **Fine-Tuning**: Trains the actual neural network weights. Best for teaching a specialized style, unique dialect, non-standard syntax (code, SQL dialects), or shrinking large models to run on-device.
  - **The Budget Rule**: "Prompt first. If you need dynamic facts, add RAG. Only fine-tune if you need specialized behavior that RAG and prompting cannot deliver."
- **Ask:**
  - Q: A company wants an AI assistant to answer questions about next week's updated travel policy. Fine-tune or RAG? — A: RAG. Policies change constantly; fine-tuning would bake in outdated facts and require retraining weekly.
  - Q: A company wants their model to consistently output valid HL7 medical records format without complex instructions. Fine-tune or RAG? — A: Fine-tune. It teaches specialized syntax and behavior.
- **Done when:** candidates can defend their choice among Prompting, RAG, and Fine-Tuning for three real-world cases.

---

### Beat 5.2 — Fine-tuning mechanics: full training vs LoRA (PEFT)
- **Slides:** NEW slide: "Parameter-Efficient Fine-Tuning (PEFT) and LoRA"
- **Say:**
  - A modern LLM has billions of parameters (e.g. 7B, 70B). Full fine-tuning updates every weight matrix $W$, requiring hundreds of gigabytes of VRAM and massive GPU clusters.
  - **LoRA (Low-Rank Adaptation)**:
    - Freezes the original pretrained weight matrix $W \in \mathbb{R}^{d \times k}$.
    - Decomposes the weight update $\Delta W$ into two low-rank matrices: $A \in \mathbb{R}^{d \times r}$ and $B \in \mathbb{R}^{r \times k}$, where rank $r \ll d$ (e.g., $r = 8$ or $16$).
    - $W_{\text{new}} = W_{\text{frozen}} + B \times A$.
  - Only $A$ and $B$ are trained! Reduces trainable parameters by $>99\%$, making fine-tuning possible on a single consumer GPU.
- **Demo (run: instructor):**
  Open `api/finetuning/train_lora.py` and point out the `LoraConfig(r=8, lora_alpha=32, target_modules=["Wqkv", "out_proj"])`. Show how rank $r=8$ creates a tiny adapter that sits beside frozen weights.
- **Ask:**
  - Q: Why is LoRA called "parameter-efficient"? — A: Because it trains less than 1% of the model's total weights by adding low-rank adapter matrices.
  - Q: Can you swap LoRA adapters at runtime? — A: Yes! The base model remains frozen; different adapters can be plugged in for coding, legal, or customer service tasks.
- **Done when:** candidates can explain the math intuition behind LoRA rank $r$.

---

### Beat 5.3 — The fine-tuning dataset: format and quality
- **Slides:** NEW slide: "Data curation: quality over quantity in instruction tuning"
- **Say:**
  - Pretraining takes trillions of tokens; fine-tuning requires only 500 to 5,000 extremely high-quality examples.
  - "Garbage in, garbage out": Ten flawed training examples will permanently damage the model's output quality.
  - Standard format: JSONL files containing prompt/completion pairs or conversational messages arrays.
- **Demo (run: agent):**
  ```bash
  python3 api/finetuning/prepare_dataset.py
  head -n 2 data/finetune_dataset.jsonl | python3 -m json.tool
  ```
  **Point out:** Inspect the JSONL structure. Each line is an independent JSON object with explicit prompt and completion pairs extracted from the HR policy documents.
- **Ask:**
  - Q: Why is 1,000 high-quality curated examples better than 100,000 scraped examples for fine-tuning? — A: Low-quality data introduces inconsistent formatting, hallucinations, and conflicting instructions directly into the weights.
- **Done when:** candidates can inspect and validate a JSONL fine-tuning dataset.

---

### Beat 5.4 — Walkthrough of the LoRA training script
- **Slides:** NEW slide: "The fine-tuning training loop (code walkthrough)"
- **Say:**
  - In class, we walk through the training script rather than running a multi-hour GPU training job.
  - Key steps in `api/finetuning/train_lora.py`:
    1. Load base model tokenizer.
    2. Configure LoRA adapter with target attention modules.
    3. Wrap base model with `get_peft_model()`.
    4. Run training loop using HuggingFace SFTTrainer.
    5. Save the lightweight adapter weights (typically only 50–100MB!).
- **Demo (run: instructor):**
  Run `python3 api/finetuning/train_lora.py` to show the pre-flight checks and configuration summary.
- **Ask:**
  - Q: Why is this script not executed live during class? — A: LLM fine-tuning requires dedicated GPUs and takes hours to converge; the skill is in architecture and evaluation.
- **Done when:** candidates can identify the 5 steps in a PEFT fine-tuning script.

---

### Beat 5.5 — Automated evaluation: LLM-as-a-judge
- **Slides:** NEW slide: "LLM-as-a-Judge: automated scoring with strict rubrics"
- **Say:**
  - Human evaluation of 5,000 responses is too slow and expensive. Traditional NLP metrics (BLEU, ROUGE) only check word overlap and fail on semantic equivalence.
  - **LLM-as-a-Judge**: Using a capable model (like GPT-4o) with a detailed rubric to evaluate candidate outputs.
  - Known biases of LLM judges to watch out for:
    - **Verbosity bias**: Tendency to favor longer, wordier answers.
    - **Position bias**: In side-by-side comparisons, favoring whichever answer is presented first.
    - **Self-enhancement bias**: Models slightly favor outputs generated by their own family.
- **Demo (run: agent):**
  ```bash
  curl -s -X POST http://localhost:8000/evaluate -H "Content-Type: application/json" -d '{
    "question": "What happens if an employee works remotely from a coffee shop without VPN?",
    "answer": "They will receive a $500 bonus.",
    "contexts": ["Working from public Wi-Fi networks without an active Meridian VPN session is strictly prohibited."]
  }' | python3 -m json.tool
  ```
  **Point out:** Faithfulness drops to `0.0`. The judge identifies that the answer directly contradicts the policy context.
- **Ask:**
  - Q: Why do BLEU and ROUGE fail for evaluating modern RAG answers? — A: They only measure exact n-gram word overlaps; an answer with identical meaning using synonyms scores poorly.
  - Q: How do you mitigate verbosity bias in an LLM judge? — A: Give explicit grading criteria and penalties for unnecessary filler text.
- **Done when:** candidates can run and interpret an LLM-as-a-judge evaluation call.

---

### Beat 5.6 — Building a regression evaluation suite
- **Slides:** NEW slide: "Regression test suites: never ship an untested prompt or model"
- **Say:**
  - In software engineering, you never ship code without unit tests. In AI engineering, you never change a prompt, model, or chunk size without running your **evaluation benchmark**.
  - A regression suite consists of:
    - 50 to 200 representative test questions.
    - Ground truth reference answers.
    - Automated scoring for Faithfulness and Relevance.
  - If a prompt edit increases latency or drops faithfulness by 3%, the CI/CD pipeline blocks the release.
- **Demo (run: agent):**
  ```bash
  python3 api/finetuning/evaluate.py
  ```
  **Point out:** Shows the benchmark table comparing generic model outputs vs grounded answers across 4 core policy questions.
- **Ask:**
  - Q: What constitutes a "regression" in an LLM application? — A: When an update improves one capability but degrades accuracy, tone, or faithfulness on existing test cases.
- **Done when:** candidates can design a test benchmark for an enterprise AI system.

---

### Beat 5.7 — The course journey recap
- **Slides:** NEW slide: "From Tokens to RAG: Week 3 AM in review"
- **Say:**
  - Monday: We took apart the token and looked inside attention ($Q, K, V$).
  - Tuesday: We learned to talk to the model with system prompts, parameters, and few-shot patterns.
  - Wednesday: We turned language into geometry with embeddings, chunking, and ChromaDB.
  - Thursday: We assembled the complete end-to-end RAG system with citations and abstention.
  - Friday: We learned how to judge models, when to fine-tune, and how to verify quality with evaluation suites.
  - **Looking Ahead to PM**: In the afternoon sessions, this RAG system becomes **Tool #1** inside an autonomous **LangGraph agent** that can plan, execute, and collaborate.
- **Done when:** candidates can summarize the 5-day GenAI journey in under two minutes.

---

## Exercise (candidates, ~25 min)
1. Write 5 diverse evaluation questions covering Meridian HR policies:
   - 2 straightforward factual questions.
   - 1 complex multi-step question.
   - 2 trick/adversarial questions intended to test abstention.
2. Run each question through `POST /generate`.
3. Score each output with `POST /evaluate` and record the faithfulness and relevance scores in your candidate notes.

## Done-check
1. State the Prompt vs RAG vs Fine-Tune decision rule.
2. Explain how LoRA reduces trainable parameter count.
3. Inspect the JSONL training format in `data/finetune_dataset.jsonl`.
4. Name two biases of LLM-as-a-judge and how to mitigate them.

## Clean-up
`scripts/setup.sh --reset`
