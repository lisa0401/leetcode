import streamlit as st
import pandas as pd
import altair as alt
import utils.auth as auth  # auth.py を utils フォルダに置いている前提

def render():
    if not st.session_state.get('login', False):
        st.warning("ログインしてください。")
        return

    username = st.session_state.get('username')
    st.title("実施した問題の記録")
    st.write("問題の記録を閲覧・追加できます。")

    # DBから記録取得
    records = auth.get_records(username)

    # --- 新しい問題の記録を追加 ---
    st.header("新しい問題の記録を追加")

    with st.form("new_record_form"):
        date = st.date_input("日付", value=pd.Timestamp.now().date())
        problem_description = st.text_input("実施した問題")
        difficulty_options = ["Easy", "Medium", "Hard"]
        difficulty = st.selectbox("難易度", difficulty_options)
        solved_options = ["解けた", "解けなかった"]
        solved_status = st.selectbox("解けたor解けなかった", solved_options)
        st.subheader("反省点（感想）")
        reflections = st.text_area("今日の振り返りや気づきを記入してください (500字まで)", height=150, max_chars=500)
        st.subheader("コードスニペット (オプション)")
        code_snippet = st.text_area("関連するコードをここに貼り付けてください", height=300)

        submit_button = st.form_submit_button("記録を追加")

        if submit_button:
            if problem_description and reflections:
                auth.add_record(username, date.strftime("%Y-%m-%d"), problem_description, difficulty, solved_status, reflections, code_snippet)
                st.success("問題が正常に記録されました！")
                st.rerun()  # ここはst.rerun()に変えてもよい
            else:
                st.warning("「実施した問題」と「反省点（感想）」は必須項目です。")

    # --- これまでの記録を表示 ---
    st.header("これまでの記録")

    if records:
        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        # カラム名を表示用に変更
        df.rename(columns={
            'date': '日付',
            'description': '実施した問題',
            'difficulty': '難易度',
            'status': '解けたor解けなかった',
            'reflection': '反省点（感想）',
            'code': 'コードスニペット'
        }, inplace=True)

        st.dataframe(df)

        # CSVダウンロード
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="記録をCSVでダウンロード", data=csv_data, file_name="problem_records.csv", mime="text/csv")

        # 個別詳細表示
        st.subheader("個別の記録詳細")
        for i, record in df.iterrows():
            with st.expander(f"記録 #{i+1}: {record['日付'].strftime('%Y-%m-%d')} - {record['実施した問題']}"):
                st.write(f"**日付:** {record['日付'].strftime('%Y-%m-%d')}")
                st.write(f"**実施した問題:** {record['実施した問題']}")
                st.write(f"**難易度:** {record['難易度']}")
                st.write(f"**解けたor解けなかった:** {record['解けたor解けなかった']}")
                st.write(f"**反省点（感想）:**")
                st.write(record['反省点（感想）'])
                if 'コードスニペット' in record and pd.notna(record['コードスニペット']) and record['コードスニペット'].strip():
                    st.write("**コードスニペット:**")
                    st.code(record['コードスニペット'], language='python')
    else:
        st.info("まだ記録がありません。")

    # --- グラフ表示などは必要に応じて追加してください ---
