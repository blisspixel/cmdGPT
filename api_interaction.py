import requests
import logging
import os

def interact_with_model(model, messages):
    """Interact with the specified OpenAI GPT model."""
    # Fetch the API key from environment variables each time the function is called
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": messages
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error in interact_with_model: {e}")
        return None
