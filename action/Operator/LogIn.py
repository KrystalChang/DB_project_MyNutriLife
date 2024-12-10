# OperatorLogIn.py
from action.Action import Action
from DB_utils import db_get_operator_id

class OperatorLogIn(Action):
    def __init__(self):
        super().__init__("OperatorLogIn")  # 初始化基類 Action，並設置 action 名稱

    def exec(self, conn):
        """執行經營者登入功能"""
        conn.send("[INFO] Operator Log In\n".encode('utf-8'))

        # 使用 read_input 讀取使用者輸入
        email = self.read_input(conn, "Enter your email")
        password = self.read_input(conn, "Enter your password")

        # 根據帳號和密碼查找 operator_id
        operator_id = db_get_operator_id(email, password)

        if operator_id:
            conn.send(f"Welcome, Operator {email}. Your operator ID is {operator_id}.\n".encode('utf-8'))
            return operator_id
        else:
            conn.send("[ERROR] Invalid login credentials.\n".encode('utf-8'))
            return None
