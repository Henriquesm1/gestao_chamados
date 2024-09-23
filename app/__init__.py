from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User  
    login_manager.login_view = 'usuarios.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.chamados import chamados_bp
    from .routes.categorias import categorias_bp
    from .routes.dashboard import dashboard_bp
    from .routes.servicos import servicos_bp
    from .routes.clientes import clientes_bp
    from .routes.usuarios import usuarios_bp

    app.register_blueprint(chamados_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(servicos_bp)
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app
