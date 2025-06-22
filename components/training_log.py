# components/training_log.py の内容

import streamlit as st
import pandas as pd
import altair as alt
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import date

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"Gemini APIの初期設定に失敗しました。GOOGLE_API_KEYが正しく設定されているか確認してください。エラー: {e}")
    model = None

import utils.auth as auth

def render():
    if not st.session_state.get('login', False):
        st.warning("ログインしてください。")
        return
    
    username = st.session_state.get('username')

    st.markdown('<h1 style="color:#E74C3C;">実施した問題の記録</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#F39C12;font-size:18px;">問題の記録を閲覧・追加できます。</p>', unsafe_allow_html=True)
    
    problem_records_from_db = auth.get_records(username) 


    # --- 新しい問題の記録を追加 ---
    st.markdown('<h2 style="color:#F39C12;font-size:18px;">新しい問題の記録を追加</h2>', unsafe_allow_html=True)

    with st.form("new_record_form"):
        date_input = st.date_input("日付", value=pd.Timestamp.now().date())

        problem_description = st.text_input("実施した問題")
        difficulty_options = ["Easy", "Medium", "Hard"]
        difficulty = st.selectbox("難易度", difficulty_options)
        st.markdown(f"選択中の難易度: **{difficulty}**")

        you_solved_options = ["解けた","解けなかった"]
        solved_status = st.selectbox("解けたor解けなかった", you_solved_options)
        st.markdown(f"選択中のステータス: **{solved_status}**")

        st.subheader("反省点（感想）")
        reflections = st.text_area(
            "今日の振り返りや気づきを記入してください (500字まで)",
            height=150,
            max_chars=500,
            key="reflections_input"
        )
        char_count = len(reflections)
        st.markdown(f"<p style='text-align: right; font-size: 0.9em; color: gray;'>{char_count}/500字</p>", unsafe_allow_html=True)

        st.subheader("コードスニペット (オプション)")
        code_snippet = st.text_area(
            "関連するコードをここに貼り付けてください",
            height=300,
            help="入力されたコードはMarkdownのコードブロックとして表示されます。",
            key="code_snippet_input"
        )

        submit_button = st.form_submit_button("記録を追加")

        if submit_button:
            if problem_description and reflections:
                auth.add_record(
                    username,
                    date_input.strftime("%Y-%m-%d"),
                    problem_description,
                    difficulty,
                    solved_status,
                    reflections,
                    code_snippet
                )
                st.success("問題が正常に記録され、データベースに保存されました！")
                st.rerun()
            else:
                st.warning("「実施した問題」と「反省点（感想）」は必須項目です。")

    # --- これまでの記録を表示 ---
    st.header("これまでの記録")

    if problem_records_from_db:
        df = pd.DataFrame(problem_records_from_db)
        df['date'] = pd.to_datetime(df['date'])

        df.rename(columns={
            'date': '日付',
            'description': '実施した問題',
            'difficulty': '難易度',
            'status': '解けたor解けなかった',
            'reflection': '反省点（感想）',
            'code': 'コードスニペット'
        }, inplace=True)

        df = df.sort_values(by='日付', ascending=False)

        st.dataframe(df)

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="記録をCSVでダウンロード",
            data=csv_data,
            file_name="problem_records.csv",
            mime="text/csv",
        )

        # 個別の記録詳細表示（コードスニペット表示用）
        st.subheader("個別の記録詳細")
        for i, record in df.iterrows():
            # expander_key = f"record_exp_{record.get('id', i)}_{record['日付'].strftime('%Y%m%d')}" # 元のキー定義
            # ★ここを修正: key引数を削除★
            with st.expander(f"記録 #{i+1}: {record['日付'].strftime('%Y-%m-%d')} - {record['実施した問題']}", expanded=False):
                st.write(f"**日付:** {record['日付'].strftime('%Y-%m-%d')}")
                st.write(f"**実施した問題:** {record['実施した問題']}")
                st.write(f"**難易度:** {record['難易度']}")
                st.write(f"**解けたor解けなかった:** {record['解けたor解けなかった']}")
                st.write(f"**反省点（感想）:**")
                st.write(record['反省点（感想）'])
                
                if 'コードスニペット' in record and pd.notna(record['コードスニペット']) and isinstance(record['コードスニペット'], str) and record['コードスニペット'].strip():
                    st.write("**コードスニペット:**")
                    st.code(record['コードスニペット'], language='python') # 以前のタイプミスは修正済み
            
            if model:
                button_key = f"ai_eval_button_{i}"
                if st.button(f"AIにこのコードを評価してもらう（{record['実施した問題']}）", key=button_key):
                    prompt = f"Leetcodeの問題「{record['実施した問題']}」に対して、次のPythonコードを評価してください。\n```python\n{record['コードスニペット']}\n```"
                    with st.spinner("Geminiが評価中..."):
                        try:
                            response = model.generate_content(prompt)
                            st.success("✅ Geminiの評価結果")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"Gemini APIエラー: {e}")
            
            else:
                st.info("まだ記録がありません。")


        # --- グラフ表示と統計情報 ---
        st.header("分析ダッシュボード")

        if problem_records_from_db:
            df_analysis = df.copy()

            st.subheader("難易度別の問題数")
            difficulty_counts = df_analysis['難易度'].value_counts().reset_index()
            difficulty_counts.columns = ['難易度', '問題数']

            difficulty_order = ["Easy", "Medium", "Hard"]
            difficulty_counts['難易度'] = pd.Categorical(difficulty_counts['難易度'], categories=difficulty_order, ordered=True)
            difficulty_counts = difficulty_counts.sort_values('難易度')

            chart = alt.Chart(difficulty_counts).mark_bar().encode(
                x=alt.X('難易度', sort=difficulty_order, title='難易度'),
                y=alt.Y('問題数', title='問題数'),
                tooltip=['難易度', '問題数']
            ).properties(
                title='問題の難易度分布'
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

            st.subheader("解いた問題の総数")
            total_problems = len(problem_records_from_db)
            st.metric(label="総問題数", value=total_problems)

            st.subheader("解けた問題の割合")
            solved_problems_count = df_analysis[df_analysis['解けたor解けなかった'] == '解けた'].shape[0]
            if total_problems > 0:
                solved_percentage = (solved_problems_count / total_problems) * 100
                st.metric(label="解けた問題の割合", value=f"{solved_percentage:.1f}%")
            else:
                st.info("まだ記録がないため、解けた問題の割合は算出できません。")

            st.subheader("あなたの学習レベル")
            if total_problems < 5:
                st.write("まだ始まったばかり！着実に進めましょう。 (初級レベル)")
                st.image("image/one.png")
            elif 5 <= total_problems < 15:
                st.write("素晴らしい！学習が順調に進んでいます。 (中級レベル)")
                st.image("image/two.png")
            else:
                st.write("ベテラン学習者ですね！さらなる高みを目指しましょう。 (上級レベル)")
                st.image("image/three.png")
        else:
            st.info("グラフや統計情報を表示するには、少なくとも1つの記録を追加してください。")

    else:
        st.warning("ログインしてください。")