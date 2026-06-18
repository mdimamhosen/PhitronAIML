import os
import io
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from api import genNote, genAudio
from PIL import Image

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

st.set_page_config(
    page_title="Note Summary & Quiz Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Note Summary & Quiz Generator")
st.divider()

# Session state initialization
if "notes_text" not in st.session_state:
    st.session_state.notes_text = None
if "audio_script" not in st.session_state:
    st.session_state.audio_script = None
if "audio_fp" not in st.session_state:
    st.session_state.audio_fp = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []

# Sidebar Configuration
with st.sidebar:
    st.subheader("Upload Notes")
    uploaded_files = st.file_uploader("Upload files (Images, PDFs, Text)", accept_multiple_files=True)
    difficulty = st.radio("Select difficulty level", ["Easy", "Medium", "Hard"])
    clicked = st.button("Process Notes", type="primary")

def clean_json_string(s):
    s = s.strip()
    if s.startswith("```json"):
        s = s[7:]
    elif s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()

# Main Area Implementation
if clicked and uploaded_files and difficulty:
    if not api_key:
        st.error("GEMINI_API_KEY is missing. Please set it in your environment or .env file.")
        st.stop()
        
    client = genai.Client(api_key=api_key)
    
    # Reset session states on new processing
    st.session_state.notes_text = None
    st.session_state.audio_script = None
    st.session_state.audio_fp = None
    st.session_state.quiz_data = None
    st.session_state.quiz_submitted = False
    st.session_state.quiz_answers = []
    
    try:
        images = [Image.open(file) for file in uploaded_files]
        
        # Call genNote from api.py
        summary_text = genNote(images, difficulty)
        st.session_state.notes_text = summary_text
        
        # Call genAudio from api.py
        audio_script, audio_fp = genAudio(images, difficulty)
        st.session_state.audio_script = audio_script
        st.session_state.audio_fp = audio_fp
        
        with st.spinner("Generating Practice Quiz..."):
            quiz_prompt = f"""
            Based on the following study notes, generate a practice quiz with exactly 3 multiple-choice questions.
            The difficulty level should be: {difficulty}.
            
            Return the response as a valid JSON list of 3 objects. Each object must have these exact keys:
            - "question": The question text
            - "options": A list of 4 string options
            - "correct_answer": The exact string of the correct option from the options list
            - "explanation": A brief explanation of why this answer is correct
            
            Notes:
            {summary_text}
            """
            quiz_response = client.models.generate_content(
                model=gemini_model,
                contents=[quiz_prompt],
                config={"response_mime_type": "application/json"}
            )
            cleaned_json = clean_json_string(quiz_response.text)
            st.session_state.quiz_data = json.loads(cleaned_json)
            
    except Exception as e:
        st.error(f"Gemini API Error: The service is currently unavailable or overloaded (503). Please try again in a few moments. (Details: {e})")

elif clicked and not uploaded_files:
    st.warning("Please upload at least one file first")

# Display Results from Session State
if st.session_state.notes_text is not None:
    summary_text = st.session_state.notes_text
    audio_script = st.session_state.audio_script
    audio_fp = st.session_state.audio_fp
    quiz_data = st.session_state.quiz_data
    
    # Display Results in Tabs
    tab1, tab2, tab3 = st.tabs(["Summary", "Audio Guide", "Practice Quiz"])
    
    with tab1:
        st.subheader("Summary Guide")
        st.markdown(summary_text)
        st.download_button(
            label="Download Notes (Markdown)",
            data=summary_text,
            file_name="Study_Guide.md",
            mime="text/markdown"
        )
        
    with tab2:
        st.subheader("Spoken Audio Transcript")
        st.markdown(audio_script)
        st.audio(audio_fp, format="audio/mp3")
        
    with tab3:
        st.subheader("Practice Quiz")
        if quiz_data:
            with st.form("quiz_form"):
                answers = []
                for i, q in enumerate(quiz_data):
                    st.markdown(f"##### Question {i+1}: {q['question']}")
                    ans = st.radio("Choose the correct option:", options=q['options'], key=f"q_{i}", index=None)
                    answers.append(ans)
                    st.divider()
                
                submitted = st.form_submit_button("Submit Answers")
                if submitted:
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_answers = answers
            
            if st.session_state.quiz_submitted:
                st.subheader("Quiz Results")
                score = 0
                for i, q in enumerate(quiz_data):
                    user_ans = st.session_state.quiz_answers[i]
                    correct_ans = q['correct_answer']
                    
                    st.markdown(f"**Question {i+1}: {q['question']}**")
                    st.write(f"Your Answer: `{user_ans}`")
                    if user_ans == correct_ans:
                        st.success("Correct!")
                        score += 1
                    else:
                        st.error(f"Incorrect. The correct answer was: `{correct_ans}`")
                    st.info(f"Explanation: {q['explanation']}")
                    st.divider()
                
                st.metric(label="Your Score", value=f"{score}/{len(quiz_data)}")
        else:
            st.error("No quiz questions available. Please try processing your notes again.")
else:
    if not clicked:
        st.info("Upload your notes in the sidebar and click 'Process Notes' to start.")
