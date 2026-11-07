import base64
import html
from pathlib import Path

import streamlit as st
from PIL import Image

# ------------------------------------------------------------------
# Assets (put aurora_logo.png and aurora_icon.png in the assets/ folder)
# ------------------------------------------------------------------
ASSETS = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS / "aurora_logo.png"
ICON_PATH = ASSETS / "aurora_icon.png"

# ------------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Aurora Chatbot",
    page_icon=Image.open(ICON_PATH) if ICON_PATH.exists() else "✨",
    layout="centered",
)

# ------------------------------------------------------------------
# Styling: a night sky with a soft aurora glow
# Palette: night #0B1220 / mint #7FE3C4 / violet #A78BFA /
#          mist #E6EEF5 / slate #9FB0C0
# ------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --night: #0B1220;
    --mint: #7FE3C4;
    --violet: #A78BFA;
    --mist: #E6EEF5;
    --slate: #9FB0C0;
    --glass: rgba(255, 255, 255, 0.05);
    --line: rgba(127, 227, 196, 0.22);
}

/* ---------- Base ---------- */
html, body, .stApp, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--mist);
}

.stApp {
    background:
        radial-gradient(900px 420px at 15% -5%, rgba(127, 227, 196, 0.18), transparent 60%),
        radial-gradient(800px 420px at 90% 0%, rgba(167, 139, 250, 0.20), transparent 60%),
        linear-gradient(180deg, #0B1220 0%, #0D1726 55%, #0B1220 100%);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}
header[data-testid="stHeader"] { background: transparent; }

.block-container {
    max-width: 720px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    text-align: center;
    padding: 1.5rem 1rem 1.5rem;
}
.hero::before {
    content: "";
    position: absolute;
    inset: -10% 5% auto 5%;
    height: 260px;
    background:
        radial-gradient(closest-side, rgba(127, 227, 196, 0.30), transparent),
        radial-gradient(closest-side, rgba(167, 139, 250, 0.26), transparent);
    background-size: 60% 100%, 60% 100%;
    background-position: 10% 0, 90% 0;
    background-repeat: no-repeat;
    filter: blur(40px);
    z-index: 0;
    animation: drift 14s ease-in-out infinite alternate;
}
@keyframes drift {
    from { transform: translateX(-3%); }
    to   { transform: translateX(3%); }
}
@media (prefers-reduced-motion: reduce) {
    .hero::before { animation: none; }
}
.hero img.logo {
    position: relative;
    z-index: 1;
    width: min(400px, 78%);
    height: auto;
}
.hero h1 {
    position: relative;
    z-index: 1;
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    font-size: clamp(1.9rem, 6vw, 2.5rem);
    letter-spacing: 0.01em;
    line-height: 1.1;
    margin: 1rem 0 0;
    padding: 0;
    color: var(--mist);
}
.hero p {
    position: relative;
    z-index: 1;
    margin: 0.8rem auto 0;
    max-width: 30rem;
    font-size: 1.02rem;
    line-height: 1.6;
    color: var(--slate);
}

/* ---------- Disclaimer ---------- */
.note {
    margin: 1.5rem 0 2rem;
    padding: 0.85rem 1.1rem;
    border-left: 3px solid var(--mint);
    background: rgba(127, 227, 196, 0.07);
    border-radius: 0 12px 12px 0;
    font-size: 0.9rem;
    line-height: 1.55;
    color: #BFD3DF;
}

/* ---------- Input ---------- */
.stTextInput label p {
    font-weight: 500;
    font-size: 1rem;
    color: var(--mist);
}
.stTextInput div[data-baseweb="input"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 14px;
    transition: border-color .2s, box-shadow .2s;
}
.stTextInput div[data-baseweb="input"]:focus-within {
    border-color: var(--mint);
    box-shadow: 0 0 0 3px rgba(127, 227, 196, 0.18);
}
.stTextInput input {
    color: var(--mist);
    padding: 0.85rem 1rem;
    font-size: 1rem;
}
.stTextInput input::placeholder { color: #6F8396; }

/* ---------- Buttons ---------- */
button[data-testid="stBaseButton-secondary"],
.stButton button[kind="secondary"] {
    background: transparent;
    color: var(--slate);
    border: 1px solid var(--line);
    border-radius: 999px;
    font-size: 0.88rem;
    padding: 0.25rem 0.9rem;
    transition: color .2s, border-color .2s, background .2s;
}
button[data-testid="stBaseButton-secondary"]:hover,
.stButton button[kind="secondary"]:hover {
    color: var(--mint);
    border-color: var(--mint);
    background: rgba(127, 227, 196, 0.08);
}

button[data-testid="stBaseButton-primary"],
.stButton button[kind="primary"] {
    background: linear-gradient(100deg, #7FE3C4 0%, #A78BFA 100%);
    color: #0B1220;
    font-weight: 600;
    border: none;
    border-radius: 14px;
    padding: 0.65rem 1.6rem;
    transition: transform .15s, box-shadow .2s;
}
button[data-testid="stBaseButton-primary"]:hover,
.stButton button[kind="primary"]:hover {
    color: #0B1220;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(127, 227, 196, 0.25);
}
button:focus-visible {
    outline: 2px solid var(--mint) !important;
    outline-offset: 2px;
}

/* ---------- Answer cards ---------- */
.card {
    margin-top: 1.25rem;
    padding: 1.25rem 1.4rem;
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 18px;
    backdrop-filter: blur(8px);
}
.card h3 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    font-size: 1.35rem;
    margin: 0 0 0.5rem;
    padding: 0;
    color: var(--mist);
}
.card p {
    margin: 0;
    line-height: 1.7;
    color: #CBD8E3;
}
.card.answer { border-color: rgba(167, 139, 250, 0.4); }

div[data-testid="stAlert"] {
    background: rgba(167, 139, 250, 0.10);
    border: 1px solid rgba(167, 139, 250, 0.35);
    border-radius: 12px;
    color: var(--mist);
}

.chip-label {
    margin: 1.1rem 0 0.4rem;
    font-size: 0.9rem;
    color: var(--slate);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ------------------------------------------------------------------
# Hero ( icon)
# ------------------------------------------------------------------
def logo_html() -> str:
    if LOGO_PATH.exists():
        encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
        return f'<img class="logo" alt="Aurora Shining Skincare" src="data:image/png;base64,{encoded}">'
    return ""


st.markdown(
    f"""
    <div class="hero">
        {logo_html()}
        <h1>Aurora Chatbot</h1>
        <p>Welcome to Aurora, your AI skincare assistant. Ask about facial
        skin concerns and receive general skincare information.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Disclaimer
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="note">
        Aurora provides general skincare information. It does not diagnose
        skin conditions or replace professional medical advice.
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# User input
# ------------------------------------------------------------------
st.session_state.setdefault("question", "")


def use_example(text: str) -> None:
    st.session_state.question = text


user_question = st.text_input(
    "What is your facial skin concern?",
    placeholder="Example: Why is my skin dry?",
    key="question",
)

st.markdown('<div class="chip-label">Or start with a common concern</div>', unsafe_allow_html=True)

EXAMPLES = {
    "Dry skin": "Why is my skin dry?",
    "Oily skin": "How do I manage oily skin?",
    "Acne": "What can help with acne-prone skin?",
    "Dark spots": "How can I fade dark spots?",
}
chip_cols = st.columns(len(EXAMPLES))
for col, (label, example) in zip(chip_cols, EXAMPLES.items()):
    col.button(label, key=f"chip_{label}", on_click=use_example, args=(example,))

st.write("")

# ------------------------------------------------------------------
# Action
# ------------------------------------------------------------------
if st.button("Get skincare advice", type="primary"):
    if user_question.strip():
        safe_question = html.escape(user_question.strip())

        st.markdown(
            f"""
            <div class="card">
                <h3>Your question</h3>
                <p>{safe_question}</p>
            </div>
            <div class="card answer">
                <h3>Aurora's response</h3>
                <p>Thank you for sharing your concern! Aurora's AI response
                system will be connected in the next development step.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("Please enter your skincare concern.")