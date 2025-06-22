import streamlit as st
import pathlib
import textwrap
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

def to_markdown(text):
  text = text.replace('•', '  *')
  return st.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def render():
    if st.session_state['login']:
        if "chat" not in st.session_state:
            st.session_state.chat = model.start_chat(history=[])
        st.markdown('<h1 style="color:#E74C3C;">チャットで相談</h1>', unsafe_allow_html=True)
        st.write("AIチャットで相談できます。")
        # ここにチャットインターフェースを実装
        user_input = st.chat_input("メッセージを入力してください")
        if user_input:
            # ユーザーの入力を表示
            with st.chat_message("user"):
                st.markdown(user_input)

            # Gemini APIで返答を生成
            response = st.session_state.chat.send_message(user_input)

            # Geminiの返答を表示
            with st.chat_message("assistant"):
                st.markdown(response.text)
    else:
        st.warning("ログインしてください。")