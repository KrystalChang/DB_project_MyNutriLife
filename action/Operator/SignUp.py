from action.Action import Action
from DB_utils import db_register_operator, email_exist

class OperatorSignUp(Action):
    def __init__(self):
        super().__init__("OperatorSignUp")
        
    def exec(self, conn):
        # 獲取經營者輸入
        operator_name = self.read_input(conn, "operator name")
        email = self.read_input(conn, "email")
        while email_exist(email, "operator"):
            conn.send("Email already exists. Please use another email.\n".encode('utf-8'))
            email = self.read_input(conn, "another email")

        password = self.read_input(conn, "password")
        
        # 新增經營者到資料庫
        operator_id = db_register_operator(operator_name, password, email)
        conn.send(f"Successfully registered! Your operator ID is {operator_id}\n".encode('utf-8'))

        return operator_id
