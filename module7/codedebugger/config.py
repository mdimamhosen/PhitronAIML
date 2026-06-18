import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the current directory
load_dotenv()

def get_api_key():
    """
    Retrieves the Gemini API Key from the environment.
    """
    return os.getenv("GEMINI_API_KEY")

def get_model_name():
    """
    Retrieves the Gemini Model name from the environment, defaulting to gemini-3-flash-preview.
    """
    return os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

