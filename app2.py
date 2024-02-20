import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], input_prompt])
    return response.text

# Function to prepare image data for Gemini Pro Vision API
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Image Processing Techniques with AI")
st.header("Image Processing Techniques with AI")

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Default prompt
default_prompt = """
You are an Expert in Image Processing and you have to detect the Fly in the uploaded image by the User.

Display the Final Answer as Detected in Green Color otherwise Not Detected in Red Color in Bold

Note : Only the Answer should be Detected or Not Detected (Other than that Nothing to be Given)
"""

# Submit button
submit = st.button("Submit")

# If submit button is clicked
if submit:
    # Check if image is uploaded
    if uploaded_file is None:
        st.error("Please upload an image.")
    else:
        custom_prompt = default_prompt
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(custom_prompt, image_data)
        st.subheader("Response:")
        st.write(response)
