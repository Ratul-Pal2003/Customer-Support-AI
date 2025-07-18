import threading
from assistant.mistral_client import mistral_generate
from assistant.state import rag_q

def process_rag():
    while True:
        transcript, context, top_score = rag_q.get()
        try:
            generated_answer = mistral_generate(transcript, context)
            print(f"📚 Generated Answer: {generated_answer} (score: {top_score:.2f})")
        except Exception as e:
            print(f"[Generation Error] {e}")

def start_rag_thread():
    thread = threading.Thread(target=process_rag, daemon=True)
    thread.start()
