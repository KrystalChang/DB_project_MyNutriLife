from DB_utils import db_write_article
from action.Action import Action

class WriteArticle(Action):  # 繼承 Action 類別
    def __init__(self):
        super().__init__("WriteArticle")  # 呼叫父類別的初始化方法

    def exec(self, conn, operator_id):
        """執行寫文章功能"""
        # 讓經營者輸入文章標題與內容
        title = self.read_input(conn, "Enter the article title:")
        content = self.read_input(conn, "Enter the article content:")

        # 呼叫 db_write_article 函數插入文章
        try:
            article_id = db_write_article(title, content, operator_id)
            conn.send(f"Article written successfully with ID {article_id}\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] Failed to write article: {e}\n".encode('utf-8'))
