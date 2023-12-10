import os
import subprocess
from dotenv import load_dotenv

def load_environment_variables():
    """Load environment variables from the .env file."""
    load_dotenv()

def check_voiceexamples_file():
    """Check for the existence of the 'voiceexamples.html' file and generate it if not present."""
    html_file_path = 'voiceexamples.html'
    utility_script_path = 'utility-getvoices.py'

    if not os.path.exists(html_file_path):
        print(f"'{html_file_path}' not found. Running '{utility_script_path}' to generate it...")
        subprocess.run(['python', utility_script_path], check=True)
        print(f"'{html_file_path}' has been generated.")
    else:
        print(f"'{html_file_path}' already exists.")
