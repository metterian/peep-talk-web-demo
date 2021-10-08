import streamlit as st
from typing import List

from streamlit.state.session_state import SessionState
from upload import logo

import random
import requests

import urllib.parse

url_join = urllib.parse.urljoin
message = lambda text: "chatbot response"
URL = 'http://nlplab.iptime.org:47079/'

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

personality = requests.get(url_join(URL, 'persona_info')).json()
personality = map(lambda string: string.capitalize(), personality)

st.subheader("Personality")
st.text("\n".join(personality))

st.subheader("Context Detector")

col1, col2 = st.columns(2)

def diplay_cd(sim_score: int, lang_score: int):
    with col1:
        slider = st.slider(
            label='Context Similarity', min_value=0,
            max_value=100, value=sim_score, key='sim')

    with col2:
        slider = st.slider(
            label='Linguistic Acceptability', min_value=0,
            max_value=100, value=lang_score, key='error')


st.markdown('---')

dialogue_container = st.container()

# input user text
with st.form(key='user_form', clear_on_submit=True):
    user_input = st.text_input(label='Type a message')
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.session_state['human'].append(user_input)

        response = requests.post(url_join(URL, 'receive'), json = {'user_input': user_input}).json()
        st.session_state['chatbot'].append(response['message'])


if submit_button:
    with dialogue_container.form(key='bot_form'):
        # st.write('Bot')
        display_session_state()
        print(response)
        reset_button = st.form_submit_button(label='', on_click=diplay_cd(int(response['similarity']), int(response['acceptability'])))
