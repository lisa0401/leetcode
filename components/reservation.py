import streamlit as st
from datetime import date

def render():
    if st.session_state['login']:
        st.title("やることリスト")
        st.write("やることリストをまとめることができます。")

        #初期化
        if "tasks" not in st.session_state:
            st.session_state.tasks = []
        if "id_counter" not in st.session_state:
            st.session_state.id_counter = 0
        
        #タスクの追加フォーム
        with st.form(key = "add_task_form", clear_on_submit=True):
            col1, col2 = st.columns([2,1])
            with col1:
                new_task = st.text_input("新しいタスクを入力", key = "task_input")
            with col2:
                due = st.date_input("締切", value=date.today())
            priority = st.selectbox("優先度", ["高", "中", "低"], index=1)
            submitted = st.form_submit_button("追加")

            if submitted and new_task: #送信され、かつ空白でない時に処理を実行                
                st.session_state.tasks.append({"title": new_task,"due": str(due), "priority" : priority, "done": False, "added_id": st.session_state.id_counter}) #タスクは辞書形式で追加
                st.session_state.id_counter += 1
                st.success(f"「{new_task}」を追加しました!")
        
        st.write("## タスク一覧")

        # ソート方法選択
        sort_method = st.selectbox("ソート方法を選択", options=["追加順", "優先度順", "日付順"])

        priority_order = {"高": 0, "中": 1, "低": 2}

        def sort_tasks(task, method):
            if method == "追加順":
                return sorted(task, key=lambda x: x["added_id"])
            elif method == "優先度順":
            # 優先度
                return sorted(task, key=lambda x: x["priority"])
            elif method == "日付順":
            # 締切日
                return sorted(task, key=lambda x: x["due"])
            else:
                return task
        
        
        # ソートしたリストを取得
        sorted_tasks = sort_tasks(st.session_state.tasks, sort_method)

        #タスクを表示・更新・削除
        for i, task in enumerate(st.session_state.tasks):
            cols = st.columns([0.05, 0.5, 0.15, 0.12, 0.08, 0.1]) #チェックボックス、タイトル、締め切り、優先度、完了、削除

            #チェックボックス
            with cols[0]:
                checked = st.checkbox("", value=task["done"], key=f"check_{i}")
                task["done"] = checked
            with cols[1]:
                if task["done"]:
                    st.markdown(f"~~{task['title']}~~")
                else:
                    st.markdown(f"{task['title']}")
            with cols[2]:
                st.markdown(f"`{task['due']}`")
            with cols[3]:
                color = {"高": "red", "中": "orange", "低": "green"}[task["priority"]]
                st.markdown(f"<span style='color:{color}'>{task['priority']}</span>", unsafe_allow_html=True)
            with cols[4]:
                if not task["done"]:
                    if st.button("完了", key = f"done_{i}"):
                        st.session_state.tasks[i]["done"] = True
            with cols[5]:
                if st.button("削除", key = f"delate_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun() #削除後にページを更新
                    break         
    else:
        st.warning("ログインしてください。")