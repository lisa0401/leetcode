import pandas as pd
import streamlit as st
from datetime import date

class MachineManager:
    def __init__(self):
        # 各テーブルのCSVパス
        self.machine_table_path = "db/machine_table.csv"
        self.reservation_table_path = "db/reservation_table.csv"

    def get_machines(self):
        """指定した日に利用可能なマシン一覧を取得"""
        # 予約テーブルを読み込む
        machine_table = pd.read_csv(self.machine_table_path)
        available_machines = machine_table["ID"].unique().tolist()
        return available_machines
    
    # 予約情報をすべて取得
    def get_all_available_times(self):
        reservation_table = pd.read_csv(self.reservation_table_path)
        return reservation_table
    
    def get_available_times(self, date, machine):
        """指定したマシンと日に利用可能な時間を取得"""
        reservation_table = pd.read_csv(self.reservation_table_path)
        reserved_slots = reservation_table[
            (reservation_table["Date"] == date) &
            (reservation_table["Machine ID"] == machine)
        ]["Time Slot"].tolist()

        # 全時間スロットを生成
        all_time_slots = [f"{hour:02}:{minute:02}" for hour in range(24) for minute in range(0, 60, 10)]

        # 利用可能な時間を算出
        available_slots = [time for time in all_time_slots if time not in reserved_slots]
        return available_slots

    def reserve(self, date, machine, time):
        """指定された日時に予約を追加"""
        reservation_table = pd.read_csv(self.reservation_table_path)

        # 型の統一
        reservation_table['Date'] = reservation_table['Date'].astype(str)
        reservation_table['Time Slot'] = reservation_table['Time Slot'].astype(str)
        reservation_table['Machine ID'] = reservation_table['Machine ID'].astype(str)

        # 型を統一した上で重複確認
        duplicate_check = reservation_table[
            (reservation_table["Date"] == str(date)) &
            (reservation_table["Time Slot"] == str(time)) &
            (reservation_table["Machine ID"] == str(machine))
        ]
        
        if not duplicate_check.empty:
            return False  # 既に予約済み

        # 以下、先ほどと同様の処理
        new_reservation = pd.DataFrame([{
            "Date": date,
            "Time Slot": time,
            "Machine ID": machine
        }])

        updated_reservation_table = pd.concat([reservation_table, new_reservation], ignore_index=True)
        updated_reservation_table.to_csv(self.reservation_table_path, index=False)
        return True

class TrainingManager:
    def __init__(self):
        # 各テーブルのCSVパス
        self.user = st.session_state['user']
        self.machine_table_path = "db/machine_table.csv"
        self.training_table_path = "db/training_table.csv"

    def get_machines(self):
        """利用可能なマシン一覧を取得"""
        machine_table = pd.read_csv(self.machine_table_path)
        machines = machine_table["Machine"].unique().tolist()
        return machines

    def get_menu(self, machine):
        """指定されたマシンのトレーニングメニューと重量候補を取得"""
        machine_table = pd.read_csv(self.machine_table_path)
        training_table = pd.read_csv(self.training_table_path)

        # マシンに対応する重さリスト
        max_weights = machine_table[machine_table['Machine'] == machine]['Weight'].unique().tolist()

        # トレーニングメニュー候補
        menus = training_table[training_table['Machine'] == machine]['Menu'].unique().tolist()

        return max_weights, menus

    def log(self, machine, menu, weight, duration, reps, sets):
        """トレーニング内容を記録"""
        # 現在の記録を読み込み (存在しない場合は空のDataFrameを作成)
        try:
            training_log = pd.read_csv(f"db/{self.user}/training_log.csv")
        except FileNotFoundError:
            # 必要なカラムのみ用意して初期化
            training_log = pd.DataFrame(columns=["Date", "Machine", "Menu", "Weight", "Duration", "Reps", "Sets"])

        # 新しい記録を作成 (日付のみ記録)
        new_log = {
            "Date": date.today().strftime("%Y-%m-%d"),  # 日付のみ記録
            "Machine": machine,
            "Menu": menu,
            "Weight": weight,
            "Duration": duration,
            "Reps": reps,
            "Sets": sets,
        }

        # 記録を追加して保存
        training_log = pd.concat([training_log, pd.DataFrame([new_log])], ignore_index=True)
        training_log.to_csv(f"db/{self.user}/training_log.csv", index=False)

        return new_log

# ユーザ情報の取得   
class UserManager:
    def __init__(self):
        # 各テーブルのCSVパス
        self.user = st.session_state['user']
        self.user_table_path = "db/user_table.csv"
        self.training_log_path = f"db/{self.user}/training_log.csv"  # トレーニング記録用CSV

    # ユーザ情報の取得
    def get_user_info(self):
        user_table = pd.read_csv(self.user_table_path)
        # 鍛えたい箇所、レベル
        user_info = user_table[user_table['User'] == self.user]
        return user_info
    
    # 過去2週間分のトレーニング記録を取得
    def get_training_log(self):
        training_log = pd.read_csv(self.training_log_path)
        training_log = training_log[training_log['Date'] >= date.today()-14]
        return training_log