from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set API keys as app config
app.config['LANGSMITH_TRACING'] = os.getenv('LANGSMITH_TRACING')
app.config['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
app.config['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
app.config['GOOGLE_API_KEY'] = os.getenv('Gemini_Api_Key')
app.config['SERPAPI_KEY'] = os.getenv('serp_api_key')

# Import routes after app initialization to avoid circular imports
from app import routes