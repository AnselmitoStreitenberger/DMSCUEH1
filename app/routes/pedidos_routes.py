from flask import Blueprint, request, jsonify
from app.models.models import Pedido
from app.db import db

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/api/pedidos')

@pedidos_bp.route('/', methods=['GET'])
def get_all():
    items = Pedido.query.all()
    return jsonify([{
        'fecha_creacion': getattr(i, 'fecha_creacion'), 'codigo_pedido': getattr(i, 'codigo_pedido'), 'fecha_ped_fab': getattr(i, 'fecha_ped_fab'), 'factura': getattr(i, 'factura'), 'remito': getattr(i, 'remito')
    } for i in items])

@pedidos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Pedido.query.get_or_404(id)
    return jsonify({
        'fecha_creacion': getattr(i, 'fecha_creacion'), 'codigo_pedido': getattr(i, 'codigo_pedido'), 'fecha_ped_fab': getattr(i, 'fecha_ped_fab'), 'factura': getattr(i, 'factura'), 'remito': getattr(i, 'remito')
    })

@pedidos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Pedido(
        fecha_creacion=data.get('fecha_creacion'), codigo_pedido=data.get('codigo_pedido'), fecha_ped_fab=data.get('fecha_ped_fab'), factura=data.get('factura'), remito=data.get('remito')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Pedido creado', 'id': getattr(i, 'id', None)}), 201

@pedidos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Pedido.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Pedido eliminado'})
