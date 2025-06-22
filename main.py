from PIL import Image
import streamlit as st
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
logo_path = BASE_DIR / "logo.png"
try:
    favicon = Image.open(logo_path)
except FileNotFoundError:
    favicon = None

st.set_page_config(
    page_title="LeetCode記録サイト",
    page_icon=favicon,
    layout="wide"
)

# --- テーマの定義 (変更なし) ---
THEMES = {
    "デフォルト": {
        "bg_color": "#FFF7F0",
        "text_color": "#2e2e2e",
        "h_color": "#543939",
        "primary_btn_bg": "#A7C7E7",
        "primary_btn_hover": "#FFD8A9",
        "sidebar_bg": "#F4A7B9",
        "sidebar_text": "#2e2e2e",
        "sidebar_link": "#2e2e2e",
    },
    "ダークモード": {
        "bg_color": "#212121",
        "text_color": "#f0f2f6",
        "h_color": "#ffffff",
        "primary_btn_bg": "#424242",
        "primary_btn_hover": "#616161",
        "sidebar_bg": "#121212",
        "sidebar_text": "#f0f2f6",
        "sidebar_link": "#BBDEFB",
    },
    "ミニマル・グリーン": {
        "bg_color": "#E8F5E9",
        "text_color": "#388E3C",
        "h_color": "#1B5E20",
        "primary_btn_bg": "#4CAF50",
        "primary_btn_hover": "#81C784",
        "sidebar_bg": "#A5D6A7",
        "sidebar_text": "#388E3C",
        "sidebar_link": "#1B5E20",
    }
}

def get_theme_css(theme_name):
    theme = THEMES.get(theme_name, THEMES["デフォルト"])
    return f"""
    <style>
    .stApp {{
        background-color: {theme['bg_color']};
        font-family: 'Poppins', sans-serif;
        color: {theme['text_color']};
        padding: 0 2rem;
    }}

    h1, h2, .stMarkdown h1, .stMarkdown h2 {{
        color: {theme['h_color']};
    }}

    button[kind="primary"] {{
        background-color: {theme['primary_btn_bg']};
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }}

    [data-testid="stSidebar"] {{
        background-color: {theme['sidebar_bg']};
        color: {theme['sidebar_text']};
    }}

    [data-testid="stSidebar"] .stMarkdown a {{
        color: {theme['sidebar_link']};
    }}

    .login-container input, .login-container button {{
        margin-top: 1rem;
        width: 300px;
        border-radius: 6px;
        border: 1px solid #DDD;
        background-color: white;
    }}

    button[kind="primary"]:hover {{
        background-color: {theme['primary_btn_hover']};
        color: {theme['text_color']};
    }}

    /* サイドバーメニューの色設定（順番に適用） */
    section[data-testid="stSidebar"] label:nth-of-type(1) div span {{ color: #E74C3C !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(2) div span {{ color: #2ECC71 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(3) div span {{ color: #F39C12 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(4) div span {{ color: #2ECC71 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(5) div span {{ color: #E74C3C !important; }}

    /* Streamlitのデフォルトメニューとフッターを非表示 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """

# セッション状態に現在のテーマを保存
if 'current_theme' not in st.session_state:
    st.session_state['current_theme'] = "デフォルト"

# 選択されたテーマのCSSを適用
st.markdown(get_theme_css(st.session_state['current_theme']), unsafe_allow_html=True)


# --- ここから既存のメインアプリコード ---

# セッション状態の初期化
if 'login' not in st.session_state:
    st.session_state['login'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# 'current_page_name' セッションステートの初期化と決定
if 'current_page_name' not in st.session_state:
    if st.session_state['login']:
        st.session_state['current_page_name'] = "やることリスト"
    else:
        st.session_state['current_page_name'] = "ログイン"

st.markdown('<h1 style="color:#2ECC71;">LeetCode記録サイトへようこそ！</h1>', unsafe_allow_html=True)


# サイドバーでページ選択
st.sidebar.title("LeetCode記録サイト")

# ページ選択肢の定義
all_page_names = [
    "アカウント登録",
    "ログイン",
    "やることリスト",
    "チャットで相談",
    "実施した問題の記録",
]

# current_page_name に基づいて index を決定
try:
    default_index = all_page_names.index(st.session_state['current_page_name'])
except ValueError:
    default_index = 0

selected_by_radio = st.sidebar.radio(
    "ページを選んでください",
    all_page_names,
    index=default_index,
    key="sidebar_page_selector"
)

# ユーザーがサイドバーで選択を変更したら、セッションステートを更新
if selected_by_radio != st.session_state['current_page_name']:
    st.session_state['current_page_name'] = selected_by_radio
    st.rerun()


# テーマ選択UIをサイドバーに追加
st.sidebar.markdown("---")
st.sidebar.subheader("テーマ")
selected_theme = st.sidebar.selectbox(
    "テーマを選択",
    list(THEMES.keys()),
    index=list(THEMES.keys()).index(st.session_state['current_theme']),
    key="theme_selector"
)

# 選択されたテーマが変更されたらセッションステートを更新し再実行
if selected_theme != st.session_state['current_theme']:
    st.session_state['current_theme'] = selected_theme
    st.rerun()

# --- ログアウトボタンの追加 ---
st.sidebar.markdown("---") # 区切り線
if st.session_state.get('login', False): # ログインしている場合のみ表示
    st.sidebar.write(f"こんにちは、{st.session_state['username']}さん！")
    if st.sidebar.button("ログアウト", key="logout_button"):
        # セッションの状態をリセット
        st.session_state['login'] = False
        st.session_state['username'] = None
        
        # ユーザーデータが保持されている他のセッションステートもクリアすると安全
        # 例:
        if 'tasks' in st.session_state:
            del st.session_state['tasks']
        if 'records' in st.session_state: # もし training_log などで 'records' をセッションステートに保持している場合
            del st.session_state['records']
        if 'gemini_chat_messages' in st.session_state: # チャット履歴をクリア
            del st.session_state['gemini_chat_messages']

        # ログインページに遷移
        st.session_state['current_page_name'] = "ログイン"
        st.rerun()


# ページの表示ロジック
if st.session_state['current_page_name'] == "アカウント登録":
    from components import register
    register.render()
elif st.session_state['current_page_name'] == "ログイン":
    if not st.session_state['login']:
        from components import login
        login.render()
    else:
        st.session_state['current_page_name'] = "やることリスト"
        st.rerun()
elif st.session_state['current_page_name'] == "やることリスト":
    from components import reservation
    reservation.render()
elif st.session_state['current_page_name'] == "チャットで相談":
    from components import chat
    chat.render()
elif st.session_state['current_page_name'] == "実施した問題の記録":
    from components import training_log
    training_log.render()