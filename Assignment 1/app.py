import streamlit as st

# Task 1: UI Shell
st.title("Echo Chamber 9000")

st.write(
    "Welcome! Enter your name and a message below, then click the **Transmit** button."
)

# Task 2: Multi-Data Collection
user_name = st.text_input("Enter your Name")

user_message = st.text_input("Enter your Message")


# Task 3: Action Gate
if st.button("Transmit"):

    # Task 4: Conditional Routing
    if user_name.strip() == "":
        st.error("Please provide your name.")

    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")


    # Task 5: Formatted Output
    else:
        st.html(f"<h3 style='color: green;'>Transmission successful!</h3>")

        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )

        # Advanced Challenge
        character_count = len(user_message)
        token_count = character_count / 4

        st.info(
            f"System Check: Your message will consume approximately "
            f"{token_count:.2f} tokens from our context window."
        )