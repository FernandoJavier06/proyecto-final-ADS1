from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Registro de Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app