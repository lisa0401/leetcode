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
    st.markdown('<h1 style="color:#E74C3C;">やることリスト</h1>', unsafe_allow_html=True)
    st.markdown('<h1 style="color:#F39C12;font-size:18px;">やることリストをまとめることができます</h1>', unsafe_allow_html=True)



    # --- 連続学習記録（問題記録ベース）と最長記録の表示 ---
    all_problem_records = auth.get_records(username) # すべての問題記録を取得

    # ユニークな記録日付のセットを作成 (計算用)
    recorded_dates_set = set()
    if all_problem_records:
        for rec in all_problem_records:
            try:
                recorded_dates_set.add(date.fromisoformat(rec['rec_date']))
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
            if last_date is None or current_rec_date == last_date + timedelta(days=1): 
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
        difficulty = st.selectbox("優先度", ["高", "中", "低"], index=1)
        submitted = st.form_submit_button("追加")

        if submitted and new_task:
            auth.add_task(username, new_task, str(due), difficulty)
            st.session_state.tasks.append({
                "id": None,
                "title": new_task,
                "due": str(due),
                "difficulty": difficulty,
                "done": False
            })
            st.success(f"「{new_task}」を追加しました!")
            st.rerun()

    st.write("## タスク一覧")

    sort_method = st.selectbox("ソート方法を選択", options=["追加順", "優先度順", "日付順"])
    difficulty_order = {"高": 0, "中": 1, "低": 2}

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
            return sorted(processed_tasks, key=lambda x: (difficulty_order.get(x["difficulty"], 99), x["due"]))
        elif method == "日付順":
            return sorted(processed_tasks, key=lambda x: (x["due"], difficulty_order.get(x["difficulty"], 99)))
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
            color = {"高": "red", "中": "orange", "低": "green"}.get(task["difficulty"], "gray")
            st.markdown(f"<span style='color:{color}'>{task['difficulty']}</span>", unsafe_allow_html=True)

        with cols[4]:
            if not task["done"]:
                if st.button("完了", key=f"done_task_{task.get('id', i)}"):
                    task["done"] = True
                    if task["id"]:
                        auth.update_task_done(task["id"], True)

                    # ✅ training_log.py に表示するための記録形式に変換して追加
                    if "records" not in st.session_state:
                        st.session_state["records"] = []

                    st.session_state["records"].append({
                        "日付": date.today(),
                        "実施した問題": task["title"],
                        "難易度": task["difficulty"],  # "高", "中", "低"のまま
                        "解けたor解けなかった": "解けた",  # タスク完了は「解けた」とみなす
                        "反省点（感想）": "",  # タスクからは入力されていないので空
                        "コードスニペット": ""  # 同上
                    })

                    st.rerun()

        with cols[5]:
            if st.button("削除", key=f"delete_task_{task.get('id', i)}"):
                if task["id"]:
                    auth.delete_task(task["id"])
                st.session_state.tasks = [t for t in st.session_state.tasks if t.get('id') != task['id']]
                st.rerun()
