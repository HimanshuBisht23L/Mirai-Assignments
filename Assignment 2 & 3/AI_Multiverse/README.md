# AI Multiverse Chatbot

A beginner-friendly, clean, and modern AI Multiverse Chatbot built with Python and Streamlit for Assignment 2.

## File Structure
- `app.py`: Main Streamlit app containing the UI, layout, state management, and custom styles.
- `personalities.py`: Contains the metadata and dummy responses for each AI character.
- `requirements.txt`: Streamlit packages.

## Running the Application
To run the app locally:
```bash
# Create .env file
GEMINI_API_KEY=YOUR_API_KEY

# Install dependencies
pip install -r ./requirements.txt

OR

# Using Virtual Environment
python -m venv venv
venv/Scripts/activate
pip install -r ./requirements.txt


# To Run App
streamlit run app.py
```
