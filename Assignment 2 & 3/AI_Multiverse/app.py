import streamlit as st
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai
from personalities import PERSONALITIES

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def generate_ai_response(personality, message):
    if not api_key:
        return (
            "⚠️ **API Key is missing!**\n\n"
            "Please open the `.env` file in the project folder and paste your Gemini API key: "
            "`GEMINI_API_KEY=your_actual_key_here`\n\n"
            "After saving the file, restart the app or type a new message."
        )

    try:
        p_data = PERSONALITIES.get(personality, {})
        role = p_data.get("role", "AI Assistant")
        
        system_instruction = f"You are a {personality} ({role}). You must respond strictly in character, using appropriate tone, humor, or professional style."

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"❌ **Gemini API Error:** {str(e)}"

st.set_page_config(
    page_title="AI Multiverse Chatbot",
    page_icon="🌍",
    layout="wide"
)

# store the active personality in session state
if "active_personality" not in st.session_state:
    st.session_state.active_personality = "Software Engineer"

# Initialize conversation history for all personalities at start
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        p_name: [{"role": "assistant", "content": p_data["greeting"]}]
        for p_name, p_data in PERSONALITIES.items()
    }

active_p = st.session_state.active_personality
p_info = PERSONALITIES[active_p]


with st.sidebar:
    st.markdown("## 🌍 AI Multiverse")
    st.write("Navigate between different universes and chat with diverse AI personas.")
    
    # Dropdown to select personality
    personality_list = list(PERSONALITIES.keys())
    selected_p = st.selectbox(
        "Choose AI Personality:",
        options=personality_list,
        index=personality_list.index(active_p)
    )
    
    # If the user switches personality, update active selection and rerun
    if selected_p != active_p:
        st.session_state.active_personality = selected_p
        st.rerun()
        
    st.markdown("---")
    # Show active personality card
    st.markdown(f"**Current Role:** {p_info['role']}")
    st.markdown(f"**Avatar Symbol:** {p_info['emoji']}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        # Reset current personality's history to just the initial greeting
        st.session_state.chat_history[active_p] = [
            {"role": "assistant", "content": p_info["greeting"]}
        ]
        st.toast("Chat history cleared!", icon="🧹")
        st.rerun()

# Main Chat Screen Layout
st.title("🌍 AI Multiverse")
st.markdown("### Talk with different AI Personalities.")
st.write(f"Currently connected to the dimension of: **{p_info['emoji']} {active_p}**")
st.markdown("---")

# Display the conversation history
current_history = st.session_state.chat_history[active_p]
for chat in current_history:
    role = chat["role"]
    content = chat["content"]
    
    # Assign custom avatars based on role
    avatar = p_info["emoji"] if role == "assistant" else "👤"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

# Chat Input at the bottom using walrus operator as requested
if prompt := st.chat_input(f"Type a message to {active_p}..."):
    # Immediately save and render the user message
    st.session_state.chat_history[active_p].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # Generate and render the AI response with a spinner
    with st.chat_message("assistant", avatar=p_info["emoji"]):
        response_placeholder = st.empty()
        with st.spinner(f"{active_p} is thinking..."):
            ai_response = generate_ai_response(active_p, prompt)
            response_placeholder.markdown(ai_response)
            
    # Immediately save the assistant response and rerun to update history layout
    st.session_state.chat_history[active_p].append({"role": "assistant", "content": ai_response})
    st.rerun()
