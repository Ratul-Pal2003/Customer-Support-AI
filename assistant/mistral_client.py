from huggingface_hub import InferenceClient
import os
from .config import HF_API_KEY

# Shared HF client for Mistral
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    api_key=HF_API_KEY,
    provider="together"
)

def mistral_generate(prompt: str, context: str) -> str:
    try:
        messages = [
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": f"Answer the user's question based on this context:\n\n{context}\n\nUser question:\n{prompt}"}
        ]
        response = client.chat.completions.create(messages=messages, stream=False)
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Mistral API Error: {e}")

def generate_voice_reply(intent: str) -> str:
    prompt = f"""
You are a friendly and helpful voice assistant in a customer service call.
The user wants to: \"{intent}\".

Give a short and helpful response (2–3 sentences max). Do not ask any questions.
Instead, clearly state what the next steps are or what action is being taken.
If needed, ask if the customer would like to speak to a human agent.
"""

    try:
        messages = [
            {"role": "system", "content": "You are a friendly customer service voice bot."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(messages=messages, stream=False)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, there was an error generating a response: {e}"
