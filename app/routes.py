import os
from flask import Blueprint, render_template, request
from agent.serpapi_news_tool import SerpAPINewsTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from flask import session, request, render_template
from agent.db_query_tool import DBQueryTool

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
db_query = DBQueryTool(db=serpapi_news._db)
tools = [serpapi_news,db_query]
model_with_tools = llm.bind_tools(tools)
agent_executor = create_react_agent(model_with_tools, tools)

@main.route('/', methods=['GET', 'POST'])
def index():
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if request.method == 'POST':
        query = request.form.get('query')
        
        # Add user message to history
        session['chat_history'].append({
            'role': 'user',
            'content': query
        })
        
        # Get LLM response
        response = agent_executor.invoke({
            "messages": [
                HumanMessage(content=query)
            ]
        })
        
        # Get LLM output and add to history
        try:
            messages = response["messages"]
            llm_response = messages[-1].content  # Get last message content
            
            session['chat_history'].append({
                'role': 'assistant',
                'content': llm_response
            })
        except Exception as e:
            session['chat_history'].append({
                'role': 'assistant',
                'content': f"Error processing response: {str(e)}"
            })
                
        return render_template('index.html', messages=session['chat_history'])
    
    return render_template('index.html', messages=session.get('chat_history', []))

@main.teardown_app_request
def cleanup_database(exception=None):
    serpapi_news._db.clear_database()