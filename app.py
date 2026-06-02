import streamlit as st
import requests
import os

st.header("Exam helper")
st.write("It helps in exam times")

uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["jpg", "pdf", "png"])

if st.button("Submit"):
    if uploaded_files is not None:
        save_dir = "saved_files"
        os.makedirs(save_dir, exist_ok=True)
        
        # Save the file to the local directory
        for uploaded_file in uploaded_files:
            file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"File saved successfully at {file_path}")