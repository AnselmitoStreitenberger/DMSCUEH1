from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.models import Pedido, PedidoDetalle, PedidoCliente
from app.db import db

pedidosarmado_bp = Blueprint('pedidosarmado', __name__, url_prefix='/api/pedidosarmado')

@pedidosarmado_bp.route('/agregar', methods=['POST'])
def agregar_a_pedido_actual():
    data = request.get_json()
    codigo_pieza = data.get('codigo_pieza')
    cantidad = data.get('cantidad', 1)
    cliente_id = data.get('cliente_id')  # puede ser None
    senia = data.get('senia', 0.0)

    if not codigo_pieza or cantidad <= 0:
        return jsonify({'error': 'Código de pieza y cantidad válida son obligatorios'}), 400

    # 1. Buscar pedido actual (fecha_ped_fab IS NULL)
    pedido = Pedido.query.filter_by(fecha_ped_fab=None).first()
    if not pedido:
        pedido = Pedido(fecha_creacion=datetime.now())
        db.session.add(pedido)
        db.session.commit()

    # 2. Buscar si el detalle ya existe
    detalle = PedidoDetalle.query.filter_by(pedido_id=pedido.id, codigo_pieza=codigo_pieza).first()

    if detalle:
        detalle.cantidad += cantidad
    else:
        detalle = PedidoDetalle(
            codigo_pieza=codigo_pieza,
            pedido_id=pedido.id,
            cantidad=cantidad,
            estado='para pedir'  # ajustá si usás Enum real
        )
        db.session.add(detalle)
        db.session.flush()  # para obtener detalle.id antes del commit

    # 3. Asociar cliente (si se pasó)
    if cliente_id is not None:
        pedido_cliente = PedidoCliente(
            cliente_id=cliente_id,
            pedido_detalle_id=detalle.id,
            senia=senia,
            entregado=False,
            cantidad=cantidad
        )
        db.session.add(pedido_cliente)

        

    db.session.commit()
    return jsonify({'message': 'Pedido actualizado', 'pedido_id': pedido.id, 'detalle_id': detalle.id})

@pedidosarmado_bp.route('/finalizar', methods=['POST'])
def finalizar_pedido_actual():
    pedido = Pedido.query.filter_by(fecha_ped_fab=None).first()
    if not pedido:
        return jsonify({'error': 'No hay pedido abierto para pedir a fábrica'}), 404

    # Marcar como pedido a fábrica
    pedido.fecha_ped_fab = datetime.now()

    # Buscar y actualizar los detalles
    detalles = PedidoDetalle.query.filter_by(pedido_id=pedido.id).all()
    piezas_actualizadas = []

    for d in detalles:
        d.estado = 'pedido'
        piezas_actualizadas.append({
            'detalle_id': d.id,
            'codigo_pieza': d.codigo_pieza,
            'cantidad': d.cantidad
        })

    db.session.commit()

    return jsonify({
        'message': 'Pedido a fábrica finalizado',
        'pedido_id': pedido.id,
        'piezas_actualizadas': piezas_actualizadas
    })

@pedidosarmado_bp.route('/estado/<int:detalle_id>', methods=['PATCH'])
def actualizar_estado(detalle_id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    if nuevo_estado not in ['para pedir', 'pedido', 'recibido', 'sin stock fabrica']:
        return jsonify({'error': 'Estado inválido'}), 400

    detalle = PedidoDetalle.query.get_or_404(detalle_id)
    detalle.estado = nuevo_estado
    db.session.commit()

    return jsonify({'message': 'Estado actualizado', 'detalle_id': detalle.id})

@pedidosarmado_bp.route('/pendientes', methods=['GET'])
def listar_pendientes_para_pedir():
    pendientes = PedidoDetalle.query.filter_by(estado='para pedir').all()
    return jsonify([{
        'detalle_id': d.id,
        'codigo_pieza': d.codigo_pieza,
        'pedido_id': d.pedido_id,
        'cantidad': d.cantidad
    } for d in pendientes])

@pedidosarmado_bp.route('/por_cliente/<int:cliente_id>', methods=['GET'])
def pedidos_por_cliente(cliente_id):
    relaciones = PedidoCliente.query.filter_by(cliente_id=cliente_id).all()
    
    resultado = []
    for r in relaciones:
        detalle = PedidoDetalle.query.get(r.pedido_detalle_id)
        resultado.append({
            'detalle_id': detalle.id,
            'codigo_pieza': detalle.codigo_pieza,
            'estado': detalle.estado,
            'cantidad': r.cantidad,
            'senia': r.senia,
            'entregado': r.entregado
        })

    return jsonify(resultado)