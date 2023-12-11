import requests
from dotenv import load_dotenv
import os
import json

# Load .env file
load_dotenv()

# Get API key from .env
api_key = os.getenv('ELEVENLABS_API_KEY')

# Check if API key is loaded
if not api_key:
    print("API key not found in .env file.")
    exit()

# ElevenLabs API endpoint
url = 'https://api.elevenlabs.io/v1/voices'

# Headers for the API request
headers = {
    'xi-api-key': api_key
}

# Make the API request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    print(f"Failed to get voices. Status code: {response.status_code}")
    exit()

# Parse response
voices_data = response.json().get('voices', [])

# Start of HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
<title>Voice Samples</title>
<style>
table {
    border-collapse: collapse;
    width: 100%;
}
th, td {
    text-align: left;
    padding: 8px;
}
tr:nth-child(even) {background-color: #f2f2f2;}
pre {
    white-space: pre-wrap;       /* CSS formatting for pre tag */
    margin-left: 20px;           /* Indentation for JSON */
}
</style>
</head>
<body>
<h1>Available Voices</h1>
<table border='1'>
<tr>
<th>Name</th>
<th>Voice ID</th>
<th>Category</th>
<th>Labels</th>
<th>Sample</th>
<th>Config JSON</th>
</tr>
"""

# Function to add indentation
def add_indentation(text, num_spaces=4):
    return '\n'.join(' ' * num_spaces + line for line in text.split('\n'))

# Add voice data to HTML content
for voice in voices_data:
    voice_id = voice.get('voice_id', 'No ID')
    name = voice.get('name', 'No name')
    category = voice.get('category', 'No category')
    labels = ', '.join([f"{key.capitalize()}: {value}" for key, value in voice.get('labels', {}).items()])
    preview_url = voice.get('preview_url', '#')
    voice_config = {
        "name": name,
        "voice_id": voice_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": True
        }
    }

    # Correctly formatted JSON with additional indentation
    formatted_json = json.dumps(voice_config, indent=4)
    formatted_json = add_indentation(formatted_json)
    formatted_json = formatted_json + ",\n" if voice != voices_data[-1] else formatted_json

    html_content += f"<tr><td>{name}</td><td>{voice_id}</td><td>{category}</td><td>{labels}</td><td><audio controls src='{preview_url}'>Your browser does not support the audio element.</audio></td><td><pre>{formatted_json}</pre></td></tr>\n"

# End of HTML content
html_content += """
</table>
</body>
</html>
"""

# Create output HTML file
with open('voiceexamples.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("Voice samples HTML file created: voiceexamples.html")
