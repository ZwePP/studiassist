"""
AI Study Assistant - Streamlit Frontend
Clean interface for students to ask subject questions.
"""

import streamlit as st
import requests

# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { max-width: 700px; margin: 0 auto; }

    .answer-box {
        background: #000;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        white-space: pre-wrap;
        line-height: 1.7;
    }

    .meta-tag {
        display: inline-block;
        background: #e0e7ff;
        color: #3730a3;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin-right: 6px;
    }

    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }

    .stButton > button:hover { background: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📚 AI Study Assistant")
st.caption("Ask any academic question — powered by Claude AI")
st.divider()

# ── Check API health ─────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_api():
    try:
        r = requests.get(f"{API_URL}/", timeout=3)
        return r.status_code == 200
    except:
        return False

if not check_api():
    st.error("⚠️ Backend is not running. Start it with: `uvicorn backend:app --reload`")
    st.stop()

# ── Input Form ───────────────────────────────────────────────────────────────
SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology",
            "Computer Science", "Business", "Economics", "Literature"]

col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("📖 Subject", SUBJECTS)
with col2:
    level = st.selectbox("🎓 Level", ["High School", "Undergraduate", "Graduate"])

question = st.text_area(
    "Your Question",
    placeholder="e.g. Explain the difference between supervised and unsupervised learning.",
    height=110
)

ask_btn = st.button("Ask AI ✨", use_container_width=True)

# ── History ──────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Submit ───────────────────────────────────────────────────────────────────
if ask_btn:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                with requests.post(
                    f"{API_URL}/ask",
                    json={"subject": subject, "question": question, "level": level},
                    stream=True,
                    timeout=30
                ) as response:
                    if response.status_code == 200:
                        answer = ""
                        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                            if chunk:
                                answer += chunk
                        st.session_state.history.insert(0, {
                            "subject": subject, "level": level,
                            "question": question, "answer": answer, "tokens": "—"
                        })
                    else:
                        st.error(f"API error {response.status_code}: {response.json().get('detail')}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Is it running?")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
# ── Clear History ─────────────────────────────────────────────────────────────
if st.session_state.history:
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# ── Display Results ──────────────────────────────────────────────────────────
if st.session_state.history:
    st.divider()
    for i, item in enumerate(st.session_state.history):
        with st.container():
            st.markdown(
                f'<span class="meta-tag">{item["subject"]}</span>'
                f'<span class="meta-tag">{item["level"]}</span>'
                f'<span class="meta-tag">~{item["tokens"]} tokens</span>',
                unsafe_allow_html=True
            )
            st.markdown(f"**Q:** {item['question']}")
            st.markdown(
                f'<div class="answer-box">{item["answer"]}</div>',
                unsafe_allow_html=True
            )
            if i < len(st.session_state.history) - 1:
                st.divider()
