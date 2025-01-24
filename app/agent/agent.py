from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from app.tools.search_tools import SerpAPINewsTool

def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
    
    search = TavilySearchResults(max_results=2)
    serpapi_news = SerpAPINewsTool()
    tools = [search, serpapi_news]
    
    model_with_tools = llm.bind_tools(tools)
    return create_react_agent(model_with_tools, tools)