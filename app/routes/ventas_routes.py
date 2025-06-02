from flask import Blueprint, request, jsonify
from app.models.models import Venta
from app.db import db

ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

@ventas_bp.route('/', methods=['GET'])
def get_all():
    items = Venta.query.all()
    return jsonify([{
        'cliente_id': getattr(i, 'cliente_id'), 'fecha': getattr(i, 'fecha'), 'valor_total_dolar': getattr(i, 'valor_total_dolar'), 'valor_total_pesos': getattr(i, 'valor_total_pesos'), 'factura': getattr(i, 'factura')
    } for i in items])

@ventas_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Venta.query.get_or_404(id)
    return jsonify({
        'cliente_id': getattr(i, 'cliente_id'), 'fecha': getattr(i, 'fecha'), 'valor_total_dolar': getattr(i, 'valor_total_dolar'), 'valor_total_pesos': getattr(i, 'valor_total_pesos'), 'factura': getattr(i, 'factura')
    })

@ventas_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Venta(
        cliente_id=data.get('cliente_id'), fecha=data.get('fecha'), valor_total_dolar=data.get('valor_total_dolar'), valor_total_pesos=data.get('valor_total_pesos'), factura=data.get('factura')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Venta creado', 'id': getattr(i, 'id', None)}), 201

@ventas_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Venta.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Venta eliminado'})
