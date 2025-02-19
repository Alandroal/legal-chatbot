import gradio as gr
import requests

# Function to call FastAPI backend
def ask_legal_bot(user_input, history=None):
    print(f"🛠️ Debug: Received user input -> {user_input}")  # Debugging print

    response = requests.post("http://127.0.0.1:8000/query", json={"query": user_input})
    
    if response.status_code != 200:
        print("❌ Error: Backend returned non-200 status code")
        return "Error: Unable to get response from server.", history

    bot_reply = response.json().get("response", "Sorry, I couldn't process that.")

    # Ensure history is initialized
    if history is None:
        history = []

    # Append messages in OpenAI-style format
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_reply})

    # Debugging - Print history format
    print(f"✅ Debug: Sending history -> {history}")  

    return "", history  # ✅ Return empty string + message history as a tuple

# Define Gradio Chat Interface with OpenAI-style messaging
chatbot_ui = gr.ChatInterface(
    fn=ask_legal_bot, 
    title="Legal Assistant Chatbot", 
    type="messages"  # ✅ Ensures correct message format
)

# Launch the chatbot UI
chatbot_ui.launch(share=True)



