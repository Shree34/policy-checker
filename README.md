Insurance Assistant  

1. What it is  
A **zero-friction, plain-English insurance helper**.  
Upload any number of `.txt` or `.pdf` policy documents, ask a question, and get a **single, human answer**—no JSON, no code, no long error dumps.

2. Live demo  
https://insurance-assistant.streamlit.app  

3. Features  
• **Merged context** – all policies are concatenated into one prompt, so you get one concise answer instead of a list of per-file replies.  
• **Plain text only** – the model is forced to return conversational English, never JSON or markup.  
• **Rate-limit aware** – if you hit the free-tier quota, the user sees a single friendly sentence instead of a wall of text.  
• **Drag-and-drop UI** – multi-file upload, chat history, mobile-friendly.  
• **One-click deploy** – works on Streamlit Cloud, Hugging Face Spaces, or any server with `streamlit run`.

4. Tech stack  
• Python ≥ 3.9  
• Streamlit · Google Generative AI SDK (`google-generativeai`)  
• Gemini 1.5 Flash (1 M token context)  

5. 30-second quick start  
```bash
git clone https://github.com/<your-org>/insurance-assistant.git
cd insurance-assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# add GEMINI_API_KEY=your_key_here in .env
streamlit run streamlit_app.py
```

6. Environment variables  
| Variable | Required | Purpose |  
| --- | --- | --- |  
| `GEMINI_API_KEY` | ✅ | Google AI Studio / Vertex key |  
| `PORT` | ❌ | Only for Render / Heroku (default 8501) |  

7. Folder layout  
```
insurance-assistant/
├── streamlit_app.py        # main app
├── requirements.txt        # 4 lines
├── .env.example            # shows GEMINI_API_KEY
└── README.md               # this file
```

8. Deployment options  
A. **Streamlit Community Cloud**  
   1. Fork the repo  
   2. Go to https://share.streamlit.io → “New app” → pick your fork  
   3. Paste `GEMINI_API_KEY` in the Secrets box  
   4. Deploy  

B. **Hugging Face Spaces**  
   Choose “Streamlit” template → add `GEMINI_API_KEY` under Settings → Variables.  

C. **Docker**  
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

9. Extending / hacking  
• Swap `gemini-1.5-flash` for `gemini-1.5-pro` in `MODEL` if you have higher limits.  
• To support `.docx`, add `python-docx` and read paragraphs in `merge_docs()`.  
• To persist chat history, dump `st.session_state.messages` to SQLite or Firestore on every turn.  

10. License  
MIT – feel free to embed in commercial products.

11. Contributing  
Issues and PRs welcome. Please run `black . && ruff check` before submitting.

