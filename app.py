import os
import streamlit as st
import google.generativeai as genai

# Initialize a list to store the history of generated texts
if 'generated_history' not in st.session_state:
    st.session_state.generated_history = []

def main():
    st.set_page_config(page_title="GenAI Streamlit App")
    st.title("GenAI Streamlit App")

    # Sidebar menu to show previous queries
    st.sidebar.title("Previous Queries")
    for idx, text in enumerate(st.session_state.generated_history[::-1], start=1):
        # Display the first few words of each query as menu items
        first_few_words = " ".join(text.split()[:5]) + "..." if len(text.split()) > 5 else text
        if st.sidebar.button(f"Query {idx}: {first_few_words}", key=f"query_{idx}"):
            st.text_area("Previous Query:", value=text, height=200)

    # Set the API key
    os.environ['GOOGLE_API_KEY'] = "YOUR_GOOGLE_API"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    # Create the GenAI model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # User input for prompt
    prompt = st.text_area("Enter your prompt:", height=200)

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

    if st.button("Generate Content"):
        try:
            if uploaded_file is not None:
                image_data = uploaded_file.read()  # Read the uploaded image file

                # Construct image_input with mime_type and data
                image_input = {
                    'mime_type': uploaded_file.type,
                    'data': image_data
                }
            else:
                image_input = None

            # Combine the history of generated texts with the new prompt
            combined_prompt = "\n".join(st.session_state.generated_history + [prompt])

            # Generate content using the combined prompt and the uploaded image or text
            if image_input:
                response = model.generate_content([combined_prompt, image_input])
            else:
                response = model.generate_content(combined_prompt)

            # Store the generated text in history
            st.session_state.generated_history.append(response.text)

            # Display the generated text
            st.write(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.error("Please retry or report this issue.")

if __name__ == "__main__":
    main()
