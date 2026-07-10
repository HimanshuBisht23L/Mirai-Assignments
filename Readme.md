# Mirai Assignments

This repository contains my project and homework submissions for the Mirai program. 

---

## 📂 Repository Structure

The assignments are organized in folders:

*   **[Assignment 1](./Assignment%201)**: **Echo Chamber 9000**
    *   *Description*: A Streamlit-based UI shell designed for input collection, conditional routing/validation, and formatted output generation. It simulates message transmission and includes an advanced token estimation challenge based on character length.
    *   *Core Stack*: Python, Streamlit
*   **[Assignment 2](./Assignment%202/AI_Multiverse)**: **AI Multiverse Chatbot**
    *   *Description*: A responsive Streamlit chatbot application featuring different AI personalities, conversation history tracking via session state, custom CSS aesthetics, and extensibility for AI APIs.
    *   *Core Stack*: Python, Streamlit, dotenv

---

## 🚀 How to Run the Assignments Locally

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Set Up a Virtual Environment (Recommended)
Navigate to the assignment folder of your choice and set up a virtual environment:

```bash
# Navigate to the assignment folder (e.g., Assignment 1)
cd "Assignment 1"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install the required packages using the `requirements.txt` file located in the assignment folder:
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
Launch the app with Streamlit:
```bash
streamlit run app.py
```

---

## 🛠️ Assignment Profiles

### Assignment 1: Echo Chamber 9000
- **Features**: User name and message input validation, success/error alert handling, token usage approximation.
- **Tech Highlights**: Streamlit state and UI components (`st.text_input`, `st.button`, `st.success`, `st.info`).

### Assignment 2: AI Multiverse Chatbot
- **Features**: Sidebar for selecting different AI personas, persistent chat history in the session state, custom styling, mock/generative responses.
- **Tech Highlights**: Custom CSS injects, `st.chat_message`, `st.chat_input`, and environment variable configuration via `dotenv`.
