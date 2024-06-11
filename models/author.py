from database.connection import get_db_connection
from models.magazine import Magazine  # Import Magazine here

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def articles(self):
        from models.article import Article  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles_data]

    @property
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines_data = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines_data]

    def __repr__(self):
        return f'<Author {self.name}>'