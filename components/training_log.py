import streamlit as st
import pandas as pd
import altair as alt
import utils.auth as auth  # auth.py を utils フォルダに置いている前提
# import google.generativeai as genai # AIチャット機能が必要な場合はコメント解除

def render():
    if not st.session_state.get('login', False):
        st.warning("ログインしてください。")
        return

    username = st.session_state.get('username')
    st.title("実施した問題の記録")
    st.write("問題の記録を閲覧・追加できます。")

    # DBから記録取得
    # records は辞書のリストの形式を想定 (例: [{'date': '...', 'description': '...'}, ...])
    records = auth.get_records(username)

    # --- 新しい問題の記録を追加 ---
    st.header("新しい問題の記録を追加")

    with st.form("new_record_form"):
        date = st.date_input("日付", value=pd.Timestamp.now().date())
        problem_description = st.text_input("実施した問題")
        difficulty_options = ["Easy", "Medium", "Hard"] # 難易度オプション
        difficulty = st.selectbox("難易度", difficulty_options)
        # st.markdown(f"選択中の難易度: **{difficulty}**") # 必要であれば表示

        solved_options = ["解けた", "解けなかった"] # 解けた/解けなかったオプション
        solved_status = st.selectbox("解けたor解けなかった", solved_options)
        # st.markdown(f"選択中のステータス: **{solved_status}**") # 必要であれば表示

        st.subheader("反省点（感想）")
        reflections = st.text_area(
            "今日の振り返りや気づきを記入してください (500字まで)",
            height=150,
            max_chars=500,
            key="reflections_input" # キーを追加
        )
        char_count = len(reflections)
        st.markdown(f"<p style='text-align: right; font-size: 0.9em; color: gray;'>{char_count}/500字</p>", unsafe_allow_html=True)


        st.subheader("コードスニペット (オプション)")
        code_snippet = st.text_area(
            "関連するコードをここに貼り付けてください",
            height=300,
            help="入力されたコードはMarkdownのコードブロックとして表示されます。",
            key="code_snippet_input" # キーを追加
        )

        submit_button = st.form_submit_button("記録を追加")

        if submit_button:
            if problem_description and reflections:
                # 日付をDB保存に適した文字列形式に変換
                auth.add_record(username, date.strftime("%Y-%m-%d"), problem_description, difficulty, solved_status, reflections, code_snippet)
                st.success("問題が正常に記録されました！")
                st.rerun()  # 記録追加後、ページを再読み込みして最新データを表示
            else:
                st.warning("「実施した問題」と「反省点（感想）」は必須項目です。")

    # --- これまでの記録を表示 ---
    st.header("これまでの記録")

    if records:
        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date']) # 日付カラムをdatetime型に変換
        
        # カラム名を表示用に日本語に変更
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
                st.write(record['反省点（感想）']) # Markdownはそのまま反映されないのでst.write

                if 'コードスニペット' in record and pd.notna(record['コードスニペット']) and record['コードスニペット'].strip():
                    st.write("**コードスニペット:**")
                    st.code(record['コードスニペット'], language='python') # Pythonコードと仮定

    else:
        st.info("まだ記録がありません。")

    # --- グラフ表示と統計情報 ---
    st.header("分析ダッシュボード")

    if records: # データがある場合のみ表示
        df_analysis = pd.DataFrame(records) # 分析用にもう一度DataFrameを作成（元のカラム名で）
        df_analysis['date'] = pd.to_datetime(df_analysis['date']) # グラフのために日付型を再確認

        # 難易度別の問題数グラフ
        st.subheader("難易度別の問題数")
        # ここでは元のカラム名 'difficulty' を使用
        difficulty_counts = df_analysis['difficulty'].value_counts().reset_index()
        difficulty_counts.columns = ['難易度', '問題数'] # 表示用のカラム名に

        # 難易度の順序を定義 (表示順を制御するため)
        # ユーザーが指定した["Easy", "Medium", "Hard"]に合わせる
        difficulty_order = ["Easy", "Medium", "Hard"]
        # 順序に基づいてソート
        difficulty_counts['難易度'] = pd.Categorical(difficulty_counts['難易度'], categories=difficulty_order, ordered=True)
        difficulty_counts = difficulty_counts.sort_values('難易度')

        chart = alt.Chart(difficulty_counts).mark_bar().encode(
            x=alt.X('難易度', sort=difficulty_order, title='難易度'), # 順序を明示的に指定
            y=alt.Y('問題数', title='問題数'),
            tooltip=['難易度', '問題数']
        ).properties(
            title='問題の難易度分布'
        ).interactive() # グラフをインタラクティブにする

        st.altair_chart(chart, use_container_width=True)

        # 解いた問題カウント
        st.subheader("解いた問題の総数")
        total_problems = len(records) # DBから取得したrecordsリストの長さを取得
        st.metric(label="総問題数", value=total_problems)

        # 解けた問題の割合
        st.subheader("解けた問題の割合")
        # ここでは元のカラム名 'status' を使用
        solved_problems_count = df_analysis[df_analysis['status'] == '解けた'].shape[0]
        if total_problems > 0:
            solved_percentage = (solved_problems_count / total_problems) * 100
            st.metric(label="解けた問題の割合", value=f"{solved_percentage:.1f}%")
        else:
            st.info("まだ記録がないため、解けた問題の割合は算出できません。")

        # レベル変化
        st.subheader("あなたの学習レベル")
        if total_problems < 5:
            st.write("まだ始まったばかり！着実に進めましょう。 (初級レベル)")
            st.image("image/one.png") # 画像のパスは環境に合わせて調整してください
        elif 5 <= total_problems < 15:
            st.write("素晴らしい！学習が順調に進んでいます。 (中級レベル)")
            st.image("image/two.png") # 画像のパスは環境に合わせて調整してください
        else:
            st.write("ベテラン学習者ですね！さらなる高みを目指しましょう。 (上級レベル)")
            st.image("image/three.png") # 画像のパスは環境に合わせて調整してください

    else:
        st.info("グラフや統計情報を表示するには、少なくとも1つの記録を追加してください。")

    