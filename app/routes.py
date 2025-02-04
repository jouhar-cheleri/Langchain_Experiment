import os
from flask import Blueprint, render_template, request
from agent.serpapi_news_tool import SerpAPINewsTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

main = Blueprint('main', __name__)

# Initialize the LLM and tools
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ.get("Gemini_Api_Key")
)

serpapi_news = SerpAPINewsTool()
tools = [serpapi_news]
model_with_tools = llm.bind_tools(tools)
agent_executor = create_react_agent(model_with_tools, tools)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        response = agent_executor.invoke({
            "messages": [
                HumanMessage(content=query)
            ]
        })
        results = response["messages"]
        
        # Parse the ToolMessage content
        news_results = []
        for message in results:
            if message.name == 'serpapi_news_search':
                content = message.content
                articles = content.split('\n\n')
                for article in articles:
                    lines = article.split('\n')
                    if len(lines) >= 3:
                        title = lines[0].replace('Title: ', '')
                        link = lines[1].replace('Link: ', '')
                        snippet = lines[2].replace('Snippet: ', '')
                        news_results.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet
                        })
        
        return render_template('index.html', results=news_results, enumerate=enumerate)
    return render_template('index.html', results=None, enumerate=enumerate)