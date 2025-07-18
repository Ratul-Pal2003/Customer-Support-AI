import edge_tts
import os
import time
import pygame
from threading import Lock
import subprocess

audio_play_lock = Lock()

# Optional: disable audio playback in headless mode (e.g., Streamlit Cloud)
IS_HEADLESS = os.getenv("STREAMLIT_ENV") == "cloud"

def safe_play_audio(mp3_file):
    if IS_HEADLESS:
        print(f"[HEADLESS] Skipping audio playback: {mp3_file}")
        return

    if audio_play_lock.acquire(blocking=False):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"[Audio Error] {e}")
        finally:
            pygame.mixer.quit()
            audio_play_lock.release()

async def speak_with_edge_tts(text: str):
    try:
        mp3_file = "response.mp3"

        # Cleanup old file
        if os.path.exists(mp3_file):
            try:
                os.remove(mp3_file)
            except PermissionError:
                print(f"[Wait] Waiting to delete locked {mp3_file}...")
                time.sleep(0.5)

        # Generate MP3 using Edge TTS
        communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
        await communicate.save(mp3_file)

        time.sleep(0.2)  # Ensure file is written
        safe_play_audio(mp3_file)

        # Final cleanup
        try:
            os.remove(mp3_file)
        except Exception as e:
            print(f"[Cleanup Error] Couldn't delete {mp3_file}: {e}")

    except Exception as e:
        print(f"[TTS Error] {e}")
