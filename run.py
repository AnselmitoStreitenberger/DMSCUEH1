import os

from app import create_app
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

config_mapping = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

config_name = os.getenv('FLASK_CONFIG', 'development')
config_class = config_mapping.get(config_name, DevelopmentConfig)

app = create_app(config_class)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
