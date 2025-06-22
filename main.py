import streamlit as st
from PIL import Image
import pathlib


BASE_DIR = pathlib.Path(__file__).parent
logo_path = BASE_DIR / "logo.png"
logo_img = Image.open(logo_path)

st.set_page_config(
    page_title="競プロアプリ",
    page_icon=logo_img,
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #FFF7F0;
        font-family: 'Poppins', sans-serif;
        color: #2e2e2e;
        padding: 0 2rem;
    }

    h1, h2, .stMarkdown h1, .stMarkdown h2 {
        color: #2e2e2e;
    }

    button[kind="primary"] {
        background-color: #A7C7E7;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }

    [data-testid="stSidebar"] {
        background-color: #F4A7B9;
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

    button[kind="primary"]:hover {
        background-color: #FFD8A9;
        color: #2e2e2e;
    }

    /* サイドバーメニューの色設定（順番に適用） */
    section[data-testid="stSidebar"] label:nth-of-type(1) div span {
        color: #E74C3C !important; /* 赤 */
    }
    section[data-testid="stSidebar"] label:nth-of-type(2) div span {
        color: #2ECC71 !important; /* 緑 */
    }
    section[data-testid="stSidebar"] label:nth-of-type(3) div span {
        color: #F39C12 !important; /* オレンジ */
    }
    section[data-testid="stSidebar"] label:nth-of-type(4) div span {
        color: #2ECC71 !important; /* 緑 */
    }
    section[data-testid="stSidebar"] label:nth-of-type(5) div span {
        color: #E74C3C !important; /* 赤 */
    }
    </style>
""", unsafe_allow_html=True)


if 'login' not in st.session_state:
    st.session_state['login'] = False


st.markdown('<h1 style="color:#2ECC71;">競プロアプリへようこそ！</h1>', unsafe_allow_html=True)


st.sidebar.title("競プロアプリ")
selected = st.sidebar.radio("ページを選んでください", [
    "アカウント登録",
    "ログイン",
    "やることリスト",
    "チャットで相談",
    "実施した問題の記録"
])


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
