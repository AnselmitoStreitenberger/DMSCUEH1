import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import TestingConfig
from app.db import db


def setup_app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    return app


def test_create_repuesto():
    app = setup_app()
    client = app.test_client()
    payload = {
        'codigo_pieza': 'ABC123',
        'descripcion': 'Tornillo',
        'precio': 1.5,
        'stock_min': 1,
        'stock_real': 5,
        'stock_disp': 5
    }
    response = client.post('/api/repuestos/', data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['codigo_pieza'] == 'ABC123'


def test_create_repuesto_validation_error():
    app = setup_app()
    client = app.test_client()
    payload = {'codigo_pieza': ''}
    response = client.post('/api/repuestos/', data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400
