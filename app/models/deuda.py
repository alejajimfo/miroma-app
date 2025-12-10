from datetime import datetime
from app import db

class Deuda(db.Model):
    """Modelo para gestionar deudas"""
    __tablename__ = 'deudas'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Información básica de la deuda
    descripcion = db.Column(db.String(200), nullable=False)
    monto_original = db.Column(db.Float, nullable=False)
    monto_pendiente = db.Column(db.Float, nullable=False)
    
    # Tipo de deuda: 'debo' (yo debo) o 'me_deben' (me deben)
    tipo = db.Column(db.String(20), nullable=False)
    
    # A quién le debo o quién me debe
    persona = db.Column(db.String(100), nullable=False)
    
    # Estado: 'pendiente', 'pagada'
    estado = db.Column(db.String(20), default='pendiente')
    
    # Fechas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    fecha_pago_completo = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='deudas')
    abonos = db.relationship('AbonoDeuda', backref='deuda', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'monto_original': self.monto_original,
            'monto_pendiente': self.monto_pendiente,
            'tipo': self.tipo,
            'persona': self.persona,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_vencimiento': self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            'fecha_pago_completo': self.fecha_pago_completo.isoformat() if self.fecha_pago_completo else None,
            'total_abonos': sum(abono.monto for abono in self.abonos),
            'abonos': [abono.to_dict() for abono in self.abonos]
        }

class AbonoDeuda(db.Model):
    """Modelo para registrar abonos a deudas"""
    __tablename__ = 'abonos_deuda'
    
    id = db.Column(db.Integer, primary_key=True)
    deuda_id = db.Column(db.Integer, db.ForeignKey('deudas.id'), nullable=False)
    
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha_abono = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'monto': self.monto,
            'descripcion': self.descripcion,
            'fecha_abono': self.fecha_abono.isoformat() if self.fecha_abono else None
        }