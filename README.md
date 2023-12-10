## cmdGPT - Elevate Your CLI with OpenAI GPT & ElevenLabs Voice
Unleash the power of AI in your terminal with cmdGPT! Tailored for tech enthusiasts and developers, this cutting-edge chat interface connects you to the forefront of AI advancements, featuring the latest OpenAI GPT models as of December 2023. Dive into an exhilarating conversational adventure, blending the robust capabilities of GPT-3.5 and GPT-4 with the remarkably lifelike voices from ElevenLabs' text-to-speech technology. cmdGPT isn't just a tool; it's your gateway to exploring the rich possibilities of conversational AI, all within the familiar realm of your command line. Get ready to be captivated by its unique, immersive chatting experience that sets a new standard in AI interactions!

<img src="examples/cmdGPT.png" width="600"/>

### Features
Terminal-based chat interface for a streamlined experience.
Selection from different GPT models, including GPT-3.5 and GPT-4.
Voice selection for audio responses using ElevenLabs text-to-speech technology.
Colorful ASCII art title and startup instructions.
Error logging for troubleshooting.
Optional command-line arguments for model and voice selection.
Chat transcript preservation for record-keeping.

<img src="examples/cmdGPT2.png" width="600"/>

### Prerequisites
Python 3.11 or newer.
openai Python package for OpenAI API interaction.
colorama for terminal color support.
python-dotenv for managing environment variables.
pyaudio and pydub for audio playback functionalities.
OpenAI Service Subscription and ElevenLabs API key.

### Setup & Installation
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

### Usage
Run cmdGPT:
python ./cmdgpt.py
Optionally, specify the model, voice, and system message using:
--model MODEL_NAME for selecting a specific GPT model.
--voice VOICE_OPTION for choosing a voice for audio responses.
--system "SYSTEM_MESSAGE" to set an initial system message.
For Example: python ./cmdgpt.py --model gpt-4-1106-preview --voice 6 --system "Pretend you're Santa Claus but you now need to make a little extra money so you're trying to sell people on extended car warrantys."
If not provided, the application will prompt for these selections.

### Interact with cmdGPT:
Upon starting, an ASCII art title and instructions are displayed.
Choose your desired GPT model and voice option, or hit enter for defaults (the latest model and no voice).
Provide a system message or use the default by pressing Enter.
Start chatting! Type exit or quit to end the session, or reset or clear to restart the chat.

### Additional Voices
When you first run cmdGPT, it will check if the voiceexamples.html file exists.  If not, it will run the utility-getvoices.py script to interact with the Elevenlabs API to build a simple html site to test out different voices.  You can use that information to add those to the config.json to adjust options as you'd like.

### Contributing
Fork the project, open issues, or submit pull requests to contribute. All contributions are welcome!

### License
This project is open-source and available under the MIT License
