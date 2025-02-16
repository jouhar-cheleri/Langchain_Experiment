import sqlite3
from typing import List, Tuple

class NewsDatabase:
    def __init__(self, db_name: str = "news.db"):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS News (
                    Slno INTEGER PRIMARY KEY AUTOINCREMENT,
                    Title TEXT NOT NULL,
                    Link TEXT NOT NULL,
                    Snippet TEXT,
                    content TEXT
                )
            ''')
            conn.commit()
    
    def insert_news(self, title: str, link: str, snippet: str) -> bool:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO News (Title, Link, Snippet) VALUES (?, ?, ?)",
                    (title, link, snippet)
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error inserting news: {e}")
            return False
    
    def get_all_news(self) -> List[Tuple]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM News")
            return cursor.fetchall()
    def clear_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM News")
            conn.commit()
    # def get_news_by_slno(self, slno: int) -> Tuple:
    #     with sqlite3.connect(self.db_name) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT * FROM News WHERE Slno = ?", (slno,))
    #         return cursor.fetchone()