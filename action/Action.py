class Action():    
    def __init__(self, action_name):
        self.action_name = action_name  # 初始化 action 類別，並設定此 action 的名稱，例如 "SignUp"
    
    def exec(self, conn, **kwargs): # 執行某個 action 
        raise NotImplementedError("This method should be overridden in subclasses")
    
    def get_name(self): # 取得當前 Action 物件的 action_name，用來識別這個動作是什麼操作
        return self.action_name
    
    def read_input(self, conn, show_str): # 用來向客戶端發送提示訊息，並接收客戶端的輸入
        # show_str 會顯示在提示訊息中，告訴用戶需要輸入什麼資訊（如「Please enter user name」）。
        ret = conn.send(f'[INPUT]Please enter {show_str}: '.encode('utf-8'))
        recv_msg = conn.recv(100).decode("utf-8")
        return recv_msg
    
    def send_table(self, conn, table):
        # 將表格切割成每行數據並拼接成一個完整的字符串
        table_data = table + "\n" + "[END]\n"  # 在表格後附加結束標記
        conn.sendall(table_data.encode('utf-8'))  # 一次性發送整個表格


