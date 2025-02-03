from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Load environment variables
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("Gemini_Api_Key")
os.environ["serpapi_key"] = os.getenv("serp_api_key")

from app import main