import streamlit as st
from datetime import date
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

    # DBからタスクを取得してセッションステートに保持
    if "tasks" not in st.session_state:
        st.session_state.tasks = auth.get_tasks(username)

    # タスク追加フォーム
    with st.form(key="add_task_form", clear_on_submit=True):
        col1, col2 = st.columns([2,1])
        with col1:
            new_task = st.text_input("新しいタスクを入力", key="task_input")
        with col2:
            due = st.date_input("締切", value=date.today())
        priority = st.selectbox("優先度", ["高", "中", "低"], index=1)
        submitted = st.form_submit_button("追加")

        if submitted and new_task:
            # DBに追加
            auth.add_task(username, new_task, str(due), priority)
            # セッションにも追加
            st.session_state.tasks.append({
                "id": None,  # ここは後でDBから更新できるようにするか省略可
                "title": new_task,
                "due": str(due),
                "priority": priority,
                "done": False
            })
            st.success(f"「{new_task}」を追加しました!")
            # 再取得も可→st.session_state.tasks = auth.get_tasks(username)

    st.write("## タスク一覧")

    # ソート方法選択
    sort_method = st.selectbox("ソート方法を選択", options=["追加順", "優先度順", "日付順"])

    priority_order = {"高": 0, "中": 1, "低": 2}

    def sort_tasks(tasks, method):
        if method == "追加順":
            # idがNoneの場合があるのでidではなく順序を維持
            return tasks
        elif method == "優先度順":
            return sorted(tasks, key=lambda x: (priority_order[x["priority"]], x["due"]))
        elif method == "日付順":
            return sorted(tasks, key=lambda x: (x["due"], priority_order[x["priority"]]))
        else:
            return tasks

    sorted_tasks = sort_tasks(st.session_state.tasks, sort_method)

    for i, task in enumerate(sorted_tasks):
        cols = st.columns([0.05, 0.5, 0.15, 0.12, 0.08, 0.1])

        with cols[0]:
            checked = st.checkbox("", value=task["done"], key=f"check_{i}")
            if checked != task["done"]:
                task["done"] = checked
                # DB更新
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
            color = {"高": "red", "中": "orange", "低": "green"}[task["priority"]]
            st.markdown(f"<span style='color:{color}'>{task['priority']}</span>", unsafe_allow_html=True)

        with cols[4]:
            if not task["done"]:
                if st.button("完了", key=f"done_{i}"):
                    task["done"] = True
                    if task["id"]:
                        auth.update_task_done(task["id"], True)

        with cols[5]:
            if st.button("削除", key=f"delete_{i}"):
                if task["id"]:
                    auth.delete_task(task["id"])
                st.session_state.tasks.pop(i)
                st.rerun()
