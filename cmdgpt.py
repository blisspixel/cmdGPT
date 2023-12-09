import os
import platform
import logging
import threading
import random
import asyncio
import subprocess
import websockets
import json
import base64
import pyaudio
import argparse
import requests
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
from datetime import datetime
from colorama import init, Fore
import openai
from dotenv import load_dotenv

# Initialize environment and colorama
load_dotenv()
init(autoreset=True)

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
log_filename = datetime.now().strftime("logs/cmdgptlog%Y%m%d.txt")
logging.basicConfig(filename=log_filename, level=logging.DEBUG)

def parse_args():
    parser = argparse.ArgumentParser(description="cmdGPT Chat Application")
    # Updated model choices
    parser.add_argument('--model', type=str, default='gpt-4-1106-preview', choices=['gpt-4-1106-preview', 'gpt-4-vision-preview', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo'], help='Choose the model to use')
    parser.add_argument('--voice', type=int, default=0, help='Choose the voice option (0 for no voice)')
    return parser.parse_args()

# Initialize OpenAI client with BETA endpoint
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to the 'voiceexamples.html' file
html_file_path = 'voiceexamples.html'

# Path to the 'utility-getvoices.py' script
utility_script_path = 'utility-getvoices.py'

# Check if 'voiceexamples.html' exists
if not os.path.exists(html_file_path):
    print(f"'{html_file_path}' not found. Running '{utility_script_path}' to generate it...")
    
    # Run the 'utility-getvoices.py' script
    subprocess.run(['python', utility_script_path], check=True)

    print(f"'{html_file_path}' has been generated.")

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v1"
}

# Define colors for different types of messages
user_color = Fore.RED
cmdGPT_color = Fore.WHITE
system_color = Fore.LIGHTBLACK_EX

# Clear screen function for different OS
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Display initial ASCII art title
def display_initial_title():
    title_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    chosen_color = random.choice(title_colors)
    title = f"{chosen_color}                    _  ____ ____ _____\n  ___ _ __ ___   __| |/ ___|  _ \\_   _|\n / __| '_ ` _ \\ / _` | |  _| |_) || |  \n| (__| | | | | | (_| | |_| |  __/ | |  \n \\___|_| |_| |_|\\__,_|\\____|_|    |_|"
    print(title)
    print("\nInstructions:")
    print("- Type 'clear' to start a new chat.")
    print("- Type 'reset' to reset the chat and set a new system message.")
    print("- Type 'exit' or 'quit' to end the session.")
    print("----------------------------------------------")

# Display a short title
def display_short_title(model_name):
    print(f"{system_color}cmdGPT | {model_name} | 'clear', 'reset', 'exit' or 'quit'")

# Function to animate the processing message
async def animate_processing(message):
    dots = 1
    while True:
        print(f"\r{message}" + "." * dots + " " * (3 - dots), end="")
        dots = (dots % 3) + 1
        await asyncio.sleep(0.5)  # Adjust the speed of animation as needed

# Function to clear the processing message
def clear_processing_message():
    print("\r" + " " * 60 + "\r", end="")

def select_model():
    print("\nSelect a model:")
    models = {
        "1": "gpt-4-1106-preview",  # Latest GPT-4 model
        "2": "gpt-4",
        "3": "gpt-3.5-turbo-1106",
        "4": "gpt-3.5-turbo",
        # "5": "future-model-placeholder"  # Placeholder for future models
    }
    for key, value in models.items():
        print(f"{key}. {value}")
    choice = input("Enter your choice (default is 1): ")
    return models.get(choice, "gpt-4-1106-preview")  # Default to latest GPT-4 model

def interact_with_model(model, messages):
    try:
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error in interact_with_model: {e}")
        return None

def load_custom_voices():
    config_path = "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: config.json file not found.")
    except json.JSONDecodeError:
        print("Error: config.json is not properly formatted.")
    return []

def select_voice():
    print("\nSelect a voice or type '0' for no voice:")
    custom_voices = load_custom_voices()

    print("0. No Voice")
    for i, voice in enumerate(custom_voices, 1):
        print(f"{i}. {voice['name']}")

    voice_choice = input("Enter your choice: ")
    print(f"Voice choice entered: '{voice_choice}'")  # Debug print

    if not voice_choice or voice_choice == '0':  # Handle empty input or '0' as no voice
        return None

    try:
        voice_index = int(voice_choice) - 1
        if 0 <= voice_index < len(custom_voices):
            return custom_voices[voice_index]
    except ValueError:
        pass

    print("Invalid choice, defaulting to No Voice.")
    return None

