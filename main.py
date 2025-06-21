import streamlit as st

# グローバルCSSの埋め込み
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Poppins', sans-serif;
        color: #1c1c1c;
        padding: 0 2rem;
    }

    h1, h2, .stMarkdown h1, .stMarkdown h2 {
        color: #003366 !important;
    }

    button[kind="primary"] {
        background-color: #0074D9;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }

    [data-testid="stSidebar"] {
        background-color: #0F172A;
        color: white;
    }

    [data-testid="stSidebar"] .stMarkdown a {
        color: #38BDF8;
    }

    /* ログインページ中央揃え */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
        text-align: center;
    }

    .login-container input, .login-container button {
        margin-top: 1rem;
        width: 300px;
    }

    </style>
""", unsafe_allow_html=True)


# ここから本格的にUIを組み始める
st.title("競プロアプリへようこそ！")

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
