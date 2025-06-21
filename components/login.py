import streamlit as st
from utils import auth  # auth.py を utils フォルダに置いている場合

def render():
    auth.create_user_table()  # 初期化（初回のみ）

    st.title("ログインページ")

    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if auth.verify_user(username, password):
            st.success("ログイン成功！")
            # ✅ ここでセッションにユーザー名を保存
            st.session_state['login'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが正しくありません")

    st.write("---")
    st.subheader("新規ユーザー登録")

    new_user = st.text_input("新しいユーザー名", key="new_user")
    new_pass = st.text_input("新しいパスワード", type="password", key="new_pass")

    if st.button("登録"):
        if auth.add_user(new_user, new_pass):
            st.success("ユーザー登録に成功しました。上のフォームからログインしてください。")
        else:
            st.error("そのユーザー名はすでに使われています。")
