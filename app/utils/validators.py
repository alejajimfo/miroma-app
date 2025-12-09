import re
from email_validator import validate_email, EmailNotValidError

def validar_email(email):
    """Validar formato de email"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validar_password(password):
    """
    Validar contraseña:
    - Mínimo 8 caracteres
    - Al menos una letra
    - Al menos un número
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[a-zA-Z]', password):
        return False, "La contraseña debe contener al menos una letra"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, "Contraseña válida"

def validar_monto(monto):
    """Validar que el monto sea positivo"""
    try:
        monto_float = float(monto)
        if monto_float <= 0:
            return False, "El monto debe ser mayor a 0"
        return True, "Monto válido"
    except (ValueError, TypeError):
        return False, "Monto inválido"

def validar_categoria_gasto(categoria):
    """Validar categoría de gasto"""
    categorias_validas = [
        'hogar', 'comida', 'transporte', 'salud',
        'entretenimiento', 'educacion', 'ropa', 'otros'
    ]
    return categoria.lower() in categorias_validas

def validar_categoria_pendiente(categoria):
    """Validar categoría de pendiente"""
    categorias_validas = ['hogar', 'tramites', 'eventos', 'familia']
    return categoria.lower() in categorias_validas

def validar_tipo_plan(tipo):
    """Validar tipo de plan"""
    tipos_validos = ['viaje', 'vehiculo', 'hogar', 'evento', 'personalizado']
    return tipo.lower() in tipos_validos

def validar_estado_item(estado):
    """Validar estado de item de plan"""
    estados_validos = ['pendiente', 'en_progreso', 'pagado']
    return estado.lower() in estados_validos
