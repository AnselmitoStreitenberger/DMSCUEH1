from flask import Flask
from app.db import db
from flask_migrate import Migrate
from app.config import Config
from app.routes import register_routes  # ✅ Importar la función que registra las rutas

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    from app.models import models  # importa los modelos aquí
    register_routes(app)           # ✅ Registrar todos los blueprints

    return app