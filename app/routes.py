import os
from flask import Blueprint, render_template, request
from agent.serpapi_news_tool import SerpAPINewsTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from flask import session
from agent.db_query_tool import DBQueryTool
from agent.article_extractor_tool import ArticleExtractorTool

main = Blueprint('main', __name__)

def cleanup_database():
    print("Cleaning up database on application shutdown...")
    serpapi_news._db.clear_database()
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
article_extractor = ArticleExtractorTool(db=serpapi_news._db)
tools = [serpapi_news,db_query,article_extractor]
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
        
        # Convert session history to LangChain message format
        messages = []
        for msg in session['chat_history']:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            else:
                messages.append(AIMessage(content=msg['content']))
        
        # Pass full conversation history to LLM
        response = agent_executor.invoke({
            "messages": messages  # Now passing full history instead of just current message
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

