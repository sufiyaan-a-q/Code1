"""
Human Body Factoid Generator - Streamlit App
"""

import streamlit as st
import anthropic
import random

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
st.markdown('<div class="subtitle-text">Discover fascinating facts about the human body powered by Claude AI</div>', unsafe_allow_html=True)
st.divider()

# Suggested body parts
BODY_PARTS = [
    "Heart", "Brain", "Liver", "Lungs", "Kidney",
    "Skin", "Eyes", "Bones", "Stomach", "Blood",
    "Muscles", "DNA", "Teeth", "Ears", "Nose"
]

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
for i, part in enumerate(BODY_PARTS[:10]):
    if cols[i % 5].button(part, use_container_width=True):
        body_part = part

st.divider()

# Generate button
generate = st.button("✨ Generate Factoids", type="primary", use_container_width=True)

# Generation logic
if generate:
    if not body_part.strip():
        st.warning("⚠️ Please enter or select a body part first!")
    else:
        styles = [
            "surprising and counterintuitive",
            "related to evolutionary biology",
            "about world records or extremes",
            "about medical or scientific discoveries",
            "about how the body part functions at the cellular level",
            "about historical or cultural significance",
            "about how it compares to other animals",
            "about common myths or misconceptions",
        ]
        selected_styles = random.sample(styles, min(num_facts, len(styles)))

        with st.spinner(f"Generating {num_facts} factoid(s) about the **{body_part}**..."):
            try:
                api_key = st.secrets["ANTHROPIC_API_KEY"]
                client = anthropic.Anthropic(api_key=api_key)

                prompt = f"""Generate {num_facts} fascinating and accurate factoid(s) about the human {body_part}.

Each factoid should be:
- A different style from this list (use one per factoid): {', '.join(selected_styles)}
- Concise (1-3 sentences)
- Scientifically accurate
- Engaging and surprising

Format as a JSON array of strings, each string being one factoid.
Return ONLY the JSON array, no other text."""

                message = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )

                import json
                response_text = message.content[0].text.strip()
                # Clean up markdown fences if present
                response_text = response_text.replace("```json", "").replace("```", "").strip()
                factoids = json.loads(response_text)

                st.success(f"🧬 Here are your factoids about the **{body_part.title()}**!")
                for i, fact in enumerate(factoids, 1):
                    st.markdown(f'<div class="factoid-box">💡 <b>Fact #{i}:</b> {fact}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

# Footer
st.divider()
st.markdown("<center><small>Powered by Claude AI · Built with Streamlit</small></center>", unsafe_allow_html=True)
