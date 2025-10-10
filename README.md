## Resume Chatbot

A small Gradio chatbot that answers questions about Akanksha using a short summary and text extracted from a LinkedIn PDF.

### Quick start (uv)
```bash
cd /home/akanksha_linux/ai-hands-on/ai-hands-on
uv sync
```

Create a `.env` file in the project root (same folder as the top-level README):
```env
OPENAI_API_KEY=your_openai_key
# Optional (for push notifications via Pushover)
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_USER=your_pushover_user_key
```

Ensure the profile assets exist under this folder:
- `resume/me/summary.txt` — a short bio/summary (plain text)
- `resume/me/linkedin.pdf` — your exported LinkedIn profile PDF

Run the chatbot:
```bash
uv run python resume/app.py
```
This launches a local Gradio UI. Open the printed URL in your browser.

### Files
- `resume/app.py`: Chatbot entry. Loads `.env`, reads `me/summary.txt` and extracts text from `me/linkedin.pdf`, uses OpenAI, and exposes two function-tools that can push notifications via Pushover.
- `resume/me/summary.txt`: Your summary text.
- `resume/me/linkedin.pdf`: Your LinkedIn export PDF.

### Common tasks
- Add a dependency (managed at project root):
```bash
uv add <package>
```

- Ensure your editor uses uv's virtualenv:
```bash
uv run python -c "import sys; print(sys.executable)"
```
Set your IDE interpreter to that path.

### WSL: copy LinkedIn PDF into this folder
From WSL, copy your LinkedIn PDF into `resume/me/`:
```bash
cp "/mnt/c/Users/<WindowsUser>/Downloads/linkedin.pdf" \
   "/home/akanksha_linux/ai-hands-on/ai-hands-on/resume/me/linkedin.pdf"
```

### Troubleshooting
- Import errors (e.g., dotenv): ensure the dep exists in `pyproject.toml` and run `uv sync`. Also confirm your IDE uses the uv venv (`.venv`).
- PDF text empty: verify the PDF is readable; try a different export from LinkedIn.

### License
Personal/experimental use.


