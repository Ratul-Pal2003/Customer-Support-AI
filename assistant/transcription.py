import numpy as np
import tempfile
import os
import threading
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

from .config import SAMPLE_RATE, MODEL_SIZE
from .intent_rag import detect_intent_and_rag

# Whisper model (loaded once)
whisper_model = WhisperModel(MODEL_SIZE, compute_type="auto")

# Used to avoid re-processing same transcriptions
processed_texts = set()
processed_lock = threading.Lock()

def transcribe_buffer(audio_buffer):
    import streamlit as st  # Safe to import here for session state

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        wav.write(filename, SAMPLE_RATE, (audio_buffer * 32767).astype(np.int16))

    segments, _ = whisper_model.transcribe(filename)

    for segment in segments:
        text = segment.text.strip()
        if len(text.split()) < 3 or len(text) < 10:
            continue

        with processed_lock:
            if text in processed_texts:
                continue
            processed_texts.add(text)

        print(f"\n📝 [{segment.start:.1f}s - {segment.end:.1f}s] {text}")

        # Live update for UI
        st.session_state["live_transcript"] = text

        # Intent detection + RAG
        detect_intent_and_rag(text)

    os.remove(filename)
