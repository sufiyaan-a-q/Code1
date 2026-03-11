"""
Human Body Factoid Generator - Streamlit App
Powered by Groq (Free API)
"""

import streamlit as st
from groq import Groq
import random
import json
import re

# Page config
st.set_page_config(
    page_title="Body Factoids",
    page_icon="🫀",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #f0ece4;
}

.stApp {
    background: radial-gradient(ellipse at 20% 10%, #1a0a2e 0%, #0a0a0f 50%, #0d1a0a 100%);
    min-height: 100vh;
}

/* Hide default streamlit elements */
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 2rem; max-width: 760px; }

/* Hero section */
.hero {
    text-align: center;
    padding: 3rem 1rem 1.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7fff6a;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    background: linear-gradient(135deg, #f0ece4 30%, #7fff6a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem;
}
.hero-sub {
    font-size: 1rem;
    color: #888;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* Decorative line */
.divider-fancy {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
    color: #333;
}
.divider-fancy::before, .divider-fancy::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a3a, transparent);
}
.divider-fancy span {
    font-size: 1.2rem;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(127,255,106,0.2) !important;
    border-radius: 12px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(127,255,106,0.5) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #888 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(127,255,106,0.2) !important;
    border-radius: 12px !important;
    color: #f0ece4 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7fff6a !important;
    box-shadow: 0 0 0 3px rgba(127,255,106,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #555 !important; }

/* Generate button */
.stButton > button {
    background: linear-gradient(135deg, #7fff6a, #3ad62e) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(127,255,106,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(127,255,106,0.4) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* Selected badge */
.selected-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(127,255,106,0.1);
    border: 1px solid rgba(127,255,106,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    color: #7fff6a;
    font-weight: 500;
    margin: 0.5rem 0 1.5rem;
}

/* Factoid cards */
.factoid-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #7fff6a;
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin: 1rem 0;
    position: relative;
    animation: fadeUp 0.4s ease forwards;
    opacity: 0;
}
.factoid-card:nth-child(1) { animation-delay: 0.1s; }
.factoid-card:nth-child(2) { animation-delay: 0.2s; }
.factoid-card:nth-child(3) { animation-delay: 0.3s; }
.factoid-card:nth-child(4) { animation-delay: 0.4s; }
.factoid-card:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.factoid-number {
    font-family: 'Playfair Display', serif;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7fff6a;
    margin-bottom: 0.6rem;
    font-weight: 700;
}
.factoid-text {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #d8d4cc;
    font-weight: 300;
}

/* Result header */
.result-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0ece4;
    margin: 2rem 0 0.5rem;
}
.result-sub {
    font-size: 0.85rem;
    color: #555;
    margin-bottom: 1rem;
}

/* Spinner */
.stSpinner > div { border-top-color: #7fff6a !important; }

/* Success/warning overrides */
.stAlert { border-radius: 12px !important; }

/* Footer */
.footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-size: 0.75rem;
    color: #333;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-powered curiosity engine</div>
    <h1 class="hero-title">The Human Body,<br>Demystified.</h1>
    <p class="hero-sub">Pick any body part and discover facts that will genuinely surprise you.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-fancy"><span>🫀</span></div>', unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────
BODY_PARTS = [
    "— choose a body part —",
    "Heart", "Brain", "Liver", "Lungs", "Kidney",
    "Skin", "Eyes", "Bones", "Stomach", "Blood",
    "Spine", "Teeth", "Ears", "Nose", "Tongue",
]

col1, col2 = st.columns([2, 1])
with col1:
    selected = st.selectbox("Body part", BODY_PARTS)
    custom = st.text_input("Or type any body part", placeholder="e.g. appendix, cornea, lymph nodes…")
with col2:
    num_facts = st.selectbox("Facts to generate", [1, 2, 3, 4, 5], index=1)

body_part = custom.strip() if custom.strip() else (selected if selected != BODY_PARTS[0] else "")

if body_part:
    st.markdown(f'<div class="selected-badge">🔬 {body_part}</div>', unsafe_allow_html=True)

generate = st.button("Generate Factoids →", use_container_width=True)

# ── Generation ────────────────────────────────────────────
def parse_factoids(text, num_facts):
    text = re.sub(r"```json|```", "", text).strip()
    text = re.sub(r",\s*([\]}])", r"\1", text)
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return [str(f) for f in result]
    except Exception:
        pass
    matches = re.findall(r'"((?:[^"\\]|\\.)*)"', text)
    if matches:
        return matches[:num_facts]
    lines = [l.strip("-•123456789. ").strip() for l in text.splitlines() if l.strip()]
    return [l for l in lines if len(l) > 20][:num_facts]

if generate:
    if not body_part:
        st.warning("⚠️ Please select or type a body part first.")
    else:
        styles = [
            "surprising and counterintuitive",
            "related to evolutionary biology",
            "about world records or extremes",
            "about medical or scientific discoveries",
            "about cellular level functions",
            "about historical or cultural significance",
            "comparing to other animals",
            "about common myths or misconceptions",
        ]
        selected_styles = random.sample(styles, min(num_facts, len(styles)))

        with st.spinner("Thinking…"):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt = f"""Generate exactly {num_facts} fascinating and accurate factoid(s) about the human {body_part}.

Each factoid should be:
- Style (one per factoid): {', '.join(selected_styles)}
- Concise (1-3 sentences)
- Scientifically accurate
- Engaging and surprising

Return ONLY a valid JSON array of strings with NO trailing commas. Example:
["Fact one here.", "Fact two here."]
Do not add anything before or after the JSON array."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                )
                response_text = response.choices[0].message.content.strip()
                factoids = parse_factoids(response_text, num_facts)

                if not factoids:
                    st.error("Couldn't parse the response. Please try again.")
                else:
                    st.markdown(f'<div class="result-header">{body_part.title()}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-sub">{len(factoids)} fact{"s" if len(factoids) > 1 else ""} generated</div>', unsafe_allow_html=True)
                    cards_html = ""
                    for i, fact in enumerate(factoids, 1):
                        cards_html += f"""
                        <div class="factoid-card">
                            <div class="factoid-number">Fact {i:02d}</div>
                            <div class="factoid-text">{fact}</div>
                        </div>"""
                    st.markdown(cards_html, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ── Footer ────────────────────────────────────────────────
st.markdown('<div class="footer">POWERED BY GROQ · LLAMA 3.3 · BUILT WITH STREAMLIT</div>', unsafe_allow_html=True)
