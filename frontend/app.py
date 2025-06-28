import streamlit as st
import openai
import os
from dotenv import load_dotenv
from prompts import get_intro_prompt, get_feedback_prompt, get_next_task_prompt
from utils import calculate_xp, get_task_intro

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="PersonaForge", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Courier New', monospace;
    }
    .stButton button {
        background-color: #00adb5;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    .stTextArea textarea {
        background-color: #2d2d2d;
        color: white;
        font-family: 'Courier New', monospace;
    }
    .stTextInput input {
        background-color: #2d2d2d;
        color: white;
    }
    pre, code {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("PersonaForge")
st.markdown("####  Simulate a Workday ·  Build Skills ·  Earn XP")

if "name" not in st.session_state:
    st.session_state.name = None
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "task_num" not in st.session_state:
    st.session_state.task_num = 1
if "task_response" not in st.session_state:
    st.session_state.task_response = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "role" not in st.session_state:
    st.session_state.role = None
if "prev_answer" not in st.session_state:
    st.session_state.prev_answer = ""
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

if not st.session_state.name:
    name = st.text_input("Enter your name to begin:")
    if st.button("Start Simulation") and name:
        st.session_state.name = name
        st.rerun()

if st.session_state.name:
    st.markdown(f"### Welcome, {st.session_state.name}")

    if not st.session_state.role:
        role = st.selectbox("Choose your career simulation:", [
            "Social Media Manager",
            "Office Admin",
            "Customer Support Agent",
        ])
        if st.button(" Begin Workday"):
            st.session_state.role = role
            intro_prompt = get_intro_prompt(role, st.session_state.task_num)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": intro_prompt}]
            )
            st.session_state.task_response = response.choices[0].message.content
            st.session_state.feedback = None

    st.markdown(
        f"<div style='position:sticky;top:0;background:#222;padding:10px;border-radius:10px;margin-bottom:20px;'>"
        f"<b>XP:</b> {st.session_state.xp} | <b>Task:</b> {st.session_state.task_num}/3 | <b>Role:</b> {st.session_state.role}"
        f"</div>", unsafe_allow_html=True
    )

    st.progress((st.session_state.task_num - 1) / 3)

    col1, col2 = st.columns([2, 3])

    with col1:
        if st.session_state.task_response:
            st.markdown("###  Task")
            st.code(st.session_state.task_response, language="markdown")

    with col2:
        if st.session_state.task_response:
            st.markdown("###  Your Response")
            user_answer = st.text_area("", height=250)
            file_upload = st.file_uploader(" Upload a file (optional)")
            if st.button(" Submit Task"):
                feedback_prompt = get_feedback_prompt(user_answer, st.session_state.role, file_upload)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": feedback_prompt}]
                )
                feedback = response.choices[0].message.content
                xp_earned = calculate_xp(feedback)
                st.session_state.feedback = feedback
                st.session_state.xp += xp_earned
                st.session_state.prev_answer = user_answer
                st.session_state.leaderboard[st.session_state.name] = st.session_state.xp

    if st.session_state.feedback:
        st.markdown("###  Feedback")
        st.code(st.session_state.feedback, language="markdown")
        st.markdown(f" XP Earned: **{calculate_xp(st.session_state.feedback)}**")

        if st.session_state.task_num < 3:
            if st.button(" Next Task"):
                st.session_state.task_num += 1
                task_prompt = get_next_task_prompt(
                    st.session_state.role,
                    st.session_state.task_num,
                    st.session_state.prev_answer
                )
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": task_prompt}]
                )
                st.session_state.task_response = response.choices[0].message.content
                st.session_state.feedback = None
        else:
            st.balloons()
            st.success(" Workday complete!")
            if st.button(" Start Over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]

    st.markdown("---")
    st.markdown("###  Leaderboard (This Session)")
    leaderboard = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)
    for i, (user, score) in enumerate(leaderboard):
        st.markdown(f"**{i+1}. {user}** — {score} XP")
