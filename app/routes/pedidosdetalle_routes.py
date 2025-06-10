from flask import Blueprint, request, jsonify
from app.models.models import PedidoDetalle
from app.db import db

pedidosdetalle_bp = Blueprint('pedidosdetalle', __name__, url_prefix='/api/pedidosdetalle')

@pedidosdetalle_bp.route('/', methods=['GET'])
def get_all():
    items = PedidoDetalle.query.all()
    return jsonify([{
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'pedido_id': getattr(i, 'pedido_id'), 'cantidad': getattr(i, 'cantidad'), 'estado': getattr(i, 'estado'), 'fecha_recibido': getattr(i, 'fecha_recibido')
    } for i in items])

@pedidosdetalle_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = PedidoDetalle.query.get_or_404(id)
    return jsonify({
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'pedido_id': getattr(i, 'pedido_id'), 'cantidad': getattr(i, 'cantidad'), 'estado': getattr(i, 'estado'), 'fecha_recibido': getattr(i, 'fecha_recibido')
    })

@pedidosdetalle_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = PedidoDetalle(
        codigo_pieza=data.get('codigo_pieza'), pedido_id=data.get('pedido_id'), cantidad=data.get('cantidad'), estado=data.get('estado'), fecha_recibido=data.get('fecha_recibido')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'PedidoDetalle creado', 'id': getattr(i, 'id', None)}), 201

@pedidosdetalle_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = PedidoDetalle.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'PedidoDetalle eliminado'})

@pedidosdetalle_bp.route('/marcar_recibidos', methods=['PATCH'])
def marcar_detalles_recibidos():
    data = request.get_json()
    ids = data.get('ids', [])

    if not ids:
        return jsonify({'error': 'No se enviaron IDs'}), 400

    detalles = PedidoDetalle.query.filter(PedidoDetalle.id.in_(ids)).all()

    for d in detalles:
        d.estado = 'recibido'
        d.fecha_recibido = datetime.now()

    db.session.commit()

    return jsonify({
        'message': f'{len(detalles)} detalle(s) marcados como recibidos',
        'ids': [d.id for d in detalles]
    })