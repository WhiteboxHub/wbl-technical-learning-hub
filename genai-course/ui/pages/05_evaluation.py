import streamlit as st
import os
import httpx

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Module 5: Evaluation & Fine-Tuning", page_icon="⚖️", layout="wide")
st.title("⚖️ LLM Evaluation & Fine-Tuning Hub")
st.caption("Module 5: How to evaluate RAG quality (LLM-as-a-Judge) and choose between RAG vs. Fine-Tuning.")

tab_eval, tab_matrix, tab_lora = st.tabs([
    "🧑‍⚖️ LLM-as-a-Judge Evaluator",
    "📊 RAG vs Fine-Tuning Decision Matrix",
    "🔧 PEFT / LoRA Walkthrough"
])

# -----------------------------------------------------------------------------
# TAB 1: LLM-as-a-Judge
# -----------------------------------------------------------------------------
with tab_eval:
    st.subheader("Automated RAG Evaluation (The RAG Triad)")
    st.write(
        "Modern LLM systems use a secondary judge model (`gpt-4o-mini`) with a strict scoring prompt "
        "to grade answers on **Faithfulness** (groundedness in context) and **Answer Relevance** (addressing the prompt)."
    )

    presets = {
        "1. Faithful & Relevant (Ground-Truth Answer)": {
            "question": "What is the company match on the 401(k) plan and when does it vest?",
            "answer": "Meridian provides a 100% dollar-for-dollar match on employee 401(k) contributions up to 5% of eligible base salary. All employer matching contributions vest immediately upon deposit.",
            "context": "Meridian Solutions sponsors a safe-harbor 401(k) retirement savings plan through Vanguard. The company provides a 100% dollar-for-dollar match on employee contributions up to 5% of eligible base salary. All company matching contributions vest immediately on a 100% schedule from your first day of enrollment."
        },
        "2. Hallucinated / Fabricated Answer (Unfaithful)": {
            "question": "How many days of PTO do employees receive in year 1?",
            "answer": "Employees receive unlimited paid time off (PTO) with a mandatory minimum of 30 days off per year.",
            "context": "0 to 2 Years of Service: 15 days (120 hours) of combined Paid Time Off per calendar year, accrued semi-monthly at 5.0 hours per pay period. Unused PTO exceeding 10 days on December 31st will be forfeited."
        },
        "3. Off-Topic / Evasive Answer (Irrelevant)": {
            "question": "Can I work remotely from a coffee shop without a VPN?",
            "answer": "Meridian Solutions was founded in 2018 and has corporate offices in Austin, Chicago, and Seattle with on-site cafeterias.",
            "context": "Remote work from public spaces (coffee shops, airports, hotels) is strictly prohibited unless connected to the Meridian WireGuard corporate VPN with full-disk encryption enabled."
        }
    }

    selected_preset = st.selectbox("Load Test Scenario:", list(presets.keys()))
    preset = presets[selected_preset]

    col_q, col_a = st.columns(2)
    with col_q:
        q_text = st.text_input("User Question:", value=preset["question"])
    with col_a:
        a_text = st.text_area("Generated Answer to Grade:", value=preset["answer"], height=80)

    ctx_text = st.text_area("Retrieved Context Passage (Ground Truth):", value=preset["context"], height=100)

    if st.button("Run LLM-as-a-Judge Evaluation", type="primary"):
        with st.spinner("Judge model evaluating answer against context..."):
            try:
                with httpx.Client(timeout=15.0) as client:
                    res = client.post(f"{API_URL}/evaluate", json={
                        "question": q_text,
                        "answer": a_text,
                        "contexts": [ctx_text]
                    })
                    if res.status_code == 200:
                        eval_data = res.json()
                        faith = eval_data.get("faithfulness", 0.0)
                        relev = eval_data.get("relevance", 0.0)
                        reasoning = eval_data.get("reasoning", "")

                        st.markdown("---")
                        st.subheader("Judge Scorecard")
                        c1, c2 = st.columns(2)
                        
                        faith_status = "🟢 Fully Grounded" if faith >= 0.8 else ("🟡 Partially Supported" if faith >= 0.4 else "🔴 Hallucinated / Unfaithful")
                        relev_status = "🟢 Highly Relevant" if relev >= 0.8 else ("🟡 Weakly Relevant" if relev >= 0.4 else "🔴 Off-Topic")

                        c1.metric("Faithfulness Score", f"{faith:.2f}", faith_status)
                        c2.metric("Answer Relevance Score", f"{relev:.2f}", relev_status)

                        st.info(f"**Judge Reasoning:** {reasoning}")
                    else:
                        st.error(f"Evaluation API Error: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to evaluation API: {e}")

# -----------------------------------------------------------------------------
# TAB 2: RAG vs Fine-Tuning Matrix
# -----------------------------------------------------------------------------
with tab_matrix:
    st.subheader("Architectural Decision Matrix: RAG vs. Fine-Tuning")
    st.write(
        "A common industry mistake is fine-tuning a model when RAG was required (or vice versa). "
        "Use this matrix to make the right engineering tradeoff:"
    )

    st.markdown("""
| Dimension | Retrieval-Augmented Generation (RAG) | Supervised Fine-Tuning (PEFT/LoRA) |
| :--- | :--- | :--- |
| **Primary Goal** | **Knowledge Access**: Inject dynamic facts, documents, private policies. | **Form & Behavior**: Learn specialized syntax, tone, structured output, or dialect. |
| **Knowledge Recency** | Real-time (instant update upon document upsert to ChromaDB). | Static (frozen at training time; requires retraining to update facts). |
| **Hallucination Risk** | **Low**: Answers are constrained to cited context chunks. | **Medium-High**: Can still hallucinate facts confidently. |
| **Auditability** | **High**: Traceable via exact document citations `[1]`, `[2]`. | **Low**: Black-box neural network weights. |
| **Engineering Cost** | Low-to-moderate (Vector DB + Chunking pipeline). | High (curated dataset, GPU compute, LoRA rank tuning). |
| **Best Used For** | HR policies, customer support knowledgebases, legal discovery. | Emitting proprietary JSON schemas, clinical tone adaptation, code generation. |
""")

    st.success("💡 **Rule of Thumb**: Use **RAG** for facts and knowledge; use **Fine-Tuning** for style, tone, and format.")

# -----------------------------------------------------------------------------
# TAB 3: PEFT / LoRA Walkthrough
# -----------------------------------------------------------------------------
with tab_lora:
    st.subheader("Parameter-Efficient Fine-Tuning (PEFT) & LoRA")
    st.markdown("""
Instead of retraining all 2.7 Billion parameters of a model like **Phi-2**, **LoRA (Low-Rank Adaptation)** freezes the pretrained weights $W_0$ and trains low-rank decomposition matrices $A$ and $B$:
$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$

Where:
- $r$ is the rank (typically $8$ or $16$).
- Only **0.1% to 1%** of total parameters are trained, cutting VRAM requirements from 40GB+ down to a consumer GPU (8-16GB).
""")

    st.subheader("Included Code Walkthrough in the Repository")
    st.markdown("""
The repository includes three ready-to-run fine-tuning scripts in `api/finetuning/`:
1. `prepare_dataset.py`: Converts raw HR policies into instruction-tuning QA pairs (`{"instruction": "...", "response": "..."}`).
2. `train_lora.py`: Fine-tunes **Microsoft Phi-2** using Hugging Face `transformers`, `peft`, and `trl.SFTTrainer`.
3. `evaluate.py`: Benchmarks the base model vs. the fine-tuned adapter on enterprise policy extraction.
""")
