# client.py

import socket
import os
import uuid
import platform
import subprocess

def receive_all(sock, length):
    """
    接收指定長度的資料。
    """
    data = b''
    while len(data) < length:
        part = sock.recv(length - len(data))
        if not part:
            break
        data += part
    return data

def open_image(image_path):
    """
    根據操作系統自動打開圖片文件。
    """
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(['open', image_path])
    elif platform.system() == 'Windows':    # Windows
        os.startfile(image_path)
    else:                                   # Linux variants
        subprocess.call(['xdg-open', image_path])

def start_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            print("Connecting to server...")
            client.connect(("127.0.0.1", 12345))
            print("Connected to server.")

            while True:
                # 接收伺服器的消息
                data = client.recv(4096)
                if not data:
                    print("Disconnected from server.")
                    break
                try:
                    message = data.decode('utf-8')
                except UnicodeDecodeError as e:
                    print(f"Error decoding message: {e}")
                    break

                if message.startswith("[IMAGE]"):
                    image_size_data = client.recv(1024).decode('utf-8')
                    try:
                        image_size = int(image_size_data)
                    except ValueError:
                        print("[ERROR] Invalid image size received.")
                        continue
                    client.sendall(b"ACK")
                    image_data = receive_all(client, image_size)
                    if len(image_data) != image_size:
                        print("[ERROR] Incomplete image data received.")
                        continue
                    unique_id = uuid.uuid4().hex
                    image_filename = f"nutrient_analysis_plot_{unique_id}.png"
                    with open(image_filename, 'wb') as img_file:
                        img_file.write(image_data)
                    print(f"[INFO] Line plot has been saved as {image_filename}. Opening the image...")
                    open_image(image_filename)
                else:
                    print(message, end="")  
                    if "[CHOICE]" in message or "[INPUT]" in message:
                        user_input = input()
                        client.sendall(user_input.encode('utf-8'))

                    elif "[SUCCESS]" in message or "[ERROR]" in message:
                        if "[SUCCESS]" in message:
                            break

    except ConnectionRefusedError:
        print("Connection refused. Ensure that the server is running and accessible.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_client()
