import streamlit as st
from datetime import date, timedelta
import pandas as pd
import altair as alt
import utils.auth as auth

def render():
    if not st.session_state.get("login", False):
        st.warning("ログインしてください。")
        return

    username = st.session_state.get("username", None)
    if username is None:
        st.warning("ユーザ情報が見つかりません。")
        return

    st.title("やることリスト")
    st.write("やることリストをまとめることができます。")

    # --- 連続学習記録（問題記録ベース）と最長記録の表示 ---
    all_problem_records = auth.get_records(username) # すべての問題記録を取得

    # ユニークな記録日付のセットを作成 (計算用)
    recorded_dates_set = set()
    if all_problem_records:
        for rec in all_problem_records:
            try:
                recorded_dates_set.add(date.fromisoformat(rec['date']))
            except (KeyError, ValueError):
                continue

    # ---------------------------------------------
    # 現在の連続記録の計算
    current_streak = 0
    check_date = date.today()

    if check_date in recorded_dates_set:
        current_streak = 1
        check_date -= timedelta(days=1)
    else:
        check_date -= timedelta(days=1)

    while check_date in recorded_dates_set:
        current_streak += 1
        check_date -= timedelta(days=1)
    # ---------------------------------------------

    # ---------------------------------------------
    # 最長記録の計算
    longest_streak = 0
    if recorded_dates_set: # 記録がある場合のみ計算
        sorted_unique_dates = sorted(list(recorded_dates_set))
        temp_current_streak = 0
        last_date = None

        for current_rec_date in sorted_unique_dates:
            if last_date is None or current_rec_date == last_rec_date + timedelta(days=1): # ここを修正: last_rec_date -> last_date
                temp_current_streak += 1
            else:
                temp_current_streak = 1
            
            longest_streak = max(longest_streak, temp_current_streak)
            last_date = current_rec_date
    # ---------------------------------------------

    # ---------------------------------------------
    # 今日の問題数を計算
    today_solved_count = 0
    today_iso_date = date.today().isoformat()
    if all_problem_records:
        for rec in all_problem_records:
            if rec.get('date') == today_iso_date:
                today_solved_count += 1
    # ---------------------------------------------


    col_streak1, col_streak2, col_today_solved = st.columns(3) # カラム数を3つに増やす
    with col_streak1:
        st.metric(label="問題記録連続日数", value=f"{current_streak}日")
    with col_streak2:
        st.metric(label="最長連続記録", value=f"{longest_streak}日")
    with col_today_solved: # 新しいカラムに表示
        st.metric(label="今日解いた問題数", value=f"{today_solved_count}問")
    
    st.markdown("---") # 区切り線

    # ★レベルに応じた画像表示の追加★
    st.subheader("あなたの学習レベル (今日解いた問題数で変わるよ☆)")
    total_problems = len(all_problem_records) # 総問題数を問題記録の数から取得

    if total_problems < 5:
        st.write("まだ始まったばかり！着実に進めましょう。 (初級レベル)")
        st.image("image/one.png") # 画像のパスは環境に合わせて調整してください
    elif 5 <= total_problems < 15:
        st.write("素晴らしい！学習が順調に進んでいます。 (中級レベル)")
        st.image("image/two.png") # 画像のパスは環境に合わせて調整してください
    else:
        st.write("ベテラン学習者ですね！さらなる高みを目指しましょう。 (上級レベル)")
        st.image("image/three.png") # 画像のパスは環境に合わせて調整してください
    
    st.markdown("---") # 区切り線


    # DBからタスクを取得してセッションステートに保持
    if "tasks" not in st.session_state:
        st.session_state.tasks = auth.get_tasks(username)

    # タスク追加フォーム
    st.header("新しいタスクを入力")
    with st.form(key="add_task_form", clear_on_submit=True):
        col1, col2 = st.columns([2,1])
        with col1:
            new_task = st.text_input("新しいタスクを入力", key="task_input")
        with col2:
            due = st.date_input("締切", value=date.today())
        priority = st.selectbox("優先度", ["高", "中", "低"], index=1)
        submitted = st.form_submit_button("追加")

        if submitted and new_task:
            auth.add_task(username, new_task, str(due), priority)
            st.session_state.tasks.append({
                "id": None,
                "title": new_task,
                "due": str(due),
                "priority": priority,
                "done": False
            })
            st.success(f"「{new_task}」を追加しました!")
            st.rerun()

    st.write("## タスク一覧")

    sort_method = st.selectbox("ソート方法を選択", options=["追加順", "優先度順", "日付順"])
    priority_order = {"高": 0, "中": 1, "低": 2}

    def sort_tasks(tasks, method):
        processed_tasks = []
        for task in tasks:
            t_copy = task.copy()
            if isinstance(t_copy["due"], str):
                try:
                    t_copy["due"] = date.fromisoformat(t_copy["due"])
                except ValueError:
                    t_copy["due"] = date.min
            processed_tasks.append(t_copy)

        if method == "追加順":
            return tasks
        elif method == "優先度順":
            return sorted(processed_tasks, key=lambda x: (priority_order.get(x["priority"], 99), x["due"]))
        elif method == "日付順":
            return sorted(processed_tasks, key=lambda x: (x["due"], priority_order.get(x["priority"], 99)))
        else:
            return tasks

    sorted_tasks = sort_tasks(st.session_state.tasks, sort_method)

    for i, task in enumerate(sorted_tasks):
        cols = st.columns([0.05, 0.5, 0.15, 0.12, 0.08, 0.1])

        with cols[0]:
            checked = st.checkbox("", value=task["done"], key=f"check_task_{task.get('id', i)}")
            if checked != task["done"]:
                task["done"] = checked
                if task["id"]:
                    auth.update_task_done(task["id"], checked)

        with cols[1]:
            if task["done"]:
                st.markdown(f"~~{task['title']}~~")
            else:
                st.markdown(task["title"])

        with cols[2]:
            st.markdown(f"`{task['due']}`")

        with cols[3]:
            color = {"高": "red", "中": "orange", "低": "green"}.get(task["priority"], "gray")
            st.markdown(f"<span style='color:{color}'>{task['priority']}</span>", unsafe_allow_html=True)

        with cols[4]:
            if not task["done"]:
                if st.button("完了", key=f"done_task_{task.get('id', i)}"):
                    task["done"] = True
                    if task["id"]:
                        auth.update_task_done(task["id"], True)
                    st.rerun()

        with cols[5]:
            if st.button("削除", key=f"delete_task_{task.get('id', i)}"):
                if task["id"]:
                    auth.delete_task(task["id"])
                st.session_state.tasks = [t for t in st.session_state.tasks if t.get('id') != task['id']]
                st.rerun()


    # --- 既にやった問題の記録表示と検索機能 ---
    st.write("## 既にやった問題の記録")

    problem_records_display = all_problem_records # 上で取得済みのデータを使用

    if problem_records_display:
        df_problems = pd.DataFrame(problem_records_display)
        df_problems['date'] = pd.to_datetime(df_problems['date'])

        df_problems.rename(columns={
            'date': '日付',
            'description': '実施した問題',
            'difficulty': '難易度',
            'status': '解けたor解けなかった',
            'reflection': '反省点（感想）',
            'code': 'コードスニペット'
        }, inplace=True)

        df_problems = df_problems.sort_values(by='日付', ascending=False)

        st.subheader("問題記録の検索・フィルタリング")
        search_col1, search_col2, search_col3 = st.columns([1,1,1])

        with search_col1:
            search_query = st.text_input("キーワード検索 (問題名/感想)", "", key="problem_search_query")
        with search_col2:
            difficulty_options_filter = ["Easy", "Medium", "Hard"]
            search_difficulty = st.selectbox("難易度でフィルタ", ["すべて"] + difficulty_options_filter, key="problem_search_difficulty")
        with search_col3:
            search_solved_status = st.selectbox("解決状況でフィルタ", ["すべて", "解けた", "解けなかった"], key="problem_search_solved_status")

        filtered_df = df_problems.copy()
        if search_query:
            filtered_df = filtered_df[
                filtered_df['実施した問題'].str.contains(search_query, case=False, na=False) |
                filtered_df['反省点（感想）'].str.contains(search_query, case=False, na=False)
            ]
        if search_difficulty != "すべて":
            filtered_df = filtered_df[filtered_df['難易度'] == search_difficulty]
        if search_solved_status != "すべて":
            filtered_df = filtered_df[filtered_df['解けたor解けなかった'] == search_solved_status]

        if not filtered_df.empty:
            st.dataframe(filtered_df)

            csv_data_filtered = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="フィルタされた記録をCSVでダウンロード",
                data=csv_data_filtered,
                file_name="filtered_problem_records.csv",
                mime="text/csv",
                key="download_filtered_problems_csv"
            )

            st.subheader("フィルタされた記録詳細")
            for i, rec in filtered_df.iterrows():
                expander_key = f"problem_record_expander_{rec.get('id', i)}_{rec['日付'].strftime('%Y%m%d')}"
                with st.expander(f"記録 #{i+1}: {rec['日付'].strftime('%Y-%m-%d')} - {rec['実施した問題']}", expanded=False):
                    st.write(f"**日付:** {rec['日付'].strftime('%Y-%m-%d')}")
                    st.write(f"**実施した問題:** {rec['実施した問題']}")
                    st.write(f"**難易度:** {rec['難易度']}")
                    st.write(f"**解けたor解けなかった:** {rec['解けたor解けなかった']}")
                    st.write(f"**反省点（感想）:**")
                    st.write(rec['反省点（感想）'])
                    if 'コードスニペット' in rec and pd.notna(rec['コードスニペット']) and isinstance(rec['コードスニペット'], str) and rec['コードスニペット'].strip():
                        st.write("**コードスニペット:**")
                        st.code(rec['コードスニペット'], language='python')
        else:
            st.info("検索条件に合致する記録がありません。")

    else:
        st.info("まだ実施した問題の記録がありません。記録ページで追加してください。")