from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Usuario

bp = Blueprint('configuracion', __name__, url_prefix='/configuracion')

@bp.route('/perfil', methods=['PUT'])
@login_required
def actualizar_perfil():
    """Actualizar perfil del usuario"""
    data = request.get_json() if request.is_json else request.form
    
    if 'apodo' in data:
        apodo = data['apodo'].strip()
        if apodo:
            current_user.apodo = apodo
    
    if 'ingreso_mensual' in data:
        ingreso = float(data['ingreso_mensual'])
        if ingreso >= 0:
            current_user.ingreso_mensual = ingreso
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Perfil actualizado exitosamente',
        'usuario': current_user.to_dict(include_private=True)
    }), 200

@bp.route('/cambiar-password', methods=['PUT'])
@login_required
def cambiar_password():
    """Cambiar contraseña"""
    data = request.get_json() if request.is_json else request.form
    
    password_actual = data.get('password_actual', '')
    password_nueva = data.get('password_nueva', '')
    
    # Verificar contraseña actual
    if not current_user.check_password(password_actual):
        return jsonify({'error': 'Contraseña actual incorrecta'}), 400
    
    # Validar nueva contraseña
    from app.utils.validators import validar_password
    valido, mensaje = validar_password(password_nueva)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Actualizar contraseña
    current_user.set_password(password_nueva)
    db.session.commit()
    
    return jsonify({'mensaje': 'Contraseña actualizada exitosamente'}), 200

@bp.route('/desvincular', methods=['POST'])
@login_required
def desvincular():
    """Desvincular de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    current_user.pareja_id = None
    db.session.commit()
    
    return jsonify({'mensaje': 'Desvinculado exitosamente'}), 200
