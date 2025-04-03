from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__,
                template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
                static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets')))
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # Import routes
        from .routes import auth, views
        
        # Register blueprints
        app.register_blueprint(auth.bp)
        app.register_blueprint(views.bp)
        
        # Create database tables
        db.create_all()
        
        return app
