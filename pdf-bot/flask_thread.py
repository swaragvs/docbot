from flask import Flask, request, jsonify
from threading import Thread
from pdf_utils import extract_text_from_pdf
from ai_utils import chat_with_ai, chat_history

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_files():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "❌ No file uploaded"}), 400
    preview = extract_text_from_pdf(file.read())
    return jsonify({"message": "✅ File processed successfully", "preview": preview})

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "⚠️ No valid prompt provided"}), 400
    bot_response = chat_with_ai(user_prompt)
    chat_history.append({"role": "user", "content": user_prompt})
    chat_history.append({"role": "assistant", "content": bot_response})
    return jsonify({"response": bot_response})

def run_flask():
    Thread(target=lambda: app.run(port=5001, debug=False, use_reloader=False), daemon=True).start()
