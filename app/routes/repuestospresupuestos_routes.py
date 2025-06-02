from flask import Blueprint, request, jsonify
from app.models.models import RepuestoPresupuesto
from app.db import db

repuestospresupuestos_bp = Blueprint('repuestospresupuestos', __name__, url_prefix='/api/repuestospresupuestos')

@repuestospresupuestos_bp.route('/', methods=['GET'])
def get_all():
    items = RepuestoPresupuesto.query.all()
    return jsonify([{
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'presupuesto_id': getattr(i, 'presupuesto_id'), 'cantidad': getattr(i, 'cantidad')
    } for i in items])

@repuestospresupuestos_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = RepuestoPresupuesto.query.get_or_404(id)
    return jsonify({
        'codigo_pieza': getattr(i, 'codigo_pieza'), 'presupuesto_id': getattr(i, 'presupuesto_id'), 'cantidad': getattr(i, 'cantidad')
    })

@repuestospresupuestos_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = RepuestoPresupuesto(
        codigo_pieza=data.get('codigo_pieza'), presupuesto_id=data.get('presupuesto_id'), cantidad=data.get('cantidad')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoPresupuesto creado', 'id': getattr(i, 'id', None)}), 201

@repuestospresupuestos_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = RepuestoPresupuesto.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoPresupuesto eliminado'})
