from dotenv import load_dotenv
import os
from google import genai
import streamlit as st
from io import BytesIO
# pyrefly: ignore [missing-import]
from gtts import gTTS




load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = os.getenv('GEMINI_MODEL')

client = genai.Client(api_key=api_key)




def genNote(images, difficulty):
    with st.spinner("Processing your notes..."):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                images,
                f"""You are an expert academic professor. Your task is to transcribe, structure, and synthesize comprehensive study notes from the provided whiteboard images/lecture slides.
                
                Target Difficulty Level: {difficulty}
                
                Follow these strict guidelines:
                1. STRUCTURE: Organize the content using a clear hierarchy (H1 for Main Topic, H2 for sub-topics, H3 for details).
                2. FORMATTING: Use Markdown formatting:
                   - Bold key terminology upon first occurrence.
                   - Use structured bullet points, numbered lists, or blockquotes to highlight core definitions.
                   - Create tables to compare concepts or summarize data if present.
                   - Use standard LaTeX/Math syntax (e.g., $f(x)$ or $$formula$$) for any mathematical equations.
                3. ADAPT DIFFICULTY:
                   - Easy: Keep language simple, explain jargon, use intuitive analogies, focus on foundational ideas.
                   - Medium: Standard academic level, balance formulas and conceptual explanations.
                   - Hard: High technical rigor, deep details, formal definitions, and advanced insights.
                4. ACCURACY: Base your output directly on the whiteboard content. Do not invent unrelated concepts, but present shorthand notes in full, grammatically correct sentences.
                5. OUTPUT CONSTRAINT: Output ONLY the markdown notes. Do not write any conversational preambles or postambles (e.g., do not say "Here are the notes:"). Start immediately with the title (#)."""
            ]
        )
        return response.text



def genAudio(images, difficulty):
    with st.spinner("Processing your notes..."):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[
                images,
                f"""You are an expert academic professor. Write a brief, engaging spoken audio script (around 100-150 words) that summarizes the provided whiteboard images for a student listening on the go.
                Do not include any introductory or concluding remarks (such as "Sure, here is the script"), output only the raw spoken script itself.
                
                Target Difficulty Level: {difficulty}"""
            ]
        )
        audio_script = response.text
        tts = gTTS(text=audio_script, lang="en")
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_script, audio_fp