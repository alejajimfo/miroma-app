from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Deuda, AbonoDeuda

bp = Blueprint('deudas', __name__, url_prefix='/deudas')

@bp.route('/', methods=['GET'])
@login_required
def listar_deudas():
    """Listar todas las deudas del usuario"""
    try:
        deudas = Deuda.query.filter_by(usuario_id=current_user.id).order_by(Deuda.fecha_creacion.desc()).all()
        
        # Separar por tipo
        debo = [d.to_dict() for d in deudas if d.tipo == 'debo']
        me_deben = [d.to_dict() for d in deudas if d.tipo == 'me_deben']
        
        # Calcular totales
        total_debo = sum(d['monto_pendiente'] for d in debo if d['estado'] == 'pendiente')
        total_me_deben = sum(d['monto_pendiente'] for d in me_deben if d['estado'] == 'pendiente')
        
        return jsonify({
            'deudas': {
                'debo': debo,
                'me_deben': me_deben
            },
            'totales': {
                'debo': total_debo,
                'me_deben': total_me_deben,
                'balance': total_me_deben - total_debo
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
@login_required
def crear_deuda():
    """Crear nueva deuda"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['descripcion', 'monto', 'tipo', 'persona']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        # Validar tipo
        if data['tipo'] not in ['debo', 'me_deben']:
            return jsonify({'error': 'Tipo debe ser "debo" o "me_deben"'}), 400
        
        # Validar monto
        try:
            monto = float(data['monto'])
            if monto <= 0:
                return jsonify({'error': 'El monto debe ser mayor a 0'}), 400
        except ValueError:
            return jsonify({'error': 'Monto inválido'}), 400
        
        # Crear deuda
        deuda = Deuda(
            usuario_id=current_user.id,
            descripcion=data['descripcion'].strip(),
            monto_original=monto,
            monto_pendiente=monto,
            tipo=data['tipo'],
            persona=data['persona'].strip(),
            fecha_vencimiento=datetime.strptime(data['fecha_vencimiento'], '%Y-%m-%d').date() if data.get('fecha_vencimiento') else None
        )
        
        db.session.add(deuda)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Deuda creada exitosamente',
            'deuda': deuda.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:deuda_id>/abono', methods=['POST'])
@login_required
def agregar_abono(deuda_id):
    """Agregar abono a una deuda"""
    try:
        deuda = Deuda.query.filter_by(id=deuda_id, usuario_id=current_user.id).first()
        if not deuda:
            return jsonify({'error': 'Deuda no encontrada'}), 404
        
        if deuda.estado == 'pagada':
            return jsonify({'error': 'La deuda ya está pagada'}), 400
        
        data = request.get_json()
        
        # Validar monto
        try:
            monto_abono = float(data.get('monto', 0))
            if monto_abono <= 0:
                return jsonify({'error': 'El monto del abono debe ser mayor a 0'}), 400
            if monto_abono > deuda.monto_pendiente:
                return jsonify({'error': 'El abono no puede ser mayor al monto pendiente'}), 400
        except ValueError:
            return jsonify({'error': 'Monto inválido'}), 400
        
        # Crear abono
        abono = AbonoDeuda(
            deuda_id=deuda.id,
            monto=monto_abono,
            descripcion=data.get('descripcion', '').strip()
        )
        
        # Actualizar monto pendiente
        deuda.monto_pendiente -= monto_abono
        
        # Si se pagó completamente, marcar como pagada
        if deuda.monto_pendiente <= 0:
            deuda.estado = 'pagada'
            deuda.fecha_pago_completo = datetime.utcnow()
            deuda.monto_pendiente = 0
        
        db.session.add(abono)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Abono agregado exitosamente',
            'deuda': deuda.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:deuda_id>/marcar-pagada', methods=['PUT'])
@login_required
def marcar_pagada(deuda_id):
    """Marcar deuda como pagada completamente"""
    try:
        deuda = Deuda.query.filter_by(id=deuda_id, usuario_id=current_user.id).first()
        if not deuda:
            return jsonify({'error': 'Deuda no encontrada'}), 404
        
        if deuda.estado == 'pagada':
            return jsonify({'error': 'La deuda ya está pagada'}), 400
        
        # Si hay monto pendiente, crear un abono por el resto
        if deuda.monto_pendiente > 0:
            abono = AbonoDeuda(
                deuda_id=deuda.id,
                monto=deuda.monto_pendiente,
                descripcion='Pago completo'
            )
            db.session.add(abono)
        
        # Marcar como pagada
        deuda.estado = 'pagada'
        deuda.monto_pendiente = 0
        deuda.fecha_pago_completo = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Deuda marcada como pagada',
            'deuda': deuda.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:deuda_id>/reactivar', methods=['PUT'])
@login_required
def reactivar_deuda(deuda_id):
    """Reactivar una deuda pagada (deshacer pago)"""
    try:
        deuda = Deuda.query.filter_by(id=deuda_id, usuario_id=current_user.id).first()
        if not deuda:
            return jsonify({'error': 'Deuda no encontrada'}), 404
        
        if deuda.estado != 'pagada':
            return jsonify({'error': 'La deuda no está pagada'}), 400
        
        # Eliminar el último abono (pago completo)
        ultimo_abono = AbonoDeuda.query.filter_by(deuda_id=deuda.id).order_by(AbonoDeuda.fecha_abono.desc()).first()
        if ultimo_abono and ultimo_abono.descripcion == 'Pago completo':
            db.session.delete(ultimo_abono)
        
        # Recalcular monto pendiente
        total_abonos = sum(abono.monto for abono in deuda.abonos if abono != ultimo_abono)
        deuda.monto_pendiente = deuda.monto_original - total_abonos
        
        # Reactivar deuda
        deuda.estado = 'pendiente'
        deuda.fecha_pago_completo = None
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Deuda reactivada exitosamente',
            'deuda': deuda.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:deuda_id>', methods=['DELETE'])
@login_required
def eliminar_deuda(deuda_id):
    """Eliminar una deuda"""
    try:
        deuda = Deuda.query.filter_by(id=deuda_id, usuario_id=current_user.id).first()
        if not deuda:
            return jsonify({'error': 'Deuda no encontrada'}), 404
        
        db.session.delete(deuda)
        db.session.commit()
        
        return jsonify({'mensaje': 'Deuda eliminada exitosamente'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:deuda_id>/abonos/<int:abono_id>', methods=['DELETE'])
@login_required
def eliminar_abono(deuda_id, abono_id):
    """Eliminar un abono específico"""
    try:
        deuda = Deuda.query.filter_by(id=deuda_id, usuario_id=current_user.id).first()
        if not deuda:
            return jsonify({'error': 'Deuda no encontrada'}), 404
        
        abono = AbonoDeuda.query.filter_by(id=abono_id, deuda_id=deuda_id).first()
        if not abono:
            return jsonify({'error': 'Abono no encontrado'}), 404
        
        # Restaurar monto pendiente
        deuda.monto_pendiente += abono.monto
        
        # Si estaba pagada, reactivar
        if deuda.estado == 'pagada':
            deuda.estado = 'pendiente'
            deuda.fecha_pago_completo = None
        
        db.session.delete(abono)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Abono eliminado exitosamente',
            'deuda': deuda.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500