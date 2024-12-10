# NutrientAnalysis.py

from action.Action import Action  
from DB_utils import db_get_nutrient_id_by_name, db_get_daily_nutrient_records
import matplotlib.pyplot as plt
import pandas as pd
import io

import platform
import os

class NutrientAnalysis(Action):
    def __init__(self):
        super().__init__("NutrientAnalysis")  

    def exec(self, conn, user_id):  
        try:
            # Step 1: 提示用戶輸入查詢範圍
            start_date = self.read_input(conn, "the start date (YYYY-MM-DD)")
            end_date = self.read_input(conn, "the end date (YYYY-MM-DD)")

            # Step 2: 提示用戶輸入想查詢的營養素名稱
            nutrient_name = self.read_input(conn, "the nutrient name (請輸入「熱量」或「總碳水化合物」或「膳食纖維」)")
            nutrient_id = db_get_nutrient_id_by_name(nutrient_name) 

            if not nutrient_id:
                conn.send(f"[ERROR] Nutrient '{nutrient_name}' not found.\n".encode('utf-8'))
                return
            
            # Step 3: 查詢用戶每日的營養素攝取數據
            records = db_get_daily_nutrient_records(user_id, nutrient_id, start_date, end_date)
            
            if not records:
                conn.send("[INFO] No records found for the specified period.\n".encode('utf-8'))
                return

            # Step 4: 將數據格式化並發送給用戶
            df = pd.DataFrame(records, columns=["Date", "N_Consumed_Amount", "CSR"])
            table = df.to_string(index=False)  
            conn.send(f"\n[INFO] Here are your nutrient records:\n{table}\n".encode('utf-8'))

            # Step 5: 詢問用戶是否生成折線圖
            generate_plot = self.read_input(conn, "if you want to generate a line plot (yes/no)").strip().lower()

            if generate_plot == "yes":
                # 生成圖表並獲取二進制數據
                image_data = self._generate_plot(df, nutrient_name, start_date, end_date)
                # 傳送圖片數據給客戶端
                conn.sendall("[IMAGE]".encode('utf-8'))  
                conn.sendall(f"{len(image_data)}".encode('utf-8'))
                conn.recv(1024)  
                conn.sendall(image_data)
                conn.send("[INFO] Line plot has been generated and sent to you.\n".encode('utf-8'))
            else:
                conn.send("[INFO] Line plot generation skipped.\n".encode('utf-8'))

        except Exception as e:
            conn.send(f"[ERROR] An error occurred: {str(e)}\n".encode('utf-8'))

    def _generate_plot(self, df, nutrient_name, start_date, end_date):
        """生成折線圖，處理缺失日期並顯示每日 CSR 值變化，支持中文字體。"""
        from matplotlib import rcParams

        # 設置中文字體
        # rcParams['font.sans-serif'] = ['Microsoft YaHei'] 
        # rcParams['axes.unicode_minus'] = False
        
        if platform.system() == "Windows":
            rcParams['font.sans-serif'] = ['SimHei']
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')  # Windows Desktop path
        elif platform.system() == "Darwin":
            rcParams['font.sans-serif'] = ['PingFang HK']
            desktop_path = os.path.join(os.environ['HOME'], 'Desktop')  # macOS Desktop path
        else:
            rcParams['font.sans-serif'] = ['Noto Sans CJK SC']
            desktop_path = os.path.join(os.environ['HOME'], 'Desktop')  # Linux Desktop path

        rcParams['axes.unicode_minus'] = False


        plt.switch_backend('Agg')

        # 生成完整日期範圍並處理數據
        date_range = pd.date_range(start=start_date, end=end_date)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df = df.reindex(date_range, fill_value=0).reset_index()
        df.columns = ['Date', 'N_Consumed_Amount', 'CSR']

        # 繪製圖表
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['CSR'], marker="o", label=f"CSR ({nutrient_name})")
        plt.axhline(y=1, color="r", linestyle="--", label="CSR = 1")
        plt.xlabel("日期")
        plt.ylabel("CSR 值")
        plt.title(f"{nutrient_name} 每日 CSR 趨勢圖")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image_data = buf.read()
        buf.close()

        return image_data


