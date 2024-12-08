from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        # Import routes
        from app.routes import main as main_blueprint
        app.register_blueprint(main_blueprint)
        
        # Create database tables
        db.create_all()
        
    return app
