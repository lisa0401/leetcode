import streamlit as st

# def show():
#     st.title("Welcome to the Home Page!")

def render():
    if st.session_state['login']:
        st.title("チャットで相談")
        st.write("AIチャットで相談できます。")
        # ここにチャットインターフェースを実装
    else:
        st.warning("ログインしてください。")