from action.Action import Action  # Make sure Action is properly imported
from DB_utils import db_update_article, db_get_all_articles, db_get_article_by_id

class EditArticle(Action):
    def __init__(self):
        super().__init__("EditArticle")

    def exec(self, conn, operator_id):
        # 顯示所有 Published 的文章
        articles = db_get_all_articles()
        table = "Article ID | Title\n"
        for article in articles:
            table += f"{article[0]} | {article[1]}\n"

        self.send_table(conn, table)

        # 輸入文章 ID
        article_id = self.read_input(conn, "the article ID you want to edit")

        # 確認文章是否存在且狀態為 Published
        article_details = db_get_article_by_id(article_id)

        if article_details:
            current_title, current_content = article_details

            conn.send(f"Current title: {current_title}\nCurrent content: {current_content}\n".encode('utf-8'))
            new_title = self.read_input(conn, "the new title for the article")
            new_content = self.read_input(conn, "the new content for the article")

            db_update_article(article_id, new_title, new_content)
            conn.send("Article has been updated.\n".encode('utf-8'))
        else:
            conn.send("[ERROR] Article not found or is not editable.\n".encode('utf-8'))
