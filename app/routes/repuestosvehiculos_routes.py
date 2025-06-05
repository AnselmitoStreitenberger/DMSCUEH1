from flask import Blueprint, request, jsonify
from app.models.models import RepuestoVehiculo
from app.db import db

repuestosvehiculos_bp = Blueprint('repuestosvehiculos', __name__, url_prefix='/api/repuestosvehiculos')


# GET todos con datos del vehículo
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


# GET por código de pieza
@repuestosvehiculos_bp.route('/por_codigo/<string:codigo>', methods=['GET'])
def get_by_codigo(codigo):
    items = RepuestoVehiculo.query.filter_by(codigo_pieza=codigo).all()
    return jsonify([{
        'vehiculo_id': i.vehiculo_id,
        'nombre': i.vehiculo.nombre,
        'codigo_manual': i.vehiculo.codigo_manual
    } for i in items])


# POST uno solo
@repuestosvehiculos_bp.route('/', methods=['POST'])
def create_repuesto_vehiculo():
    data = request.get_json()
    i = RepuestoVehiculo(
        codigo_pieza=data.get('codigo_pieza'),
        vehiculo_id=data.get('vehiculo_id')
    )
    db.session.add(i)
    db.session.commit()
    return jsonify({
        'message': 'RepuestoVehiculo creado',
        'codigo_pieza': i.codigo_pieza,
        'vehiculo_id': i.vehiculo_id
    }), 201


# POST múltiple (batch)
@repuestosvehiculos_bp.route('/batch', methods=['POST'])
def create_multiple_repuesto_vehiculo():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'error': 'Se espera una lista de relaciones'}), 400

    items = []
    for entry in data:
        codigo = entry.get('codigo_pieza')
        vehiculo = entry.get('vehiculo_id')

        # Evitar duplicados
        existe = RepuestoVehiculo.query.filter_by(codigo_pieza=codigo, vehiculo_id=vehiculo).first()
        if not existe:
            i = RepuestoVehiculo(codigo_pieza=codigo, vehiculo_id=vehiculo)
            db.session.add(i)
            items.append(i)

    db.session.commit()
    return jsonify({
        'message': 'Relaciones creadas',
        'relaciones': [{'codigo_pieza': i.codigo_pieza, 'vehiculo_id': i.vehiculo_id} for i in items]
    }), 201


# DELETE por clave compuesta
@repuestosvehiculos_bp.route('/<string:codigo_pieza>/<int:vehiculo_id>', methods=['DELETE'])
def delete_repuesto_vehiculo(codigo_pieza, vehiculo_id):
    i = RepuestoVehiculo.query.filter_by(codigo_pieza=codigo_pieza, vehiculo_id=vehiculo_id).first_or_404()
    db.session.delete(i)
    db.session.commit()
    return jsonify({'message': 'RepuestoVehiculo eliminado'})
