from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario, Pareja
from app.utils.validators import validar_email, validar_password

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevo usuario"""
    if request.method == 'GET':
        return render_template('auth/registro.html')
    
    data = request.get_json() if request.is_json else request.form
    
    # Validar datos
    email = data.get('email', '').strip()
    password = data.get('password', '')
    apodo = data.get('apodo', '').strip()
    rol = data.get('rol', '').strip()
    ingreso_mensual = float(data.get('ingreso_mensual', 0))
    
    # Validaciones
    if not validar_email(email):
        return jsonify({'error': 'Email inválido'}), 400
    
    valido, mensaje = validar_password(password)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    if rol not in ['esposa', 'esposo']:
        return jsonify({'error': 'Rol inválido'}), 400
    
    # Verificar si el email ya existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    # Crear usuario
    usuario = Usuario(
        email=email,
        apodo=apodo,
        rol=rol,
        ingreso_mensual=ingreso_mensual
    )
    usuario.set_password(password)
    
    db.session.add(usuario)
    db.session.commit()
    
    # Login automático
    login_user(usuario)
    
    # Crear token JWT
    access_token = create_access_token(identity=usuario.id)
    
    return jsonify({
        'mensaje': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict(),
        'access_token': access_token
    }), 201

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login de usuario"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.get_json() if request.is_json else request.form
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not usuario.check_password(password):
        return jsonify({'error': 'Email o contraseña incorrectos'}), 401
    
    login_user(usuario)
    
    # Crear token JWT
    access_token = create_access_token(identity=usuario.id)
    
    return jsonify({
        'mensaje': 'Login exitoso',
        'usuario': usuario.to_dict(),
        'access_token': access_token
    }), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout de usuario"""
    logout_user()
    return jsonify({'mensaje': 'Logout exitoso'}), 200

@bp.route('/generar-codigo', methods=['POST'])
@login_required
def generar_codigo():
    """Generar código de vinculación"""
    if current_user.pareja_id:
        return jsonify({'error': 'Ya estás vinculado a una pareja'}), 400
    
    # Crear nueva pareja
    pareja = Pareja(
        codigo_vinculacion=Pareja.generar_codigo(),
        usuario1_id=current_user.id
    )
    
    db.session.add(pareja)
    db.session.commit()
    
    # Actualizar usuario
    current_user.pareja_id = pareja.id
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Código generado exitosamente',
        'codigo': pareja.codigo_vinculacion,
        'pareja_id': pareja.id
    }), 201

@bp.route('/vincular', methods=['POST'])
@login_required
def vincular():
    """Vincular con pareja usando código"""
    if current_user.pareja_id:
        return jsonify({'error': 'Ya estás vinculado a una pareja'}), 400
    
    data = request.get_json() if request.is_json else request.form
    codigo = data.get('codigo', '').strip()
    
    # Buscar pareja con ese código
    pareja = Pareja.query.filter_by(codigo_vinculacion=codigo, activo=False).first()
    
    if not pareja:
        return jsonify({'error': 'Código inválido o expirado'}), 404
    
    # Verificar que no sea el mismo usuario
    if pareja.usuario1_id == current_user.id:
        return jsonify({'error': 'No puedes vincularte contigo mismo'}), 400
    
    # Vincular
    pareja.usuario2_id = current_user.id
    pareja.activo = True
    from datetime import datetime
    pareja.fecha_vinculacion = datetime.utcnow()
    
    current_user.pareja_id = pareja.id
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Vinculación exitosa',
        'pareja': pareja.to_dict()
    }), 200

@bp.route('/perfil', methods=['GET'])
@login_required
def perfil():
    """Obtener perfil del usuario actual"""
    return jsonify({
        'usuario': current_user.to_dict(include_private=True)
    }), 200

@bp.route('/actualizar-ingreso', methods=['PUT'])
@login_required
def actualizar_ingreso():
    """Actualizar ingreso mensual (privado)"""
    data = request.get_json() if request.is_json else request.form
    ingreso = float(data.get('ingreso_mensual', 0))
    
    if ingreso < 0:
        return jsonify({'error': 'El ingreso no puede ser negativo'}), 400
    
    current_user.ingreso_mensual = ingreso
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Ingreso actualizado exitosamente',
        'ingreso_mensual': ingreso
    }), 200

