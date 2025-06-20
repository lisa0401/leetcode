import streamlit as st

def render():
    if st.session_state['login']:
        st.title("やることリスト")
        st.write("やることリストをまとめることができます。")
        # ここに予約フォームなどを実装
    else:
        st.warning("ログインしてください。")