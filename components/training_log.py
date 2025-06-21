import streamlit as st

def render():
    if st.session_state['login']:
        st.title("実施した問題の記録")
        st.write("問題の記録を閲覧・追加できます。")
        # ここに表示・追加機能を実装
    else:
        st.warning("ログインしてください。")