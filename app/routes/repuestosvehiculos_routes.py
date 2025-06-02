from flask import Blueprint, request, jsonify
from app.models.models import RepuestoVehiculo
from app.db import db

repuestosvehiculos_bp = Blueprint('repuestosvehiculos', __name__, url_prefix='/api/repuestosvehiculos')

@repuestosvehiculos_bp.route('/', methods=['GET'])
def get_all():
    items = RepuestoVehiculo.query.all()
    return jsonify([{
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'vehiculo_id': getattr(i, 'vehiculo_id')
    } for i in items])

@repuestosvehiculos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = RepuestoVehiculo.query.get_or_404(id)
    return jsonify({
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'vehiculo_id': getattr(i, 'vehiculo_id')
    })

@repuestosvehiculos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = RepuestoVehiculo(
        codigo_pieza=data.get('codigo_pieza'), vehiculo_id=data.get('vehiculo_id')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoVehiculo creado', 'id': getattr(i, 'id', None)}), 201

@repuestosvehiculos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = RepuestoVehiculo.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoVehiculo eliminado'})
