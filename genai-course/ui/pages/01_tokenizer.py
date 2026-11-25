import streamlit as st
import os
import httpx
import pandas as pd

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Module 1: Tokenizer", page_icon="🔤", layout="wide")
st.title("🔤 Tokenizer & Context Window Explorer")
st.caption("Module 1: How LLMs see language as tokens, not words.")

sample_texts = {
    "Tricky Capitalization": "ChatGPT vs chatgpt vs ChatGpt vs CHATGPT",
    "HR Sentence": "Priya Raman works in Human Resources at Meridian Solutions. She manages 12 specialists.",
    "Punctuation & Spaces": "Hello world!  Hello,world... 1234567890",
    "Code Snippet": "def calculate_pto(years: int) -> int: return 15 if years < 3 else 20",
}

tab_single, tab_compare = st.tabs(["📝 Interactive Tokenizer", "⚖️ Side-by-Side Comparison"])

with tab_single:
    selection = st.selectbox("Load sample text or type below:", list(sample_texts.keys()))
    user_text = st.text_area("Input text to tokenize:", value=sample_texts[selection], height=100)
    model_choice = st.selectbox("Select model encoding:", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "text-embedding-3-small"], key="single_model")

    if st.button("Tokenize Now", type="primary"):
        with st.spinner("Tokenizing..."):
            try:
                with httpx.Client(timeout=5.0) as client:
                    res = client.post(f"{API_URL}/tokenize", json={"text": user_text, "model": model_choice})
                    if res.status_code == 200:
                        data = res.json()
                        
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Token Count", data["token_count"])
                        c2.metric("Character Count", len(user_text))
                        ratio = len(user_text) / data["token_count"] if data["token_count"] > 0 else 0
                        c3.metric("Chars per Token", f"{ratio:.2f}")
                        c4.metric("Context Window", f"{data.get('context_limit', 128000):,} tokens")

                        st.markdown("---")
                        st.subheader("🎨 Subword Token Breakdown")
                        st.write("Each colored badge is an **individual token** passed to the Transformer attention heads:")
                        
                        # High-contrast badges with white text (works in both dark and light modes)
                        palette = [
                            ("#1D4ED8", "#93C5FD"),  # Blue
                            ("#B45309", "#FDE68A"),  # Amber
                            ("#047857", "#A7F3D0"),  # Emerald
                            ("#6D28D9", "#DDD6FE"),  # Purple
                            ("#B91C1C", "#FECACA"),  # Red
                            ("#0E7490", "#A5F3FC"),  # Cyan
                            ("#A21CAF", "#F5D0FE"),  # Fuchsia
                        ]
                        
                        html_tokens = []
                        table_data = []
                        for i, (tid, word) in enumerate(zip(data["tokens"], data["words"])):
                            bg_color, tag_color = palette[i % len(palette)]
                            clean_word = word.replace(" ", "␣").replace("\n", "↵")
                            
                            html_tokens.append(
                                f'<span style="display:inline-flex; align-items:center; margin:4px 3px; '
                                f'background-color:{bg_color}; color:#FFFFFF; padding:5px 10px; '
                                f'border-radius:6px; font-family:Consolas, Monaco, monospace; font-size:15px; '
                                f'box-shadow: 0 1px 3px rgba(0,0,0,0.2);">'
                                f'<span style="font-weight:700; letter-spacing:0.5px;">{clean_word}</span>'
                                f'<span style="background-color:rgba(255,255,255,0.22); color:#FFFFFF; '
                                f'margin-left:8px; padding:1px 6px; border-radius:4px; font-size:12px; font-weight:600;">'
                                f'{tid}</span>'
                                f'</span>'
                            )
                            
                            table_data.append({
                                "Token #": i + 1,
                                "Subword Text": repr(word)[1:-1],  # reveals leading spaces
                                "Token ID": tid,
                                "Char Length": len(word),
                            })
                            
                        st.markdown(f'<div style="line-height:2.2; margin-bottom:15px;">{"".join(html_tokens)}</div>', unsafe_allow_html=True)
                        st.caption("␣ denotes a leading space token.")
                        
                        st.markdown("---")
                        st.subheader("📋 Token Detail Table")
                        st.dataframe(pd.DataFrame(table_data), use_container_width=True)
                        
                        st.markdown("---")
                        st.subheader("🔢 Raw Token IDs Array (Model Input)")
                        st.code(str(data["tokens"]))
                    else:
                        st.error(f"Error {res.status_code}: {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")

with tab_compare:
    st.subheader("⚖️ Side-by-Side Comparison (BPE Case & Wording)")
    st.write("Compare how capitalization, spelling, or phrasing changes token count and splits:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        cmp_text_a = st.text_input("Input A (e.g. Title Case):", value="ChatGPT")
    with col_b:
        cmp_text_b = st.text_input("Input B (e.g. Lower Case):", value="chatgpt")
        
    cmp_model = st.selectbox("Model Encoding:", ["gpt-4o-mini", "gpt-4o"], key="compare_model")
    
    if st.button("Compare Splits", type="primary"):
        with st.spinner("Analyzing both strings..."):
            try:
                with httpx.Client(timeout=5.0) as client:
                    res_a = client.post(f"{API_URL}/tokenize", json={"text": cmp_text_a, "model": cmp_model})
                    res_b = client.post(f"{API_URL}/tokenize", json={"text": cmp_text_b, "model": cmp_model})
                    
                    if res_a.status_code == 200 and res_b.status_code == 200:
                        data_a = res_a.json()
                        data_b = res_b.json()
                        
                        ca, cb = st.columns(2)
                        with ca:
                            st.markdown(f"### 🔠 '{cmp_text_a}'")
                            st.metric("Total Tokens", data_a["token_count"])
                            st.write("**Subwords & IDs:**")
                            for i, (tid, word) in enumerate(zip(data_a["tokens"], data_a["words"])):
                                st.info(f"Token {i+1}: `{repr(word)}` (ID: `{tid}`)")
                                
                        with cb:
                            st.markdown(f"### 🔡 '{cmp_text_b}'")
                            st.metric("Total Tokens", data_b["token_count"])
                            st.write("**Subwords & IDs:**")
                            for i, (tid, word) in enumerate(zip(data_b["tokens"], data_b["words"])):
                                st.warning(f"Token {i+1}: `{repr(word)}` (ID: `{tid}`)")
                                
                        st.markdown("---")
                        diff = data_b["token_count"] - data_a["token_count"]
                        if diff != 0:
                            st.write(f"💡 **Insight**: `{cmp_text_b}` requires **{abs(diff)} {'more' if diff > 0 else 'fewer'} tokens** than `{cmp_text_a}` because BPE has specialized tokens for common capitalizations like `Chat` and `GPT`!")
                        else:
                            st.write("💡 Both produce the same total token count, but check the subword boundaries!")
                    else:
                        st.error("API error during comparison.")
            except Exception as e:
                st.error(f"Error: {e}")
