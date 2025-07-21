"""
HackRx 6.0 – Insurance Assistant
Plain-text, single-context mode
"""

import os, textwrap, streamlit as st, google.generativeai as genai
from dotenv import load_dotenv

# ---------- Gemini ----------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-1.5-flash"
MAX_TOKENS = 1_000_000   # 1 M token context window

# ---------- helpers ----------
def build_prompt(context: str, question: str) -> str:
    return textwrap.dedent(f"""
        You are an expert insurance analyst.
        Read the combined policy text below and answer the user’s question in **plain, conversational English**.
        Do NOT include JSON, code, or links.

        Policies:
        {context[:MAX_TOKENS]}

        Question:
        {question}

        Answer:
    """).strip()

def merge_docs(files) -> str:
    """Concatenate all uploaded files into one big string."""
    full_text = ""
    for file in files:
        full_text += f"\n\n--- {file.name} ---\n"
        full_text += file.read().decode("utf-8", errors="ignore")
        file.seek(0)   # reset for next read
    return full_text.strip()

# ---------- UI ----------
st.set_page_config(page_title="Insurance AI", layout="centered")
st.title("🏥 HackRx 6.0 – Insurance Assistant")

uploaded = st.file_uploader(
    "📄 Upload policy documents (.txt or .pdf)",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

# chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# display history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

if uploaded:
    prompt = st.chat_input("Ask anything about the policies…")
    if prompt:
        st.session_state.messages.append(("user", prompt))
        st.chat_message("user").write(prompt)

        with st.spinner("Reading all documents…"):
            context = merge_docs(uploaded)
            try:
                model = genai.GenerativeModel(MODEL)
                answer = model.generate_content(build_prompt(context, prompt)).text.strip()
            except Exception as e:
                if "429" in str(e):
                    answer = "🚦 You’ve hit the daily free-tier limit. Please try again tomorrow or upgrade your plan."
                else:
                    answer = f"⚠️ Error: {e}"

        st.session_state.messages.append(("assistant", answer))
        st.chat_message("assistant").write(answer)
else:
    st.info("Upload at least one policy file to start chatting.")