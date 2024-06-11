from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @property
    def articles(self):
        from models.article import Article  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles_data = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in articles_data]

    @property
    def contributors(self):
        from models.author import Author  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors_data]

    @property
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles_data = cursor.fetchall()
        conn.close()
        return [title["title"] for title in titles_data]

    @property
    def contributing_authors(self):
        from models.author import Author  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors_data = cursor.fetchall()
        conn.close()
        return [Author(author["id"], author["name"]) for author in authors_data] if authors_data else []

    def __repr__(self):
        return f'<Magazine {self.name}>'
