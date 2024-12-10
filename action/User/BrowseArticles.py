from action.Action import Action
from DB_utils import db_get_all_articles, db_get_article_by_id, db_add_to_favorite

class BrowseArticles(Action):
    def __init__(self):
        super().__init__("BrowseArticles")

    def exec(self, conn, operator_id):  # operator_id 是 user 的 ID
        # 步驟 1: 顯示所有文章的 A_id 和 title
        articles = db_get_all_articles()
        table = "Article ID | Title\n"
        for article in articles:
            table += f"{article[0]} | {article[1]}\n"
        
        self.send_table(conn, table)  # 發送文章列表給客戶端
        
        # 步驟 2: 讓用戶選擇要查看的文章 A_id
        article_id = self.read_input(conn, "the article ID you want to view")
        
        # 步驟 3: 根據 A_id 取得該文章的內容
        article_details = db_get_article_by_id(article_id)
        
        if article_details:
            title, content = article_details
            # 顯示文章內容
            conn.send(f"Title: {title}\nContent: {content}\n".encode('utf-8'))
            
            # 步驟 4: 詢問用戶是否要收藏該文章
            response = self.read_input(conn, "Do you want to add this article to your favorites? (yes/no)").lower()
            if response == 'yes':
                db_add_to_favorite(article_id, operator_id)  # 將文章加入收藏
                conn.send("[INFO] Article has been added to your favorites.\n".encode('utf-8'))
            else:
                conn.send("[INFO] Article not added to favorites.\n".encode('utf-8'))
        else:
            conn.send("[ERROR] Article not found.\n".encode('utf-8'))
