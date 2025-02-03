from flask import request, jsonify, render_template
from app import app
from app.serpapi_tool import SerpAPINewsTool
from app.news_database import NewsDatabase
from app.llm_instance import llm, agent_executor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query = data.get('query')
    response = agent_executor.invoke({
        "messages": [
            {"content": query}
        ]
    })
    return jsonify(response["messages"])

if __name__ == '__main__':
    app.run(debug=True)