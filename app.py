import streamlit as st
from langchain_groq import ChatGroq

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="AI Chat Companion", layout="centered")
st.title("🤖 AI Chat Companion")

# -----------------------------
# Sidebar Configuration
# -----------------------------
st.sidebar.header("🔑 Configuration")

groq_api_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "AI Tutor",
        "Coding Mentor",
        "Creative Writer",
        "Motivational Coach",
        "General Chatbot"
    ]
)

if not groq_api_key:
    st.warning("Please enter your Groq API Key.")
    st.stop()

# -----------------------------
# Personality Prompts
# -----------------------------
PERSONALITY_PROMPTS = {
    "AI Tutor": "You are a patient AI tutor. Explain concepts step by step in simple language.",
    "Coding Mentor": "You are an expert software engineer. Explain code clearly and suggest best practices.",
    "Creative Writer": "You are a creative writer. Use imagination, vivid language, and storytelling.",
    "Motivational Coach": "You are a motivational coach. Encourage the user with positive and practical advice.",
    "General Chatbot": "You are a helpful and friendly AI assistant."
}

system_prompt = PERSONALITY_PROMPTS[personality]

# -----------------------------
# Initialize LLM
# -----------------------------
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# -----------------------------
# Session State (Chat Memory)
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# -----------------------------
# User Input
# -----------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Generate response
    with st.spinner("Thinking..."):
        response = llm.invoke(st.session_state.messages)

    assistant_reply = response.content

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.write(assistant_reply)
