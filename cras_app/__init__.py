# cras_app/__init__.py

from flask import Flask
from config import Config
from cras_app.extensions import db, migrate, login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões com o aplicativo
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'
    login.login_message = "Por favor, faça login para acessar esta página."
    login.login_message_category = "is-info"

    # Registrar blueprints
    from cras_app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
