import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection
from database.setup import create_tables

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_tables()

    def setUp(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Set up test data
        self.cursor.execute('INSERT INTO authors (name) VALUES (?)', ("John Doe",))
        self.author_id = self.cursor.lastrowid
        self.cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', ("Tech Weekly", "Technology"))
        self.magazine_id = self.cursor.lastrowid
        self.cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                            ("Test Title", "Test Content", self.author_id, self.magazine_id))
        self.conn.commit()

    def tearDown(self):
        self.cursor.execute('DELETE FROM articles')
        self.cursor.execute('DELETE FROM magazines')
        self.cursor.execute('DELETE FROM authors')
        self.conn.commit()
        self.conn.close()

    def test_author_creation(self):
        author = Author(self.author_id, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", self.author_id, self.magazine_id)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_articles(self):
        author = Author(self.author_id, "John Doe")
        articles = author.articles
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test Title")

    def test_author_magazines(self):
        author = Author(self.author_id, "John Doe")
        magazines = author.magazines
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].name, "Tech Weekly")

    def test_magazine_articles(self):
        magazine = Magazine(self.magazine_id, "Tech Weekly", "Technology")
        articles = magazine.articles
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test Title")

    def test_magazine_contributors(self):
        magazine = Magazine(self.magazine_id, "Tech Weekly", "Technology")
        contributors = magazine.contributors
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].name, "John Doe")

    def test_magazine_article_titles(self):
        magazine = Magazine(self.magazine_id, "Tech Weekly", "Technology")
        article_titles = magazine.article_titles
        self.assertEqual(len(article_titles), 1)
        self.assertEqual(article_titles[0], "Test Title")

    def test_magazine_contributing_authors(self):
        # Create more articles to test contributing authors
        self.cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                            ('Another Title', 'Content', self.author_id, self.magazine_id))
        self.cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                            ('Yet Another Title', 'Content', self.author_id, self.magazine_id))
        self.conn.commit()

        magazine = Magazine(self.magazine_id, "Tech Weekly", "Technology")
        contributing_authors = magazine.contributing_authors
        self.assertEqual(len(contributing_authors), 1)

if __name__ == "__main__":
    unittest.main()
