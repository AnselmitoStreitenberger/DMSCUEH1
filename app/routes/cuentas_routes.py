from flask import Blueprint, request, jsonify
from app.models.models import Cuenta
from app.db import db

cuentas_bp = Blueprint('cuentas', __name__, url_prefix='/api/cuentas')

@cuentas_bp.route('/', methods=['GET'])
def get_all():
    items = Cuenta.query.all()
    return jsonify([{
        'identificador': getattr(i, 'identificador'), 'numero_de_cuenta': getattr(i, 'numero_de_cuenta'), 'saldo': getattr(i, 'saldo')
    } for i in items])

@cuentas_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Cuenta.query.get_or_404(id)
    return jsonify({
        'identificador': getattr(i, 'identificador'), 'numero_de_cuenta': getattr(i, 'numero_de_cuenta'), 'saldo': getattr(i, 'saldo')
    })

@cuentas_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    i = Cuenta(
        identificador=data.get('identificador'), numero_de_cuenta=data.get('numero_de_cuenta'), saldo=data.get('saldo')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Cuenta creado', 'id': getattr(i, 'id', None)}), 201

@cuentas_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Cuenta.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Cuenta eliminado'})
