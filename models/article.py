from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @property
    def author(self):
        from models.author import Author  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author_data = cursor.fetchone()
        conn.close()
        return Author(author_data["id"], author_data["name"]) if author_data else None

    @property
    def magazine(self):
        from models.magazine import Magazine  # Import here to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine_data = cursor.fetchone()
        conn.close()
        return Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"]) if magazine_data else None

    def __repr__(self):
        return f'<Article {self.title}>'

