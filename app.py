import streamlit as st
from typing import List

from streamlit.state.session_state import SessionState
from upload import logo

import random


message = lambda text: "chatbot response"

def right_align(text, bold = False):
    return f"<p style='text-align: right;'>{text}</p>"

def bold(text):
    return f"<p style='text-align: right;'><b>{text}</b></p>"


def display_session_state():
    if not st.session_state.chatbot:
        return
    for human, chatbot in zip(st.session_state.human, st.session_state.chatbot):
        st.markdown(right_align(f'You: {human}'), unsafe_allow_html=True)
        st.write(f'Bot: {chatbot}')


personality = [
    "My father was a member of the communist party.",
    "I' ve a career in party planning.",
    "I like to perform stand up comedy.",
    "I enjoy deep sea diving.",
]

# Initialization
if 'chatbot' not in st.session_state:
    st.session_state['human'] = []
    st.session_state['chatbot'] = []



title_container = st.container()
col1, col2 = st.columns([1, 20])
with title_container:
    with col1:
        st.image('/Users/seungjun/PyProject/peep-talk-web-demo/logo.png', width=64)
    with col2:
        st.title('PEEP-Talk')


st.subheader("Personality")
st.text("\n".join(personality))

st.subheader("Context Detector")

col1, col2 = st.columns(2)

def diplay_cd():
    with col1:
        slider = st.slider(
            label='Context Similarity', min_value=0,
            max_value=100, value=random.randint(0,100), key='sim')

    with col2:
        slider = st.slider(
            label='Linguistic Acceptability', min_value=0,
            max_value=100, value=random.randint(0,100), key='error')


st.markdown('---')

dialogue_container = st.container()

# input user text
with st.form(key='user_form', clear_on_submit=True):
    user_input = st.text_input(label='Type a message')

    submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        st.session_state['human'].append(user_input)

        response = message(user_input)
        st.session_state['chatbot'].append(response)


if submit_button:
    with dialogue_container.form(key='bot_form'):
        # st.write('Bot')
        display_session_state()

        reset_button = st.form_submit_button(label='', on_click=diplay_cd())





