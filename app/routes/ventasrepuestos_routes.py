from flask import Blueprint, request, jsonify
from app.models.models import VentaRepuesto
from app.db import db

ventasrepuestos_bp = Blueprint('ventasrepuestos', __name__, url_prefix='/api/ventasrepuestos')

@ventasrepuestos_bp.route('/', methods=['GET'])
def get_all():
    items = VentaRepuesto.query.all()
    return jsonify([{
        'venta_id': getattr(i, 'venta_id'), 'codigo_pieza': getattr(i, 'codigo_pieza'), 'cantidad': getattr(i, 'cantidad')
    } for i in items])

@ventasrepuestos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = VentaRepuesto.query.get_or_404(id)
    return jsonify({
        'venta_id': getattr(i, 'venta_id'), 'codigo_pieza': getattr(i, 'codigo_pieza'), 'cantidad': getattr(i, 'cantidad')
    })

@ventasrepuestos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = VentaRepuesto(
        venta_id=data.get('venta_id'), codigo_pieza=data.get('codigo_pieza'), cantidad=data.get('cantidad')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'VentaRepuesto creado', 'id': getattr(i, 'id', None)}), 201

@ventasrepuestos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = VentaRepuesto.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'VentaRepuesto eliminado'})
