from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Ahorro, AporteAhorro
from app.utils.validators import validar_monto

bp = Blueprint('ahorros', __name__, url_prefix='/ahorros')

@bp.route('/', methods=['GET'])
@login_required
def listar():
    """Listar metas de ahorro de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    ahorros = Ahorro.query.filter_by(pareja_id=current_user.pareja_id).all()
    
    return jsonify({
        'ahorros': [ahorro.to_dict() for ahorro in ahorros]
    }), 200

@bp.route('/', methods=['POST'])
@login_required
def crear():
    """Crear meta de ahorro"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    data = request.get_json() if request.is_json else request.form
    
    nombre = data.get('nombre', '').strip()
    meta_monto = float(data.get('meta_monto', 0))
    fecha_objetivo = data.get('fecha_objetivo')
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    
    valido, mensaje = validar_monto(meta_monto)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Crear ahorro
    ahorro = Ahorro(
        pareja_id=current_user.pareja_id,
        nombre=nombre,
        meta_monto=meta_monto
    )
    
    if fecha_objetivo:
        ahorro.fecha_objetivo = datetime.fromisoformat(fecha_objetivo.replace('Z', '+00:00'))
    
    db.session.add(ahorro)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Meta de ahorro creada exitosamente',
        'ahorro': ahorro.to_dict()
    }), 201

@bp.route('/<int:ahorro_id>/aportar', methods=['POST'])
@login_required
def aportar(ahorro_id):
    """Agregar aporte a meta de ahorro"""
    ahorro = Ahorro.query.get_or_404(ahorro_id)
    
    if ahorro.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    data = request.get_json() if request.is_json else request.form
    monto = float(data.get('monto', 0))
    notas = data.get('notas', '').strip()
    
    valido, mensaje = validar_monto(monto)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Crear aporte
    aporte = AporteAhorro(
        ahorro_id=ahorro_id,
        usuario_id=current_user.id,
        monto=monto,
        notas=notas
    )
    
    # Actualizar monto actual
    ahorro.monto_actual += monto
    
    # Verificar si se completó la meta
    if ahorro.monto_actual >= ahorro.meta_monto:
        ahorro.completado = True
    
    db.session.add(aporte)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Aporte agregado exitosamente',
        'ahorro': ahorro.to_dict(),
        'aporte': aporte.to_dict()
    }), 201

@bp.route('/<int:ahorro_id>', methods=['DELETE'])
@login_required
def eliminar(ahorro_id):
    """Eliminar meta de ahorro"""
    ahorro = Ahorro.query.get_or_404(ahorro_id)
    
    if ahorro.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    db.session.delete(ahorro)
    db.session.commit()
    
    return jsonify({'mensaje': 'Meta de ahorro eliminada'}), 200
