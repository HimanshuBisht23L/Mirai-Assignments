import os
import json
import tempfile
import requests
from io import BytesIO
from PIL import Image
from gtts import gTTS
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



# Cache Gemini Client Initialization
@st.cache_resource
def get_gemini_model(api_key):
    """Initialize and cache the Gemini model."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


# Session State Initialization
def init_session_state():
    """Set up initial session state variables if not already present."""
    if "chat" not in st.session_state:
        st.session_state.chat = None
    if "story_history" not in st.session_state:
        st.session_state.story_history = []
    if "current_story" not in st.session_state:
        st.session_state.current_story = None
    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None
    if "generated_audio" not in st.session_state:
        st.session_state.generated_audio = None


# JSON Helper & Story Generation    
def parse_json_response(text):
    """Clean markdown code blocks and parse JSON safely."""
    cleaned = text.strip()
    # Remove markdown code formatting if Gemini returns it
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    return json.loads(cleaned)


def generate_story(prompt_text, api_key):
    """Call Gemini API to get the next story node in JSON format."""
    try:
        model = get_gemini_model(api_key)

        # Initialize chat session if needed
        if st.session_state.chat is None:
            st.session_state.chat = model.start_chat(history=[])

        response = st.session_state.chat.send_message(prompt_text)
        story_data = parse_json_response(response.text)
        return story_data
    except Exception as e:
        st.error(f"Failed to generate story scene: {e}")
        return None


# Image Generation via Pollinations API
def generate_image(prompt):
    """Fetch image from Pollinations API based on prompt."""
    try:
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=450&nologo=true"

        response = requests.get(url, timeout=12)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            st.toast("Image server is busy, skipping visual...")
            return None
    except Exception:
        st.toast("Image server is busy, skipping visual...")
        return None


# Audio Generation via gTTS
def generate_audio(text):
    """Convert story text into audio speech file using gTTS."""
    try:
        tts = gTTS(text=text, lang="en")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.warning(f"Audio generation skipped: {e}")
        return None


# UI & Main Layout
def start_new_story(genre, art_style, api_key):
    """Start a fresh story session with initial prompt."""
    # Reset session state for a new story
    st.session_state.chat = None
    st.session_state.story_history = []
    st.session_state.current_story = None
    st.session_state.generated_image = None
    st.session_state.generated_audio = None

    system_prompt = f"""
You are an interactive visual novel narrator.
Genre: {genre}
Art Style: {art_style}

Create the opening scene of a new interactive story in this genre and style.

CRITICAL INSTRUCTION: You MUST return ONLY valid JSON.
Do not wrap in ```json markdown. Do not include any explanations.

JSON schema:
{{
    "story_text": "Opening scene setting up the story (2-4 sentences).",
    "image_prompt": "Visual description of scene for image generation in {art_style} style.",
    "options": [
        "First choice action",
        "Second choice action",
        "Third choice action"
    ]
}}
"""
    story_data = generate_story(system_prompt, api_key)
    if story_data:
        st.session_state.current_story = story_data

        # Generate image and audio for the first scene
        image_prompt = story_data.get("image_prompt", "")
        story_text = story_data.get("story_text", "")

        st.session_state.generated_image = generate_image(image_prompt)
        st.session_state.generated_audio = generate_audio(story_text)


def process_choice(choice, api_key):
    """Handle choice button click and generate next scene."""
    st.session_state.story_history.append(choice)

    prompt = f"""
The player chose: "{choice}".

Continue the story naturally based on this choice.

CRITICAL INSTRUCTION: Return ONLY valid JSON matching this schema exactly without markdown:
{{
    "story_text": "Next scene description (2-4 sentences).",
    "image_prompt": "Detailed description of current scene for image generator.",
    "options": [
        "Choice 1",
        "Choice 2",
        "Choice 3"
    ]
}}
"""
    story_data = generate_story(prompt, api_key)
    if story_data:
        st.session_state.current_story = story_data

        image_prompt = story_data.get("image_prompt", "")
        story_text = story_data.get("story_text", "")

        st.session_state.generated_image = generate_image(image_prompt)
        st.session_state.generated_audio = generate_audio(story_text)
        st.rerun()


def main():
    st.set_page_config(page_title="AI Visual Novel Generator", page_icon="📖", layout="centered")
    init_session_state()

    st.title("📖 AI Interactive Visual Novel")
    st.caption("Step into an interactive AI-generated story with visuals and narration!")

    # Sidebar for Settings
    st.sidebar.title("Story Settings")

    api_key_input = st.sidebar.text_input("Gemini API Key (Optional if in .env)", type="password", help="Enter key or leave blank to use .env file")
    api_key = api_key_input or os.getenv("GEMINI_API_KEY", "")

    genre = st.sidebar.selectbox("Story Genre", ["Fantasy", "Cyberpunk", "Sci-Fi", "Mystery", "Horror", "Adventure"])
    art_style = st.sidebar.selectbox("Art Style", ["Anime", "Pixel Art", "Digital Art", "Cinematic", "Comic Book"])

    if st.sidebar.button("Start New Story", type="primary"):
        if not api_key:
            st.sidebar.error("Please enter your Gemini API Key first!")
        else:
            with st.spinner("Creating your story universe..."):
                start_new_story(genre, art_style, api_key)

    # Main Page Display
    current = st.session_state.current_story
    if current:
        # Display Image if available
        if st.session_state.generated_image is not None:
            st.image(st.session_state.generated_image, caption="Current Scene Visual", use_column_width=True)

        # Display Story Text
        st.subheader("Current Scene")
        st.write(current.get("story_text", ""))

        # Audio Player
        if st.session_state.generated_audio is not None:
            st.audio(st.session_state.generated_audio, format="audio/mp3")

        st.divider()

        # Dynamic Choice Buttons
        st.write("### What will you do next?")
        options = current.get("options", [])
        for idx, option in enumerate(options):
            if st.button(option, key=f"option_btn_{idx}"):
                if not api_key:
                    st.error("Gemini API key is required to continue!")
                else:
                    with st.spinner("Generating next chapter..."):
                        process_choice(option, api_key)
    else:
        st.info("👈 Configure your settings in the sidebar and click **Start New Story** to begin your adventure!")


if __name__ == "__main__":
    main()
