import streamlit as st
from PIL import Image
import base64
import io
import google.generativeai as genai
from gtts import gTTS

with open('key_file.txt') as f:
    api_key = f.read()

genai.configure(api_key=api_key)

sys_prompt = """
You are a visual assistant. Your role is to identify objects in an image and provide a detailed description of the content of the image.
"""


model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=sys_prompt
)

# converting image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def text_to_audio(text):
    tts = gTTS(text, lang='en')  
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer) 
    audio_buffer.seek(0)  
    return audio_buffer

# Streamlit
st.title("🤖 AI Powered Solution for Assisting Visually Impaired Individuals")
uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
text_input = st.selectbox("Choose a functionality",("Describe Image🖼️","Detect objects🔍","Guidance for visually impaired🧑‍🦯‍➡️"))

if uploaded_image is not None:
    # Load the image
    img = Image.open(uploaded_image)

    # Display the uploaded image
    st.image(img, caption="Uploaded Image", use_container_width=True)
    button_click = st.button("Analyse🔍")
    if button_click== True:
    # Convert the image to base64 
        image_base64 = image_to_base64(img)

    # input 
        contents = [
            {"text": text_input},
            {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
    ]

        response = model.generate_content(contents)

    # Display responses
        st.write("**Analysis:**")
        st.write(response.text)
        audio_file = text_to_audio(response.text)
        st.audio(audio_file, format="audio/mp3", start_time=0)

else:
    st.write("Please upload an image.")
