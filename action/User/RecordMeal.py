from action.Action import Action  # 確保 Action 已正確導入
from DB_utils import user_record_meal, db_get_food_id_by_name  # 加入查詢 Food ID 的函數

class RecordMeal(Action):
    def __init__(self):
        super().__init__("RecordMeal")  # 設定動作名稱為 RecordMeal

    def exec(self, conn, user_id):  # 使用 user_id 作為參數
        try:
            # Step 1: 提示用戶輸入飲食資訊
            conn.send("Please enter the following information for your meal:\n".encode('utf-8'))

            # 讀取用戶輸入
            f_name = self.read_input(conn, "the food name (F_name)")  # 食物名稱
            date = self.read_input(conn, "the date of the meal (YYYY-MM-DD)")  # 日期
            time = self.read_input(conn, "the time of the meal (HH:MM)")  # 時間
            eaten_grams = int(self.read_input(conn, "the amount of food eaten in grams"))  # 食用克數

            # Step 2: 從資料庫查詢 F_id
            f_id = db_get_food_id_by_name(f_name)

            if not f_id:  # 如果查詢不到 F_id
                conn.send(f"[ERROR] Food name '{f_name}' not found in the database.\n".encode('utf-8'))
                return

            # Step 3: 呼叫資料庫函數記錄飲食
            result = user_record_meal(user_id, f_id, date, time, eaten_grams)

            # Step 4: 返回結果訊息
            if result["status"] == "success":
                conn.send("[INFO] Your meal has been recorded.\n".encode('utf-8'))
            else:
                conn.send(f"[ERROR] {result['message']}\n".encode('utf-8'))

        except Exception as e:
            # 處理例外情況
            conn.send(f"[ERROR] Failed to record meal: {str(e)}\n".encode('utf-8'))
