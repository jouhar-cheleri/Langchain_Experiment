from typing import Optional
from langchain_core.tools import BaseTool
from newspaper import Article
import sqlite3
from pydantic import PrivateAttr
from models.news_database import NewsDatabase

class ArticleExtractorTool(BaseTool):
    name: str = "article_extractor"
    description: str = """
    Useful for extracting the complete content of a news article from its URL.
    Input should be a URL/link to a news article.
    Returns the full text content of the article from database if exists, otherwise scrapes from web.
    Use this when user asks for full article or complete content of a news item.
    or when you want to extract the full content of a news article for comparing with another article content etc.
    
    """
    _db: NewsDatabase = PrivateAttr()

    def __init__(self, db: Optional[NewsDatabase] = None):
        super().__init__()
        self._db = db if db else NewsDatabase()

    def _check_existing_content(self, url: str) -> Optional[str]:
        try:
            with sqlite3.connect(self._db.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT content FROM News WHERE Link = ? AND content IS NOT NULL", (url,))
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error checking existing content: {e}")
            return None

    def _run(self, url: str) -> str:
        try:
            # First check if content exists in database
            existing_content = self._check_existing_content(url)
            if existing_content:
                print(f"Found existing content for URL: {url}")
                return existing_content

            print(f"No existing content found, scraping URL: {url}")
            # If not in database, scrape from web
            article = Article(url)
            article.download()
            article.parse()
            content = article.text

            if content:
                # Store new content in database
                with sqlite3.connect(self._db.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE News SET content = ? WHERE Link = ?", (content, url))
                    conn.commit()
                return content
            return "Could not extract article content."

        except Exception as e:
            return f"Error extracting article content: {str(e)}"

    def _arun(self, url: str) -> str:
        raise NotImplementedError("Async version not implemented")