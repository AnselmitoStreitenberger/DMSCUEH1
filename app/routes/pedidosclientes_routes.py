from flask import Blueprint, request, jsonify
from app.models.models import PedidoCliente
from app.db import db

pedidosclientes_bp = Blueprint('pedidosclientes', __name__, url_prefix='/api/pedidosclientes')

@pedidosclientes_bp.route('/', methods=['GET'])
def get_all():
    items = PedidoCliente.query.all()
    return jsonify([{
        'cliente_id': getattr(i, 'cliente_id'), 'pedido_detalle_id': getattr(i, 'pedido_detalle_id'), 'ventas_id': getattr(i, 'ventas_id'), 'senia': getattr(i, 'senia'), 'entregado': getattr(i, 'entregado'), 'cantidad': getattr(i, 'cantidad')
    } for i in items])

@pedidosclientes_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = PedidoCliente.query.get_or_404(id)
    return jsonify({
        'cliente_id': getattr(i, 'cliente_id'), 'pedido_detalle_id': getattr(i, 'pedido_detalle_id'), 'ventas_id': getattr(i, 'ventas_id'), 'senia': getattr(i, 'senia'), 'entregado': getattr(i, 'entregado'), 'cantidad': getattr(i, 'cantidad')
    })

@pedidosclientes_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = PedidoCliente(
        cliente_id=data.get('cliente_id'), pedido_detalle_id=data.get('pedido_detalle_id'), ventas_id=data.get('ventas_id'), senia=data.get('senia'), entregado=data.get('entregado'), cantidad=data.get('cantidad')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'PedidoCliente creado', 'id': getattr(i, 'id', None)}), 201

@pedidosclientes_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = PedidoCliente.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'PedidoCliente eliminado'})
