from flask_thread import run_flask
from gradio_ui import launch_gradio

# Start Flask in a background thread
run_flask()

# Launch Gradio interface
launch_gradio()
