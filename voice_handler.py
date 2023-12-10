import logging
import pyaudio
import json
import threading
import base64
import asyncio
import websockets
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import os

def load_custom_voices():
    """Load custom voice settings from a configuration file."""
    config_path = "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: config.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: config.json is not properly formatted.")
        return []

def select_voice():
    """Allow the user to select a voice option."""
    custom_voices = load_custom_voices()
    print("\nSelect a voice or type '0' for no voice:")
    print("0. No Voice")
    for i, voice in enumerate(custom_voices, 1):
        print(f"{i}. {voice['name']}")

    voice_choice = input("Enter your choice: ")
    if not voice_choice or voice_choice == '0':
        return None

    try:
        return custom_voices[int(voice_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice, defaulting to No Voice.")
        return None

def play_audio(audio_segment):
    """Play an audio segment."""
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(audio_segment.sample_width),
                        channels=audio_segment.channels,
                        rate=audio_segment.frame_rate,
                        output=True)
        stream.write(audio_segment.raw_data)
        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"Error while playing audio: {e}")

async def stream_audio_websocket(voice_config, text, before_audio_play_callback):
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_config['voice_id']}/stream-input"
    try:
        async with websockets.connect(uri) as websocket:
            # Send initial settings
            await websocket.send(json.dumps({
                "text": " ",
                "voice_settings": voice_config.get("voice_settings", {}),
                "xi_api_key": os.getenv("ELEVENLABS_API_KEY"),
            }))

            # Send the text for TTS conversion
            await websocket.send(json.dumps({"text": text + " ", "try_trigger_generation": True}))

            # Signal end of input
            await websocket.send(json.dumps({"text": ""}))

            # Initialize a large audio buffer
            audio_buffer = BytesIO()

            # Receive and buffer the audio
            is_final = False
            while not is_final:
                response = await websocket.recv()
                data = json.loads(response)
                if data.get("audio"):
                    audio_data = base64.b64decode(data["audio"])
                    audio_buffer.write(audio_data)

                if data.get("isFinal"):
                    is_final = True

            # Call the callback right before playing audio
            before_audio_play_callback()

            audio_buffer.seek(0)
            audio_segment = AudioSegment.from_mp3(audio_buffer)

            # Play audio in a new thread
            audio_thread = threading.Thread(target=play_audio, args=(audio_segment,))
            audio_thread.start()

            return audio_buffer

    except Exception as e:
        logging.error(f"Error in stream_audio_websocket: {e}")
        print(f"An error occurred in audio streaming: {e}")