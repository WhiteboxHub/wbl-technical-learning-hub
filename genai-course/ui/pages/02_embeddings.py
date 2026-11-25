import streamlit as st
import os
import httpx
import math

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Module 3: Embeddings", page_icon="❖", layout="wide")
st.title("❖ Embeddings & Cosine Similarity")
st.caption("Module 3: Meaning as coordinates in high-dimensional vector space.")

st.markdown("""
Compare semantic similarity between pairs of sentences using **text-embedding-3-small** (1,536 dimensions).
""")

col1, col2 = st.columns(2)
text_a = col1.text_input("Sentence A:", value="How many vacation days do new hires receive?")
text_b = col2.text_input("Sentence B:", value="What is the annual PTO accrual for first-year employees?")

text_c = st.text_input("Sentence C (for contrast):", value="How do I connect to the corporate WireGuard VPN?")

if st.button("Compute Embeddings & Compare Similarity", type="primary"):
    with st.spinner("Generating embeddings via OpenAI..."):
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.post(f"{API_URL}/embed", json={"texts": [text_a, text_b, text_c]})
                if res.status_code == 200:
                    data = res.json()
                    vecs = data["embeddings"]
                    
                    def cos_sim(v1, v2):
                        dot = sum(x * y for x, y in zip(v1, v2))
                        mag1 = math.sqrt(sum(x ** 2 for x in v1))
                        mag2 = math.sqrt(sum(x ** 2 for x in v2))
                        return dot / (mag1 * mag2) if mag1 and mag2 else 0.0

                    sim_ab = cos_sim(vecs[0], vecs[1])
                    sim_ac = cos_sim(vecs[0], vecs[2])
                    sim_bc = cos_sim(vecs[1], vecs[2])

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Similarity (A vs B) - Same Concept", f"{sim_ab:.4f}")
                    c2.metric("Similarity (A vs C) - Unrelated", f"{sim_ac:.4f}")
                    c3.metric("Similarity (B vs C) - Unrelated", f"{sim_bc:.4f}")

                    st.info(f"Generated {len(vecs)} vectors with {data['dimensions']} dimensions using `{data['model']}`.")
                    
                    st.subheader("First 10 Dimensions of Vector A:")
                    st.code(str([round(x, 5) for x in vecs[0][:10]]))
                else:
                    st.error(f"API Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Error calling API: {e}")
