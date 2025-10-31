# AI Chatbot with PDF Analysis

Short description

- Flask backend exposes endpoints for uploading PDFs (/upload) and chatting (/chat).
- Gradio UI that allows optional PDF upload and free-text questions that include document context.
- Uses PyMuPDF (fitz) to extract text and a Hugging Face text-generation pipeline for responses.

Requirements

- Python 3.8+
- Libraries (install using pip):
  pip install -r requirements.txt
  # or manually:
  pip install Flask gradio python-dotenv transformers huggingface_hub pymupdf

Environment

- Create a `.env` file in the project root with your Hugging Face token:
  HUGGINGFACE_API_TOKEN=your_token_here

Notes

- The script uses a CPU-only HF pipeline by default (model='gpt2' in the example). Replace with a suitable model if available.
- Gradio runs on port 7860 by default and is launched non-blocking so the Flask thread can coexist.
- If you only want the backend, you can import and run the Flask app independently.

Run

- From the project directory:
  python test.py

Security & usage

- This project demonstrates local usage; do not expose tokens in public repos.
- Adjust model, token usage, and resource limits for production use.
