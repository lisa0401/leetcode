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


# アプリの基本設定
st.set_page_config(page_title="競プロアプリ", layout="wide")

# ここから本格的にUIを組み始める
st.title("競プロアプリへようこそ！")

# ページの選択メニュー
pages = {
    "ログイン": "pages.login",
    "ホーム": "pages.home",
    "やることリスト": "pages.reservation",
    "チャットで相談": "pages.chat",
    "実施した問題の記録": "pages.training_log",
}

# 選択されたページをインポートして表示
selected_page = st.sidebar.radio("ナビゲーション", list(pages.keys()))
page_module = __import__(pages[selected_page], fromlist=[""])

# 選択されたページの内容をレンダリング
if hasattr(page_module, "render"):
    page_module.render()
else:
    st.error("ページが見つかりませんでした。")
