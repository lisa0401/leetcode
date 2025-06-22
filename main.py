# main.py の内容

from PIL import Image
import streamlit as st
import pathlib

# --- ファイルパスの修正 ---
# BASE_DIR を正しく設定し、faviconの読み込みを修正
BASE_DIR = pathlib.Path(__file__).parent
logo_path = BASE_DIR / "logo.png"

# favicon が存在しない場合のフォールバックを追加
try:
    favicon = Image.open(logo_path)
except FileNotFoundError:
    # logo.png がない場合のデフォルトアイコンまたは何もしない
    favicon = None # Streamlitのデフォルトアイコンを使用

st.set_page_config(
    page_title="競プロアプリ",
    page_icon=favicon,
    layout="wide"
)

# --- グローバルCSSの埋め込み ---
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

# --- セッション状態の初期化 ---
if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# ★★★ ページの選択肢と初期表示ページの決定ロジック ★★★
# ページの選択肢の定義（st.sidebar.radio の options と一致させる）
all_page_names = [
    "アカウント登録",
    "ログイン",
    "やることリスト",
    "チャットで相談",
    "実施した問題の記録",
]

# 'current_page_name' セッションステートの初期化と決定
if 'current_page_name' not in st.session_state:
    if st.session_state['login']:
        st.session_state['current_page_name'] = "やることリスト"
    else:
        st.session_state['current_page_name'] = "ログイン"

st.markdown('<h1 style="color:#2ECC71;">競プロアプリへようこそ！</h1>', unsafe_allow_html=True) # アプリのメインタイトル


# サイドバーでページ選択
st.sidebar.title("競プロアプリ")

# current_page_name に基づいて index を決定
try:
    default_index = all_page_names.index(st.session_state['current_page_name'])
except ValueError:
    # 万が一 current_page_name が all_page_names にない場合のフォールバック
    default_index = 0 # 「アカウント登録」をデフォルトに

selected_by_radio = st.sidebar.radio(
    "ページを選んでください",
    all_page_names,
    index=default_index, # current_page_name に対応する位置を選択
    key="sidebar_page_selector" # キーを追加
)

# ユーザーがサイドバーで選択を変更したら、セッションステートを更新
if selected_by_radio != st.session_state['current_page_name']:
    st.session_state['current_page_name'] = selected_by_radio
    st.rerun() # ページ切り替えをトリガー

# ★★★ ページの表示ロジック (st.session_state['current_page_name'] を使用) ★★★
# ここで各コンポーネントのrender()関数を呼び出す
if st.session_state['current_page_name'] == "アカウント登録":
    from components import register
    register.render()
elif st.session_state['current_page_name'] == "ログイン":
    # ログイン済みでなければログインページを表示
    if not st.session_state['login']:
        from components import login
        login.render()
    else:
        # ログイン済みにもかかわらずこのページに来たら、自動で「やることリスト」へ
        st.session_state['current_page_name'] = "やることリスト"
        st.rerun() # 再実行してやることリストへ遷移
elif st.session_state['current_page_name'] == "やることリスト":
    from components import reservation
    reservation.render()
elif st.session_state['current_page_name'] == "チャットで相談":
    from components import chat
    chat.render()
elif st.session_state['current_page_name'] == "実施した問題の記録":
    from components import training_log
    training_log.render()