import sounddevice as sd
import numpy as np
import queue
import threading

from .config import SAMPLE_RATE, BLOCK_DURATION, BUFFER_DURATION
from .transcription import transcribe_buffer

# Shared audio queue
audio_q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"[Audio Warning] {status}")
    audio_q.put(indata.copy())

def stream_audio():
    buffer = []
    max_blocks = int(BUFFER_DURATION / BLOCK_DURATION)

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        blocksize=int(SAMPLE_RATE * BLOCK_DURATION)
    ):
        print("🎙️ Listening... Press Ctrl+C to stop.\n")
        try:
            while True:
                chunk = audio_q.get()
                buffer.append(chunk)
                if len(buffer) > max_blocks:
                    buffer.pop(0)
                full_audio = np.concatenate(buffer, axis=0)
                threading.Thread(
                    target=transcribe_buffer,
                    args=(full_audio,),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("\n🛑 Stopped.")

def start_audio_stream():
    stream_audio()
