from google import genai
from PIL import Image
import config

def get_gemini_client():
    """
    Initializes and returns the Gemini client using the API key from config.py.
    """
    api_key = config.get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")
    return genai.Client(api_key=api_key)

def analyze_code_error(image: Image.Image, mode: str) -> str:
    """
    Analyzes the uploaded code error image using Gemini API based on the mode.
    
    Parameters:
        image (PIL.Image.Image): The uploaded screenshot of the error/code.
        mode (str): Either "Hints" or "Solution with code".
        
    Returns:
        str: Markdown formatted response from Gemini.
    """
    client = get_gemini_client()
    
    if mode == "Hints":
        prompt = (
            "You are an expert programming tutor and debugging assistant.\n"
            "Analyze the uploaded image, which contains a code error, traceback, or buggy code.\n"
            "Provide helpful hints, explanations, and guidance to help the user understand and fix the issue themselves.\n"
            "DO NOT write the final corrected code block or complete solution code. Focus on guiding the user conceptually.\n"
            "Provide your response in clear, well-structured Markdown."
        )
    elif mode == "Solution with code":
        prompt = (
            "You are an expert software engineer and debugger.\n"
            "Analyze the uploaded image, which contains a code error, traceback, or buggy code.\n"
            "1. Explain the bug or error clearly, including what caused it.\n"
            "2. Provide the corrected code blocks showing the solution.\n"
            "3. Explain the changes made to fix the issue.\n"
            "Provide your response in clear, beautiful, and well-structured Markdown."
        )
    else:
        raise ValueError(f"Invalid mode: {mode}")
        
    response = client.models.generate_content(
        model=config.get_model_name(),
        contents=[image, prompt]
    )
    
    return response.text
