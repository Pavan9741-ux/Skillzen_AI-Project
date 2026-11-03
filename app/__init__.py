"""SkillZen AI - Application Factory"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillzen.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    from app.routes import main_bp, auth_bp, student_bp, admin_bp, api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import Admin
    return Admin.query.get(int(user_id))