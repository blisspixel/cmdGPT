import os
from datetime import datetime
from pydub import AudioSegment
from utils import sanitize_for_filename

current_chat_filename = None

def save_chat_transcript(messages, last_saved_index=0, filename=None):
    """Saves the chat transcript to a file, starting from the last saved index."""
    global current_chat_filename

    if not os.path.exists('chat_transcripts'):
        os.makedirs('chat_transcripts')

    if filename is None and current_chat_filename is None:
        current_chat_filename = datetime.now().strftime("chat_transcripts/chat_%Y%m%d%H%M%S.txt")

    try:
        with open(current_chat_filename, 'a', encoding='utf-8') as file:
            for message in messages[last_saved_index:]:
                role = message["role"].capitalize()
                content = message["content"]
                file.write(f"{role}: {content}\n")
    except Exception as e:
        print(f"An error occurred while saving the chat transcript: {e}")

def manage_chat_transcript_files():
    """Manages the storage of chat transcript files."""
    transcript_files = [os.path.join("chat_transcripts", f) for f in os.listdir("chat_transcripts") if f.endswith('.txt')]
    transcript_files.sort(key=os.path.getctime, reverse=True)

    # Keep only the last 10 transcript files
    for file in transcript_files[10:]:
        os.remove(file)

def save_audio_file(audio_buffer, filename):
    if not os.path.exists('chat_transcripts'):
        os.makedirs('chat_transcripts')

    sanitized_filename = sanitize_for_filename(filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    audio_file_path = os.path.join('chat_transcripts', f"{sanitized_filename}_{timestamp}.mp3")

    try:
        with open(audio_file_path, 'wb') as file:
            file.write(audio_buffer.getvalue())
    except OSError as e:
        print(f"An error occurred while saving the audio file: {e}")
    finally:
        audio_buffer.close()

def manage_audio_files():
    """Manages the storage of audio files."""
    audio_files = [os.path.join("chat_transcripts", f) for f in os.listdir("chat_transcripts") if f.endswith('.mp3')]
    audio_files.sort(key=os.path.getctime, reverse=True)

    # Keep only the last 10 audio files
    for file in audio_files[10:]:
        os.remove(file)

def get_sorted_transcript_files():
    """Returns a list of sorted transcript files."""
    files = [os.path.join("chat_transcripts", f) for f in os.listdir("chat_transcripts")]
    files = [f for f in files if os.path.isfile(f)]
    return sorted(files, key=os.path.getctime)

def manage_transcript_files():
    """Manages the storage of all transcript files."""
    files = get_sorted_transcript_files()
    while len(files) > 10:
        os.remove(files.pop(0))