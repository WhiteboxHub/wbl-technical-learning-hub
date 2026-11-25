import streamlit as st
import os
import httpx

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Module 4: RAG Chat", page_icon="🛡️", layout="wide")
st.title("🛡️ RAG Policy Assistant & Grounding Inspector")
st.caption("Module 4: Retrieval-Augmented Generation over Meridian Solutions HR Documents.")

st.sidebar.subheader("RAG Parameters")
n_results = st.sidebar.slider("Number of Chunks to Retrieve:", min_value=1, max_value=5, value=3)
temperature = st.sidebar.slider("Generation Temperature:", min_value=0.0, max_value=1.5, value=0.2, step=0.1)

sample_queries = [
    "How many days of PTO do I get after 2 years?",
    "What is the company match on the 401(k) plan?",
    "Can I work remotely from a coffee shop without VPN?",
    "What is the capital of Mars? (Test Abstention)"
]

query_pick = st.selectbox("Sample questions:", sample_queries)
user_query = st.text_input("Or enter your question:", value=query_pick)

if st.button("Ask Assistant (Run RAG)", type="primary"):
    with st.spinner("Running RAG pipeline (embed -> retrieve -> generate)..."):
        try:
            with httpx.Client(timeout=15.0) as client:
                res = client.post(f"{API_URL}/generate", json={
                    "query": user_query,
                    "n_results": n_results,
                    "temperature": temperature
                })
                if res.status_code == 200:
                    data = res.json()
                    
                    if data["abstained"]:
                        st.warning("⚠️ **Model Abstained** (Confidence below threshold or out-of-domain)")
                    else:
                        st.success("✅ **Grounded Answer Generated**")

                    st.markdown("### Generated Answer")
                    st.write(data["answer"])

                    st.markdown("### Cited Sources")
                    if data["sources"]:
                        st.info(f"Sources referenced: {', '.join(data['sources'])}")
                    else:
                        st.caption("No explicit document citations detected.")

                    st.markdown("### Retrieved Chunks Inspection (Context passed to LLM)")
                    for i, chunk in enumerate(data.get("retrieved_chunks", [])):
                        with st.expander(f"Chunk [{i+1}] — Source: {chunk.get('document_id')} | Similarity: {chunk.get('score')}"):
                            st.write(chunk.get("text"))
                else:
                    st.error(f"API Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Error querying RAG API: {e}")
