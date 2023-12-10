import os
import subprocess
import random
import platform
import asyncio
from datetime import datetime
from colorama import Fore, init

# Initialize colorama for colored terminal text
init(autoreset=True)

def check_and_run_getvoices():
    """Check if 'voiceexamples.html' exists and run 'getvoices.py' if not."""
    if not os.path.exists('voiceexamples.html'):
        print("Running 'getvoices.py' to generate 'voiceexamples.html'...")
        subprocess.run(['python', 'getvoices.py'])

def clear_screen():
    """Clears the terminal screen."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def display_initial_title():
    """Displays the initial ASCII art title and instructions."""
    title_colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    chosen_color = random.choice(title_colors)
    title = f"{chosen_color}                    _  ____ ____ _____\n  ___ _ __ ___   __| |/ ___|  _ \\_   _|\n / __| '_ ` _ \\ / _` | |  _| |_) || |  \n| (__| | | | | | (_| | |_| |  __/ | |  \n \\___|_| |_| |_|\\__,_|\\____|_|    |_|"
    print(title)
    print("\nInstructions:")
    print("- Type 'clear' to start a new chat.")
    print("- Type 'reset' to reset the chat and set a new system message.")
    print("- Type 'exit' or 'quit' to end the session.")
    print("----------------------------------------------")

def display_short_title(model_name, voice_name, system_message):
    """Displays a short title with the selected model, voice name, and system message."""
    system_color = Fore.LIGHTBLACK_EX
    voice_display = f" | {voice_name}" if voice_name else " | No Voice"
    print(f"{system_color}cmdGPT | {model_name}{voice_display} | '{system_message}' | 'clear', 'reset', 'exit' or 'quit'")


def sanitize_for_filename(text, max_length=20):
    """Sanitizes a string to be safe for use as a filename."""
    invalid_chars = '<>:"/\\|?*'
    sanitized = ''.join(c for c in text if c not in invalid_chars)
    return sanitized[:max_length]

async def animate_processing(message):
    """Animate a processing message."""
    dots = 1
    while True:
        print(f"\r{message}" + "." * dots + " " * (3 - dots), end="")
        dots = (dots % 3) + 1
        await asyncio.sleep(0.5)

def clear_processing_message():
    """Clear the processing message."""
    print("\r" + " " * 60 + "\r", end="")