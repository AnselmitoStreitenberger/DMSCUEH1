from flask import Blueprint, request, jsonify
from app.models.models import RepuestoVehiculo
from app.db import db

repuestosvehiculos_bp = Blueprint('repuestosvehiculos', __name__, url_prefix='/api/repuestosvehiculos')

@repuestosvehiculos_bp.route('/', methods=['GET'])
def get_all_repuesto_vehiculo():
    items = RepuestoVehiculo.query.all()
    return jsonify([{
        'id': i.id,
        'codigo_pieza': i.codigo_pieza,
        'vehiculo_id': i.vehiculo_id
    } for i in items])

@repuestosvehiculos_bp.route('/<int:id>', methods=['GET'])
def get_repuesto_vehiculo_by_id(id):
    i = RepuestoVehiculo.query.get_or_404(id)
    return jsonify({
        'id': i.id,
        'codigo_pieza': i.codigo_pieza,
        'vehiculo_id': i.vehiculo_id
    })
@repuestosvehiculos_bp.route('/', methods=['GET'])
def get_all():
    items = RepuestoVehiculo.query.all()
    return jsonify([{
        'codigo_pieza': i.codigo_pieza,
        'vehiculo_id': i.vehiculo_id,
        'vehiculo': {
            'nombre': i.vehiculo.nombre,
            'ano': i.vehiculo.ano,
            'codigo_manual': i.vehiculo.codigo_manual
        }
    } for i in items])
@repuestosvehiculos_bp.route('/por_codigo/<string:codigo>', methods=['GET'])
def get_by_codigo(codigo):
    items = RepuestoVehiculo.query.filter_by(codigo_pieza=codigo).all()
    return jsonify([{
        'vehiculo_id': i.vehiculo_id,
        'nombre': i.vehiculo.nombre,
        'codigo_manual': i.vehiculo.codigo_manual
    } for i in items])

@repuestosvehiculos_bp.route('/', methods=['POST'])
def create_repuesto_vehiculo():
    data = request.get_json()
    i = RepuestoVehiculo(
        codigo_pieza=data.get('codigo_pieza'),
        vehiculo_id=data.get('vehiculo_id')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoVehiculo creado', 'id': i.id}), 201

@repuestosvehiculos_bp.route('/batch', methods=['POST'])
def create_multiple_repuesto_vehiculo():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'error': 'Se espera una lista de relaciones'}), 400

    items = []
    for entry in data:
        i = RepuestoVehiculo(
            codigo_pieza=entry.get('codigo_pieza'),
            vehiculo_id=entry.get('vehiculo_id')
        )
        db.session.add(i)
        items.append(i)

    db.session.commit()
    return jsonify({'message': 'Relaciones creadas', 'ids': [i.id for i in items]}), 201

@repuestosvehiculos_bp.route('/<int:id>', methods=['DELETE'])
def delete_repuesto_vehiculo(id):
    i = RepuestoVehiculo.query.get_or_404(id)
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoVehiculo eliminado'})