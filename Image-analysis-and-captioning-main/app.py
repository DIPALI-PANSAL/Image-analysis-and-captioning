import streamlit as st
import subprocess
import requests
from PIL import Image
import io

st.title("Image Captioning Application")

# Function to start the FastAPI server
def start_api():
    process = subprocess.Popen(["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000"])
    return process

# Function to stop the FastAPI server
def stop_api(process):
    process.terminate()

# Start the FastAPI server
api_process = start_api()

# Function to get the caption from the FastAPI backend
def get_caption(image):
    # Convert the PIL image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Send the image to the FastAPI backend
    files = {'file': img_byte_arr}
    response = requests.post("http://127.0.0.1:8000/predict/", files=files)
    
    if response.status_code == 200:
        return response.json().get('caption', 'No caption found')
    else:
        return "Error in generating caption"

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="unique_uploader")

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Get the caption
    caption = get_caption(image)
    
    # Display the caption
    st.write(f"Caption: {caption}")

# Stop the API when the Streamlit app is closed
st.write("Stopping API...")
stop_api(api_process)


