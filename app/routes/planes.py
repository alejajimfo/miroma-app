from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import PlanFuturo, ItemPlan, Usuario, Pareja
from app.services import CalculadoraAportes
from app.utils.validators import validar_tipo_plan, validar_estado_item, validar_monto

bp = Blueprint('planes', __name__, url_prefix='/planes')

# Plantillas de items por tipo de plan
PLANTILLAS_PLANES = {
    'viaje': [
        'Vuelos', 'Alojamiento', 'Transporte local',
        'Comidas', 'Actividades/Tours', 'Extras'
    ],
    'vehiculo': [
        'Valor del vehículo', 'SOAT', 'Tecnomecánica',
        'Seguro', 'Gasolina primer mes', 'Mantenimiento', 'Imprevistos'
    ],
    'hogar': [
        'Muebles', 'Electrodomésticos', 'Decoración',
        'Remodelación', 'Herramientas', 'Imprevistos'
    ],
    'evento': [
        'Lugar/Venue', 'Catering', 'Decoración',
        'Música/Entretenimiento', 'Invitaciones', 'Fotografía/Video', 'Extras'
    ],
    'personalizado': []
}

@bp.route('/', methods=['GET'])
@login_required
def listar():
    """Listar planes de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    planes = PlanFuturo.query.filter_by(pareja_id=current_user.pareja_id).all()
    
    return jsonify({
        'planes': [plan.to_dict(current_user.id) for plan in planes]
    }), 200

@bp.route('/', methods=['POST'])
@login_required
def crear():
    """Crear plan futuro"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a una pareja'}), 400
    
    data = request.get_json() if request.is_json else request.form
    
    nombre = data.get('nombre', '').strip()
    tipo = data.get('tipo', '').strip().lower()
    fecha_objetivo = data.get('fecha_objetivo')
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    
    if not validar_tipo_plan(tipo):
        return jsonify({'error': 'Tipo de plan inválido'}), 400
    
    # Crear plan
    plan = PlanFuturo(
        pareja_id=current_user.pareja_id,
        nombre=nombre,
        tipo=tipo
    )
    
    if fecha_objetivo:
        plan.fecha_objetivo = datetime.fromisoformat(fecha_objetivo.replace('Z', '+00:00'))
    
    db.session.add(plan)
    db.session.flush()  # Para obtener el ID
    
    # Agregar items predefinidos según el tipo
    items_plantilla = PLANTILLAS_PLANES.get(tipo, [])
    for nombre_item in items_plantilla:
        item = ItemPlan(
            plan_id=plan.id,
            nombre=nombre_item,
            monto_estimado=0.0,
            estado='pendiente'
        )
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Plan creado exitosamente',
        'plan': plan.to_dict(current_user.id)
    }), 201

@bp.route('/<int:plan_id>/items', methods=['POST'])
@login_required
def agregar_item(plan_id):
    """Agregar item a plan"""
    plan = PlanFuturo.query.get_or_404(plan_id)
    
    if plan.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    data = request.get_json() if request.is_json else request.form
    
    nombre = data.get('nombre', '').strip()
    monto_estimado = float(data.get('monto_estimado', 0))
    
    # Validaciones
    if not nombre:
        return jsonify({'error': 'El nombre es requerido'}), 400
    
    valido, mensaje = validar_monto(monto_estimado)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Calcular aportes
    pareja = Pareja.query.get(current_user.pareja_id)
    usuario1 = Usuario.query.get(pareja.usuario1_id)
    usuario2 = Usuario.query.get(pareja.usuario2_id)
    
    aportes = CalculadoraAportes.calcular_aportes(
        usuario1.ingreso_mensual,
        usuario2.ingreso_mensual,
        monto_estimado
    )
    
    # Crear item
    item = ItemPlan(
        plan_id=plan_id,
        nombre=nombre,
        monto_estimado=monto_estimado,
        estado='pendiente',
        aporte_usuario1=aportes['aporte_usuario1'],
        aporte_usuario2=aportes['aporte_usuario2']
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Item agregado exitosamente',
        'item': item.to_dict(current_user.id)
    }), 201

@bp.route('/<int:plan_id>/items/<int:item_id>', methods=['PUT'])
@login_required
def actualizar_item(plan_id, item_id):
    """Actualizar item de plan"""
    plan = PlanFuturo.query.get_or_404(plan_id)
    
    if plan.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    item = ItemPlan.query.get_or_404(item_id)
    
    if item.plan_id != plan_id:
        return jsonify({'error': 'Item no pertenece a este plan'}), 400
    
    data = request.get_json() if request.is_json else request.form
    
    # Actualizar campos
    if 'estado' in data:
        estado = data['estado'].lower()
        if not validar_estado_item(estado):
            return jsonify({'error': 'Estado inválido'}), 400
        item.estado = estado
        
        if estado == 'pagado':
            item.fecha_pago = datetime.utcnow()
    
    if 'monto_real' in data:
        item.monto_real = float(data['monto_real'])
    
    if 'notas' in data:
        item.notas = data['notas']
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Item actualizado exitosamente',
        'item': item.to_dict(current_user.id)
    }), 200

@bp.route('/<int:plan_id>', methods=['GET'])
@login_required
def obtener(plan_id):
    """Obtener detalle de un plan"""
    plan = PlanFuturo.query.get_or_404(plan_id)
    
    if plan.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    return jsonify({
        'plan': plan.to_dict(current_user.id)
    }), 200

@bp.route('/<int:plan_id>', methods=['DELETE'])
@login_required
def eliminar(plan_id):
    """Eliminar plan"""
    plan = PlanFuturo.query.get_or_404(plan_id)
    
    if plan.pareja_id != current_user.pareja_id:
        return jsonify({'error': 'No tienes permiso'}), 403
    
    db.session.delete(plan)
    db.session.commit()
    
    return jsonify({'mensaje': 'Plan eliminado exitosamente'}), 200
