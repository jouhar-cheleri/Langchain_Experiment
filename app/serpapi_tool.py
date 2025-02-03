from typing import Optional
from langchain_core.tools import BaseTool
from serpapi import GoogleSearch
import os
from app.news_database import NewsDatabase

class SerpAPINewsTool(BaseTool):
    name: str = "serpapi_news_search"
    description: str = ("Useful for searching recent news articles about a specific topic. "
                        "Input should be a search query string. "
                        "First determine whether user is seeking for news or not, if yes then search for news articles related to the query. "
                        "For example if user asks for news about covid-19, then pass covid-19 to tool, even user doesn't mention news directly in query.")

    def __init__(self):
        self.db = NewsDatabase()

    def _run(self, query: str) -> str:
        params = {
            "q": query,
            "api_key": os.environ["serpapi_key"],
            "tbm": "nws",
            "hl": "en",
            "gl": "In",
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            if "news_results" in results:
                formatted_results = []
                for article in results["news_results"][:10]:  # Limit to top 10 news results
                    title = article['title']
                    link = article.get('link', '')
                    snippet = article.get('snippet', '')

                    # Store in database
                    self.db.insert_news(title, link, snippet)

                    formatted_results.append(
                        f"Title: {title}\n"
                        f"Link: {link}\n"
                        f"Snippet: {snippet}\n"
                    )
                return formatted_results
            return "No news results found."

        except Exception as e:
            return f"Error performing news search: {str(e)}"

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async version not implemented")