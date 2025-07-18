import edge_tts
import os
import time
import simpleaudio as sa
from threading import Lock
import subprocess

audio_play_lock = Lock()

def safe_play_audio(wav_file):
    if audio_play_lock.acquire(blocking=False):
        try:
            wave_obj = sa.WaveObject.from_wave_file(wav_file)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        finally:
            audio_play_lock.release()

async def speak_with_edge_tts(text: str):
    try:
        mp3_file = "response.mp3"
        wav_file = "response.wav"

        # Cleanup old files
        for file in [mp3_file, wav_file]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except PermissionError:
                    print(f"[Wait] Waiting to delete locked {file}...")
                    time.sleep(0.5)

        # Generate MP3 using Edge TTS
        communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
        await communicate.save(mp3_file)

        # Convert to WAV using ffmpeg
        subprocess.run(
            ["ffmpeg", "-y", "-i", mp3_file, wav_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(0.2)  # Ensure file is written
        safe_play_audio(wav_file)

        # Final cleanup
        for file in [mp3_file, wav_file]:
            try:
                os.remove(file)
            except Exception as e:
                print(f"[Cleanup Error] Couldn't delete {file}: {e}")

    except Exception as e:
        print(f"[TTS Error] {e}")
