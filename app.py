import streamlit as st

import google.generativeai as genai

f = open('key_file.txt')
key = f.read()

genai.configure(api_key=key)

system_prompt ="""you are a code review user will submit 
                their code to you, you have to analyse it and create a code review containing the errors 
                in the code and tell the user about the mistakes pointwise as bug report and also you should
                also generate corrected code as fixed code. Incase if the code contains no error tell
                user its perfect"""

model = genai.GenerativeModel(model_name='models/gemini-1.5-flash',system_instruction=system_prompt)

st.title("AN AI Code Reviewer💬")

user_prompt=st.text_area("Enter your python code here ...",placeholder="Type your code here",height=150)

button_click = st.button("Generate")

if button_click ==True:

    response=model.generate_content(user_prompt)
    
    st.write(response.text)