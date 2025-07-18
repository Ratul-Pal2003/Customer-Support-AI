import streamlit as st
import asyncio
from assistant.config import INTENTS
from assistant.transcription import transcribe_buffer
from assistant.intent_rag import detect_intent_and_rag
from assistant.audio import start_audio_stream
from assistant.rag_handler import start_rag_thread

st.set_page_config(page_title="AI Voice Assistant", layout="wide")

st.title("🎤 Real-Time Voice Assistant")
st.markdown("This assistant transcribes your voice, detects intent, and responds with AI.")

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("▶️ Start Assistant" if not st.session_state.started else "🔁 Restart Assistant"):
    st.session_state.started = True
    st.success("Assistant is running...")
    start_rag_thread()
    start_audio_stream()

st.markdown("#### Supported Intents")
st.write(INTENTS)
