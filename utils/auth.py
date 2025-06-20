# ユーザテーブルにアクセス
# 入力されたメールアドレスとパスワードを参照
import pandas as pd

def authenticate_user(mail, password):
    # ユーザーテーブルを読み込み
    user_table = pd.read_csv('db/user_table.csv')

    # 条件を確認
    matching_users = user_table[(user_table['Email'] == mail) & (user_table['Password'] == password)]

    # ユーザーが見つからない場合の処理
    if matching_users.empty:
        return None  # またはエラーメッセージを返す

    # ユーザー名を返す
    return matching_users.iloc[0]['User']