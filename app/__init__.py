from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
mail = Mail()

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Configurar login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    
    # Registrar blueprints
    from app.routes import auth, gastos, ahorros, planes, pendientes, configuracion, reportes
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(gastos.bp)
    app.register_blueprint(ahorros.bp)
    app.register_blueprint(planes.bp)
    app.register_blueprint(pendientes.bp)
    app.register_blueprint(configuracion.bp)
    app.register_blueprint(reportes.bp)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    return app
