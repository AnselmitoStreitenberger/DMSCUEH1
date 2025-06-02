from flask import Blueprint, request, jsonify
from app.models.models import Presupuesto
from app.db import db

presupuestos_bp = Blueprint('presupuestos', __name__, url_prefix='/api/presupuestos')

@presupuestos_bp.route('/', methods=['GET'])
def get_all():
    items = Presupuesto.query.all()
    return jsonify([{
        'vehiculo_id': getattr(i, 'vehiculo_id'), 'cliente_id': getattr(i, 'cliente_id'), 'precio': getattr(i, 'precio'), 'se_pidio': getattr(i, 'se_pidio')
    } for i in items])

@presupuestos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Presupuesto.query.get_or_404(id)
    return jsonify({
        'vehiculo_id': getattr(i, 'vehiculo_id'), 'cliente_id': getattr(i, 'cliente_id'), 'precio': getattr(i, 'precio'), 'se_pidio': getattr(i, 'se_pidio')
    })

@presupuestos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Presupuesto(
        vehiculo_id=data.get('vehiculo_id'), cliente_id=data.get('cliente_id'), precio=data.get('precio'), se_pidio=data.get('se_pidio')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Presupuesto creado', 'id': getattr(i, 'id', None)}), 201

@presupuestos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Presupuesto.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Presupuesto eliminado'})
