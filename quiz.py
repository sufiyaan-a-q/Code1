"""
IIT JEE Practice Quiz Generator - Streamlit App
Powered by Groq (Free API)
"""

import streamlit as st
from groq import Groq
import json
import re

# Page config
st.set_page_config(
    page_title="IIT JEE Quiz",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Crimson+Pro:ital,wght@0,400;0,700;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #04080f;
    color: #e8eaf0;
}
.stApp {
    background: radial-gradient(ellipse at 80% 0%, #0d1f3c 0%, #04080f 55%, #0d0a1f 100%);
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; max-width: 800px; }

/* Hero */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #f5a623;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Crimson Pro', serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    background: linear-gradient(135deg, #e8eaf0 30%, #f5a623 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.8rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #667;
    font-weight: 300;
}

/* Divider */
.divider-fancy {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.5rem 0;
    color: #1a2a3a;
}
.divider-fancy::before, .divider-fancy::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e3050, transparent);
}

/* Selectbox & inputs */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(245,166,35,0.2) !important;
    border-radius: 12px !important;
    color: #e8eaf0 !important;
}
.stSelectbox > div > div:hover { border-color: rgba(245,166,35,0.5) !important; }
label[data-testid="stWidgetLabel"] p {
    color: #667 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #f5a623, #e8860a) !important;
    color: #04080f !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(245,166,35,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(245,166,35,0.4) !important;
}

/* Question card */
.question-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-top: 3px solid #f5a623;
    border-radius: 16px;
    padding: 1.75rem;
    margin: 1.5rem 0 1rem;
}
.question-meta {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #f5a623;
    margin-bottom: 0.75rem;
}
.question-text {
    font-family: 'Crimson Pro', serif;
    font-size: 1.25rem;
    line-height: 1.6;
    color: #e8eaf0;
    margin-bottom: 1.5rem;
}

/* Option buttons */
.option-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    margin: 0.5rem 0;
    color: #b0b8c8;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.option-btn:hover { border-color: #f5a623; color: #e8eaf0; background: rgba(245,166,35,0.07); }
