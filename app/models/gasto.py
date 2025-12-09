from datetime import datetime
from app import db

class GastoCompartido(db.Model):
    """Modelo de Gasto Compartido"""
    __tablename__ = 'gastos_compartidos'
    
    id = db.Column(db.Integer, primary_key=True)
    pareja_id = db.Column(db.Integer, db.ForeignKey('parejas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Aportes calculados (almacenados para histórico)
    aporte_usuario1 = db.Column(db.Float)
    aporte_usuario2 = db.Column(db.Float)
    
    # Relaciones
    pareja = db.relationship('Pareja', back_populates='gastos_compartidos')
    
    def to_dict(self, usuario_id=None):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'monto_total': self.monto_total,
            'categoria': self.categoria,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'notas': self.notas,
        }
        
        # Solo mostrar el aporte del usuario que consulta
        if usuario_id:
            pareja = self.pareja
            if pareja.usuario1_id == usuario_id:
                data['mi_aporte'] = self.aporte_usuario1
            elif pareja.usuario2_id == usuario_id:
                data['mi_aporte'] = self.aporte_usuario2
        
        return data
    
    def __repr__(self):
        return f'<GastoCompartido {self.nombre}>'


class GastoPersonal(db.Model):
    """Modelo de Gasto Personal (privado)"""
    __tablename__ = 'gastos_personales'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    notas = db.Column(db.Text)
    
    # Relaciones
    usuario = db.relationship('Usuario', back_populates='gastos_personales')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'monto': self.monto,
            'categoria': self.categoria,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'notas': self.notas,
        }
    
    def __repr__(self):
        return f'<GastoPersonal {self.nombre}>'
