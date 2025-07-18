import streamlit as st
import time
import threading

from assistant.config import INTENTS
from assistant.transcription import transcribe_buffer
from assistant.intent_rag import detect_intent_and_rag
from assistant.audio import start_audio_stream
from assistant.rag_handler import start_rag_thread

st.set_page_config(page_title="AI Voice Assistant", layout="wide")

st.title("🎤 Real-Time Voice Assistant")
st.markdown("This assistant transcribes your voice, detects intent, and responds with AI.")

# Initialize state
if "started" not in st.session_state:
    st.session_state.started = False
if "live_transcript" not in st.session_state:
    st.session_state.live_transcript = ""
if "transcript_history" not in st.session_state:
    st.session_state.transcript_history = []

# UI Controls
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.started:
        if st.button("▶️ Start Assistant"):
            st.session_state.started = True
            st.success("Assistant is running...")
            start_rag_thread()
            threading.Thread(target=start_audio_stream, daemon=True).start()
            threading.Thread(target=lambda: update_transcript_loop(), daemon=True).start()

with col2:
    if st.session_state.started:
        if st.button("⏹ Stop Assistant"):
            st.session_state.started = False
            st.warning("Assistant stopped.")

# Live Transcript
st.markdown("### 📝 Live Transcript")
transcript_placeholder = st.empty()

# Transcript History
st.markdown("### 📜 Transcript History")
history_box = st.container()

# Background UI update loop
def update_transcript_loop():
    while st.session_state.get("started", False):
        current = st.session_state.get("live_transcript", "").strip()
        if current and (len(st.session_state.transcript_history) == 0 or current != st.session_state.transcript_history[-1]):
            st.session_state.transcript_history.append(current)
        transcript_placeholder.write(f"**{current}**")
        with history_box:
            st.markdown("\n".join(f"- {line}" for line in st.session_state.transcript_history[-15:]))  # show last 15
        time.sleep(1)

# Supported Intents
st.markdown("#### 📚 Supported Intents")
st.write(INTENTS)
