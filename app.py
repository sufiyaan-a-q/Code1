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
    page_title="🧬 Human Body Factoid Generator",
    page_icon="🧬",
    layout="centered"
)

# Styling
st.markdown("""
    <style>
        .factoid-box {
            background-color: #f0f4ff;
            border-left: 5px solid #4F8BF9;
            padding: 16px 20px;
            border-radius: 8px;
            margin: 12px 0;
            font-size: 16px;
            color: #1a1a2e;
        }
        .title-text {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 700;
            color: #1a1a2e;
        }
        .subtitle-text {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-text">🧬 Human Body Factoid Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Discover fascinating facts about the human body — powered by Groq AI</div>', unsafe_allow_html=True)
st.divider()

# Suggested body parts
BODY_PARTS = [
    "Heart", "Brain", "Liver", "Lungs", "Kidney",
    "Skin", "Eyes", "Bones", "Stomach", "Blood",
]

def parse_factoids(text, num_facts):
    """Robustly parse factoids from LLM response."""
    # Clean markdown fences
    text = re.sub(r"```json|```", "", text).strip()
    # Remove trailing commas before ] or }
    text = re.sub(r",\s*([\]}])", r"\1", text)
    # Try JSON parse first
    try:
        result = json.loads(text)
        if isinstance(result, list):
            return [str(f) for f in result]
    except Exception:
        pass
    # Fallback: extract quoted strings
    matches = re.findall(r'"((?:[^"\\]|\\.)*)"', text)
    if matches:
        return matches[:num_facts]
    # Last resort: split by newlines
    lines = [l.strip("-•123456789. ").strip() for l in text.splitlines() if l.strip()]
    return [l for l in lines if len(l) > 20][:num_facts]

# Input section
col1, col2 = st.columns([2, 1])
with col1:
    body_part = st.text_input(
        "🔍 Enter a body part",
        placeholder="e.g. heart, brain, liver...",
        label_visibility="collapsed"
    )
with col2:
    num_facts = st.selectbox("Number of facts", [1, 2, 3, 4, 5], index=0)

# Quick select buttons
st.markdown("**Quick select:**")
cols = st.columns(5)
for i, part in enumerate(BODY_PARTS):
    if cols[i % 5].button(part, use_container_width=True):
        body_part = part

st.divider()

# Generate button
generate = st.button("✨ Generate Factoids", type="primary", use_container_width=True)

if generate:
    if not body_part.strip():
        st.warning("⚠️ Please enter or select a body part first!")
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

        with st.spinner(f"Generating {num_facts} factoid(s) about the **{body_part}**..."):
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
                    st.error("Could not parse response. Please try again.")
                else:
                    st.success(f"🧬 Here are your factoids about the **{body_part.title()}**!")
                    for i, fact in enumerate(factoids, 1):
                        st.markdown(f'<div class="factoid-box">💡 <b>Fact #{i}:</b> {fact}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Footer
st.divider()
st.markdown("<center><small>Powered by Groq AI · Built with Streamlit</small></center>", unsafe_allow_html=True)
