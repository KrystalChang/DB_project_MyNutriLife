from DB_utils import db_get_user_id
from action.Action import Action

class LogIn(Action):
    def __init__(self):
        super().__init__("LogIn")

    def exec(self, conn):
        conn.send("[INFO] Welcome to the User Login!\n".encode('utf-8'))
        
        # 讀取用戶輸入
        username = self.read_input(conn, "username")
        password = self.read_input(conn, "password")
        
        # 根據帳號和密碼查詢用戶 ID
        u_id = db_get_user_id(username, password)

        if u_id:
            conn.send(f"Welcome, {username}! Your user ID is {u_id}.\n".encode('utf-8'))
            return u_id  # 返回用戶 ID
        else:
            conn.send("[ERROR] Invalid login credentials. Please try again.\n".encode('utf-8'))
            return None

