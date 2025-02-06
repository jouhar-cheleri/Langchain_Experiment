import sqlite3
from typing import Optional, List
from langchain_core.tools import BaseTool
from pydantic import PrivateAttr
from models.news_database import NewsDatabase

class DBQueryTool(BaseTool):
    name: str = "db_query"
    description: str = """
    Useful for querying news articles from database. user request has to be converted ton
    mysql query format. For example, to get all news articles, the user may say get
    all news articles. The tool will convert this to a mysql query format like
    "SELECT * FROM News". The tool will execute the query and return the results.
    only one table is there in DB which is News table. 
    """
    _db: NewsDatabase = PrivateAttr()
    _allowed_patterns: List[str] = [
        "SELECT * FROM News",
        "SELECT * FROM News WHERE",
        "SELECT * FROM News ORDER BY",
        "SELECT * FROM News LIMIT"
    ]

    def __init__(self, db: Optional[NewsDatabase] = None):
        super().__init__()
        self._db = db if db else NewsDatabase()

    def _is_safe_query(self, query: str) -> bool:
        query = query.strip().upper()
        return any(query.startswith(pattern) for pattern in self._allowed_patterns)

    def _run(self, query: str) -> str:
        try:
            if not self._is_safe_query(query):
                return "Invalid or unsafe query pattern detected"

            with sqlite3.connect(self._db.db_name) as conn:
                cursor = conn.cursor()
                results = cursor.execute(query).fetchall()
                
                if not results:
                    return "No results found"

                formatted_results = []
                for row in results:
                    formatted_results.append(
                        f"ID: {row[0]}\n"
                        f"Title: {row[1]}\n"
                        f"Link: {row[2]}\n"
                        f"Snippet: {row[3]}\n"
                    )
                return "\n---\n".join(formatted_results)

        except Exception as e:
            return f"Error executing query: {str(e)}"

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async version not implemented")