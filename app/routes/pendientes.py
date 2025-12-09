from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Pendiente
from app.utils.validators import validar_categoria_pendiente

bp = Blueprint('pendientes', __name__, url_prefix='/pendientes')

@bp.route('/', methods=['GET'])
@login_required
def listar():
    """Listar pendientes de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    pendientes = Pendiente.query.filter_by(pareja_id=current_user.pareja_id).order_by(Pendiente.completado, Pendiente.fecha_creacion.desc()).all()
    
    return jsonify({
        'pendientes': [p.to_dict() for p in pendientes]
    }), 200

@bp.route('/', methods=['POST'])
@login_required
def crear():
    """Crear pendiente"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    data = request.get_json() if request.is_json else request.form
    
    titulo = data.get('titulo', '').strip()
    categoria = data.get('categoria', '').strip().lower()
    recordatorio = data.get('recordatorio')
    notas = data.get('notas', '').strip()
    
    # Validaciones
    if not titulo:
        return jsonify({'error': 'El título es requerido'}), 400
    
    if not validar_categoria_pendiente(categoria):
        return jsonify({'error': 'Categoría inválida'}), 400
    
    # Crear pendiente
    pendiente = Pendiente(
        pareja_id=current_user.pareja_id,
        titulo=titulo,
        categoria=categoria,
        notas=notas,
        creado_por=current_user.id
    )
    
    if recordatorio:
        pendiente.recordatorio = datetime.fromisoformat(recordatorio.replace('Z', '+00:00'))
    
    db.session.add(pendiente)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Pendiente creado exitosamente',
        'pendiente': pendiente.to_dict()
    }), 201

@bp.route('/<int:pendiente_id>/completar', methods=['PUT'])
@login_required
def completar(pendiente_id):
    """Marcar pendiente como completado"""
    pendiente = Pendiente.query.get_or_404(pendiente_id)
    
    if pendiente.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    pendiente.completado = not pendiente.completado
    
    if pendiente.completado:
        pendiente.fecha_completado = datetime.utcnow()
    else:
        pendiente.fecha_completado = None
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Pendiente actualizado',
        'pendiente': pendiente.to_dict()
    }), 200

@bp.route('/<int:pendiente_id>', methods=['DELETE'])
@login_required
def eliminar(pendiente_id):
    """Eliminar pendiente"""
    pendiente = Pendiente.query.get_or_404(pendiente_id)
    
    if pendiente.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    db.session.delete(pendiente)
    db.session.commit()
    
    return jsonify({'mensaje': 'Pendiente eliminado'}), 200
