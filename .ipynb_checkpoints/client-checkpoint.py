# client.py
import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))

    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            print(data, end="")  # 顯示伺服器訊息

            if "[CHOICE]" in data:
                user_input = input()
                client.send(user_input.encode('utf-8'))

            elif "[SUCCESS]" in data or "[ERROR]" in data:
                print(data)
                if "[SUCCESS]" in data:  # 若成功離開系統則結束
                    break
            elif "[INPUT]" in data:
                user_input = input()  # 等待用戶輸入訊息
                client.send(user_input.encode('utf-8'))
            elif "[TABLE]" in data:  # 處理表格訊息
                table_data = []
                while True:
                    data = client.recv(2048).decode('utf-8')
                    if "[END]" in data:  # 如果檢測到結束標記
                        data = data.replace("[END]", "")  # 去掉結束標記
                        if data.strip():  # 檢查是否有剩餘數據
                            table_data.append(data)
                        break
                    table_data.append(data)  # 拼接收到的數據

                print("".join(table_data))  # 打印完整表格

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    print("Connecting to server...")
    start_client()
