from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import GastoCompartido, GastoPersonal, Usuario, Pareja
from app.services import CalculadoraAportes
from app.utils.validators import validar_monto, validar_categoria_gasto

bp = Blueprint('gastos', __name__, url_prefix='/gastos')

@bp.route('/compartidos', methods=['GET'])
@login_required
def listar_compartidos():
    """Listar gastos compartidos de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    gastos = GastoCompartido.query.filter_by(pareja_id=current_user.pareja_id).order_by(GastoCompartido.fecha.desc()).all()
    
    return jsonify({
        'gastos': [gasto.to_dict(current_user.id) for gasto in gastos]
    }), 200

@bp.route('/compartidos', methods=['POST'])
@login_required
def crear_compartido():
    """Crear gasto compartido"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    data = request.get_json() if request.is_json else request.form
    
    nombre = data.get('nombre', '').strip()
    monto_total = float(data.get('monto_total', 0))
    categoria = data.get('categoria', '').strip().lower()
    notas = data.get('notas', '').strip()
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    
    valido, mensaje = validar_monto(monto_total)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    if not validar_categoria_gasto(categoria):
        return jsonify({'error': 'Categoría inválida'}), 400
    
    # Obtener pareja y calcular aportes
    pareja = Pareja.query.get(current_user.pareja_id)
    usuario1 = Usuario.query.get(pareja.usuario1_id)
    usuario2 = Usuario.query.get(pareja.usuario2_id)
    
    aportes = CalculadoraAportes.calcular_aportes(
        usuario1.ingreso_mensual,
        usuario2.ingreso_mensual,
        monto_total
    )
    
    # Crear gasto
    gasto = GastoCompartido(
        pareja_id=current_user.pareja_id,
        nombre=nombre,
        monto_total=monto_total,
        categoria=categoria,
        notas=notas,
        creado_por=current_user.id,
        aporte_usuario1=aportes['aporte_usuario1'],
        aporte_usuario2=aportes['aporte_usuario2']
    )
    
    db.session.add(gasto)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Gasto compartido creado exitosamente',
        'gasto': gasto.to_dict(current_user.id)
    }), 201

@bp.route('/compartidos/<int:gasto_id>', methods=['DELETE'])
@login_required
def eliminar_compartido(gasto_id):
    """Eliminar gasto compartido"""
    gasto = GastoCompartido.query.get_or_404(gasto_id)
    
    if gasto.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso para eliminar este gasto'}), 403
    
    db.session.delete(gasto)
    db.session.commit()
    
    return jsonify({'mensaje': 'Gasto eliminado exitosamente'}), 200

@bp.route('/personales', methods=['GET'])
@login_required
def listar_personales():
    """Listar gastos personales del usuario"""
    gastos = GastoPersonal.query.filter_by(usuario_id=current_user.id).order_by(GastoPersonal.fecha.desc()).all()
    
    return jsonify({
        'gastos': [gasto.to_dict() for gasto in gastos]
    }), 200

@bp.route('/personales', methods=['POST'])
@login_required
def crear_personal():
    """Crear gasto personal"""
    data = request.get_json() if request.is_json else request.form
    
    nombre = data.get('nombre', '').strip()
    monto = float(data.get('monto', 0))
    categoria = data.get('categoria', '').strip().lower()
    notas = data.get('notas', '').strip()
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    
    valido, mensaje = validar_monto(monto)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    if not validar_categoria_gasto(categoria):
        return jsonify({'error': 'Categoría inválida'}), 400
    
    # Crear gasto
    gasto = GastoPersonal(
        usuario_id=current_user.id,
        nombre=nombre,
        monto=monto,
        categoria=categoria,
        notas=notas
    )
    
    db.session.add(gasto)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Gasto personal creado exitosamente',
        'gasto': gasto.to_dict()
    }), 201

@bp.route('/personales/<int:gasto_id>', methods=['DELETE'])
@login_required
def eliminar_personal(gasto_id):
    """Eliminar gasto personal"""
    gasto = GastoPersonal.query.get_or_404(gasto_id)
    
    if gasto.usuario_id != current_user.id:
        return jsonify({'error': 'No tienes permiso para eliminar este gasto'}), 403
    
    db.session.delete(gasto)
    db.session.commit()
    
    return jsonify({'mensaje': 'Gasto eliminado exitosamente'}), 200

@bp.route('/semaforo', methods=['GET'])
@login_required
def semaforo_financiero():
    """Obtener estado del semáforo financiero"""
    # Calcular gastos del mes actual
    from datetime import datetime
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    # Gastos compartidos
    gastos_compartidos = GastoCompartido.query.filter_by(pareja_id=current_user.pareja_id).all()
    
    total_compartidos = 0
    pareja = Pareja.query.get(current_user.pareja_id)
    for gasto in gastos_compartidos:
        if gasto.fecha.month == mes_actual and gasto.fecha.year == año_actual:
            if pareja.usuario1_id == current_user.id:
                total_compartidos += gasto.aporte_usuario1
            else:
                total_compartidos += gasto.aporte_usuario2
    
    # Gastos personales
    gastos_personales = GastoPersonal.query.filter_by(usuario_id=current_user.id).all()
    total_personales = sum(
        gasto.monto for gasto in gastos_personales
        if gasto.fecha.month == mes_actual and gasto.fecha.year == año_actual
    )
    
    total_gastos = total_compartidos + total_personales
    
    # Calcular semáforo
    semaforo = CalculadoraAportes.calcular_semaforo_financiero(
        total_gastos,
        current_user.ingreso_mensual
    )
    
    return jsonify({
        'semaforo': semaforo,
        'total_gastos': total_gastos,
        'gastos_compartidos': total_compartidos,
        'gastos_personales': total_personales
    }), 200
