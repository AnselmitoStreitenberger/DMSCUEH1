from flask import Blueprint, request, jsonify
from app.db import db
from app.models.models import RepuestoCompatible

repuestoscompatibles_bp = Blueprint('repuestoscompatibles', __name__)

# Obtener reemplazos de un repuesto
@repuestoscompatibles_bp.route('/api/repuestoscompatibles/<codigo_pieza>', methods=['GET'])
def obtener_reemplazos(codigo_pieza):
    relaciones = RepuestoCompatible.query.filter(
        (RepuestoCompatible.codigo_pieza_1 == codigo_pieza) |
        (RepuestoCompatible.codigo_pieza_2 == codigo_pieza)
    ).all()

    reemplazos = [
        r.codigo_pieza_2 if r.codigo_pieza_1 == codigo_pieza else r.codigo_pieza_1
        for r in relaciones
    ]
    return jsonify(reemplazos), 200

# Crear una relación de compatibilidad
@repuestoscompatibles_bp.route('/api/repuestoscompatibles', methods=['POST'])
def crear_compatibilidad():
    data = request.get_json()
    pieza1 = data.get('codigo_pieza_1').lower()
    pieza2 = data.get('codigo_pieza_2').lower()

    if not pieza1 or not pieza2 or pieza1 == pieza2:
        return jsonify({'error': 'Códigos inválidos'}), 400

    cod1, cod2 = sorted([pieza1, pieza2])
    existente = RepuestoCompatible.query.get((cod1, cod2))
    if not existente:
        nueva = RepuestoCompatible(codigo_pieza_1=cod1, codigo_pieza_2=cod2)
        db.session.add(nueva)

    # Buscar todos los compatibles existentes de cada pieza
    relacionados_1 = set([
        r.codigo_pieza_2 if r.codigo_pieza_1 == pieza1 else r.codigo_pieza_1
        for r in RepuestoCompatible.query.filter(
            (RepuestoCompatible.codigo_pieza_1 == pieza1) | (RepuestoCompatible.codigo_pieza_2 == pieza1)
        ).all()
    ])

    relacionados_2 = set([
        r.codigo_pieza_2 if r.codigo_pieza_1 == pieza2 else r.codigo_pieza_1
        for r in RepuestoCompatible.query.filter(
            (RepuestoCompatible.codigo_pieza_1 == pieza2) | (RepuestoCompatible.codigo_pieza_2 == pieza2)
        ).all()
    ])

    todos = relacionados_1.union(relacionados_2, {pieza1, pieza2})

    nuevos_pares = set()
    for a in todos:
        for b in todos:
            if a != b:
                par = tuple(sorted([a, b]))
                nuevos_pares.add(par)

    existentes = set(
        tuple(sorted([r.codigo_pieza_1, r.codigo_pieza_2]))
        for r in RepuestoCompatible.query.filter(
            RepuestoCompatible.codigo_pieza_1.in_(todos),
            RepuestoCompatible.codigo_pieza_2.in_(todos)
        ).all()
    )

    for par in nuevos_pares - existentes:
        db.session.add(RepuestoCompatible(codigo_pieza_1=par[0], codigo_pieza_2=par[1]))

    db.session.commit()
    return jsonify({'mensaje': 'Compatibilidades actualizadas con propagación'}), 201

# Eliminar una relación de compatibilidad
@repuestoscompatibles_bp.route('/api/repuestoscompatibles', methods=['DELETE'])
def eliminar_compatibilidad():
    data = request.get_json()
    pieza1 = data.get('codigo_pieza_1')
    pieza2 = data.get('codigo_pieza_2')

    if not pieza1 or not pieza2 or pieza1 == pieza2:
        return jsonify({'error': 'Códigos inválidos'}), 400

    cod1, cod2 = sorted([pieza1, pieza2])
    existente = RepuestoCompatible.query.get((cod1, cod2))
    if not existente:
        return jsonify({'error': 'No existe'}), 404

    db.session.delete(existente)
    db.session.commit()
    return jsonify({'mensaje': 'Compatibilidad eliminada'}), 200
