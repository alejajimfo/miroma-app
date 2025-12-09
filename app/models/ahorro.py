from datetime import datetime
from app import db

class Ahorro(db.Model):
    """Modelo de Meta de Ahorro"""
    __tablename__ = 'ahorros'
    
    id = db.Column(db.Integer, primary_key=True)
    pareja_id = db.Column(db.Integer, db.ForeignKey('parejas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    meta_monto = db.Column(db.Float, nullable=False)
    monto_actual = db.Column(db.Float, default=0.0)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_objetivo = db.Column(db.DateTime)
    completado = db.Column(db.Boolean, default=False)
    
    # Relaciones
    pareja = db.relationship('Pareja', back_populates='ahorros')
    aportes = db.relationship('AporteAhorro', back_populates='ahorro', lazy='dynamic')
    
    @property
    def progreso(self):
        """Calcular progreso en porcentaje"""
        if self.meta_monto == 0:
            return 0
        return min((self.monto_actual / self.meta_monto) * 100, 100)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'meta_monto': self.meta_monto,
            'monto_actual': self.monto_actual,
            'progreso': round(self.progreso, 2),
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_objetivo': self.fecha_objetivo.isoformat() if self.fecha_objetivo else None,
            'completado': self.completado,
        }
    
    def __repr__(self):
        return f'<Ahorro {self.nombre}>'


class AporteAhorro(db.Model):
    """Modelo de Aporte a Ahorro"""
    __tablename__ = 'aportes_ahorro'
    
    id = db.Column(db.Integer, primary_key=True)
    ahorro_id = db.Column(db.Integer, db.ForeignKey('ahorros.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    
    # Relaciones
    ahorro = db.relationship('Ahorro', back_populates='aportes')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'monto': self.monto,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'notas': self.notas,
        }
    
    def __repr__(self):
        return f'<AporteAhorro {self.monto}>'
