import os

"""Configuraciones de la aplicación."""


class Config:
    """Configuración base."""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""

    DEBUG = True


class TestingConfig(Config):
    """Configuración para pruebas."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False

