import streamlit as st
import os
import httpx

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(
    page_title="GenAI & RAG Visual Explorer",
    layout="wide",
)

st.title("GenAI & RAG Visual Explorer")
st.markdown("""
Welcome to the **Week 3 AM: Generative AI & RAG** interactive learning workspace.
This dashboard connects directly to the course **FastAPI RAG backend** and **ChromaDB vector store**.
""")

st.subheader("System Health & Status")
col1, col2, col3 = st.columns(3)

try:
    with httpx.Client(timeout=3.0) as client:
        resp = client.get(f"{API_URL}/health")
        if resp.status_code == 200:
            health = resp.json()
            col1.metric("API Status", "Healthy" if health.get("status") == "ok" else "Error")
            col2.metric("ChromaDB Status", "Connected" if health.get("chroma") == "ok" else "Disconnected")
            col3.metric("OpenAI API Key", "Configured" if health.get("openai") == "ok" else "Missing Key")
        else:
            st.error(f"API responded with status code: {resp.status_code}")
except Exception as e:
    st.error(f"Cannot reach RAG API at `{API_URL}`. Make sure Docker is running.")
    st.caption(f"Error detail: {e}")

st.markdown("---")
st.subheader("Interactive Lab Modules")
st.markdown("""
Navigate through the sidebar pages to test each layer of the GenAI stack:
1. **01 Tokenizer**: See subword splits, token counts, and context limits live.
2. **02 Embeddings**: Calculate cosine similarity and plot semantic coordinates.
3. **03 Chunker**: Compare fixed-size, recursive, and sentence chunking strategies side by side.
4. **04 RAG Chat**: Ask questions against Meridian Solutions HR policies, observe retrieved chunks, and test abstention.
5. **05 Evaluation & Fine-Tuning**: Test automated LLM-as-a-Judge scoring (faithfulness & relevance) and explore RAG vs Fine-Tuning trade-offs.
""")
