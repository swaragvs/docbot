import gradio as gr
from pdf_utils import extract_text_from_pdf
from ai_utils import chat_with_ai

def chatbot(file, user_input, history):
    if file:
        with open(file, "rb") as f:
            extract_text_from_pdf(f.read())
    response = chat_with_ai(user_input)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    return history, ""

def reset_chat():
    return [], ""

def launch_gradio():
    with gr.Blocks() as interface:
        gr.Markdown("# 🧠 AI Chatbot with PDF Analysis")
        gr.Markdown("📄 Upload a PDF and chat with an AI model analyzing its contents.")
        
        pdf_input = gr.File(label="📄 Upload a PDF", file_types=[".pdf"], type="filepath")
        chatbot_ui = gr.Chatbot(label="💬 Chat with AI", type="messages")
        user_input = gr.Textbox(label="💬 Ask something", placeholder="Type your question here...")
        reset_button = gr.Button("Reset Chat")
        
        history_state = gr.State([])
        user_input.submit(chatbot, inputs=[pdf_input, user_input, history_state], outputs=[chatbot_ui, user_input])
        reset_button.click(reset_chat, inputs=[], outputs=[chatbot_ui, user_input, history_state])

    try:
        interface.launch(share=True)
    except Exception as e:
        print(f"⚠️ Could not create share link: {str(e)}. Launching locally.")
        interface.launch(share=False)
