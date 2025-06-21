import streamlit as st

st.set_page_config(
    page_title="競プロアプリ",
    page_icon="favicon-new.png",  # Make sure this file exists in the same folder
    layout="wide"
)

# グローバルCSSの埋め込み
st.markdown("""
    <style>
    .stApp {
        background-color: #FFF7F0;  /* Soft cream */
        font-family: 'Poppins', sans-serif;
        color: #2e2e2e;
        padding: 0 2rem;
    }

    h1, h2, .stMarkdown h1, .stMarkdown h2 {
        color: #2e2e2e;  /* Dark pastel-compatible gray */
    }

    button[kind="primary"] {
        background-color: #A7C7E7;  /* Soft blue */
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }

    [data-testid="stSidebar"] {
        background-color: #F4A7B9;  /* Soft red-pink */
        color: #2e2e2e;
    }

    [data-testid="stSidebar"] .stMarkdown a {
        color: #2e2e2e;
    }

    .login-container input, .login-container button {
        margin-top: 1rem;
        width: 300px;
        border-radius: 6px;
        border: 1px solid #DDD;
        background-color: white;
    }

    /* Optional: hover effects */
    button[kind="primary"]:hover {
        background-color: #FFD8A9;  /* Soft orange on hover */
        color: #2e2e2e;
    }

    </style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'login' not in st.session_state:
    st.session_state['login'] = False

# UI
st.title("競プロアプリへようこそ！")

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
