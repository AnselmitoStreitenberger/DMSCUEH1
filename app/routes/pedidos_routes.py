from flask import Blueprint, request, jsonify
from app.models.models import Pedido , PedidoDetalle
from app.db import db
from datetime import datetime


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

@pedidos_bp.route('/<int:id>/marcar_enviado', methods=['PATCH'])
def marcar_pedido_como_enviado(id):
    pedido = Pedido.query.get_or_404(id)

    if pedido.fecha_ped_fab:
        return jsonify({'error': 'El pedido ya fue marcado como enviado'}), 400

    # 1. Marcar la fecha de envío
    pedido.fecha_ped_fab = datetime.now()

    # 2. Actualizar estado de los detalles a "pedido"
    detalles = PedidoDetalle.query.filter_by(pedido_id=pedido.id).all()
    for d in detalles:
        d.estado = 'pedido'

    db.session.commit()

    return jsonify({
        'message': 'Pedido marcado como enviado y detalles actualizados',
        'pedido_id': pedido.id,
        'fecha_ped_fab': pedido.fecha_ped_fab.isoformat(),
        'detalles_actualizados': [d.id for d in detalles]
    })
@pedidos_bp.route('/<int:id>/codigo', methods=['PATCH'])
def actualizar_codigo_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    data = request.get_json()

    nuevo_codigo = data.get('codigo_pedido')
    if not nuevo_codigo:
        return jsonify({'error': 'Falta el campo codigo_pedido'}), 400

    pedido.codigo_pedido = nuevo_codigo
    db.session.commit()

    return jsonify({
        'message': 'Código de pedido actualizado',
        'pedido_id': pedido.id,
        'codigo_pedido': pedido.codigo_pedido
    })

