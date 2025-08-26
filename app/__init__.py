from flask import Flask
from config import Config
from .extensions import db, bcrypt, loginManager
from .models import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    
    #Funtion to load user from the session
    @loginManager.user_loader
    def loadUser(userId):
        return User.query.get(int(userId))
    
    #Blueprint registry
    from .auth import authBp
    app.register_blueprint(authBp)
    
    from .inventory import inventoryBp
    app.register_blueprint(inventoryBp, url_prefix='/inventory')
    
    from .main import mainBp
    app.register_blueprint(mainBp)
    
    return app