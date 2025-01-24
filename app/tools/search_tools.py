from typing import Optional
from langchain_core.tools import BaseTool
from serpapi import GoogleSearch
from app.models.database import NewsDatabase

class SerpAPINewsTool(BaseTool):
    # Copy your existing SerpAPINewsTool class here
    # Initialize database in __init__
    def __init__(self):
        super().__init__()
        self.db = NewsDatabase()