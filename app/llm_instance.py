from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from app.serpapi_tool import SerpAPINewsTool
from langchain_community.tools.tavily_search import TavilySearchResults

# Creating LLM instance
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Adding tools
search = TavilySearchResults(max_results=2)
serpapi_news = SerpAPINewsTool()
tools = [search, serpapi_news]

model_with_tools = llm.bind_tools(tools)
agent_executor = create_react_agent(model_with_tools, tools)