import streamlit as st
from PIL import Image
from api import analyze_code_error

# Page title and description
st.set_page_config(page_title="AI Code Error Debugger", page_icon="🐞", layout="centered")

st.title("🐞 AI Code Error Debugger")
st.write("Upload a screenshot of your code error or terminal log, select the type of response, and get instant debugging help powered by Gemini.")

# 1. File uploader for images (png, jpg, jpeg)
uploaded_file = st.file_uploader(
    "Upload Error Screenshot", 
    type=["png", "jpg", "jpeg"],
    help="Upload an image (PNG, JPG, or JPEG) containing your code or error logs."
)

# Show image preview if uploaded
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Error Screenshot", use_container_width=True)

# 2. Option bar with “Hints” and “Solution with code” (initially unselected)
option = st.radio(
    "Select Output Format:",
    options=["Hints", "Solution with code"],
    index=None,
    help="Select 'Hints' for conceptual clues to solve the bug, or 'Solution with code' for the complete fix."
)

# 3. "Debug Code" button
debug_button = st.button("Debug Code", type="primary")

# 4. Input validation and trigger action on button click
if debug_button:
    # If file is not uploaded or option is not selected, show an error warning
    if uploaded_file is None or option is None:
        st.error("⚠️ Please upload an image AND select a response type (Hints or Solution with code) before clicking Debug Code.")
    else:
        # 5. Show st.spinner during the API call
        with st.spinner("Analyzing the screenshot and generating response..."):
            try:
                # Open image using PIL
                image = Image.open(uploaded_file)
                # Call the Gemini API
                result = analyze_code_error(image, option)
                
                st.success("✅ Analysis Complete!")
                st.subheader(f"🔍 Debug Output ({option})")
                # 6. Render the response beautifully using st.markdown()
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ An error occurred during analysis: {e}")