def select_model_and_voice():
    model = select_model()
    voice_config = select_voice()
    print(f"Model selected: '{model}', Voice config selected: '{voice_config}'")  # Debug print
    return model, voice_config

def save_chat_transcript(messages):
    if not os.path.exists('chat_transcripts'):
        os.makedirs('chat_transcripts')
    filename = datetime.now().strftime("chat_transcripts/chat_%Y%m%d%H%M%S.txt")
    with open(filename, 'w') as file:
        for message in messages:
            role = message["role"].capitalize()
            content = message["content"]
            file.write(f"{role}: {content}\n")
    manage_transcript_files()

def get_sorted_transcript_files():
    files = [os.path.join("chat_transcripts", f) for f in os.listdir("chat_transcripts")]
    files = [f for f in files if os.path.isfile(f)]
    return sorted(files, key=os.path.getctime)

def manage_transcript_files():
    files = get_sorted_transcript_files()
    while len(files) > 10:
        os.remove(files.pop(0))

def play_audio(audio_segment):
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
        logging.error("Error while playing audio in thread: %s", str(e))

async def stream_audio_websocket(voice_config, text, display_text_callback):
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_config['voice_id']}/stream-input"

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
        progress_chars = ['.', '..', '...']
        progress_idx = 0
        while not is_final:
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("audio"):
                audio_data = base64.b64decode(data["audio"])
                audio_buffer.write(audio_data)

            if data.get("isFinal"):
                is_final = True
            else:
                # Animate processing message
                print(f"\rProcessing Audio {progress_chars[progress_idx % 3]} ", end="")
                progress_idx += 1

        # Clear the processing message right before playing the audio
        print("\r" + " " * 60 + "\r", end="")

        # Display the text right before playing audio
        display_text_callback()

        try:
            # Play the entire buffered audio with a silent segment at the beginning
            audio_buffer.seek(0)
            silence = AudioSegment.silent(duration=800)  # 800 ms of silence
            audio_segment = silence + AudioSegment.from_mp3(audio_buffer)

            # Create and start a new thread for audio playback
            audio_thread = threading.Thread(target=play_audio, args=(audio_segment,))
            audio_thread.start()

            # Optionally, join the thread if you want to wait for it to finish
            # audio_thread.join()           
            
        except Exception as e:
            logging.error("Error while playing audio: %s", str(e))
            print("There was an error playing the audio.")

        # Clean up
        audio_buffer.close()

async def chat():
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=openai.api_key)

    # Parse command line arguments
    args = parse_args()

    # Display initial ASCII art and instructions
    display_initial_title()

    while True:
        # Select model and voice configuration
        model, voice_config = select_model_and_voice()

        clear_screen()
        display_short_title(model)

        messages = []
        system_message = input("\nEnter a system message or press Enter for default: ")
        if not system_message:
            system_message = "You are a helpful assistant who responds very accurately, VERY concisely, and intelligently."
        print(f"\n{system_color}System: {system_message}")
        messages.append({"role": "system", "content": system_message})

        while True:
            user_input = input(f"\n{user_color}You: ")
            if user_input.lower() in ["exit", "quit"]:
                save_chat_transcript(messages)
                return  # Exit the application
            elif user_input.lower() == "reset":
                save_chat_transcript(messages)
                clear_screen()
                display_initial_title()  # Re-display ASCII art
                break
            elif user_input.lower() == "clear":
                save_chat_transcript(messages)
                messages = [{"role": "system", "content": system_message}]
                clear_screen()
                display_short_title(model)
                continue

            messages.append({"role": "user", "content": user_input})

            try:
                processing_task = asyncio.create_task(animate_processing("Processing OpenAI Chat"))  # Start animation

                # Make synchronous call to OpenAI API within an asynchronous context
                response = await asyncio.to_thread(client.chat.completions.create, model=model, messages=messages)

                processing_task.cancel()  # Stop the animation
                clear_processing_message()  # Clear the processing message

                assistant_message = response.choices[0].message.content

                if voice_config:
                    await stream_audio_websocket(voice_config, assistant_message, lambda: print(f"{cmdGPT_color}cmdGPT: {assistant_message}"))
                else:
                    print(f"{cmdGPT_color}cmdGPT: {assistant_message}")

                messages.append({"role": "assistant", "content": assistant_message})

            except Exception as e:
                processing_task.cancel()  # Stop the animation in case of an error
                print("\r" + " " * 50 + "\r", end="")  # Clear the 'Processing...' message
                logging.error("Error while getting response from OpenAI: %s", str(e))
                print("There was an error processing the request. Check the logs for more details.")

if __name__ == "__main__":
    asyncio.run(chat())