from flask import Blueprint, request, jsonify
from app.models.models import Vehiculo
from app.db import db

vehiculos_bp = Blueprint('vehiculos', __name__, url_prefix='/api/vehiculos')

@vehiculos_bp.route('/', methods=['GET'])
def get_all():
    items = Vehiculo.query.all()
    return jsonify([{
        'nombre': getattr(i, 'nombre'), 'ano': getattr(i, 'ano'), 'codigo_manual': getattr(i, 'codigo_manual')
    } for i in items])

@vehiculos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Vehiculo.query.get_or_404(id)
    return jsonify({
        'nombre': getattr(i, 'nombre'), 'ano': getattr(i, 'ano'), 'codigo_manual': getattr(i, 'codigo_manual')
    })

@vehiculos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Vehiculo(
        nombre=data.get('nombre'), ano=data.get('ano'), codigo_manual=data.get('codigo_manual')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Vehiculo creado', 'id': getattr(i, 'id', None)}), 201

@vehiculos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Vehiculo.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Vehiculo eliminado'})
