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

from sqlalchemy.orm import joinedload
from app.models.models import PedidoCliente, Cliente, PedidoDetalle, Pedido

@pedidosclientes_bp.route('/filtrados', methods=['GET'])
def get_filtrados():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    nombre = request.args.get('nombre')
    estado = request.args.get('estado')
    codigo_pedido = request.args.get('codigo_pedido')
    codigo_pieza = request.args.get('codigo_pieza')

    query = db.session.query(PedidoCliente, Cliente, PedidoDetalle, Pedido)\
        .join(Cliente, PedidoCliente.cliente_id == Cliente.id)\
        .join(PedidoDetalle, PedidoCliente.pedido_detalle_id == PedidoDetalle.id)\
        .join(Pedido, PedidoDetalle.pedido_id == Pedido.id)

    # Filtros opcionales
    if nombre:
        query = query.filter(Cliente.nombre.ilike(f"%{nombre}%"))
    if estado:
        query = query.filter(PedidoDetalle.estado == estado)
    if codigo_pedido:
        query = query.filter(Pedido.codigo_pedido.ilike(f"%{codigo_pedido}%"))
    if codigo_pieza:
        query = query.filter(PedidoDetalle.codigo_pieza.ilike(f"%{codigo_pieza}%"))

    # Paginación
    paginated = query.order_by(Pedido.fecha_creacion.desc())\
                     .offset((page - 1) * limit)\
                     .limit(limit)\
                     .all()

    resultados = []
    for pc, cl, pd, p in paginated:
        resultados.append({
            'nombre': cl.nombre,
            'telefono': cl.telefono,
            'codigo_pieza': pd.codigo_pieza,
            'cantidad': pc.cantidad,
            'senia': pc.senia,
            'cantidad_recibida': pd.cantidad_recibida,
            'fecha_recibido': pd.fecha_recibido.isoformat() if pd.fecha_recibido else None,
            'codigo_pedido': p.codigo_pedido,
            'estado': pd.estado,
        })

    return jsonify(resultados)

