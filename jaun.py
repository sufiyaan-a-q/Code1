"""
Jaun Elia Shayari App - Streamlit
"""

import streamlit as st
from groq import Groq
import json
import re
import random

st.set_page_config(
    page_title="جون ایلیا",
    page_icon="🌙",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Noto+Nastaliq+Urdu&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080608;
    color: #e8dcc8;
}
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #1a0a0a 0%, transparent 60%),
        radial-gradient(ellipse at 90% 100%, #0a0a1a 0%, transparent 60%),
        #080608;
    min-height: 100vh;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 720px; }

/* Grain overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 1rem;
    position: relative;
}
.moon {
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
    filter: drop-shadow(0 0 20px rgba(200,160,80,0.6));
    animation: float 4s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}
.hero-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: clamp(2rem, 7vw, 3.5rem);
    color: #c8a050;
    direction: rtl;
    line-height: 1.4;
    margin: 0 0 0.3rem;
    text-shadow: 0 0 40px rgba(200,160,80,0.3);
}
.hero-roman {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1rem, 3vw, 1.3rem);
    font-style: italic;
    color: #6a5a40;
    margin: 0 0 0.5rem;
}
.hero-sub {
    font-size: 0.8rem;
    color: #4a4030;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 500;
}

/* Divider */
.divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
}
.divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3a2a18, transparent);
}
.divider-icon { color: #c8a050; font-size: 1rem; }

/* Controls */
.stSelectbox > div > div {
    background: rgba(200,160,80,0.05) !important;
    border: 1px solid rgba(200,160,80,0.15) !important;
    border-radius: 10px !important;
    color: #e8dcc8 !important;
}
.stSelectbox > div > div:hover { border-color: rgba(200,160,80,0.4) !important; }
label[data-testid="stWidgetLabel"] p {
    color: #6a5a40 !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #c8a050, #a07830) !important;
    color: #080608 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(200,160,80,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(200,160,80,0.35) !important;
}

/* Shayari card */
.shayari-card {
    background: rgba(200,160,80,0.03);
    border: 1px solid rgba(200,160,80,0.1);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin: 1.5rem 0;
    position: relative;
    animation: fadeIn 0.6s ease forwards;
    opacity: 0;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.shayari-card::before {
    content: '"';
    position: absolute;
    top: -0.5rem;
    left: 1.5rem;
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    color: rgba(200,160,80,0.15);
    line-height: 1;
}

.shayari-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: clamp(1.2rem, 3.5vw, 1.6rem);
    direction: rtl;
    text-align: right;
    line-height: 2.2;
    color: #e8dcc8;
    margin-bottom: 1.5rem;
    text-shadow: 0 0 30px rgba(200,160,80,0.1);
}
.shayari-roman {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 0.95rem;
    color: #6a5a40;
    line-height: 1.9;
    border-top: 1px solid rgba(200,160,80,0.08);
    padding-top: 1rem;
    margin-bottom: 1rem;
}
.shayari-meaning {
    font-size: 0.85rem;
    color: #4a4030;
    line-height: 1.7;
    background: rgba(200,160,80,0.04);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    border-left: 2px solid rgba(200,160,80,0.2);
}
.shayari-theme {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c8a050;
    background: rgba(200,160,80,0.08);
    border: 1px solid rgba(200,160,80,0.15);
    border-radius: 100px;
    padding: 0.2rem 0.8rem;
    margin-bottom: 1.2rem;
}

/* Spinner */
.stSpinner > div { border-top-color: #c8a050 !important; }

.footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-size: 0.65rem;
    color: #2a2018;
    letter-spacing: 0.2em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="moon">🌙</span>
    <div class="hero-urdu">جون ایلیا</div>
    <div class="hero-roman">Jaun Elia</div>
    <div class="hero-sub">1931 – 2002 · Amroha, India</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span class="divider-icon">✦</span></div>', unsafe_allow_html=True)

# ── Controls ─────────────────────────────────────────────
THEMES = [
    "Any Theme",
    "Ishq (Love)",
    "Gham (Sorrow)",
    "Wujood (Existence)",
    "Tanhai (Loneliness)",
    "Maut (Death)",
    "Zindagi (Life)",
    "Intezaar (Waiting)",
    "Nafrat (Anguish)",
    "Falsafa (Philosophy)",
]

col1, col2 = st.columns([2, 1])
with col1:
    theme = st.selectbox("Choose a theme", THEMES)
with col2:
    count = st.selectbox("Number of shayaris", [1, 2, 3], index=0)

st.markdown("<br>", unsafe_allow_html=True)
generate = st.button("🌙 Show Shayari", use_container_width=True)

# ── Generation ────────────────────────────────────────────
def parse_shayaris(text):
    text = re.sub(r"```json|```", "", text).strip()
    text = re.sub(r",\s*([\]}])", r"\1", text)
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except Exception:
        pass
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return []

if generate:
    theme_prompt = "any theme" if theme == "Any Theme" else theme
    with st.spinner("لمحہ بھر..."):
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            prompt = f"""You are an expert on Jaun Elia, the legendary Urdu poet (1931-2002) from Amroha.

Generate {count} shayari(s) in the style of Jaun Elia on the theme: {theme_prompt}.

The shayari should feel authentic to Jaun Elia's style: raw, philosophical, melancholic, existential, and deeply personal. Use his characteristic nihilistic yet romantic tone.

Return ONLY a valid JSON array with no trailing commas:
[
  {{
    "urdu": "شعر اردو میں یہاں\\nدوسری سطر یہاں",
    "roman": "Romanized transliteration here\\nSecond line here",
    "meaning": "Brief English meaning/interpretation in 1-2 sentences.",
    "theme": "Love"
  }}
]

Each shayari should be 2-4 lines (a sher or a short nazm). Make it feel like genuine Jaun Elia — not generic Urdu poetry."""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
            )
            shayaris = parse_shayaris(response.choices[0].message.content.strip())

            if not shayaris:
                st.error("Could not load shayari. Please try again.")
            else:
                for s in shayaris:
                    urdu    = s.get("urdu", "").replace("\\n", "<br>")
                    roman   = s.get("roman", "").replace("\\n", "<br>")
                    meaning = s.get("meaning", "")
                    stheme  = s.get("theme", theme)
                    st.markdown(f"""
                    <div class="shayari-card">
                        <div class="shayari-theme">{stheme}</div>
                        <div class="shayari-urdu">{urdu}</div>
                        <div class="shayari-roman">{roman}</div>
                        <div class="shayari-meaning">💬 {meaning}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ── About ─────────────────────────────────────────────────
st.markdown('<div class="divider"><span class="divider-icon">✦</span></div>', unsafe_allow_html=True)
with st.expander("About Jaun Elia"):
    st.markdown("""
    <div style="font-size:0.9rem; line-height:1.8; color:#6a5a40;">
    <strong style="color:#c8a050;">Jaun Elia</strong> (جون ایلیا) was born on <strong style="color:#c8a050;">December 14, 1931</strong> in Amroha, India.
    One of the most distinctive and unconventional Urdu poets of the 20th century, he is known for his deeply personal,
    nihilistic, and philosophical poetry that blends existential angst with raw emotion.<br><br>
    His major collections include <em>Shayad</em>, <em>Yaani</em>, <em>Gumaan</em>, <em>Lekin</em>, and <em>Goya</em>.
    He passed away on <strong style="color:#c8a050;">November 8, 2002</strong> in Karachi, Pakistan —
    leaving behind a legacy that continues to resonate with millions.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">جون ایلیا · POWERED BY GROQ · LLAMA 3.3</div>', unsafe_allow_html=True)
