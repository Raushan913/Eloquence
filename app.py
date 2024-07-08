import os
import streamlit as st
import google.generativeai as genai

def main():
    st.set_page_config(page_title="GenAI Streamlit App")
    st.title("GenAI Streamlit App")

    # Set the API key
    os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    # Create the GenAI model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # User input
    prompt = st.text_area("Enter your prompt:", height=200)

    if st.button("Generate Content"):
        response = model.generate_content(prompt)
        st.write(response.text)

if __name__ == "__main__":
    main()
