import fitz  # Correct module import for PyMuPDF
from flask import Flask, request, jsonify
from threading import Thread
import gradio as gr
from transformers import pipeline
from huggingface_hub import login  # Import for Hugging Face authentication
import os  # Import os to access environment variables
from dotenv import load_dotenv  # Import dotenv to load .env file

# Load environment variables from .env file
load_dotenv()

# Authenticate with Hugging Face
try:
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")  # Read token from .env or environment
    if not hf_token:
        raise ValueError("HUGGINGFACE_API_TOKEN is not set.")
    login(token=hf_token)
except Exception as e:
    print(f"❌ Error authenticating with Hugging Face: {str(e)}")

# Load Hugging Face text-generation model safely (CPU only)
try:
    qa_pipeline = pipeline("text-generation", model="gpt2", device=-1)  # Replace with a valid model like 'gpt2'
except Exception as e:  # General exception handling for model loading
    print(f"❌ Error loading AI model: {str(e)}")
    qa_pipeline = None  # Prevent execution if model fails

# Function to extract text from PDF with memory-efficient reading
def extract_text_from_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        return text.strip() if text else "Could not extract text."
    except Exception as e:
        return f"⚠️ Error extracting text: {str(e)}"

# Function to interact with AI safely
def chat_with_ai(prompt):
    if not qa_pipeline:
        return "⚠️ AI model unavailable. Please check the server."
    try:
        response = qa_pipeline(prompt[:800], max_length=250, num_return_sequences=1)[0]['generated_text']
        return response.strip()
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"

# Flask Backend
app = Flask(__name__)
chat_history = []

@app.route("/upload", methods=["POST"])
def upload_files():
    file = request.files.get("file")  # Handle a single file
    if not file:
        return jsonify({"error": "❌ No file uploaded"}), 400

    extracted_text = extract_text_from_pdf(file.read())
    preview = extracted_text[:500]  # Limit preview for efficiency

    return jsonify({"message": "✅ File processed successfully", "preview": preview})

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "⚠️ No valid prompt provided"}), 400

    # Limit chat history to avoid exceeding token limits
    full_prompt = "\n".join(chat_history[-3:]) + f"\nUser: {user_prompt}"

    bot_response = chat_with_ai(full_prompt)
    chat_history.append(f"User: {user_prompt}")
    chat_history.append(f"Bot: {bot_response}")

    return jsonify({"response": bot_response})

# Run Flask in a background thread
def run_flask():
    app.run(port=5001, debug=False, use_reloader=False)

Thread(target=run_flask, daemon=True).start()

# Gradio Interface
def chatbot(file, user_input):
    extracted_text = ""
    if file:
        try:
            # file is expected as a filepath (type="filepath")
            with open(file, "rb") as f:
                extracted_text = extract_text_from_pdf(f.read())
        except Exception as e:
            # handle file read errors gracefully
            extracted_text = f"⚠️ Error reading uploaded file: {e}"
    pdf_content = extracted_text[:1000]  # Limit input length for efficiency

    # Limit user input length to avoid overly long prompts
    user_input = (user_input or "").strip()
    if len(user_input) > 1000:
        user_input = user_input[:1000]

    prompt = f"📝 Analyze this document:\n{pdf_content}\n\n💬 User Query: {user_input}" if file else user_input
    return chat_with_ai(prompt)

# Update Gradio App
interface = gr.Interface(
    fn=chatbot,
    inputs=[
        gr.File(label="📄 Upload a PDF (Optional)", file_types=[".pdf"], type="filepath"),
        gr.Textbox(label="💬 Ask something")
    ],
    outputs="text",
    title="🧠 AI Chatbot with PDF Analysis",
    description="📄 Upload a PDF and chat with an AI model that analyzes document contents."
)

# Launch Gradio app non-blocking and fail gracefully
try:
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False, debug=False, prevent_thread_lock=True)
except Exception as e:
    print(f"❌ Gradio failed to launch: {e}")
