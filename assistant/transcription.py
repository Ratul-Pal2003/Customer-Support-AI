import numpy as np
import tempfile
import os
import threading
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

from .config import SAMPLE_RATE, MODEL_SIZE
from .intent_rag import detect_intent_and_rag

whisper_model = WhisperModel(MODEL_SIZE, compute_type="auto")

processed_texts = set()
processed_lock = threading.Lock()

def transcribe_buffer(audio_buffer, transcript_q):
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

        transcript_q.put(text)  # Pass to UI safely
        detect_intent_and_rag(text)

    os.remove(filename)
