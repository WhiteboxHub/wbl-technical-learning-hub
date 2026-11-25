import streamlit as st
import os
import httpx

API_URL = os.getenv("API_BASE_URL", "http://api:8000")

st.set_page_config(page_title="Module 3: Chunking", page_icon="✂️", layout="wide")
st.title("✂️ Chunking Strategies Visualizer")
st.caption("Module 3: How chunk size, overlap, and splitting strategies shape retrieval.")

sample_doc = """# Meridian Solutions — Paid Time Off (PTO) & Leave Policy

## 1. PTO Accrual Schedule
Meridian provides combined Paid Time Off (PTO) covering vacation, personal days, and wellness time. PTO accrues semi-monthly starting from your first day of employment.

- 0 to 2 Years of Service: 15 days (120 hours) per calendar year, accrued at 5.0 hours per pay period.
- 3 to 5 Years of Service: 20 days (160 hours) per calendar year, accrued at 6.67 hours per pay period.
- 6+ Years of Service: 25 days (200 hours) per calendar year, accrued at 8.33 hours per pay period.

## 2. PTO Carry-Over & Payout
Up to 10 days (80 hours) of unused accrued PTO can be rolled over into the following calendar year. Any accrued PTO exceeding 10 days on December 31st will be forfeited. Accrued, unused PTO is paid out in full on the final paycheck upon separation of employment.

## 3. Sick Leave & Medical Appointments
Meridian provides 10 dedicated paid Sick Days (80 hours) per year, allocated on January 1st. Sick leave does not accrue and is separate from PTO. Absences exceeding 3 consecutive business days require a medical note from a licensed healthcare provider."""

input_text = st.text_area("Document to chunk:", value=sample_doc, height=220)

col1, col2, col3 = st.columns(3)
strategy = col1.selectbox("Chunking Strategy:", ["recursive", "fixed", "sentence"])
chunk_size = col2.slider("Chunk Size (tokens):", min_value=30, max_value=500, value=80, step=10)
chunk_overlap = col3.slider("Chunk Overlap (tokens):", min_value=0, max_value=100, value=15, step=5)

if st.button("Chunk Document", type="primary"):
    with st.spinner("Processing chunks..."):
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.post(f"{API_URL}/chunk", json={
                    "text": input_text,
                    "strategy": strategy,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap
                })
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Produced **{data['total_chunks']} chunks** using `{data['strategy']}` strategy.")
                    
                    for i, chunk_info in enumerate(data["chunks"]):
                        with st.expander(f"Chunk #{i+1} — {chunk_info['token_count']} tokens (Chars {chunk_info['char_start']} to {chunk_info['char_end']})"):
                            st.text(chunk_info["text"])
                else:
                    st.error(f"Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Failed to chunk: {e}")
