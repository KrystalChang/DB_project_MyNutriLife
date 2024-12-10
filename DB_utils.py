# DB_utils.py
import psycopg2
from psycopg2 import sql
from datetime import datetime
import sqlite3
import bcrypt

# -----------------------------資料庫連線---------------------------------
DB_CONFIG = {
    'dbname': 'MyNutriLife',
    'user': 'postgres',
    'password': 'ideas',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    """取得資料庫連線"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


# -------------------------------User 相關功能---------------------------------
#=======================================================================


# User Sign Up 功能會用到的函數


#=======================================================================
def username_exist(username):
    """檢查使用者名稱是否已存在於資料庫"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE u_name = %s", (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


# User 註冊時會用到的函數：輸入生日後會自動計算年齡
def calculate_age(birth_date):
    """根據生日計算年齡"""
    today = datetime.today()
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# User 註冊功能
def db_register_user(username, password, email, birth_date, gender):
    """註冊新使用者並插入資料庫，根據性別與計算出的年齡自動產生 T_id"""
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # 計算年齡
    age = calculate_age(birth_date)

    # 根據性別與年齡查詢對應的 T_id
    cursor.execute("""
        SELECT t_id FROM user_type
        WHERE gender = %s AND %s BETWEEN min_age AND max_age
    """, (gender, age))

    t_id = cursor.fetchone()

    if t_id is None:
        raise ValueError("No matching user type found for the given gender and age.")

    t_id = t_id[0]  # 取得查詢結果中的 t_id

    # 插入新使用者資料到 users 資料表
    cursor.execute("""
        INSERT INTO users (u_name, password, email, birth_date, created_date, t_id)
        VALUES (%s, %s, %s, %s, CURRENT_DATE, %s)
        RETURNING u_id
    """, (username, password, email, birth_date, t_id))

    conn.commit()
    user_id = cursor.fetchone()[0]  # 取得剛新增的使用者 ID

    cursor.close()
    conn.close()
    return user_id
#=======================================================================


# User log in 功能會用到的函數


#=======================================================================
def db_get_user_id(u_name, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查詢資料庫中儲存的加密密碼
        cursor.execute('''
            SELECT u_id, password FROM users WHERE u_name = %s
        ''', (u_name,))
        
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if result:
            stored_u_id, stored_password = result
            # 驗證輸入的密碼與資料庫中的密碼是否匹配
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return stored_u_id  # 密碼正確，返回用戶 ID
            else:
                return None  # 密碼錯誤
        else:
            return None  # 用戶名不存在

    except Exception as e:
        raise Exception(f"Failed to retrieve user ID: {e}")


#=======================================================================


# User 記錄每日飲食 功能會用到的函數
# U_id F_id date time eaten_grams


#=======================================================================
def user_record_meal(u_id, f_id, date, time, eaten_grams):
    """
    記錄用戶每日飲食到資料庫的 Meal 表。
    
    Args:
        u_id (int): 用戶 ID。
        f_id (int): 食物 ID。
        date (str): 日期，格式為 YYYY-MM-DD。
        time (str): 時間，格式為 HH:MM。
        eaten_grams (int): 食用的克數。
        
    Returns:
        dict: 包含執行結果的字典。
              {"status": "success", "message": "Meal recorded successfully."}
              或
              {"status": "error", "message": "Error details."}
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 驗證輸入格式
        datetime.strptime(date, '%Y-%m-%d')  # 驗證日期格式
        datetime.strptime(time, '%H:%M')  # 驗證時間格式
        eaten_grams = int(eaten_grams)  # 確保克數是整數

        # 插入數據到資料庫
        cursor.execute('''
            INSERT INTO Meal (U_id, F_id, date, time, eaten_grams)
            VALUES (%s, %s, %s, %s, %s)
        ''', (u_id, f_id, date, time, eaten_grams))
        
        conn.commit()
        cursor.close()

        return {"status": "success", "message": "Meal recorded successfully."}

    except Exception as e:
        return {"status": "error", "message": f"Failed to record meal: {e}"}

def db_get_food_id_by_name(food_name):
    """
    根據食物名稱查詢對應的 Food ID (F_id)。
    
    Args:
        food_name (str): 食物名稱。
    
    Returns:
        int 或 None: 若找到對應 F_id，返回其值；否則返回 None。
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查詢資料庫
        cursor.execute('SELECT F_id FROM Food WHERE F_name = %s', (food_name,))
        result = cursor.fetchone()  # 獲取查詢結果

        cursor.close()
        return result[0] if result else None

    except Exception as e:
        raise Exception(f"Failed to fetch food ID: {e}")

#=======================================================================


#分析並顯示每日營養素攝取情況，並生成折線圖（可選）。


#=======================================================================
def db_get_nutrient_id_by_name(nutrient_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT N_id FROM Nutrient WHERE N_name = %s"
    cursor.execute(query, (nutrient_name,))
    result = cursor.fetchone()
    return result[0] if result else None


def db_get_daily_nutrient_records(user_id, nutrient_id, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT date, N_consumed_amount, csr
    FROM Daily_N_Consumed
    WHERE U_id = %s AND N_id = %s AND date BETWEEN %s AND %s
    ORDER BY date;
    """
    cursor.execute(query, (user_id, nutrient_id, start_date, end_date))
    return cursor.fetchall()

#=======================================================================


#使用者搜尋食物相關營養素 Search Nutrient of Food


#=======================================================================
# 查詢符合食物名稱的模糊比對結果
def db_search_food_by_name_partial(f_name_partial):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 将通配符直接拼接到字符串中
    f_name_partial = f"%{f_name_partial}%"
    query = """
    SELECT F_id, F_name 
    FROM Food
    WHERE F_name LIKE %s
    """
    cursor.execute(query, (f_name_partial,))  # 参数化查询
    results = cursor.fetchall()
    conn.close()
    return results

# 查詢某個食物所含的營養素及其含量
def db_get_nutrients_of_food(f_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT N.N_name, FCN.N_amount_in_100g_F, N.N_unit
    FROM Food_Contain_Nutrient FCN
    JOIN Nutrient N ON FCN.N_id = N.N_id
    WHERE FCN.F_id = %s
    """
    cursor.execute(query, (f_id,))
    results = cursor.fetchall()
    conn.close()
    return results

#=======================================================================


#使用者搜尋自身飲食紀錄 View Meal History
#使用者刪除自身飲食紀錄 Delete Meal


#=======================================================================
def db_get_meal_records_by_date_range(u_id, start_date, end_date):
    """
    Fetch meal records for a user within a specific date range.
    :param u_id: User ID
    :param start_date: Start date (YYYY-MM-DD)
    :param end_date: End date (YYYY-MM-DD)
    :return: List of records with F_id, F_name, eaten_grams, date, and time
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            m.F_id, f.F_name, m.eaten_grams, m.date, m.time 
        FROM 
            Meal m 
        JOIN 
            Food f 
        ON 
            m.F_id = f.F_id 
        WHERE 
            m.U_id = %s AND m.date BETWEEN %s AND %s
        ORDER BY 
            m.date, m.time;
    """
    cursor.execute(query, (u_id, start_date, end_date))
    records = cursor.fetchall()
    conn.close()
    return records


def db_delete_meal_record(u_id, f_id, date, time):
    """
    Delete a meal record by its composite primary key.
    :param u_id: User ID
    :param f_id: Food ID
    :param date: Date of the meal
    :param time: Time of the meal
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        DELETE FROM Meal 
        WHERE U_id = %s AND F_id = %s AND date = %s AND time = %s
    """
    cursor.execute(query, (u_id, f_id, date, time))
    conn.commit()
    conn.close()
#=======================================================================


#使用者瀏覽文章 Browse Articles，選擇是否將文章設為最愛


#=======================================================================
def db_add_to_favorite(a_id, u_id):
    saved_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Favorite (A_id, U_id, saved_date) VALUES (%s, %s, %s)", (a_id, u_id, saved_date))
    conn.commit()
    conn.close()
#=======================================================================


#使用者瀏覽最愛文章 Browse Favorite Articles ，可以選擇移除


#=======================================================================
def db_get_favorite_articles(u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.A_id, a.title, f.saved_date
        FROM Favorite f
        JOIN Article a ON f.A_id = a.A_id
        WHERE f.U_id = %s
    """, (u_id,))
    favorite_articles = cursor.fetchall()

    conn.close()
    return favorite_articles


def db_remove_favorite(a_id, u_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Favorite WHERE A_id = %s AND U_id = %s", (a_id, u_id))
    conn.commit()
    conn.close()
#======================================================================= 

# -------------------------------Operator 相關功能---------------------------------
# 管理者註冊功能
def db_register_operator(operator_name, password, email):
    """註冊新經營者並插入資料庫"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO operator (o_name, password, email, created_date)
        VALUES (%s, %s, %s, CURRENT_DATE)
        RETURNING o_id
    """, (operator_name, password, email))
    conn.commit()
    operator_id = cursor.fetchone()[0]  # 取得剛新增的經營者 ID
    cursor.close()
    conn.close()
    return operator_id


# 檢查經營者的 email 是否已經存在
def email_exist(email, table):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM {table} WHERE email = %s", (email,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

# 管理者 log in 功能會用到的函數：驗證名稱跟密碼
def validate_operator(email, password):
    """檢查經營者的登入信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM operator WHERE email = %s AND password = %s
    """, (email, password))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # 如果找到匹配的結果，返回 True，否則返回 False
    return result is not None


# Operator 寫文章的功能：將文章寫入資料庫並返回文章ID
from datetime import date  # 引入 date 模組

def db_write_article(title, content, operator_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 生成文章代號和當前日期
        article_id = generate_article_id(cursor)
        published_date = date.today()

        # 插入文章資料，預設 status 為 "Published"
        cursor.execute('''
            INSERT INTO Article (A_id, title, content, published_date, status, author_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (article_id, title, content, published_date, "Published", operator_id))

        conn.commit()
        cursor.close()
        conn.close()

        return article_id
    except Exception as e:
        raise Exception(f"Failed to write article: {e}")


# Operator 寫文章所需要的函數：生成唯一的文章代號
def generate_article_id(cursor):
    cursor.execute('SELECT MAX(A_id) FROM Article')
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id else 1

# 根據 email 和 password 查找 operator_id（寫文章時會用到）
def db_get_operator_id(email, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查詢資料庫中儲存的加密密碼
        cursor.execute('''
            SELECT O_id, password FROM operator WHERE email = %s
        ''', (email,))

        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if result:
            stored_o_id, stored_password = result
            # 驗證輸入的密碼與資料庫中的密碼是否匹配
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return stored_o_id  # 密碼正確，返回operator ID
            else:
                return None  # 密碼錯誤
        else:
            return None  # 用戶名不存在
    except Exception as e:
        raise Exception(f"Failed to retrieve operator ID: {e}")

# Operator修改文章用的函數：從資料庫中取出所有「published」的文章 ID 和標題
def db_get_all_articles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 過濾出狀態為 "Published" 的文章
        cursor.execute("SELECT A_id, title FROM Article WHERE status = 'Published' ORDER BY A_id ASC")
        articles = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return articles
    except Exception as e:
        raise Exception(f"Error fetching articles: {e}")


# Fetch a specific article by its ID
def db_get_article_by_id(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT title, content FROM Article WHERE A_id = %s", (article_id,))
        article = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return article
    except Exception as e:
        raise Exception(f"Error fetching article by ID: {e}")

# Update an article in the database
def db_update_article(article_id, new_title, new_content):
    """
    更新文章內容，實現交易管理與併行控制
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 啟動交易
        conn.autocommit = False  # 禁用自動提交，手動管理交易

        # 嘗試鎖定目標文章
        cursor.execute("""
            SELECT A_id 
            FROM Article 
            WHERE A_id = %s 
            FOR UPDATE NOWAIT
        """, (article_id,))
        locked_article = cursor.fetchone()

        if not locked_article:
            raise Exception(f"Article with ID {article_id} does not exist.")

        # 執行更新操作
        cursor.execute("""
            UPDATE Article
            SET title = %s, content = %s
            WHERE A_id = %s
        """, (new_title, new_content, article_id))

        # 提交交易
        conn.commit()
        print(f"Article {article_id} updated successfully.")
    except psycopg2.OperationalError as e:
        conn.rollback()  # 回滾交易
        raise Exception(f"Article is locked by another user: {e}")
    except Exception as e:
        conn.rollback()  # 回滾交易
        raise Exception(f"Error updating article: {e}")
    finally:
        cursor.close()
        conn.close()



def db_delete_article(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 更新文章的 status 為 "Deleted"
        cursor.execute("""
            UPDATE Article
            SET status = %s
            WHERE A_id = %s
        """, ("Deleted", article_id))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Error deleting article: {e}")
