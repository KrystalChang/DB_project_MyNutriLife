# server.py

import socket
import threading
import logging
from action.User.SignUp import SignUp
from action.User.LogIn import LogIn
from action.User.RecordMeal import RecordMeal
from action.User.NutrientAnalysis import NutrientAnalysis
from action.User.SearchNutrientofFood import SearchNutrientofFood
from action.User.ViewMealHistory import ViewMealHistory
from action.User.BrowseArticles import BrowseArticles
from action.User.BrowseFavoriteArticles import BrowseFavoriteArticles
from action.Operator.SignUp import OperatorSignUp
from action.Operator.LogIn import OperatorLogIn
from action.Operator.WriteArticle import WriteArticle
from action.Operator.EditArticle import EditArticle
from action.Operator.DeleteArticle import DeleteArticle

# 設定日誌
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_client(conn, addr):
    logging.info(f"Handling client {addr}")
    try:
        # 讓用戶選擇角色（User 或 Operator）
        message = "[CHOICE] Choose your role:\n1. User\n2. Operator\n3. Leave\n"
        conn.sendall(message.encode('utf-8'))
        role_choice = conn.recv(1024).decode('utf-8').strip()
        logging.debug(f"Client {addr} selected role: {role_choice}")

        if role_choice == "1":
            # 用戶選擇 User
            user_id = None
            while True:
                if user_id is None:
                    # 尚未登入，提供註冊或登入選項
                    message = "[CHOICE] Choose an action:\n1. SignUp\n2. LogIn\n3. Leave\n"
                    conn.sendall(message.encode('utf-8'))
                    action_choice = conn.recv(1024).decode('utf-8').strip()

                    if action_choice == "1":
                        action = SignUp()  # 用戶註冊
                        action.exec(conn)
                    elif action_choice == "2":
                        action = LogIn()  # 用戶登入
                        user_id = action.exec(conn) 
                        logging.info(f"Client {addr} logged in as User ID: {user_id}")
                    elif action_choice == "3":
                        success_message = "[SUCCESS] Leaving the system.\n"
                        conn.sendall(success_message.encode('utf-8'))
                        logging.info(f"Client {addr} is leaving the system.")
                        break  # 離開系統
                    else:
                        error_message = "[ERROR] Invalid choice.\n"
                        conn.sendall(error_message.encode('utf-8'))
                        logging.warning(f"Client {addr} made an invalid choice.")
                else:
                    # 用戶已登入，提供功能選項
                    message = (
                        "[CHOICE] Choose an action:\n"
                        "1. Record Meal\n"
                        "2. Nutrient Analysis\n"
                        "3. Search Nutrient of Food\n"
                        "4. View Meal History\n"
                        "5. Browse Articles\n"
                        "6. Browse or Delete Favorite Articles\n"
                        "7. Leave\n"
                    )
                    conn.sendall(message.encode('utf-8'))
                    action_choice = conn.recv(1024).decode('utf-8').strip()

                    if action_choice == "1":
                        action = RecordMeal()
                        action.exec(conn, user_id)       
                    elif action_choice == "2":
                        action = NutrientAnalysis()
                        action.exec(conn, user_id)    
                    elif action_choice == "3":
                        action = SearchNutrientofFood()
                        action.exec(conn, user_id) 
                    elif action_choice == "4":
                        action = ViewMealHistory()
                        action.exec(conn, user_id) 
                    elif action_choice == "5":
                        action = BrowseArticles()
                        action.exec(conn, user_id) 
                    elif action_choice == "6":
                        action = BrowseFavoriteArticles()
                        action.exec(conn, user_id) 
                    elif action_choice == "7":
                        success_message = "[SUCCESS] Leaving the system.\n"
                        conn.sendall(success_message.encode('utf-8'))
                        logging.info(f"Client {addr} is leaving the system.")
                        break  # 離開系統
                    else:
                        error_message = "[ERROR] Invalid choice.\n"
                        conn.sendall(error_message.encode('utf-8'))
                        logging.warning(f"Client {addr} made an invalid choice.")

        elif role_choice == "2":
            # 用戶選擇 Operator
            operator_id = None
            while True:
                if operator_id is None:
                    # 尚未登入，提供註冊或登入選項
                    message = "[CHOICE] Choose an action:\n1. SignUp\n2. LogIn\n3. Leave\n"
                    conn.sendall(message.encode('utf-8'))
                    action_choice = conn.recv(1024).decode('utf-8').strip()

                    if action_choice == "1":
                        action = OperatorSignUp()  # 經營者註冊
                        action.exec(conn)
                    elif action_choice == "2":
                        action = OperatorLogIn()  # 經營者登入
                        operator_id = action.exec(conn)  
                        logging.info(f"Client {addr} logged in as Operator ID: {operator_id}")
                    elif action_choice == "3":
                        success_message = "[SUCCESS] Leaving the system.\n"
                        conn.sendall(success_message.encode('utf-8'))
                        logging.info(f"Client {addr} is leaving the system.")
                        break 
                    else:
                        error_message = "[ERROR] Invalid choice.\n"
                        conn.sendall(error_message.encode('utf-8'))
                        logging.warning(f"Client {addr} made an invalid choice.")
                else:
                    # 經營者已登入，提供功能選項
                    message = (
                        "[CHOICE] Choose an action:\n"
                        "1. Write Article\n"
                        "2. Edit Article\n"
                        "3. Delete Article\n"
                        "4. Leave\n"
                    )
                    conn.sendall(message.encode('utf-8'))
                    action_choice = conn.recv(1024).decode('utf-8').strip()

                    if action_choice == "1":
                        action = WriteArticle()
                        action.exec(conn, operator_id)
                    elif action_choice == "2":
                        action = EditArticle()
                        action.exec(conn, operator_id)
                    elif action_choice == "3":
                        action = DeleteArticle()
                        action.exec(conn, operator_id)
                    elif action_choice == "4":
                        success_message = "[SUCCESS] Leaving the system.\n"
                        conn.sendall(success_message.encode('utf-8'))
                        logging.info(f"Client {addr} is leaving the system.")
                        break  # 離開系統
                    else:
                        error_message = "[ERROR] Invalid choice.\n"
                        conn.sendall(error_message.encode('utf-8'))
                        logging.warning(f"Client {addr} made an invalid choice.")

        elif role_choice == "3":
            success_message = "[SUCCESS] Leaving the system.\n"
            conn.sendall(success_message.encode('utf-8'))
            logging.info(f"Client {addr} is leaving the system.")
            return  

        else:
            error_message = "[ERROR] Invalid choice.\n"
            conn.sendall(error_message.encode('utf-8'))
            logging.warning(f"Client {addr} made an invalid choice.")

    except Exception as e:
        logging.error(f"Error handling client {addr}: {e}")
        try:
            error_message = f"[ERROR] {e}\n"
            conn.sendall(error_message.encode('utf-8'))
        except:
            pass
    finally:
        conn.close()
        logging.info(f"Connection with {addr} closed.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))  
    server.listen(5)
    logging.info("Server started. Waiting for connections...")

    while True:
        conn, addr = server.accept()
        logging.info(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
