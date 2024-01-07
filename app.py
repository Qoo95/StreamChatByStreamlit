import streamlit as st
import openai
import os

openai_api_key = ''
os.environ["OPENAI_API_KEY"] = openai_api_key


class StreamHandler:
    def __init__(self, container, history):
        self.container = container
        self.text = ""
        self._box = st.chat_message
        self.qa_history = history

    def log_QA_history(self, role, content):
        self.qa_history.append({"role": role, "content": content}) 
    
    def add_to_stream(self, token):
        if token:
            self.text += token
        with self.container.container():
            for dict_conv in self.qa_history:
                self._box(dict_conv['role']).write(dict_conv['content'])
            self._box("assistant").write(self.text)
    
    def get_content(self):
        last_conv = self.text
        self.text = ""
        return last_conv


clear_button = st.button("clear")
st.markdown("### streaming box")
chat_box = st.empty()
with chat_box.container():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
stream_handler = StreamHandler(chat_box, st.session_state.chat_history)

if clear_button:
    st.session_state.chat_history = []
    
if query := st.chat_input("input your query"):
    stream_handler.log_QA_history(role="user", content=query)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # or another model you prefer
        messages=stream_handler.qa_history,
        stream=True
    )
    
    for token in response:
        stream_handler.add_to_stream(token.choices[0].delta.content)

    stream_handler.log_QA_history(role="assistant", content=stream_handler.get_content())
