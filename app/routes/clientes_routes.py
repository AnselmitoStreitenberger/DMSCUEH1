from flask import Blueprint, request, jsonify
from app.models.models import Cliente
from app.db import db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

@clientes_bp.route('', methods=['GET'])
def get_all():
    items = Cliente.query.all()
    return jsonify([{
        'id': i.id,
        'nombre': i.nombre,
        'telefono': i.telefono,
        'direccion': i.direccion,
        'correo_electronico': i.correo_electronico
    } for i in items])

@clientes_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    i = Cliente.query.get_or_404(id)
    return jsonify({
        'id': i.id,
        'nombre': i.nombre,
        'telefono': i.telefono,
        'direccion': i.direccion,
        'correo_electronico': i.correo_electronico
    })

@clientes_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    i = Cliente(
        nombre=data.get('nombre'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion'),
        correo_electronico=data.get('correo_electronico')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'Cliente creado', 'id': i.id}), 201

@clientes_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    i = Cliente.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})

@clientes_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    cliente = Cliente.query.get_or_404(id)

    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.direccion = data.get('direccion', cliente.direccion)
    cliente.correo_electronico = data.get('correo_electronico', cliente.correo_electronico)

    db.session.commit()
    return jsonify({'message': 'Cliente actualizado', 'id': cliente.id})
from sqlalchemy import or_

@clientes_bp.route('/buscar', methods=['GET'])
def buscar_general():
    term = request.args.get('term', '').lower()
    if not term:
        return jsonify([])

    # Trae todos los clientes (puede optimizarse en producción)
    clientes = Cliente.query.all()

    def coincide(cliente):
        texto = f"{cliente.nombre or ''} {cliente.telefono or ''} {cliente.direccion or ''} {cliente.correo_electronico or ''}".lower()
        return all(char in texto for char in term)

    resultados = [c for c in clientes if coincide(c)]

    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'telefono': c.telefono,
        'direccion': c.direccion,
        'correo_electronico': c.correo_electronico
    } for c in resultados])
