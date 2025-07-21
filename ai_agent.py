"""
Gemini-powered insurance analyst
"""

import os, json, textwrap
from typing import Dict, Any
import google.generativeai as genai

GEMINI_MODEL = "gemini-1.5-flash"
MAX_CONTEXT_CHARS = 2000

PROMPT_TEMPLATE = textwrap.dedent("""
You are an expert insurance analyst.
Given the context, answer the question in valid JSON.

Context:
{context}

Question:
{question}

Respond:
{{
  "decision": "Approved" | "Rejected",
  "justification": "<concise>",
  "relevant_clauses": ["<clause1>", "..."]
}}
""").strip()

# Configure Gemini key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_insurance_question(context: str, question: str) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY missing. Set environment variable."}

    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        # Gemini returns Markdown-like ```json … ```  – strip it
        raw = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}