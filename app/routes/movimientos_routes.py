from flask import Blueprint, request, jsonify
from app.models.models import Movimiento
from app.db import db

movimientos_bp = Blueprint('movimientos', __name__, url_prefix='/api/movimientos')

@movimientos_bp.route('/', methods=['GET'])
def get_all():
    items = Movimiento.query.all()
    return jsonify([{
        'cuenta_id': getattr(i, 'cuenta_id'), 'valor': getattr(i, 'valor'), 'detalle': getattr(i, 'detalle'), 'fecha': getattr(i, 'fecha')
    } for i in items])

@movimientos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Movimiento.query.get_or_404(id)
    return jsonify({
        'cuenta_id': getattr(i, 'cuenta_id'), 'valor': getattr(i, 'valor'), 'detalle': getattr(i, 'detalle'), 'fecha': getattr(i, 'fecha')
    })

@movimientos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Movimiento(
        cuenta_id=data.get('cuenta_id'), valor=data.get('valor'), detalle=data.get('detalle'), fecha=data.get('fecha')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Movimiento creado', 'id': getattr(i, 'id', None)}), 201

@movimientos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Movimiento.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Movimiento eliminado'})
