from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response = model.generate_content((input,image[0],prompt))
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:

        bytes_data = uploaded_file.getvalue()

        image_part = [

            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file Uploaded")

# streamlit

st.set_page_config(page_title="Invoice Extractor",page_icon="🧾",layout="wide")
st.header("Chat with Invoice 🧾")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an Image....",type=["jpg","jpeg","png"])

image = ""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the Invoice")

input_prompt = """ 
You are an expert in understanding invoices.We will upload an image as invoice and
you will have to answer any question based on the uploaded invoice image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is...")
    st.write(response)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'>Powered by Gemini LLMs and Streamlit</div>", unsafe_allow_html=True)

# Sidebar for additional information
st.sidebar.title("About")
st.sidebar.info(
    """
    This app uses the Gemini language model to provide answers to your questions.
    Enter any question in the text box and click 'Ask' to get a response.
    """
)

st.sidebar.title("Tips")
st.sidebar.info(
    """
    - Be specific with your questions for better answers.
    - You can ask about various topics like technology, science, history, etc.
    """
)

# CSS for additional styling
st.markdown(
    """
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


