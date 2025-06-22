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
            # ★ここを修正★ ログイン成功後、セッションステートのページ名を更新
            # main.py で定義したページ名と一致させる
            st.session_state['current_page_name'] = "やることリスト" 

            st.rerun() # ページの再実行をトリガーし、新しいページへ遷移
        else:
            st.error("ユーザー名またはパスワードが正しくありません")