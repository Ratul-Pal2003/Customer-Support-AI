import sounddevice as sd
import numpy as np
import queue
import threading

from .config import SAMPLE_RATE, BLOCK_DURATION, BUFFER_DURATION
from .transcription import transcribe_buffer

audio_q = queue.Queue()
stop_event = threading.Event()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"[Audio Warning] {status}")
    audio_q.put(indata.copy())

def stream_audio(transcript_q):
    buffer = []
    max_blocks = int(BUFFER_DURATION / BLOCK_DURATION)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=int(SAMPLE_RATE * BLOCK_DURATION)
    ):
        print("🎙️ Listening... Press Ctrl+C to stop.\n")
        while not stop_event.is_set():
            chunk = audio_q.get()
            buffer.append(chunk)
            if len(buffer) > max_blocks:
                buffer.pop(0)
            full_audio = np.concatenate(buffer, axis=0)
            threading.Thread(
                target=transcribe_buffer,
                args=(full_audio, transcript_q),
                daemon=True
            ).start()

def start_audio_stream(transcript_q):
    stop_event.clear()
    threading.Thread(target=stream_audio, args=(transcript_q,), daemon=True).start()

def stop_audio_stream():
    stop_event.set()
