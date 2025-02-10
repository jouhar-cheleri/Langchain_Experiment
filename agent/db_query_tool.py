import sqlite3
from typing import Optional, List
from langchain_core.tools import BaseTool
from pydantic import PrivateAttr
from models.news_database import NewsDatabase

class DBQueryTool(BaseTool):
    name: str = "db_query"
    description: str = """
    Useful for querying news articles from database. Can execute these types of queries:
        1. Get all articles: "SELECT * FROM News"
        2. Filter articles: "SELECT * FROM News WHERE ..."
        3. Order articles: "SELECT * FROM News ORDER BY ..."
        4. Limit results: "SELECT * FROM News LIMIT ..."
        5. Select specific columns: "SELECT SLNO, TITLE, LINK, CONTENT, SNIPPET FROM NEWS"

        The News table has columns: SLNO, TITLE, LINK, CONTENT, SNIPPET.
        Only SELECT queries are allowed for safety.. 
    """
    _db: NewsDatabase = PrivateAttr()
    _allowed_patterns: List[str] = [
        "SELECT",  # Allow any SELECT query start
        "SELECT *",
        "SELECT SLNO",
        "SELECT TITLE",
        "SELECT LINK",
        "SELECT CONTENT",
        "SELECT SNIPPET"
    ]

    def __init__(self, db: Optional[NewsDatabase] = None):
        super().__init__()
        self._db = db if db else NewsDatabase()

    def _is_safe_query(self, query: str) -> bool:
            query = query.strip().upper()
            print(f"Checking query: {query}")  # Debug print
            
            # Basic safety checks
            unsafe_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
            if any(keyword in query.upper() for keyword in unsafe_keywords):
                return False
                
            # Check if it's a SELECT query starting with allowed patterns
            is_safe = any(query.startswith(pattern.upper()) for pattern in self._allowed_patterns)
            
            # Additional validation - must contain "FROM NEWS"
            if "FROM NEWS" not in query.upper():
                is_safe = False
                
            print(f"Query is safe: {is_safe}")  # Debug print
            return is_safe
    def _run(self, query: str) -> str:
        try:
            if not self._is_safe_query(query):
                return "Invalid or unsafe query pattern detected"

            with sqlite3.connect(self._db.db_name) as conn:
                cursor = conn.cursor()
                results = cursor.execute(query).fetchall()
                
                if not results:
                    return "No results found"
                return results

        except Exception as e:
            return f"Error executing query: {str(e)}"

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async version not implemented")