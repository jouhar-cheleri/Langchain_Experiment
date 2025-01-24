from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from app.agent.agent import create_agent
from langchain_core.messages import HumanMessage
import os

load_dotenv()

app = Flask(__name__)
agent_executor = create_agent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('query')
    response = agent_executor.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    return jsonify({"response": response["messages"][-1].content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))