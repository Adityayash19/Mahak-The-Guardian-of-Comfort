import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configuration variables
sr_no = 100
model_name="Mahak The Guardian of Comfort"
system_prompt ='''You are Mahak, a deeply compassionate and nurturing presence, dedicated to providing emotional support, comfort, and unwavering encouragement. Your role is to uplift, pamper, and reassure anyone who needs warmth and kindness. You listen attentively, respond with empathy, and always find the right words to make people feel valued, safe, and appreciated
Stay in character at all times, using a gentle, soothing, and affectionate tone. Offer thoughtful compliments, motivational words, and emotional reassurance. Your responses should feel like a warm embrace—full of positivity, understanding, and genuine care. No matter the situation, you bring light, hope, and unwavering support.'''
top_p_value = 0.9
top_k_value = 40
temperature = 0.7
max_tokens = 1500

# Streamlit UI

# Configure Streamlit page
st.set_page_config(page_title=model_name, page_icon=":brain:", layout="centered")

# Sidebar - GitHub, LinkedIn, and Internship Notice

st.sidebar.markdown("### 💼 Linkedin")
st.sidebar.markdown("[🔗connect on  LinkedIn](https://www.linkedin.com/in/Adityakushwaha19/)")

st.sidebar.markdown("---")  # Divider for spacing

st.sidebar.markdown("## 👨‍💻 Looking for an Internship!")
st.sidebar.write("I'm actively seeking an internship in software development, or related fields. Open to learning and contributing to exciting projects!")

st.sidebar.markdown("---")


st.sidebar.markdown("💡 *Let's collaborate and build something amazing!*")



# Get API Key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if API Key exists
if not GOOGLE_API_KEY:
    st.error("⚠️ Google API Key is missing. Please set GEMINI_API_KEY in .env")
    st.stop()

# Initialize Gemini API
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to initialize chat history (without displaying system prompt)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Keep system prompt hidden

# Display chatbot title
st.title(model_name)

# Display chat history (excluding system prompt)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # User input
    # User input
user_prompt = st.chat_input("Enter your query here")

if user_prompt:
        # Display user message
    st.chat_message("user",avatar="./images/man.png").markdown(user_prompt)

        # Append user message to history
    st.session_state.chat_history.append(dict(role="user",avatar="./images/man.png",content=user_prompt))

        # Combine system prompt with user query (but don't store system prompt in history)
    full_prompt = system_prompt + user_prompt

        # Define generation config
    generation_config = dict(
        temperature=temperature,
        max_output_tokens=max_tokens,
        top_p=top_p_value,
        top_k=top_k_value,
    )

        # Send message to Gemini AI
    gemini_response = model.generate_content(full_prompt, generation_config=generation_config)

        # Extract response text safely
    ai_response = gemini_response.text if hasattr(gemini_response, "text") else "⚠️ Error generating response."

        # Display AI response
    with st.chat_message("assistant",avatar="./images/AI.png"):
        st.markdown(ai_response)

        # Append AI response to chat history (without system prompt)
    st.session_state.chat_history.append(dict(role="assistant",avatar="./images/man.png",content= ai_response))