from flask import Blueprint, request, jsonify
from app.models.models import VentaMovimiento
from app.db import db

ventasmovimientos_bp = Blueprint('ventasmovimientos', __name__, url_prefix='/api/ventasmovimientos')

@ventasmovimientos_bp.route('/', methods=['GET'])
def get_all():
    items = VentaMovimiento.query.all()
    return jsonify([{
        'venta_id': getattr(i, 'venta_id'), 'movimiento_id': getattr(i, 'movimiento_id')
    } for i in items])

@ventasmovimientos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = VentaMovimiento.query.get_or_404(id)
    return jsonify({
        'venta_id': getattr(i, 'venta_id'), 'movimiento_id': getattr(i, 'movimiento_id')
    })

@ventasmovimientos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = VentaMovimiento(
        venta_id=data.get('venta_id'), movimiento_id=data.get('movimiento_id')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'VentaMovimiento creado', 'id': getattr(i, 'id', None)}), 201

@ventasmovimientos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = VentaMovimiento.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'VentaMovimiento eliminado'})
