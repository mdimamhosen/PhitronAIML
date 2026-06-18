import streamlit as st

st.title("My First Streamlit App!", anchor=None)
st.write("Hello, world! This is a web app built entirely in Python.")



st.divider()


name = st.text_input("Enter you name")
password = st.text_input("Enter your password", type="password")

if st.button("Login"):
    if name == "admin" and password == "admin":
        st.success("Login successful")
    else:
        st.error("Invalid credentials")

else:
    st.write("Please enter your credentials")



choice = st.selectbox("Choose your favorite fruit", ["Apple", "Banana", "Orange"], index=None, placeholder="Choose your favorite fruit", accept_new_options=True)
st.write("You selected:", choice)

choices = st.multiselect("Choose your favorite fruits", ["Apple", "Banana", "Orange", "Mango"], placeholder="Choose your favorite fruits", accept_new_options=True)
st.write("You selected:", choices)

fileInput = st.file_uploader("Upload a file", accept_multiple_files=True)
if fileInput:  # True if the list is not empty
    st.write(f"Successfully uploaded {len(fileInput)} file(s)")
    for uploaded_file in fileInput:
        with st.expander(f"Details of {uploaded_file.name}"):
            st.write("File name:", uploaded_file.name)
            st.write("File type:", uploaded_file.type)
            st.write("File size:", uploaded_file.size, "bytes")
            st.write("File content (first 100 bytes):", uploaded_file.read(100))
else:
    st.write("Please upload one or more files")



imageInput = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if imageInput:  # True if the list is not empty
    st.write(f"Successfully uploaded {len(imageInput)} image(s)")
    for uploaded_image in imageInput:
        with st.expander(f"Details of {uploaded_image.name}"):
            st.write("Image name:", uploaded_image.name)
            st.write("Image type:", uploaded_image.type)
            st.write("Image size:", uploaded_image.size, "bytes")
else:
    st.write("Please upload one or more images")


if imageInput:
    col = st.columns(len(imageInput))
    for i, per_img in enumerate(imageInput):
        col[i].image(per_img)


