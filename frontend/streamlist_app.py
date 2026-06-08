"""
AI Study Assistant - Streamlit Frontend
Tabs: Study (RAG chat + upload), Quiz (gamified), Dashboard (performance)
"""

import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

/* === Base === */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', system-ui, sans-serif !important;
}
[data-testid="block-container"] {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Bordered container cards */
[data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlockBorderWrapper"] {
    background: #161c2a;
    border: 1px solid rgba(148,163,184,0.09);
    border-radius: 10px;
    padding: 14px 16px;
}

/* Buttons */
.stButton > button {
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13.5px !important;
    border: none !important;
    padding: 10px 16px !important;
    background: #6366f1 !important;
    color: white !important;
    transition: background 0.15s, opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.88 !important; background: #4f46e5 !important; }

/* Selectboxes */
[data-baseweb="select"] > div {
    border-radius: 6px !important;
    background: #1d2436 !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
}

/* Text inputs and textareas */
textarea, [data-baseweb="input"] input {
    border-radius: 6px !important;
    background: #1d2436 !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1d2436;
    border-radius: 8px;
    border: 1.5px dashed rgba(148,163,184,0.2);
    padding: 8px;
}

/* Tabs */
[data-baseweb="tab-list"] {
    border-bottom: 1px solid rgba(148,163,184,0.09) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-weight: 500 !important;
    font-size: 13.5px !important;
    padding: 10px 20px !important;
}

/* Divider */
hr { border-color: rgba(148,163,184,0.09) !important; }

/* Alerts */
[data-testid="stAlert"] { border-radius: 8px !important; }

/* === Custom classes used by the app === */
.answer-box {
    background: #0f172a;
    color: #e2e8f0;
    border-left: 3px solid #6366f1;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-top: 0.5rem;
    white-space: pre-wrap;
    line-height: 1.8;
    font-size: 0.92rem;
}
.meta-tag {
    display: inline-block;
    background: #1e1b4b;
    color: #a5b4fc;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    margin-right: 6px;
    font-family: 'DM Sans', sans-serif;
}
.rag-pill {
    display: inline-block;
    background: rgba(34,197,94,0.12);
    color: #4ade80;
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 500;
}
.rag-session {
    color: #4ade80;
    font-size: 0.78rem;
    font-weight: 500;
}
.rag-session::before {
    content: "● ";
    color: #4ade80;
}
.file-name {
    color: #e2e8f0;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 4px;
}
.quiz-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.score-big {
    font-size: 3.5rem;
    font-weight: 700;
    color: #6366f1;
    font-family: 'DM Sans', sans-serif;
}
.stat-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-num {
    font-size: 2rem;
    font-weight: 700;
    color: #6366f1;
    font-family: 'DM Sans', sans-serif;
}
.badge {
    display: inline-block;
    font-size: 1.6rem;
    margin: 0.2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for key, val in {
    "history": [], "session_id": "", "filename": "", "files": [],
    "quiz": [], "quiz_answers": {}, "quiz_submitted": False,
    "sessions": []  # list of {date, subject, score, total, xp}
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── API health ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_api():
    try:
        return requests.get(f"{API_URL}/", timeout=3).status_code == 200
    except:
        return False

if not check_api():
    st.error("⚠️ Backend offline. Run: `uvicorn backend:app --reload`")
    st.stop()

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology",
            "Computer Science", "History", "Economics", "Literature"]

BADGES = {
    100: ("🏆", "Perfect Score"),
    80:  ("🥇", "Gold"),
    60:  ("🥈", "Silver"),
    40:  ("🥉", "Bronze"),
    0:   ("📚", "Keep Studying"),
}

def get_badge(pct):
    for threshold, badge in BADGES.items():
        if pct >= threshold:
            return badge
    return BADGES[0]

def xp_for_score(correct, total):
    pct = (correct / total * 100) if total else 0
    return int(pct * 2)

# ── Header ────────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 📚 AI Study Assistant")
    st.caption("Upload lecture slides · Get summaries · Take quizzes · Track progress")
with col_h2:
    total_xp = sum(s.get("xp", 0) for s in st.session_state.sessions)
    st.markdown(f"""
    <div class="stat-card" style="margin-top:0.5rem">
        <div style="font-size:0.75rem;color:#64748b;margin-bottom:4px">TOTAL XP</div>
        <div class="stat-num">⚡ {total_xp}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_study, tab_quiz, tab_dashboard = st.tabs(["📖 Study", "🎯 Quiz", "📊 Dashboard"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1: STUDY
# ════════════════════════════════════════════════════════════════════════════
with tab_study:
    col_left, col_right = st.columns([1, 2])

    with col_left:
        with st.container(border=True):
            st.markdown("##### ⚙️ Settings")
            subject = st.selectbox("Subject", SUBJECTS)
            level   = st.selectbox("Level", ["High School", "Undergraduate", "Graduate"])

        with st.container(border=True):
            st.markdown("##### 📄 Lecture Slides")
            uploaded = st.file_uploader(
                "Upload PDF or PPTX",
                type=["pdf", "pptx"],
                accept_multiple_files=True,
                label_visibility="collapsed",
            )

            if uploaded:
                label = "📤 Process Files" if len(uploaded) > 1 else "📤 Process File"
                if st.button(label, use_container_width=True):
                    with st.spinner(f"Reading {len(uploaded)} file(s)..."):
                        payload = [
                            ("files", (f.name, f.read(), "application/octet-stream"))
                            for f in uploaded
                        ]
                        r = requests.post(f"{API_URL}/api/upload", files=payload)
                        if r.status_code == 200:
                            d = r.json()
                            st.session_state.session_id = d["session_id"]
                            st.session_state.filename   = d["filename"]
                            st.session_state.files      = d.get("files", [d["filename"]])
                            st.success(f"✅ Loaded: {d['filename']} ({d['chunks']} chunks)")
                        else:
                            try:
                                detail = r.json().get("detail", "Upload failed.")
                            except Exception:
                                detail = "Upload failed."
                            st.error(detail)

            if st.session_state.filename:
                files_list = st.session_state.get("files") or [st.session_state.filename]
                files_html = "<br>".join(f'<div class="file-name">📄 {n}</div>' for n in files_list)
                st.markdown(
                    f'{files_html}<div class="rag-session">RAG session active</div>',
                    unsafe_allow_html=True,
                )
                if st.button("📝 Summarize Slides", use_container_width=True):
                    with st.spinner("Summarizing..."):
                        r = requests.post(
                            f"{API_URL}/api/summarize",
                            params={
                                "session_id": st.session_state.session_id,
                                "subject": subject,
                                "level": level,
                            },
                            timeout=60,
                        )
                        if r.status_code == 200:
                            summary = r.json()["summary"]
                            st.session_state.history.insert(0, {
                                "subject": subject, "level": level,
                                "question": f"📝 Summary of: {st.session_state.filename}",
                                "answer": summary,
                            })
                        else:
                            try:
                                detail = r.json().get("detail", r.text)
                            except Exception:
                                detail = r.text or f"HTTP {r.status_code}"
                            st.error(f"Summarization failed: {detail}")

    with col_right:
        with st.container(border=True):
            h1, h2 = st.columns([3, 1])
            with h1:
                st.markdown("##### 💬 Ask a Question")
            with h2:
                if st.session_state.filename:
                    st.markdown(
                        '<div style="text-align:right;padding-top:6px">'
                        '<span class="rag-pill">● RAG Active</span></div>',
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f'<span class="meta-tag">📘 {subject}</span>'
                f'<span class="meta-tag">🎓 {level}</span>',
                unsafe_allow_html=True,
            )

            question = st.text_area(
                "Your question", height=100, label_visibility="collapsed",
                placeholder="e.g. What are the key concepts from today's lecture?",
            )

            c1, c2 = st.columns([4, 1])
            ask_btn   = c1.button("Ask AI ✨", use_container_width=True)
            clear_btn = c2.button("🗑️ Clear", use_container_width=True)

        if clear_btn:
            st.session_state.history = []
            st.rerun()

        if ask_btn:
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        r = requests.post(
                            f"{API_URL}/api/ask",
                            json={"subject": subject, "question": question,
                                  "level": level,
                                  "session_id": st.session_state.session_id},
                            timeout=60,
                        )
                        if r.status_code == 200:
                            st.session_state.history.insert(0, {
                                "subject": subject, "level": level,
                                "question": question, "answer": r.text,
                            })
                        else:
                            st.error(f"Error: {r.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Chat history
        for i, item in enumerate(st.session_state.history):
            with st.container(border=True):
                st.markdown(
                    f'<span class="meta-tag">📘 {item["subject"]}</span>'
                    f'<span class="meta-tag">🎓 {item["level"]}</span>',
                    unsafe_allow_html=True)
                st.markdown(f"**Q:** {item['question']}")
                st.markdown(f'<div class="answer-box">{item["answer"]}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2: QUIZ
# ════════════════════════════════════════════════════════════════════════════
with tab_quiz:
    q_col1, q_col2 = st.columns([1, 2])

    with q_col1:
        st.markdown("#### 🎯 Quiz Settings")
        q_subject = st.selectbox("Subject ", SUBJECTS, key="q_sub")
        q_level   = st.selectbox("Level ", ["High School", "Undergraduate", "Graduate"], key="q_lvl")
        q_count   = st.slider("Number of questions", 3, 30, 5)
        use_pdf   = st.checkbox("Use uploaded lecture slides", value=bool(st.session_state.filename))

        if st.button("🎲 Generate Quiz", use_container_width=True):
            with st.spinner("Generating quiz..."):
                r = requests.post(f"{API_URL}/api/quiz", json={
                    "session_id": st.session_state.session_id if use_pdf else "",
                    "subject": q_subject, "level": q_level, "num_questions": q_count
                })
                if r.status_code == 200:
                    st.session_state.quiz          = r.json()["quiz"]
                    st.session_state.quiz_answers  = {}
                    st.session_state.quiz_submitted = False
                else:
                    try:
                        detail = r.json().get("detail", r.text)
                    except Exception:
                        detail = r.text or f"HTTP {r.status_code}"
                    st.error(f"Quiz generation failed: {detail}")

    with q_col2:
        if not st.session_state.quiz:
            st.info("👈 Configure and generate a quiz to begin.")
        else:
            if not st.session_state.quiz_submitted:
                st.markdown("#### 📝 Answer All Questions")
                with st.form("quiz_form"):
                    for i, q in enumerate(st.session_state.quiz):
                        st.markdown(f'<div class="quiz-card"><b>Q{i+1}. {q["question"]}</b></div>',
                                    unsafe_allow_html=True)
                        choice = st.radio("", q["options"], key=f"q_{i}",
                                          label_visibility="collapsed")
                        st.session_state.quiz_answers[i] = choice
                        st.markdown("")

                    submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True)

                if submitted:
                    st.session_state.quiz_submitted = True
                    st.rerun()

            else:
                # Results
                correct = sum(
                    1 for i, q in enumerate(st.session_state.quiz)
                    if st.session_state.quiz_answers.get(i) == q["answer"]
                )
                total   = len(st.session_state.quiz)
                pct     = int(correct / total * 100)
                xp      = xp_for_score(correct, total)
                emoji, label = get_badge(pct)

                # Save session
                st.session_state.sessions.append({
                    "date": datetime.now().strftime("%b %d, %H:%M"),
                    "subject": q_subject, "level": q_level,
                    "score": correct, "total": total, "pct": pct, "xp": xp
                })

                # Score display
                st.markdown(f"""
                <div style="text-align:center;padding:1.5rem 0">
                    <div class="score-big">{correct}/{total}</div>
                    <div style="font-size:1.1rem;color:#94a3b8;margin:0.5rem 0">{pct}% correct</div>
                    <div style="font-size:2rem">{emoji}</div>
                    <div style="color:#6366f1;font-weight:600">{label} · +{xp} XP</div>
                </div>""", unsafe_allow_html=True)

                st.divider()
                st.markdown("#### 📋 Review Answers")
                for i, q in enumerate(st.session_state.quiz):
                    user_ans = st.session_state.quiz_answers.get(i, "")
                    is_right = user_ans == q["answer"]
                    icon = "✅" if is_right else "❌"
                    st.markdown(f"**{icon} Q{i+1}. {q['question']}**")
                    if not is_right:
                        st.markdown(f"- Your answer: `{user_ans}`")
                        st.markdown(f"- Correct answer: `{q['answer']}`")
                    st.markdown("")

                if st.button("🔄 New Quiz", use_container_width=True):
                    st.session_state.quiz = []
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 3: DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tab_dashboard:
    st.markdown("#### 📊 Your Performance")

    if not st.session_state.sessions:
        st.info("Complete a quiz to see your dashboard.")
    else:
        sessions = st.session_state.sessions
        total_xp    = sum(s["xp"] for s in sessions)
        avg_score   = int(sum(s["pct"] for s in sessions) / len(sessions))
        best_score  = max(s["pct"] for s in sessions)
        total_taken = len(sessions)

        # Top stats
        c1, c2, c3, c4 = st.columns(4)
        for col, label, val in [
            (c1, "⚡ Total XP",    f"{total_xp}"),
            (c2, "📝 Quizzes",     f"{total_taken}"),
            (c3, "📈 Avg Score",   f"{avg_score}%"),
            (c4, "🏆 Best Score",  f"{best_score}%"),
        ]:
            col.markdown(f"""
            <div class="stat-card">
                <div style="font-size:0.75rem;color:#64748b">{label}</div>
                <div class="stat-num">{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # Badges earned
        st.markdown("#### 🏅 Badges Earned")
        badges_html = ""
        for s in sessions:
            emoji, label = get_badge(s["pct"])
            badges_html += f'<span class="badge" title="{label} — {s["subject"]}">{emoji}</span>'
        st.markdown(badges_html, unsafe_allow_html=True)

        st.divider()

        # Score chart
        st.markdown("#### 📈 Score History")
        import pandas as pd

        df = pd.DataFrame(sessions)
        df.index = range(1, len(df) + 1)

        st.line_chart(df[["pct"]], y="pct", use_container_width=True)

        # Per-subject breakdown
        st.markdown("#### 🔬 By Subject")
        subject_stats: dict[str, list] = {}
        for s in sessions:
            subject_stats.setdefault(s["subject"], []).append(s["pct"])

        sub_df = pd.DataFrame([
            {"Subject": subj, "Avg %": int(sum(scores) / len(scores)), "Quizzes": len(scores)}
            for subj, scores in subject_stats.items()
        ])
        st.dataframe(sub_df, use_container_width=True, hide_index=True)

        # Session log
        st.markdown("#### 🗓️ Session Log")
        log_df = pd.DataFrame(sessions)[["date", "subject", "level", "score", "total", "pct", "xp"]]
        log_df.columns = ["Date", "Subject", "Level", "Correct", "Total", "Score %", "XP"]
        st.dataframe(log_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear Dashboard", use_container_width=True):
            st.session_state.sessions = []
            st.rerun()
