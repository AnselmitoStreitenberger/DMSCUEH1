"""Rutas para la gestión de repuestos."""

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import desc

from app.models.models import Repuesto
from app.db import db
from app.schemas import RepuestoSchema

repuestos_bp = Blueprint('repuestos', __name__, url_prefix='/api/repuestos')


# GET con filtros, orden y paginación
@repuestos_bp.route('/', methods=['GET'])
def get_filtered():
    """Obtener repuestos con filtros y paginación."""
    query = Repuesto.query

    # Filtro parcial por código
    if 'codigo_pieza' in request.args:
        query = query.filter(Repuesto.codigo_pieza.ilike(f"%{request.args['codigo_pieza']}%"))
    # Filtro parcial por descripción
    if 'descripcion' in request.args:
        query = query.filter(Repuesto.descripcion.ilike(f"%{request.args['descripcion']}%"))
    # Filtros numéricos
    if 'stock_min' in request.args:
        query = query.filter(Repuesto.stock_min == int(request.args['stock_min']))
    if 'stock_min__gte' in request.args:
        query = query.filter(Repuesto.stock_min >= int(request.args['stock_min__gte']))
    if 'stock_real__lte' in request.args:
        query = query.filter(Repuesto.stock_real <= int(request.args['stock_real__lte']))

    # Ordenamiento
    order_field = request.args.get('order_by', 'codigo_pieza')
    order_attr = getattr(Repuesto, order_field, Repuesto.codigo_pieza)
    if request.args.get('desc', 'false').lower() == 'true':
        query = query.order_by(desc(order_attr))
    else:
        query = query.order_by(order_attr)

    # Paginación
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    results = [{
        'codigo_pieza': r.codigo_pieza,
        'descripcion': r.descripcion,
        'precio': r.precio,
        'stock_min': r.stock_min,
        'stock_real': r.stock_real,
        'stock_disp': r.stock_disp
    } for r in paginated.items]

    return jsonify({
        'results': results,
        'total': paginated.total,
        'page': paginated.page,
        'per_page': paginated.per_page
    })


# GET por ID exacto (solo si usás ID entero, en este caso código es la PK)
@repuestos_bp.route('/codigo/<string:codigo>', methods=['GET'])
def get_by_codigo_pieza(codigo):
    """Obtener un repuesto por su código."""
    r = Repuesto.query.get_or_404(codigo)
    return jsonify({
        'codigo_pieza': r.codigo_pieza,
        'descripcion': r.descripcion,
        'precio': r.precio,
        'stock_min': r.stock_min,
        'stock_real': r.stock_real,
        'stock_disp': r.stock_disp
    })


# POST - Crear nuevo repuesto
@repuestos_bp.route('/', methods=['POST'])
def create():
    """Crear un repuesto validando la entrada."""
    schema = RepuestoSchema()
    try:
        data = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    r = Repuesto(**data)
    db.session.add(r)
    db.session.commit()
    return jsonify({'message': 'Repuesto creado', 'codigo_pieza': r.codigo_pieza}), 201


# PUT - Editar repuesto existente
@repuestos_bp.route('/<string:codigo>', methods=['PUT'])
def update(codigo):
    """Actualizar un repuesto existente."""
    r = Repuesto.query.get_or_404(codigo)
    schema = RepuestoSchema(partial=True)
    try:
        data = schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for field, value in data.items():
        setattr(r, field, value)

    db.session.commit()
    return jsonify({'message': 'Repuesto actualizado'})


# DELETE - Eliminar repuesto
@repuestos_bp.route('/<string:codigo>', methods=['DELETE'])
def delete(codigo):
    """Eliminar un repuesto."""
    r = Repuesto.query.get_or_404(codigo)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Repuesto eliminado'})