import streamlit as st
from utils import auth

def render():
    st.title("ログインページ")
    if st.session_state.get('login'):
        st.success("すでにログインしています！")
        st.stop()
    auth.create_user_table()  # DBテーブル作成（初回のみ）

    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    
    if st.button("ログイン"):
        if auth.verify_user(username, password):
            st.session_state['login'] = True
            st.success("ログインしました！")
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
