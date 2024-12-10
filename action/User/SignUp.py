from action.Action import Action
from DB_utils import db_register_user, username_exist

class SignUp(Action):
    def __init__(self):
        # 傳入動作名稱 "SignUp"
        super().__init__("SignUp")

    def exec(self, conn):
        # 獲取使用者輸入
        username = self.read_input(conn, "username")
        while username_exist(username):
            conn.send("Username already exists. Please choose another one.\n".encode('utf-8'))
            username = self.read_input(conn, "another username")

        password = self.read_input(conn, "password")
        email = self.read_input(conn, "email")
        birth_date = self.read_input(conn, "birth date (YYYY-MM-DD)")
        gender = self.read_input(conn, "gender (M/F)")

        # 新增使用者到資料庫
        try:
            user_id = db_register_user(username, password, email, birth_date, gender)
            conn.send(f"Successfully registered! Your user ID is {user_id}\n".encode('utf-8'))
        except ValueError as e:
            conn.send(f"Registration failed: {e}\n".encode('utf-8'))

        return user_id
