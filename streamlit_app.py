import streamlit as st
import time
import threading
import queue

from assistant.config import INTENTS
from assistant.audio import start_audio_stream, stop_audio_stream
from assistant.rag_handler import start_rag_thread

st.set_page_config(page_title="AI Voice Assistant", layout="wide")

st.title("🎤 Real-Time Voice Assistant")
st.markdown("This assistant transcribes your voice, detects intent, and responds with AI.")

# State
if "started" not in st.session_state:
    st.session_state.started = False
if "live_transcript" not in st.session_state:
    st.session_state.live_transcript = ""
if "transcript_history" not in st.session_state:
    st.session_state.transcript_history = []

transcript_q = queue.Queue()

# UI Controls
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.started:
        if st.button("▶️ Start Assistant"):
            st.session_state.started = True
            st.success("Assistant is running...")
            start_rag_thread()
            start_audio_stream(transcript_q)
            threading.Thread(target=lambda: update_transcript_loop(transcript_q), daemon=True).start()

with col2:
    if st.session_state.started:
        if st.button("⏹ Stop Assistant"):
            st.session_state.started = False
            stop_audio_stream()
            st.warning("Assistant stopped.")

# Transcript display
st.markdown("### 📝 Live Transcript")
transcript_placeholder = st.empty()

st.markdown("### 📜 Transcript History")
history_box = st.container()

def update_transcript_loop(q):
    while st.session_state.get("started", False):
        try:
            text = q.get(timeout=1)
            if text:
                st.session_state.live_transcript = text
                if len(st.session_state.transcript_history) == 0 or text != st.session_state.transcript_history[-1]:
                    st.session_state.transcript_history.append(text)
                transcript_placeholder.write(f"**{text}**")
                with history_box:
                    st.markdown("\n".join(f"- {line}" for line in st.session_state.transcript_history[-15:]))
        except queue.Empty:
            continue

# Intents
st.markdown("#### 📚 Supported Intents")
st.write(INTENTS)
