from flask import Blueprint, request, jsonify
from app.models.models import Repuesto
from app.db import db

repuestos_bp = Blueprint('repuestos', __name__, url_prefix='/api/repuestos')

@repuestos_bp.route('/', methods=['GET'])
def get_all():
    items = Repuesto.query.all()
    return jsonify([{
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'descripcion': getattr(i, 'descripcion'), 'precio': getattr(i, 'precio'), 'stock_min': getattr(i, 'stock_min'), 'stock_real': getattr(i, 'stock_real'), 'stock_disp': getattr(i, 'stock_disp')
    } for i in items])

@repuestos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Repuesto.query.get_or_404(id)
    return jsonify({
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'descripcion': getattr(i, 'descripcion'), 'precio': getattr(i, 'precio'), 'stock_min': getattr(i, 'stock_min'), 'stock_real': getattr(i, 'stock_real'), 'stock_disp': getattr(i, 'stock_disp')
    })

@repuestos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Repuesto(
        codigo_pieza=data.get('codigo_pieza'), descripcion=data.get('descripcion'), precio=data.get('precio'), stock_min=data.get('stock_min'), stock_real=data.get('stock_real'), stock_disp=data.get('stock_disp')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Repuesto creado', 'id': getattr(i, 'id', None)}), 201

@repuestos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Repuesto.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Repuesto eliminado'})
