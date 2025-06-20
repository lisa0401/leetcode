import streamlit as st

def render():
    st.title("ログインページ")
    st.write("ここにログインフォームを実装します。")
    # 例: ログインボタン
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if username == "test" and password == "password": # 仮の認証
            st.session_state['login'] = True
            st.success("ログインしました！")
            st.rerun() # ログイン後、ページを再読み込みしてナビゲーションを更新
        else:
            st.error("ユーザー名またはパスワードが間違っています。")