# auth.py - ユーザー・タスク・問題記録を統合管理するSQLite操作用モジュール
import sqlite3
import os

# データベースファイルのパス
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# ----------------------
# テーブル作成
# ----------------------
def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ユーザーテーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    # タスクテーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            due TEXT,
            priority TEXT,
            done INTEGER
        )
    """)

    # 問題記録テーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            description TEXT,
            difficulty TEXT,
            status TEXT,
            reflection TEXT,
            code TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            description TEXT,
            difficulty TEXT,
            status TEXT,
            reflection TEXT,
            code TEXT,
            title TEXT,
            due TEXT,
            done INTEGER
        )
    """)
    conn.commit()
    conn.close()

# ----------------------
# ユーザー管理
# ----------------------
def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # ユーザー名がすでに存在
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]

# ----------------------
# タスク管理
# ----------------------
def get_tasks(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, due, difficulty, done FROM logs WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "title": row[1],
            "due": row[2],
            "difficulty": row[3],
            "done": bool(row[4])
        })
    return logs

def add_task(username, title, due, difficulty):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (username, title, due, difficulty, done) VALUES (?, ?, ?, ?, ?)",
        (username, title, due, difficulty, 0)
    )
    conn.commit()
    conn.close()

def update_task_done(log_id, done):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE logs SET done = ? WHERE id = ?", (int(done), log_id))
    conn.commit()
    conn.close()

def delete_task(log_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()

# ----------------------
# 問題記録管理
# ----------------------
def get_records(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT date, description, difficulty, status, reflection, code 
        FROM logs WHERE username=?
    """, (username,))
    rows = c.fetchall()
    conn.close()
    logs = []
    for row in rows:
        logs.append({
            'date': row[0],
            'description': row[1],
            'difficulty': row[2],
            'status': row[3],
            'reflection': row[4],
            'code': row[5],
        })
    return logs


def add_record(username, date, description, difficulty, status, reflection, code):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO logs (username, date, description, difficulty, status, reflection, code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, date, description, difficulty, status, reflection, code))
    conn.commit()
    conn.close()

# ----------------------
# スクリプトとして実行された場合（テーブル初期化）
# ----------------------
if __name__ == "__main__":
    create_user_table()
    print("全テーブルを作成しました。")
    print("登録ユーザー一覧:", get_all_users())
