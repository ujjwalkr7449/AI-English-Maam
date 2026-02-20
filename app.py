import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

from memory import save_memory, get_memories
from prompts import SYSTEM_PROMPT

# ---------------- LOAD ENV ----------------
load_dotenv()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
# ---------------- CACHE GROQ CLIENT ----------------
@st.cache_resource
def get_client():
    return Groq(api_key=GROQ_API_KEY)

client = get_client()

st.title("AI English Ma'am 🤖")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("👤 User Info")

if st.session_state.user_name:
    st.sidebar.success(f"Name: {st.session_state.user_name}")
else:
    st.sidebar.warning("No name yet")

# ---------------- FIRST TIME NAME ASK ----------------
if st.session_state.user_name is None:

    name_input = st.text_input("Hi 🙂 What is your name?")

    if name_input:
        st.session_state.user_name = name_input

        # Save name to memory
        save_memory(f"User name is {name_input}")

        # Add first AI message
        welcome_msg = f"Hello {name_input}! 😊 How is your day going?"
        st.session_state.messages.append(
            {"role": "assistant", "content": welcome_msg}
        )

        st.rerun()

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- CHAT INPUT ----------------
if st.session_state.user_name:

    user_input = st.chat_input("Say something in English...")

    if user_input:

        # Show user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.write(user_input)

        save_memory(user_input)

        # Build messages
        memory_context = get_memories()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
                + f"\nUser name: {st.session_state.user_name}\nMemory:{memory_context}",
            }
        ] + st.session_state.messages

        # -------- CALL GROQ --------
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant" ,
            messages=messages,
            temperature=0.5,
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

        with st.chat_message("assistant"):
            st.write(ai_reply)