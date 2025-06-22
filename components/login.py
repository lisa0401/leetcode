import streamlit as st
from utils import auth

def render():
    auth.create_user_table()

    st.title("ログインページ")

    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if auth.verify_user(username, password):
            st.success("ログイン成功！")
            st.session_state['login'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが正しくありません")