@bp.route('/actualizar-perfil', methods=['PUT'])
@login_required
def actualizar_perfil():
    """Actualizar apodo del usuario"""
    data = request.get_json() if request.is_json else request.form
    apodo = data.get('apodo', '').strip()
    
    if not apodo:
        return jsonify({'error': 'El apodo no puede estar vacío'}), 400
    
    if len(apodo) > 50:
        return jsonify({'error': 'El apodo es demasiado largo'}), 400
    
    current_user.apodo = apodo
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Perfil actualizado exitosamente',
        'apodo': apodo
    }), 200

@bp.route('/cambiar-password', methods=['PUT'])
@login_required
def cambiar_password():
    """Cambiar contraseña del usuario"""
    data = request.get_json() if request.is_json else request.form
    password_actual = data.get('password_actual', '')
    password_nueva = data.get('password_nueva', '')
    
    # Verificar contraseña actual
    if not current_user.check_password(password_actual):
        return jsonify({'error': 'La contraseña actual es incorrecta'}), 401
    
    # Validar nueva contraseña
    valido, mensaje = validar_password(password_nueva)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Actualizar contraseña
    current_user.set_password(password_nueva)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Contraseña cambiada exitosamente'
    }), 200

@bp.route('/desvincular', methods=['POST'])
@login_required
def desvincular():
    """Desvincular de la pareja"""
    if not current_user.pareja_id:
        return jsonify({'error': 'No estás vinculado a ninguna pareja'}), 400
    
    pareja = Pareja.query.get(current_user.pareja_id)
    
    if pareja:
        # Desactivar la pareja
        pareja.activo = False
        
        # Desvincular ambos usuarios
        usuario1 = Usuario.query.get(pareja.usuario1_id)
        usuario2 = Usuario.query.get(pareja.usuario2_id)
        
        if usuario1:
            usuario1.pareja_id = None
        if usuario2:
            usuario2.pareja_id = None
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Desvinculación exitosa'
    }), 200

@bp.route('/eliminar-cuenta', methods=['DELETE'])
@login_required
def eliminar_cuenta():
    """Eliminar cuenta del usuario (permanente)"""
    usuario_id = current_user.id
    pareja_id = current_user.pareja_id
    
    # Si está vinculado, desvincular primero
    if pareja_id:
        pareja = Pareja.query.get(pareja_id)
        if pareja:
            # Desvincular al otro usuario
            if pareja.usuario1_id == usuario_id:
                otro_usuario = Usuario.query.get(pareja.usuario2_id)
            else:
                otro_usuario = Usuario.query.get(pareja.usuario1_id)
            
            if otro_usuario:
                otro_usuario.pareja_id = None
            
            pareja.activo = False
    
    # Eliminar gastos personales del usuario
    from app.models import GastoPersonal
    GastoPersonal.query.filter_by(usuario_id=usuario_id).delete()
    
    # Logout
    logout_user()
    
    # Eliminar usuario
    db.session.delete(current_user)
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Cuenta eliminada exitosamente'
    }), 200

@bp.route('/subir-foto', methods=['POST'])
@login_required
def subir_foto():
    """Subir foto de perfil"""
    import os
    import base64
    from werkzeug.utils import secure_filename
    
    if 'foto' not in request.files:
        return jsonify({'error': 'No se envió ninguna foto'}), 400
    
    file = request.files['foto']
    
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
    
    # Validar tipo de archivo
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400
    
    # Leer archivo y convertir a base64
    file_data = file.read()
    file_base64 = base64.b64encode(file_data).decode('utf-8')
    file_ext = file.filename.rsplit('.', 1)[1].lower()
    
    # Guardar como data URL
    foto_url = f"data:image/{file_ext};base64,{file_base64}"
    
    # Actualizar usuario
    current_user.foto_perfil = foto_url
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Foto actualizada exitosamente',
        'foto_url': foto_url
    }), 200

