import streamlit as st
import pandas as pd
import altair as alt # グラフ表示のために追加

def render():
    if st.session_state.get('login', False): # Use .get() for safer access
        st.markdown('<h1 style="color:#E74C3C;">実施した問題の記録</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#F39C12;font-size:18px;">問題の記録を閲覧・追加できます。</p>', unsafe_allow_html=True)
        

        # セッションステートに 'records' リストがない場合は初期化
        if 'records' not in st.session_state:
            st.session_state['records'] = []

        # --- 新しい問題の記録を追加 ---
        st.markdown('<h2 style="color:#F39C12;font-size:18px;">新しい問題の記録を追加</h2>', unsafe_allow_html=True)

        # st.form を使用して、ボタンが押されるまで再描画されないようにする
        with st.form("new_record_form"):
            # Date input - デフォルト値を今日に設定
            date = st.date_input("日付", value=pd.Timestamp.now().date())

            # Problem worked on (text input)
            problem_description = st.text_input("実施した問題")

            # Difficulty (select box)
            difficulty_options = ["Easy", "Medium", "Hard"]
            difficulty = st.selectbox("難易度", difficulty_options)
            st.markdown(f"選択中の難易度: **{difficulty}**") # ★太字表示の追加★

            # 「解けたor解けなかった」の選択
            you_solved_options = ["解けた","解けなかった"]
            solved_status = st.selectbox("解けたor解けなかった", you_solved_options)
            st.markdown(f"選択中のステータス: **{solved_status}**") # ★太字表示の追加★

            # Reflections/Impressions (text area for longer input)
            st.subheader("反省点（感想）")
            reflections = st.text_area(
                "今日の振り返りや気づきを記入してください (500字まで)",
                height=150,
                max_chars=500, # ★文字数制限の追加★
                key="reflections_input" # キーを追加
            )
            # 文字数カウンター
            char_count = len(reflections)
            st.markdown(f"<p style='text-align: right; font-size: 0.9em; color: gray;'>{char_count}/500字</p>", unsafe_allow_html=True)

            # ★コード入力欄の追加★
            st.subheader("コードスニペット (オプション)")
            code_snippet = st.text_area(
                "関連するコードをここに貼り付けてください",
                height=300, # コードが見やすいように高さを確保
                help="入力されたコードはMarkdownのコードブロックとして表示されます。",
                key="code_snippet_input" # キーを追加
            )


            # Submit button
            submit_button = st.form_submit_button("記録を追加")

            if submit_button:
                if problem_description and reflections: # Ensure essential fields are filled
                    # 新しい記録をセッションステートのリストに追加
                    st.session_state['records'].append({
                        '日付': date,
                        '実施した問題': problem_description,
                        '難易度': difficulty,
                        '解けたor解けなかった': solved_status,
                        '反省点（感想）': reflections,
                        'コードスニペット': code_snippet # ★コードスニペットを追加★
                    })
                    st.success("問題が正常に記録されました！")
                    # フォームをクリアし、表示を更新するために再実行
                    st.rerun()
                else:
                    st.warning("「実施した問題」と「反省点（感想）」は必須項目です。")

        # --- これまでの記録を表示 ---
        st.header("これまでの記録")

        if st.session_state['records']: # recordsリストにデータがあるかチェック
           df = pd.DataFrame(st.session_state['records'])
           df['日付'] = pd.to_datetime(df['日付']) # DataFrame表示用にTimestampに変換

           # コードスニペットカラムが存在する場合にのみ表示調整
           if 'コードスニペット' in df.columns:
               # st.dataframeでコードスニペットを表示する際に改行が効くように調整
               # ただし、st.dataframeはそのままMarkdownレンダリングはしないため、
               # コードスニペットが長い場合は、後述の展開機能などで詳細表示を推奨します。
               pass # ここでは特別なDataFrame表示調整は不要 (表示自体はされるため)


           st.dataframe(df)

           # ダウンロードボタン (メモリ上のDataFrameからCSVを生成)
           csv_data = df.to_csv(index=False).encode('utf-8')
           st.download_button(
               label="記録をCSVでダウンロード",
               data=csv_data,
               file_name="problem_records.csv",
               mime="text/csv",
           )

           # ★個別の記録詳細表示（コードスニペット表示用）★
           st.subheader("個別の記録詳細")
           # 記録を一つずつExpandableな要素で表示
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
                       # コードブロックとして表示
                       st.code(record['コードスニペット'], language='python') # Pythonコードと仮定

        else:
           st.info("まだ記録がありません。")

        # --- グラフ表示と統計情報 ---
        st.header("分析ダッシュボード")

        if st.session_state['records']: # データがある場合のみ表示
            df_analysis = pd.DataFrame(st.session_state['records'])
            df_analysis['日付'] = pd.to_datetime(df_analysis['日付']) # グラフのために日付型を再確認

            # 難易度別の問題数グラフ
            st.subheader("難易度別の問題数")
            difficulty_counts = df_analysis['難易度'].value_counts().reset_index()
            difficulty_counts.columns = ['難易度', '問題数']

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
            total_problems = len(st.session_state['records']) # recordsリストの長さを取得
            st.metric(label="総問題数", value=total_problems)

            # 解けた問題の割合
            st.subheader("解けた問題の割合")
            solved_problems_count = df_analysis[df_analysis['解けたor解けなかった'] == '解けた'].shape[0]
            if total_problems > 0:
                solved_percentage = (solved_problems_count / total_problems) * 100
                st.metric(label="解けた問題の割合", value=f"{solved_percentage:.1f}%")
            else:
                st.info("まだ記録がないため、解けた問題の割合は算出できません。")

            # レベル変化
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

# アプリをテストするためのログイン状態設定（本番では認証システムと連携）
# st.session_state['login'] = True # テスト時はコメント解除してTrueにする