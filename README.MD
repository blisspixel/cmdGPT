cmdGPT - A Command Line Interface for OpenAI GPT
cmdGPT is a terminal-based chat interface for interacting with OpenAI's GPT models, tailored for developers and enthusiasts. It offers a quick and straightforward way to chat with various GPT models without a graphical user interface.

Features
Terminal-based chat interface for a streamlined experience.
Selection from different GPT models, including GPT-3.5 and GPT-4.
Voice selection for audio responses using ElevenLabs text-to-speech technology.
Colorful ASCII art title and startup instructions.
Error logging for troubleshooting.
Optional command-line arguments for model and voice selection.
Chat transcript preservation for record-keeping.

Prerequisites
Python 3.11 or newer.
openai Python package for OpenAI API interaction.
colorama for terminal color support.
python-dotenv for managing environment variables.
pyaudio and pydub for audio playback functionalities.
Azure OpenAI Service Subscription and ElevenLabs API key.

Setup & Installation
Clone the repository:
git clone https://github.com/blisspixel/cmdGPT.git

Navigate to the cmdGPT directory:
cd cmdGPT

Install required packages:
pip install openai colorama python-dotenv pyaudio pydub

Setup your .env file:
Create a .env file in the root directory.
Add the following:
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
Replace those API keys with your respective API Keys generated from those services.

Usage
Run cmdGPT:
python ./cmdgpt.py
Optionally, specify the model and voice using --model MODEL_NAME and --voice VOICE_OPTION.
If not provided, the application will prompt for these selections.

Interact with cmdGPT:
Upon starting, an ASCII art title and instructions are displayed.
Choose your desired GPT model and voice option, or hit enter for defaults (the latest model and no voice).
Provide a system message or use the default by pressing Enter.
Start chatting! Type exit or quit to end the session, or reset or clear to restart the chat.

Additional Voices
When you first run cmdGPT, it will check if the voiceexamples.html file exists.  If not, it will run the utility-getvoices.py script to interact with the Elevenlabs API to build a simple html site to test out different voices.  You can use that information to add those to the config.json to adjust options as you'd like.

Contributing
Fork the project, open issues, or submit pull requests to contribute. All contributions are welcome!

License
This project is open-source and available under the MIT License.