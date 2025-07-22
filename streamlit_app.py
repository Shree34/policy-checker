"""
HackRx 6.0 – Insurance Assistant
"""

import os, json, textwrap, streamlit as st
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai
from dotenv import load_dotenv

# ------------------ Gemini ------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"
MAX_CONTEXT = 25_000

# ------------------ helpers ------------------
def summarise(text: str) -> str:
    prompt = f"Ultra-compact summary (120 words) of coverages & exclusions:\n{text[:MAX_CONTEXT]}"
    return genai.GenerativeModel(MODEL).generate_content(prompt).text.strip()

def answer_structured(question: str, summary: str) -> dict:
    prompt = textwrap.dedent(f"""
        You are an expert insurance analyst.
        Policy summary:
        {summary}

        Question:
        {question}

        Reply **only** valid JSON:
        {{
          "decision": "Approved" | "Rejected",
          "justification": "<short reason>",
          "relevant_clauses": ["<excerpt>", "..."]
        }}
    """)
    try:
        raw = genai.GenerativeModel(MODEL).generate_content(prompt).text.strip()
        raw = raw.removeprefix("```json").removesuffix("```").strip()
        return json.loads(raw)
    except Exception:
        return {"decision": "Error", "justification": "Parse failure", "relevant_clauses": []}

def summarise_all(files) -> str:
    texts = [f.read().decode("utf-8", errors="ignore") for f in files]
    for f in files:
        f.seek(0)
    with ThreadPoolExecutor() as pool:
        summaries = list(pool.map(summarise, texts))
    return "\n\n".join(summaries)

# ------------------ UI ------------------
st.set_page_config(page_title="Insurance AI", layout="centered")

# --- Hero / header ---
st.markdown(
    """
    <style>
    body {font-family: 'Segoe UI', sans-serif;}
    .hero {text-align: center; margin-bottom: 2rem;}
    .hero h1 {font-weight: 700; font-size: 2.2rem; color: #1E1E1E;}
    .sub {color: #666; font-size: 1rem;}
    .footer {text-align: center; font-size: 0.8rem; color: #999; margin-top: 4rem;}
    .file-uploader {max-width: 600px; margin: auto;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🏥 HackRx 6.0</h1>
        <div class="sub">Minimal Insurance Policy Assistant</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- File uploader (once) ---
with st.container():
    uploaded = st.file_uploader(
        "",
        type=["txt", "pdf"],
        accept_multiple_files=True,
        key="files",
        help="Upload one or more policy documents, then start asking.",
    )

# --- Chat area ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# ---- bottom input ----
if uploaded:
    # summarise once
    if "summary" not in st.session_state:
        with st.spinner("Reading & summarising policies…"):
            st.session_state.summary = summarise_all(uploaded)

    prompt = st.chat_input("Ask anything about the policies…", key="chat_input")
    if prompt:
        st.session_state.messages.append(("user", prompt))
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                result = answer_structured(prompt, st.session_state.summary)
            formatted = (
                f"**Decision:** {result['decision']}\n\n"
                f"**Justification:** {result['justification']}\n\n"
                f"**Relevant Clauses:**\n"
                + "\n".join(f"- {c}" for c in result["relevant_clauses"])
            )
            st.session_state.messages.append(("assistant", formatted))
            st.write(formatted)

else:
    st.info("📂 Upload at least one policy file to begin.")

# --- Footer ---
st.markdown(
    '<div class="footer">Powered by Google Gemini & Streamlit</div>',
    unsafe_allow_html=True,
)
