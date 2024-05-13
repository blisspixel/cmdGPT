import os
import argparse
import asyncio
import openai
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, init

from utils import (clear_screen, display_initial_title, display_short_title, 
                   animate_processing, clear_processing_message, sanitize_for_filename, check_and_run_getvoices)
from logging_config import setup_logging
from voice_handler import select_voice, load_custom_voices, stream_audio_websocket
from chat_management import save_chat_transcript, save_audio_file, manage_audio_files
from api_interaction import interact_with_model

# Initialize colorama and load environment variables, set up logging
init(autoreset=True)
load_dotenv()
setup_logging()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define colors for different types of messages
user_color = Fore.GREEN
cmdGPT_color = Fore.WHITE
system_color = Fore.LIGHTBLACK_EX

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="cmdGPT Chat Application")
    parser.add_argument('--model', type=str, default=None, help='Choose the model to use')
    parser.add_argument('--voice', type=int, default=None, help='Choose the voice option')
    parser.add_argument('--system', type=str, default=None, help='Specify a system message')
    return parser.parse_args()

def select_model():
    """Select the GPT model to use."""
    print("\nSelect a model:")
    models = {
        "1": "gpt-4o-2024-05-13",
        "2": "gpt-4-turbo-2024-04-09",
        "3": "gpt-4-0125-preview",
        "4": "gpt-4-1106-preview",
        "5": "gpt-4-vision-preview",
        "6": "gpt-3.5-turbo-1106",
        "7": "gpt-3.5-turbo"
    }
    for key, value in models.items():
        print(f"{key}. {value}")
    choice = input("Enter your choice (default is 1): ")
    return models.get(choice, "gpt-4o-2024-05-13")

async def chat():
    check_and_run_getvoices()
    args = parse_args()

    while True:
        display_initial_title()

        # Select model
        model = args.model if args.model else select_model()

        # Load custom voices and handle voice configuration
        custom_voices = load_custom_voices()
        if args.voice is not None:
            try:
                voice_config = custom_voices[args.voice - 1]
            except IndexError:
                print("Invalid voice option. Defaulting to No Voice.")
                voice_config = None
        else:
            voice_config = select_voice()

        # Function to select input mode
        def select_input_mode():
            print("\nSelect input mode:")
            print("1. Standard (Single line input)")
            print("2. Multi-line (Type 'end' on a new line to finish)")
            choice = input("Enter your choice (default is 1): ")
            return choice.strip() == "2"  # Returns True for multi-line, False for standard

        # Select input mode
        input_mode_multiline = select_input_mode()

        # Handling system message
        system_message = args.system if args.system else input(f"\n{system_color}Enter a system message or press Enter for default: ")
        if not system_message:
            system_message = "You are a helpful assistant who responds very accurately, VERY concisely, and intelligently. Respond with an element of reddit/4chan humor but keep it professional."

        clear_screen()
        display_short_title(model, voice_config['name'] if voice_config else None, system_message)
        messages = [{"role": "system", "content": system_message}]
        last_saved_index = 0

        while True:
            if input_mode_multiline:
                # Multi-line input with reset handling
                print(f"\n{user_color}Enter your text (type 'end' on a new line to finish, or type 'reset' to restart):")
                user_input_lines = []
                while True:
                    line = input(f"{user_color}")
                    if line.lower() == "end":
                        break
                    elif line.lower() == "reset":
                        user_input = "reset"
                        break
                    user_input_lines.append(line)
                if line.lower() != "reset":
                    user_input = "\n".join(user_input_lines)
            else:
                # Standard single line input
                user_input = input(f"\n{user_color}You: ")

            if user_input.lower() in ["exit", "quit"]:
                save_chat_transcript(messages, last_saved_index)
                return
            elif user_input.lower() == "reset":
                break  # Break the inner loop to restart selections
            elif user_input.lower() == "clear":
                save_chat_transcript(messages, last_saved_index)
                messages = [{"role": "system", "content": system_message}]
                last_saved_index = len(messages)
                clear_screen()
                display_short_title(model, voice_config['name'] if voice_config else None, system_message)
                continue

            messages.append({"role": "user", "content": user_input})

            processing_task = asyncio.create_task(animate_processing(f"{system_color}Processing OpenAI Chat"))
            response = await asyncio.to_thread(interact_with_model, model, messages)
            processing_task.cancel()
            clear_processing_message()

            if response:
                if voice_config:
                    audio_processing_task = asyncio.create_task(animate_processing(f"{system_color}Processing Audio"))

                    def stop_audio_animation():
                        audio_processing_task.cancel()
                        clear_processing_message()

                    audio_buffer = await stream_audio_websocket(voice_config, response, stop_audio_animation)

                    if audio_buffer is not None:
                        response_filename = sanitize_for_filename(response)
                        audio_filename = f"{response_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
                        save_audio_file(audio_buffer, audio_filename)
                        manage_audio_files()
                    else:
                        print("An error occurred in audio streaming: audio_buffer is None")

                    print(f"{cmdGPT_color}cmdGPT: {response}")
                else:
                    print(f"{cmdGPT_color}cmdGPT: {response}")

                messages.append({"role": "assistant", "content": response})
                save_chat_transcript(messages, last_saved_index)
                last_saved_index = len(messages)

if __name__ == "__main__":
    asyncio.run(chat())
