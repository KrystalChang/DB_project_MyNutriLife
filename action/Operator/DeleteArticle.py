from action.Action import Action  # Make sure Action is properly imported
from DB_utils import db_delete_article, db_get_all_articles


class DeleteArticle(Action):
    def __init__(self):
        super().__init__("DeleteArticle")

    def exec(self, conn, operator_id):
        articles = db_get_all_articles()
        table = "Article ID | Title\n"
        for article in articles:
            table += f"{article[0]} | {article[1]}\n"

        self.send_table(conn, table)

        article_id = self.read_input(conn, "the article ID you want to delete")

        try:
            db_delete_article(article_id)
            conn.send("Article has been deleted (status set to 'Deleted').\n".encode('utf-8'))
        except Exception as e:
            conn.send(f"[ERROR] Failed to delete article: {e}\n".encode('utf-8'))
