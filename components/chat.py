import streamlit as st
import pathlib
import textwrap
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def render():
    if st.session_state['login']:
        st.title("チャットで相談")
        st.write("AIチャットで相談できます。")
        # ここにチャットインターフェースを実装
        # モデルの初期化
        model = genai.GenerativeModel("gemini-2.5-flash")
        user_input = st.text_input("メッセージを入力してください:")
        if user_input:
            with st.spinner("Geminiが考えています..."):
                try:
                    response = model.generate_content(user_input)
                    st.success("Geminiの返答:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("ログインしてください。")