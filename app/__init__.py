from flask import Flask
from .routes import main
import atexit

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Register the blueprint
    app.register_blueprint(main)
    
    # Register cleanup function to run at application shutdown
    from .routes import cleanup_database
    atexit.register(cleanup_database)
    
    return app