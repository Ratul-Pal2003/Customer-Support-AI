import os
from dotenv import load_dotenv

from assistant.audio import stream_audio
from assistant.rag_handler import start_rag_thread
from assistant.config import HF_API_KEY

load_dotenv()

def main():
    if not HF_API_KEY:
        print("❌ Hugging Face API key not found. Set HF_API_KEY as an environment variable.")
        return

    print("✅ Voice assistant starting...\n")
    start_rag_thread()
    stream_audio()

if __name__ == "__main__":
    main()
