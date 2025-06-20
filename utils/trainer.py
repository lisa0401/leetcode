import os
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
from utils.db_manager import MachineManager, TrainingManager, UserManager

# .envファイルの読み込み
load_dotenv()

WATSONX_AI_ENDPOINT = os.getenv("WATSONX_AI_ENDPOINT")
WATSONX_AI_PROJECT_ID = os.getenv("WATSONX_AI_PROJECT_ID")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")

# LLMのパラメータ設定
params = {
    "decoding_method": "greedy",
    "max_new_tokens": 10000,
    "min_new_tokens": 1,
    "repetition_penalty": 1,
    "random_seed": 42,
    "stop_sequences": [],
}

# LLMの初期化関数
def get_llm(model_id: str, params: dict):
    llm = WatsonxLLM(
        model_id=model_id,
        url=WATSONX_AI_ENDPOINT,
        apikey=WATSONX_API_KEY,
        params=params,
        project_id=WATSONX_AI_PROJECT_ID,
    )
    return llm

# LLMの初期化
llm = get_llm(
    model_id="mistralai/mistral-large",
    params=params
)

class Trainer:
    def __init__(self, user):
        self.user = user
        self.llm = llm
        self.machine_manager = MachineManager()
        self.training_manager = TrainingManager()
        self.user_manager = UserManager()
        self.set_user_info()
        self.set_machine_info()
        self.set_reserve_info()

    def ask(self, text):
        # プロンプト編集部分
        prompt = f"""
        あなたは誠実で優秀な日本人ジムトレーナーです。特に指示が無い場合は、常に日本語で回答してください。
        質問：{text}
        また、必要であれば以下の情報を参考にしてください。
        質問者の情報：{self.user_info}
        マシンの情報：{self.machine_table}
        予約情報：{self.reserve_info}
        """
        # モデルの実行
        return self.llm.invoke(prompt)
    
    # ユーザ情報の取得
    def set_user_info(self):
        self.user_info = self.user_manager.get_user_info()
        
    # マシン情報の取得
    def set_machine_info(self):
        self.machine_table = self.machine_manager.get_machines()
        
    # 予約情報の取得
    def set_reserve_info(self):
        self.reserve_info = self.machine_manager.get_all_available_times()
    
    # 予約代行
    def reserve(self, date, machine, time):
        result = self.machine_manager.reserve(date, machine, time)
        return f"予約が完了しました: {date} {machine} {time}" if result else "予約に失敗しました。"
