import streamlit as st
from streamlit.state.session_state import SessionState
from typing import List
from truecase import get_true_case
import random
import requests
import numpy
from models import grammar

from urllib.parse import urljoin

URL = "http://nlplab.iptime.org:9060/"


def right_align(text, bold=False):
    return f"<p style='text-align: right;'>{text}</p>"


def bold(text):
    return f"<p style='text-align: right;'><b>{text}</b></p>"


def display_dialogue():
    """display between Human and Chatbot conversation"""
    # if not st.session_state.chatbot:
    #     return
    for human, chatbot, gec in zip(st.session_state.human, st.session_state.chatbot, st.session_state.gec):
        st.markdown(right_align(f"You: {human}"), unsafe_allow_html=True)
        st.write(f"Bot: {get_true_case(chatbot)}\n\nGEC: {gec}")

def get_personality():
    personality = requests.get(urljoin(URL, "personality")).json()
    personality = map(lambda string: string.capitalize(), personality)
    return personality

# Initialization
# if 'personality' not in st.session_state:


if "chatbot" not in st.session_state:
    st.session_state["personality"] = []
    st.session_state["human"] = []
    st.session_state["chatbot"] = []
    st.session_state["gec"] = []

    requests.get(urljoin("history/clear", URL))


st.image("./statics/logo.png", width=100)
st.title("PEEP-Talk")


# sub title - Personality
# personality = requests.get(urljoin(URL, "personality")).json()
# personality = map(lambda string: string.capitalize(), personality)
st.subheader("Situation")


switch = st.button(label = 'Switch!')


if switch:
    response = requests.get(urljoin(URL, "personality/swtich")).json()
    st.session_state.human = []
    st.session_state.chatbot = []
    st.session_state.personality = get_personality()
    st.text("\n".join(st.session_state.personality))

else:
    st.session_state.personality = get_personality()
    st.text("\n".join(st.session_state.personality))

    # st.write(response)


# sub title - Context Detector
st.subheader("Context Detector")
col1, col2 = st.columns(2)


def diplay_cd(sim_score: int, accept_score: int):
    with col1:
        slider = st.slider(
            label="Situation Similarity",
            min_value=0,
            max_value=100,
            value=sim_score,
            key="sim",
        )

    with col2:
        slider = st.slider(
            label="Linguistic Acceptability",
            min_value=0,
            max_value=100,
            value=accept_score,
            key="error",
        )


# divide section
# st.markdown("---")

dialogue_container = st.container()

# input user text
with st.form(key="user_form", clear_on_submit=True):
    user_input = st.text_input(label="Type a message")
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        st.session_state["human"].append(user_input)
        response = requests.post(
            urljoin(URL, "message"), json={"user_input":user_input}
        ).json()
        st.session_state["chatbot"].append(response["message"])
        st.session_state["gec"].append(response['correction'])


# messsage box
if submit_button:
    with dialogue_container.form(key="bot_form"):
        # st.write('Bot')
        display_dialogue()
        sim_score = int(response["similarity"])
        # sim_score = random.randint(50,70)
        accept_score = int(response["acceptability"])
        reset_button = st.form_submit_button(
            label="", on_click=diplay_cd(sim_score, accept_score)
        )
