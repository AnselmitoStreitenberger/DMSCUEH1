"""Factory de aplicación Flask."""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config
from app.db import db
from app.routes import register_routes

import os


def create_app(config_class=Config):
    """Crear y configurar la aplicación."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)

    from app.models import models  # Registrar modelos
    register_routes(app)

    origins = os.getenv("FRONTEND_ORIGIN", "*").split(',')
    CORS(app, origins=origins)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app