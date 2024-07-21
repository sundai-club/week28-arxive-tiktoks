import streamlit as st
import requests
import os

file_path = st.text_input("Enter pdf file path")

button = st.button("Generate Content")

if button:
    if file_path:
        if not os.path.exists(file_path):
            st.write("File not found")
            st.stop()
        else:
            generated_content = requests.post('http://localhost:8000/generate_content', json={'paper_path': file_path}).json()['generated_content']

            st.write(generated_content)
    else:
        st.write("Please enter a valid file path")
        st.stop()
