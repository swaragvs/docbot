from transformers import pipeline
import os
import requests

chat_history = []
pdf_memory = ""

# Load Hugging Face model
try:
    qa_pipeline = pipeline("text-generation", model="gpt2", device=-1)
except Exception as e:
    raise RuntimeError(f"❌ Error loading AI model: {str(e)}")

def web_search(query):
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    if not api_key or not search_engine_id:
        return "⚠️ Web search is not configured."
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("items", [])
        return "\n".join(f"{item['title']}: {item['link']}" for item in results[:3])
    return "⚠️ No search results found."

def chat_with_ai(prompt):
    global pdf_memory
    if not qa_pipeline:
        return "⚠️ AI model unavailable."
    
    if "search:" in prompt.lower():
        return web_search(prompt.split("search:", 1)[1].strip())
    
    full_context = f"Document:\n{pdf_memory[:2000]}\n\nUser: {prompt}"
    try:
        response = qa_pipeline(full_context, max_length=250, num_return_sequences=1)[0]["generated_text"]
        return response
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"
