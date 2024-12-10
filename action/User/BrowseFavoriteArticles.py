from action.Action import Action
from DB_utils import db_get_favorite_articles, db_get_article_by_id, db_remove_favorite

class BrowseFavoriteArticles(Action):
    def __init__(self):
        super().__init__("BrowseFavoriteArticles")

    def exec(self, conn, operator_id):  # operator_id 是 user 的 ID
        # 步驟 1: 顯示用戶的最愛文章（A_id, title, saved_date）
        favorite_articles = db_get_favorite_articles(operator_id)
        if not favorite_articles:
            conn.send("[INFO] You have no favorite articles.\n".encode('utf-8'))
            return
        
        table = "Article ID | Title | Saved Date\n"
        for article in favorite_articles:
            table += f"{article[0]} | {article[1]} | {article[2]}\n"
        
        self.send_table(conn, table)  # 發送最愛文章列表給客戶端
        
        # 步驟 2: 讓用戶選擇操作（查看文章或移除最愛）
        action = self.read_input(conn, "Do you want to view an article or remove an article from your favorites? (view/remove)").lower()

        if action == "view":
            # 步驟 3: 用戶選擇查看文章
            article_id = self.read_input(conn, "Enter the article ID you want to view")
            article_details = db_get_article_by_id(article_id)
            
            if article_details:
                title, content = article_details
                conn.send(f"Title: {title}\nContent: {content}\n".encode('utf-8'))
            else:
                conn.send("[ERROR] Article not found.\n".encode('utf-8'))
        
        elif action == "remove":
            # 步驟 4: 用戶選擇移除最愛文章
            article_id = self.read_input(conn, "Enter the article ID you want to remove from favorites")
            db_remove_favorite(article_id, operator_id)  # 從最愛中刪除
            conn.send(f"Article {article_id} has been removed from your favorites.\n".encode('utf-8'))
        
        else:
            conn.send("[ERROR] Invalid action. Please type 'view' or 'remove'.\n".encode('utf-8'))
