"""
Universal Shayari Generator - All Poets, All Topics
Powered by Groq (Free API)
"""

import streamlit as st
from groq import Groq
import json
import re

st.set_page_config(
    page_title="شاعری | Universal Shayari",
    page_icon="🕯️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Noto+Nastaliq+Urdu:wght@400;700&family=Outfit:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #06060a;
    color: #ddd5c4;
}
.stApp {
    background:
        radial-gradient(ellipse at 15% 5%,  #130a1a 0%, transparent 50%),
        radial-gradient(ellipse at 85% 95%, #0a1318 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, #0d0a08 0%, transparent 80%),
        #06060a;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem; max-width: 780px; }

/* ── Hero ── */
.hero { text-align: center; padding: 2.5rem 1rem 0.5rem; }
.hero-lamp { font-size: 2.8rem; display:block; margin-bottom:0.8rem;
    filter: drop-shadow(0 0 24px rgba(220,170,80,0.7));
    animation: flicker 3s ease-in-out infinite; }
@keyframes flicker {
    0%,100% { filter: drop-shadow(0 0 24px rgba(220,170,80,0.7)); }
    50%      { filter: drop-shadow(0 0 40px rgba(220,170,80,1.0)); }
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.8rem, 7vw, 5rem);
    font-weight: 300;
    letter-spacing: 0.05em;
    color: #dca050;
    margin: 0 0 0.2rem;
    text-shadow: 0 0 60px rgba(220,160,80,0.25);
}
.hero-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: clamp(1.1rem, 3vw, 1.5rem);
    color: #6a5030;
    direction: rtl;
    margin-bottom: 0.4rem;
}
.hero-sub {
    font-size: 0.75rem; color: #3a3020;
    letter-spacing: 0.25em; text-transform: uppercase;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(220,160,80,0.04) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(220,160,80,0.1) !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #5a4a30 !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(220,160,80,0.15) !important;
    color: #dca050 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input, .stTextArea textarea {
    background: rgba(220,160,80,0.04) !important;
    border: 1px solid rgba(220,160,80,0.15) !important;
    border-radius: 12px !important;
    color: #ddd5c4 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #dca050 !important;
    box-shadow: 0 0 0 3px rgba(220,160,80,0.1) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea textarea::placeholder { color: #3a3020 !important; }

.stSelectbox > div > div {
    background: rgba(220,160,80,0.04) !important;
    border: 1px solid rgba(220,160,80,0.15) !important;
    border-radius: 12px !important;
    color: #ddd5c4 !important;
}
.stSelectbox > div > div:hover { border-color: rgba(220,160,80,0.4) !important; }

label[data-testid="stWidgetLabel"] p {
    color: #5a4a30 !important; font-size: 0.7rem !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #dca050, #a07030) !important;
    color: #06060a !important; border: none !important;
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(220,160,80,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 36px rgba(220,160,80,0.38) !important;
}

/* ── Shayari card ── */
.shayari-card {
    background: linear-gradient(135deg, rgba(220,160,80,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(220,160,80,0.12);
    border-radius: 20px;
    padding: 2rem 2.2rem 1.8rem;
    margin: 1.2rem 0;
    position: relative;
    animation: riseUp 0.5s ease forwards;
    opacity: 0;
}
.shayari-card:nth-child(1) { animation-delay: 0.05s; }
.shayari-card:nth-child(2) { animation-delay: 0.15s; }
.shayari-card:nth-child(3) { animation-delay: 0.25s; }
@keyframes riseUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.shayari-card::after {
    content: '❝';
    position: absolute; top: 1rem; right: 1.5rem;
    font-size: 3rem; color: rgba(220,160,80,0.07);
    font-family: 'Cormorant Garamond', serif; line-height: 1;
}

.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; }
.poet-badge {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.18em;
    text-transform: uppercase; color: #dca050;
    background: rgba(220,160,80,0.1);
    border: 1px solid rgba(220,160,80,0.2);
    border-radius: 100px; padding: 0.25rem 0.9rem;
}
.style-badge {
    font-size: 0.65rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: #4a3a20;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 100px; padding: 0.25rem 0.8rem;
}

.shayari-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: clamp(1.15rem, 3.5vw, 1.55rem);
    direction: rtl; text-align: right;
    line-height: 2.3; color: #e8dcc8;
    margin-bottom: 1.2rem;
    text-shadow: 0 0 30px rgba(220,160,80,0.08);
}
.shayari-roman {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic; font-size: 1rem;
    color: #6a5030; line-height: 2;
    border-top: 1px solid rgba(220,160,80,0.07);
    padding-top: 1rem; margin-bottom: 0.8rem;
}
.shayari-meaning {
    font-size: 0.82rem; color: #3a3020; line-height: 1.75;
    background: rgba(0,0,0,0.2); border-radius: 8px;
    padding: 0.7rem 1rem;
    border-left: 2px solid rgba(220,160,80,0.15);
}

/* ── Divider ── */
.divider {
    display: flex; align-items: center; gap: 1rem; margin: 1.5rem 0;
}
.divider::before, .divider::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, #1e1808, transparent);
}

/* ── Poet grid ── */
.poet-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin: 0.5rem 0 1rem;
}
.poet-chip {
    background: rgba(220,160,80,0.05);
    border: 1px solid rgba(220,160,80,0.12);
    border-radius: 10px;
    padding: 0.6rem 0.8rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.poet-chip:hover { border-color: #dca050; background: rgba(220,160,80,0.1); }
.poet-chip-name { font-size: 0.78rem; font-weight: 600; color: #dca050; }
.poet-chip-era  { font-size: 0.62rem; color: #4a3a20; margin-top: 0.15rem; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #dca050 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(220,160,80,0.04) !important;
    border: 1px solid rgba(220,160,80,0.1) !important;
    border-radius: 10px !important;
    color: #6a5030 !important;
}

.footer {
    text-align: center; padding: 3rem 0 2rem;
    font-size: 0.62rem; color: #1a1408; letter-spacing: 0.2em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-lamp">🕯️</span>
    <div class="hero-title">شاعری</div>
    <div class="hero-urdu">کائنات کی شاعری کا خزانہ</div>
    <div class="hero-sub">Universal Poetry Generator · Every Poet · Every Topic</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"><span style="color:#3a2a10">✦</span></div>', unsafe_allow_html=True)

# ── Data ────────────────────────────────────────────────
POETS = {
    "Urdu / Hindi Greats": [
        ("Mirza Ghalib",       "1797–1869", "غالب"),
        ("Mir Taqi Mir",       "1723–1810", "میر"),
        ("Faiz Ahmed Faiz",    "1911–1984", "فیض"),
        ("Jaun Elia",          "1931–2002", "جون"),
        ("Allama Iqbal",       "1877–1938", "اقبال"),
        ("Parveen Shakir",     "1952–1994", "پروین"),
        ("Gulzar",             "1934–",     "گلزار"),
        ("Sahir Ludhianvi",    "1921–1980", "ساحر"),
        ("Ahmad Faraz",        "1931–2008", "فراز"),
        ("Rahat Indori",       "1950–2020", "راحت"),
        ("Habib Jalib",        "1928–1993", "جالب"),
        ("Noon Meem Rashid",   "1910–1975", "ن م راشد"),
    ],
    "Persian Masters": [
        ("Rumi",               "1207–1273", "رومی"),
        ("Hafez",              "1315–1390", "حافظ"),
        ("Omar Khayyam",       "1048–1131", "خیام"),
        ("Saadi",              "1210–1291", "سعدی"),
        ("Firdausi",           "940–1020",  "فردوسی"),
    ],
    "World Poetry": [
        ("Pablo Neruda",       "1904–1973", "Spanish"),
        ("Rabindranath Tagore","1861–1941", "Bengali"),
        ("Kahlil Gibran",      "1883–1931", "Arabic"),
        ("Rainer Maria Rilke", "1875–1926", "German"),
        ("Walt Whitman",       "1819–1892", "English"),
        ("Emily Dickinson",    "1830–1886", "English"),
    ],
}

FORMS = [
    "Ghazal (غزل)",
    "Nazm (نظم)",
    "Rubai (رباعی)",
    "Marsiya (مرثیہ)",
    "Qasida (قصیدہ)",
    "Haiku Style",
    "Free Verse",
    "Sher (شعر)",
]

LANGS = ["Urdu + Roman + English", "Urdu Only", "English Only", "Roman Urdu Only"]

# ── Tabs ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["✍️  By Topic", "👤  By Poet", "🎲  Surprise Me"])

def parse_shayaris(text):
    text = re.sub(r"```json|```", "", text).strip()
    text = re.sub(r",\s*([\]}])", r"\1", text)
    try:
        r = json.loads(text)
        if isinstance(r, list): return r
    except Exception:
        pass
    m = re.search(r'\[.*\]', text, re.DOTALL)
    if m:
        try: return json.loads(m.group())
        except Exception: pass
    return []

def build_prompt(topic, poet, form, count, lang):
    lang_instruction = {
        "Urdu + Roman + English": 'Include all three fields: "urdu", "roman", "meaning"',
        "Urdu Only":              'Include only "urdu" field. Leave "roman" and "meaning" as empty strings.',
        "English Only":           'Write in "meaning" field only (full English poem). Leave "urdu" and "roman" as empty strings.',
        "Roman Urdu Only":        'Include only "roman" (Romanized Urdu). Leave "urdu" and "meaning" as empty strings.',
    }[lang]

    return f"""You are a master of world poetry with deep knowledge of {poet}'s style and {form} form.

Generate {count} shayari/poem(s) in the style of {poet} on the topic: "{topic}".
Form: {form}

{lang_instruction}

Capture {poet}'s authentic voice, imagery, and emotional depth.

Return ONLY a valid JSON array (no trailing commas):
[
  {{
    "urdu": "اردو شعر یہاں\\nدوسری سطر",
    "roman": "Romanized line here\\nSecond line",
    "meaning": "English meaning or poem here.",
    "poet": "{poet}",
    "form": "{form}"
  }}
]"""

def render_shayaris(shayaris, lang):
    for s in shayaris:
        urdu    = s.get("urdu","").replace("\\n","<br>").replace("\n","<br>")
        roman   = s.get("roman","").replace("\\n","<br>").replace("\n","<br>")
        meaning = s.get("meaning","")
        poet_n  = s.get("poet","")
        form_n  = s.get("form","")

        urdu_block   = f'<div class="shayari-urdu">{urdu}</div>' if urdu.strip() else ""
        roman_block  = f'<div class="shayari-roman">{roman}</div>' if roman.strip() else ""
        meaning_block= f'<div class="shayari-meaning">💬 {meaning}</div>' if meaning.strip() else ""

        st.markdown(f"""
        <div class="shayari-card">
            <div class="card-top">
                <span class="poet-badge">{poet_n}</span>
                <span class="style-badge">{form_n}</span>
            </div>
            {urdu_block}
            {roman_block}
            {meaning_block}
        </div>
        """, unsafe_allow_html=True)

def call_groq(prompt):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        temperature=0.92,
    )
    return parse_shayaris(r.choices[0].message.content.strip())

# ── Tab 1: By Topic ──────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    topic = st.text_input("", placeholder="Type any topic... love, rain, motherland, loneliness, revolution, death, hope...")

    col1, col2, col3 = st.columns(3)
    with col1: poet1  = st.selectbox("Poet", [p for cat in POETS.values() for p,_,_ in cat], key="t1_poet")
    with col2: form1  = st.selectbox("Form", FORMS, key="t1_form")
    with col3: count1 = st.selectbox("Count", [1, 2, 3], key="t1_count")
    lang1 = st.selectbox("Language", LANGS, key="t1_lang")

    if st.button("🕯️ Generate Shayari", use_container_width=True, key="btn1"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("روشنی کا انتظار..."):
                try:
                    shayaris = call_groq(build_prompt(topic, poet1, form1, count1, lang1))
                    if shayaris: render_shayaris(shayaris, lang1)
                    else: st.error("Could not generate. Please try again.")
                except Exception as e:
                    st.error(f"Error: {e}")

# ── Tab 2: By Poet ───────────────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    for cat_name, poets in POETS.items():
        st.markdown(f'<div style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;color:#4a3a20;margin:1rem 0 0.5rem">{cat_name}</div>', unsafe_allow_html=True)
        grid_html = '<div class="poet-grid">'
        for name, era, urdu_name in poets:
            grid_html += f'<div class="poet-chip"><div class="poet-chip-name">{name}</div><div class="poet-chip-era">{era}</div></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown('<div class="divider"><span style="color:#3a2a10">✦</span></div>', unsafe_allow_html=True)
    all_poets = [p for cat in POETS.values() for p,_,_ in cat]
    col1, col2 = st.columns(2)
    with col1: poet2  = st.selectbox("Select Poet", all_poets, key="t2_poet")
    with col2: topic2 = st.text_input("", placeholder="Topic (or leave blank for poet's signature themes)", key="t2_topic")
    col3, col4, col5 = st.columns(3)
    with col3: form2  = st.selectbox("Form", FORMS, key="t2_form")
    with col4: count2 = st.selectbox("Count", [1,2,3], key="t2_count")
    with col5: lang2  = st.selectbox("Language", LANGS, key="t2_lang")

    if st.button("🕯️ Generate Shayari", use_container_width=True, key="btn2"):
        t = topic2.strip() if topic2.strip() else "the poet's signature themes and style"
        with st.spinner("روشنی کا انتظار..."):
            try:
                shayaris = call_groq(build_prompt(t, poet2, form2, count2, lang2))
                if shayaris: render_shayaris(shayaris, lang2)
                else: st.error("Could not generate. Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Tab 3: Surprise Me ───────────────────────────────────
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-family:Cormorant Garamond,serif;font-style:italic;font-size:1.1rem;color:#4a3a20;margin-bottom:1.5rem">Let the universe decide the poet, topic, and form.</div>', unsafe_allow_html=True)

    import random
    SURPRISE_TOPICS = [
        "the passage of time", "a letter never sent", "the last candle",
        "rain on an old roof", "forgetting a face", "revolution at dawn",
        "a mother's hands", "the city at 3am", "longing for home",
        "the first snowfall", "unrequited love", "the sound of silence",
    ]

    lang3 = st.selectbox("Language", LANGS, key="t3_lang")

    if st.button("🎲 Surprise Me!", use_container_width=True, key="btn3"):
        all_poets_flat = [p for cat in POETS.values() for p,_,_ in cat]
        rand_poet  = random.choice(all_poets_flat)
        rand_topic = random.choice(SURPRISE_TOPICS)
        rand_form  = random.choice(FORMS)
        st.markdown(f'<div style="text-align:center;padding:0.8rem;background:rgba(220,160,80,0.05);border-radius:10px;margin-bottom:1rem;font-size:0.85rem;color:#6a5030">🎲 <strong style="color:#dca050">{rand_poet}</strong> · {rand_form} · <em>{rand_topic}</em></div>', unsafe_allow_html=True)
        with st.spinner("روشنی کا انتظار..."):
            try:
                shayaris = call_groq(build_prompt(rand_topic, rand_poet, rand_form, 1, lang3))
                if shayaris: render_shayaris(shayaris, lang3)
                else: st.error("Could not generate. Please try again.")
            except Exception as e:
                st.error(f"Error: {e}")

# ── Footer ───────────────────────────────────────────────
st.markdown('<div class="divider"><span style="color:#3a2a10">✦</span></div>', unsafe_allow_html=True)
with st.expander("📜 About This App"):
    st.markdown("""
    <div style="font-size:0.88rem;line-height:1.9;color:#4a3a20;">
    This app brings together the greatest poets humanity has ever known —
    from <strong style="color:#dca050">Mirza Ghalib</strong> and <strong style="color:#dca050">Jaun Elia</strong>
    to <strong style="color:#dca050">Rumi</strong>, <strong style="color:#dca050">Pablo Neruda</strong>,
    and <strong style="color:#dca050">Tagore</strong>.<br><br>
    Type <em>any topic</em> — a feeling, a moment, a person, a place, a question —
    and receive shayari in the authentic voice of the poet you choose,
    in the form you prefer, in the language you love.
    <br><br>
    <span style="color:#2a2010">Powered by Groq · Llama 3.3 · Built with Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="footer">شاعری · UNIVERSAL POETRY · POWERED BY GROQ · LLAMA 3.3</div>', unsafe_allow_html=True)
