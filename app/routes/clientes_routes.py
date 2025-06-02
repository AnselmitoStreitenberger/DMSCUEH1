from flask import Blueprint, request, jsonify
from app.models.models import Cliente
from app.db import db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

@clientes_bp.route('/', methods=['GET'])
def get_all():
    items = Cliente.query.all()
    return jsonify([{
        'nombre': getattr(i, 'nombre'), 'telefono': getattr(i, 'telefono')
    } for i in items])

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Cliente.query.get_or_404(id)
    return jsonify({
        'nombre': getattr(i, 'nombre'), 'telefono': getattr(i, 'telefono')
    })

@clientes_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Cliente(
        nombre=data.get('nombre'), telefono=data.get('telefono')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Cliente creado', 'id': getattr(i, 'id', None)}), 201

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Cliente.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})
