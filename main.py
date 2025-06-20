import streamlit as st

if 'login' not in st.session_state:
    st.session_state['login'] = False
    
# アプリの基本設定
st.set_page_config(page_title="競プロアプリ", layout="wide")

# ヘッダー
st.sidebar.title("競プロアプ")
st.sidebar.markdown("**ページを選択してください:**")

# ページの選択メニュー
pages = {
    "ログイン": "pages.login",
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
