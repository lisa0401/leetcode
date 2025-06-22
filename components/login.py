# components/login.py の内容

import streamlit as st
from utils import auth

def render():

    st.markdown('<h1 style="color:#E74C3C;">ログインページ</h1>', unsafe_allow_html=True) # メインタイトル

    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")

    if st.button("ログイン"):
        if auth.verify_user(username, password):
            st.success("ログイン成功！")
            st.session_state['login'] = True
            st.session_state['username'] = username
            
            # ★ログイン成功後、セッションステートのページ名を更新★
            # main.py で定義したページ名と一致させる
            if 'current_page_name' in st.session_state: # current_page_name が存在するかのチェック
                st.session_state['current_page_name'] = "やることリスト"
            else:
                # 非常に稀なケースだが、念のためデフォルトを設定
                st.session_state['current_page_name'] = "やることリスト" 

            st.rerun() # ページの再実行をトリガーし、main.pyが新しいページをレンダリング

        else:
            st.error("ユーザー名またはパスワードが正しくありません")
