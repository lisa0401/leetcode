import streamlit as st

# セッション状態の初期化
if 'login' not in st.session_state:
    st.session_state['login'] = False

# アプリ設定（重要：デフォルトナビゲーションUIは無効）
st.set_page_config(
    page_title="競プロアプリ",
    layout="wide"
)

# サイドバーでページ選択
st.sidebar.title("競プロアプリ")
selected = st.sidebar.radio("ページを選んでください", [
    "アカウント登録",
    "ログイン",
    "やることリスト",
    "チャットで相談",
    "実施した問題の記録",
])

# ページの表示ロジック（components フォルダにまとめる）
if selected == "アカウント登録":
    from components import register
    register.render()
elif selected == "ログイン":
    from components import login
    login.render()
elif selected == "やることリスト":
    from components import reservation
    reservation.render()
elif selected == "チャットで相談":
    from components import chat
    chat.render()
elif selected == "実施した問題の記録":
    from components import training_log
    training_log.render()