.option-correct { border-color: #4caf7d !important; background: rgba(76,175,125,0.12) !important; color: #4caf7d !important; }
.option-wrong   { border-color: #e05c5c !important; background: rgba(224,92,92,0.12) !important; color: #e05c5c !important; }
.option-reveal  { border-color: #4caf7d !important; background: rgba(76,175,125,0.07) !important; color: #4caf7d !important; }

/* Explanation box */
.explanation-box {
    background: rgba(245,166,35,0.06);
    border: 1px solid rgba(245,166,35,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.95rem;
    line-height: 1.65;
    color: #b0b8c8;
}
.explanation-box strong { color: #f5a623; }

/* Score badge */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(245,166,35,0.1);
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 100px;
    padding: 0.4rem 1.1rem;
    font-size: 0.85rem;
    color: #f5a623;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* Progress bar */
.stProgress > div > div > div { background: linear-gradient(90deg, #f5a623, #e8860a) !important; }

/* Radio override — hide default, use custom */
.stRadio > div { gap: 0.5rem !important; }
.stRadio > div > label {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    color: #b0b8c8 !important;
}
.stRadio > div > label:hover { border-color: #f5a623 !important; color: #e8eaf0 !important; }

.footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-size: 0.7rem;
    color: #222;
    letter-spacing: 0.15em;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────
for key, val in {
    "questions": [],
    "current_q": 0,
    "score": 0,
    "answered": False,
    "selected_option": None,
    "quiz_done": False,
    "show_explanation": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Hero ───────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Practice</div>
    <h1 class="hero-title">IIT JEE Quiz<br>Generator</h1>
    <p class="hero-sub">Sharpen your skills with AI-generated JEE-level questions</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-fancy"><span>🎯</span></div>', unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────
SUBJECTS = ["Physics", "Chemistry", "Mathematics"]
TOPICS = {
    "Physics":     ["Mechanics", "Thermodynamics", "Electromagnetism", "Optics", "Modern Physics", "Waves & Sound"],
    "Chemistry":   ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Electrochemistry", "Chemical Bonding"],
    "Mathematics": ["Calculus", "Algebra", "Coordinate Geometry", "Trigonometry", "Vectors & 3D", "Probability"],
}
DIFFICULTIES = ["JEE Mains", "JEE Advanced"]

def parse_questions(text):
    text = re.sub(r"```json|```", "", text).strip()
    text = re.sub(r",\s*([\]}])", r"\1", text)
    try:
        return json.loads(text)
    except Exception:
        # Try to find JSON array in text
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return []

def generate_questions(subject, topic, difficulty, num_q):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"""Generate {num_q} multiple choice questions for {difficulty} level on the topic: {topic} ({subject}).

Each question must have exactly 4 options (A, B, C, D), one correct answer, and a brief explanation.

Return ONLY a valid JSON array in this exact format with no trailing commas:
[
  {{
    "question": "Question text here?",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "answer": "A",
    "explanation": "Brief explanation of why A is correct."
  }}
]

Make questions challenging and realistic for {difficulty}. No trailing commas in JSON."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return parse_questions(response.choices[0].message.content.strip())

# ── Quiz setup (only when no active quiz) ─────────────────
if not st.session_state.questions:
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject", SUBJECTS)
        topic   = st.selectbox("Topic", TOPICS[subject])
    with col2:
        difficulty = st.selectbox("Difficulty", DIFFICULTIES)
        num_q      = st.selectbox("Questions", [3, 5, 10], index=1)

    if st.button("🚀 Start Quiz", use_container_width=True):
        with st.spinner("Generating your quiz…"):
            qs = generate_questions(subject, topic, difficulty, num_q)
            if qs:
                st.session_state.questions   = qs
                st.session_state.current_q   = 0
                st.session_state.score       = 0
                st.session_state.answered    = False
                st.session_state.selected_option = None
                st.session_state.quiz_done   = False
                st.rerun()
            else:
                st.error("Failed to generate questions. Please try again.")

# ── Active quiz ────────────────────────────────────────────
elif not st.session_state.quiz_done:
    qs    = st.session_state.questions
    idx   = st.session_state.current_q
    total = len(qs)
    q     = qs[idx]

    # Progress
    st.markdown(f'<div class="score-badge">📊 Score: {st.session_state.score} / {total} &nbsp;|&nbsp; Q{idx+1} of {total}</div>', unsafe_allow_html=True)
    st.progress((idx) / total)

    # Question card
    st.markdown(f"""
    <div class="question-card">
        <div class="question-meta">Question {idx+1} of {total}</div>
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Options
    options = q["options"]
    answered = st.session_state.answered
    correct  = q["answer"]

    for key, val in options.items():
        label = f"**{key}.** {val}"
        if not answered:
            if st.button(label, key=f"opt_{key}", use_container_width=True):
                st.session_state.selected_option = key
                st.session_state.answered = True
                if key == correct:
                    st.session_state.score += 1
                st.rerun()
        else:
            sel = st.session_state.selected_option
            if key == correct:
                css = "option-reveal"
                prefix = "✅"
            elif key == sel:
                css = "option-wrong"
                prefix = "❌"
            else:
                css = ""
                prefix = ""
            st.markdown(f'<div class="option-btn {css}">{prefix} <strong>{key}.</strong> {val}</div>', unsafe_allow_html=True)

    # After answer
    if answered:
        sel = st.session_state.selected_option
        if sel == correct:
            st.success("🎉 Correct!")
        else:
            st.error(f"❌ Wrong! Correct answer: **{correct}. {options[correct]}**")

        st.markdown(f'<div class="explanation-box"><strong>💡 Explanation:</strong> {q["explanation"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_label = "Next Question →" if idx + 1 < total else "See Results 🏆"
        if st.button(btn_label, use_container_width=True):
            if idx + 1 < total:
                st.session_state.current_q  += 1
                st.session_state.answered    = False
                st.session_state.selected_option = None
                st.rerun()
            else:
                st.session_state.quiz_done = True
                st.rerun()

# ── Results ────────────────────────────────────────────────
elif st.session_state.quiz_done:
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct   = int((score / total) * 100)

    if pct >= 80:
        grade, emoji, color = "Excellent!", "🏆", "#4caf7d"
    elif pct >= 60:
        grade, emoji, color = "Good Job!", "👍", "#f5a623"
    else:
        grade, emoji, color = "Keep Practicing!", "📚", "#e05c5c"

    st.markdown(f"""
    <div style="text-align:center; padding: 3rem 1rem;">
        <div style="font-size: 4rem;">{emoji}</div>
        <h2 style="font-family:'Crimson Pro',serif; font-size:2.5rem; color:{color}; margin:0.5rem 0;">{grade}</h2>
        <p style="font-size:1.1rem; color:#888; margin-bottom:1rem;">You scored</p>
        <div style="font-size:4rem; font-weight:700; color:{color};">{score}<span style="font-size:2rem; color:#444;">/{total}</span></div>
        <div style="font-size:1.2rem; color:#666; margin-top:0.5rem;">{pct}% correct</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Try Another Quiz", use_container_width=True):
        for key in ["questions", "current_q", "score", "answered", "selected_option", "quiz_done"]:
            st.session_state[key] = [] if key == "questions" else (False if key in ["answered","quiz_done"] else (0 if key in ["current_q","score"] else None))
        st.rerun()

# ── Footer ─────────────────────────────────────────────────
st.markdown('<div class="footer">POWERED BY GROQ · LLAMA 3.3 · IIT JEE PREP</div>', unsafe_allow_html=True)
