import random
import requests
from io import BytesIO
from PIL import Image
import streamlit as st

# List of surprise prompts
SURPRISE_PROMPTS = [
    "An astronaut riding a horse on Mars",
    "Cyberpunk street food market in Tokyo",
    "A dragon working in an office",
    "A floating castle above the clouds",
    "A futuristic underwater city"
]


def generate_image(prompt, style, width, height, magic_enhance):
    """Sends prompt and parameters to Pollinations AI to fetch the image."""
    final_prompt = prompt

    # Add art style if selected
    if style and style != "None":
        final_prompt = f"{final_prompt}, {style} style"

    # Magic Enhance modifier
    if magic_enhance:
        final_prompt = f"{final_prompt}, masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    # URL encode the prompt text
    encoded_prompt = requests.utils.quote(final_prompt)

    # Attach width and height as query parameters
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"

    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img, response.content
        else:
            st.error("Unable to generate image. Please try again.")
            return None, None
    except Exception:
        st.error("Unable to generate image. Please try again.")
        return None, None


def main():
    st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="centered")

    st.title("🎨 AI Image Studio")
    st.caption("Generate custom artwork with Pollinations AI!")

    # Sidebar options (Magic Enhance)
    st.sidebar.title("Image Settings")
    magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

    # Main user input controls
    user_prompt = st.text_input("Enter your prompt:", "A serene mountain landscape at sunset")

    art_style = st.selectbox(
        "Select Art Style:",
        ["None", "Realistic", "Anime", "Fantasy", "Cyberpunk", "Cinematic", "Digital Art"]
    )

    # Dimension sliders
    col1, col2 = st.columns(2)
    with col1:
        width = st.slider("Width:", min_value=256, max_value=1024, value=512, step=64)
    with col2:
        height = st.slider("Height:", min_value=256, max_value=1024, value=512, step=64)

    # Action buttons
    btn_col1, btn_col2 = st.columns([1, 1])
    generate_clicked = btn_col1.button("🎨 Generate Image", type="primary")
    surprise_clicked = btn_col2.button("🎲 Surprise Me!")

    prompt_to_use = None

    if generate_clicked:
        if not user_prompt.strip():
            st.warning("Please enter a prompt first!")
        else:
            prompt_to_use = user_prompt

    elif surprise_clicked:
        #  Randomly choose a prompt and generate right away
        prompt_to_use = random.choice(SURPRISE_PROMPTS)
        st.info(f"🎲 **Surprise Prompt:** {prompt_to_use}")

    # Generate and display image when a prompt is ready
    if prompt_to_use:
        with st.spinner("Generating your image..."):
            image, image_bytes = generate_image(prompt_to_use, art_style, width, height, magic_enhance)

            if image is not None and image_bytes is not None:
                st.image(image, caption=f"Prompt: {prompt_to_use}", use_column_width=True)

                # Dynamic filename with style and .png extension
                style_prefix = art_style if art_style != "None" else "AI"
                filename = f"{style_prefix}_image.png"

                st.download_button(
                    label="📥 Download Image",
                    data=image_bytes,
                    file_name=filename,
                    mime="image/png"
                )


if __name__ == "__main__":
    main()
