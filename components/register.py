import streamlit as st
from utils import auth

def render():
    st.title("ユーザー登録")

    auth.create_user_table()  # テーブルがなければ作成

    with st.form("register_form"):
        st.subheader("アカウント情報を入力してください")
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        password_confirm = st.text_input("パスワード（確認）", type="password")
        submitted = st.form_submit_button("登録")

    if submitted:
        if not username or not password or not password_confirm:
            st.warning("すべての項目を入力してください。")
        elif password != password_confirm:
            st.error("パスワードが一致しません。")
        elif auth.add_user(username, password):
            st.success("アカウント登録が完了しました。ログインページへ進んでください。")
        else:
            st.error("このユーザー名は既に使用されています。")