@bp.route('/recuperar-password', methods=['POST'])
def recuperar_password():
    """Generar código de recuperación de contraseña"""
    import random
    import string
    from datetime import datetime, timedelta
    from flask_mail import Message
    from app import mail
    import os
    
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'error': 'Email requerido'}), 400
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        # Por seguridad, no revelar si el email existe o no
        return jsonify({
            'mensaje': 'Si el email existe, recibirás un código de recuperación'
        }), 200
    
    # Generar código de 6 dígitos
    codigo = ''.join(random.choices(string.digits, k=6))
    
    # Guardar código y expiración (15 minutos)
    usuario.codigo_recuperacion = codigo
    usuario.codigo_recuperacion_expira = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()
    
    # Intentar enviar email
    email_enviado = False
    if os.getenv('MAIL_USERNAME'):
        try:
            msg = Message(
                subject='Código de Recuperación - Miroma',
                recipients=[email],
                html=f'''
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="text-align: center; margin-bottom: 30px;">
                        <h1 style="color: #FF69B4; font-size: 2rem;">💜 Miroma</h1>
                    </div>
                    
                    <div style="background: #f5f0f5; padding: 30px; border-radius: 15px;">
                        <h2 style="color: #333; margin-bottom: 20px;">Recuperación de Contraseña</h2>
                        
                        <p style="color: #666; font-size: 1rem; line-height: 1.6;">
                            Hola <strong>{usuario.apodo}</strong>,
                        </p>
                        
                        <p style="color: #666; font-size: 1rem; line-height: 1.6;">
                            Recibimos una solicitud para restablecer tu contraseña. 
                            Usa el siguiente código de verificación:
                        </p>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0;">
                            <p style="color: #999; font-size: 0.875rem; margin-bottom: 10px;">
                                Código de verificación:
                            </p>
                            <h1 style="color: #FF69B4; font-size: 3rem; letter-spacing: 10px; margin: 0;">
                                {codigo}
                            </h1>
                        </div>
                        
                        <p style="color: #666; font-size: 0.875rem; line-height: 1.6;">
                            ⏰ Este código expira en <strong>15 minutos</strong>
                        </p>
                        
                        <p style="color: #666; font-size: 0.875rem; line-height: 1.6; margin-top: 20px;">
                            Si no solicitaste este cambio, ignora este mensaje.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; color: #999; font-size: 0.75rem;">
                        <p>Miroma - Gestiona tus finanzas en pareja 💑</p>
                    </div>
                </div>
                '''
            )
            mail.send(msg)
            email_enviado = True
        except Exception as e:
            print(f'Error enviando email: {e}')
    
    # Respuesta
    response = {
        'mensaje': 'Código de recuperación generado',
        'email_enviado': email_enviado
    }
    
    # Solo en desarrollo, mostrar el código
    if os.getenv('FLASK_ENV') == 'development' or not email_enviado:
        response['codigo'] = codigo
    
    return jsonify(response), 200

@bp.route('/verificar-codigo-recuperacion', methods=['POST'])
def verificar_codigo_recuperacion():
    """Verificar código de recuperación"""
    from datetime import datetime
    
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip()
    codigo = data.get('codigo', '').strip()
    
    if not email or not codigo:
        return jsonify({'error': 'Email y código requeridos'}), 400
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({'error': 'Código inválido o expirado'}), 400
    
    # Verificar código y expiración
    if usuario.codigo_recuperacion != codigo:
        return jsonify({'error': 'Código inválido'}), 400
    
    if not usuario.codigo_recuperacion_expira or usuario.codigo_recuperacion_expira < datetime.utcnow():
        return jsonify({'error': 'Código expirado'}), 400
    
    return jsonify({
        'mensaje': 'Código verificado correctamente',
        'email': email
    }), 200

@bp.route('/restablecer-password', methods=['POST'])
def restablecer_password():
    """Restablecer contraseña con código de recuperación"""
    from datetime import datetime
    
    data = request.get_json() if request.is_json else request.form
    email = data.get('email', '').strip()
    codigo = data.get('codigo', '').strip()
    password_nueva = data.get('password_nueva', '')
    
    if not email or not codigo or not password_nueva:
        return jsonify({'error': 'Todos los campos son requeridos'}), 400
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario:
        return jsonify({'error': 'Código inválido o expirado'}), 400
    
    # Verificar código y expiración
    if usuario.codigo_recuperacion != codigo:
        return jsonify({'error': 'Código inválido'}), 400
    
    if not usuario.codigo_recuperacion_expira or usuario.codigo_recuperacion_expira < datetime.utcnow():
        return jsonify({'error': 'Código expirado'}), 400
    
    # Validar nueva contraseña
    valido, mensaje = validar_password(password_nueva)
    if not valido:
        return jsonify({'error': mensaje}), 400
    
    # Actualizar contraseña
    usuario.set_password(password_nueva)
    
    # Limpiar código de recuperación
    usuario.codigo_recuperacion = None
    usuario.codigo_recuperacion_expira = None
    
    db.session.commit()
    
    return jsonify({
        'mensaje': 'Contraseña restablecida exitosamente'
    }), 200
