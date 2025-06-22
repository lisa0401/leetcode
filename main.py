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
    page_title="競プロアプリ",
    page_icon=favicon,
    layout="wide"
)

# --- テーマの定義 ---
# ここで複数のテーマを定義します。色コードを自由に変更・追加してください。
THEMES = {
    "デフォルト (競プロアプリ)": {
        "bg_color": "#FFF7F0",       # アプリ全体の背景 (Soft cream)
        "text_color": "#2e2e2e",     # 全体的なテキスト色 (Dark pastel-compatible gray)
        "h_color": "#2e2e2e",        # ヘッダー (h1, h2) のテキスト色
        "primary_btn_bg": "#A7C7E7", # プライマリボタンの背景 (Soft blue)
        "primary_btn_hover": "#FFD8A9", # プライマリボタンのホバー色 (Soft orange)
        "sidebar_bg": "#F4A7B9",     # サイドバーの背景 (Soft red-pink)
        "sidebar_text": "#2e2e2e",   # サイドバーのテキスト色
        "sidebar_link": "#2e2e2e",   # サイドバーのリンク色
    },
    "ダークモード": {
        "bg_color": "#212121",       # 全体の背景 (Dark Gray)
        "text_color": "#f0f2f6",     # 全体テキスト (Light Gray)
        "h_color": "#ffffff",        # ヘッダーテキスト (White)
        "primary_btn_bg": "#424242", # ボタン背景 (Gray)
        "primary_btn_hover": "#616161", # ボタンホバー (Lighter Gray)
        "sidebar_bg": "#121212",     # サイドバー背景 (Very Dark Gray)
        "sidebar_text": "#f0f2f6",   # サイドバーテキスト (Light Gray)
        "sidebar_link": "#BBDEFB",   # サイドバーリンク (Light Blue)
    },
    "ミニマル・グリーン": {
        "bg_color": "#E8F5E9",       # 薄緑
        "text_color": "#388E3C",     # 濃い緑
        "h_color": "#1B5E20",        # さらに濃い緑
        "primary_btn_bg": "#4CAF50", # 緑
        "primary_btn_hover": "#81C784", # 明るい緑
        "sidebar_bg": "#A5D6A7",     # サイドバー薄い緑
        "sidebar_text": "#388E3C",
        "sidebar_link": "#1B5E20",
    }
}

# テーマCSSを生成する関数
def get_theme_css(theme_name):
    theme = THEMES.get(theme_name, THEMES["デフォルト (競プロアプリ)"]) # 存在しないテーマならデフォルト

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

    /* サイドバーメニューの色設定（順番に適用） - これはテーマ選択では変更されません */
    section[data-testid="stSidebar"] label:nth-of-type(1) div span {{ color: #E74C3C !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(2) div span {{ color: #2ECC71 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(3) div span {{ color: #F39C12 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(4) div span {{ color: #2ECC71 !important; }}
    section[data-testid="stSidebar"] label:nth-of-type(5) div span {{ color: #E74C3C !important; }}

    /* Streamlitのデフォルトメニューとフッターを非表示 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}} /* 必要なら */
    </style>
    """

# セッション状態に現在のテーマを保存
if 'current_theme' not in st.session_state:
    st.session_state['current_theme'] = "デフォルト (競プロアプリ)"

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

st.markdown('<h1 style="color:#2ECC71;">競プロアプリへようこそ！</h1>', unsafe_allow_html=True) # アプリのメインタイトル


# サイドバーでページ選択
st.sidebar.title("競プロアプリ")

# ページ選択肢の定義（st.sidebar.radio の options と一致させる）
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
    default_index = 0 # フォールバック

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

# --- テーマ選択UIをサイドバーに追加 ---
st.sidebar.markdown("---") # 区切り線
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

# ページの表示ロジック (st.session_state['current_page_name'] を使用)
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