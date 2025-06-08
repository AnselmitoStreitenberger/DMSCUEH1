from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.models import Pedido, PedidoDetalle, PedidoCliente, Cliente
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
@pedidosarmado_bp.route('/agrupados', methods=['GET'])
def listar_pedidos_agrupados():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    estado_filtro = request.args.get('estado')  # opcional
    con_fecha_str = request.args.get('con_fecha')  # opcional
    cliente_filtro = request.args.get('cliente')  # opcional
    offset = (page - 1) * limit

    # Base query
    query = Pedido.query

    # Filtro por existencia de fecha_ped_fab
    if con_fecha_str == "true":
        query = query.filter(Pedido.fecha_ped_fab.isnot(None))
    elif con_fecha_str == "false":
        query = query.filter(Pedido.fecha_ped_fab.is_(None))

    pedidos = query.order_by(Pedido.id.desc()).offset(offset).limit(limit).all()
    resultado = []

    for pedido in pedidos:
        detalles = PedidoDetalle.query.filter_by(pedido_id=pedido.id).all()

        if estado_filtro:
            detalles = [d for d in detalles if d.estado == estado_filtro]

        if not detalles:
            continue  # salteamos pedidos sin detalles válidos

        detalle_info = []

        for detalle in detalles:
            relaciones = PedidoCliente.query.filter_by(pedido_detalle_id=detalle.id).all()
            clientes_info = []

            for r in relaciones:
                cliente = Cliente.query.get(r.cliente_id)
                if cliente:
                    # Aplicar filtro de nombre de cliente (case-insensitive)
                    if cliente_filtro and cliente_filtro.lower() not in cliente.nombre.lower():
                        continue

                    clientes_info.append({
                        'id': cliente.id,
                        'nombre': cliente.nombre,
                        'telefono': cliente.telefono,
                        'cantidad': r.cantidad,
                        'senia': r.senia,
                        'entregado': r.entregado
                    })

            # Si se aplicó filtro por cliente y no hay coincidencias, saltear este detalle
            if cliente_filtro and not clientes_info:
                continue

            detalle_info.append({
                'detalle_id': detalle.id,
                'codigo_pieza': detalle.codigo_pieza,
                'cantidad_total': detalle.cantidad,
                'cantidad_recibida': detalle.cantidad_recibida,
                'estado': detalle.estado,
                'clientes': clientes_info
                
            })

        if not detalle_info:
            continue  # saltear pedido si no hay detalles que cumplan el filtro

        resultado.append({
            'pedido_id': pedido.id,
            'codigo_pedido': pedido.codigo_pedido,
            'fecha_creacion': pedido.fecha_creacion,
            'fecha_ped_fab': pedido.fecha_ped_fab,
            'detalles': detalle_info
        })

    return jsonify({
        'pagina': page,
        'limite': limit,
        'estado': estado_filtro,
        'con_fecha': con_fecha_str,
        'cliente': cliente_filtro,
        'resultados': resultado
    })
