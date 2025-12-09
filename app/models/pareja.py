from datetime import datetime
from app import db
import secrets

class Pareja(db.Model):
    """Modelo de Pareja"""
    __tablename__ = 'parejas'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_vinculacion = db.Column(db.String(6), unique=True, nullable=False)
    usuario1_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario2_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vinculacion = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=False)
    
    # Relaciones
    usuarios = db.relationship('Usuario', back_populates='pareja', foreign_keys='Usuario.pareja_id')
    gastos_compartidos = db.relationship('GastoCompartido', back_populates='pareja', lazy='dynamic')
    ahorros = db.relationship('Ahorro', back_populates='pareja', lazy='dynamic')
    planes = db.relationship('PlanFuturo', back_populates='pareja', lazy='dynamic')
    pendientes = db.relationship('Pendiente', back_populates='pareja', lazy='dynamic')
    
    @staticmethod
    def generar_codigo():
        """Generar código de 6 dígitos único"""
        while True:
            codigo = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
            if not Pareja.query.filter_by(codigo_vinculacion=codigo).first():
                return codigo
    
    def get_usuarios(self):
        """Obtener ambos usuarios de la pareja"""
        from app.models.usuario import Usuario
        usuarios = []
        if self.usuario1_id:
            usuarios.append(Usuario.query.get(self.usuario1_id))
        if self.usuario2_id:
            usuarios.append(Usuario.query.get(self.usuario2_id))
        return usuarios
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'codigo_vinculacion': self.codigo_vinculacion,
            'usuario1_id': self.usuario1_id,
            'usuario2_id': self.usuario2_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_vinculacion': self.fecha_vinculacion.isoformat() if self.fecha_vinculacion else None,
            'activo': self.activo,
        }
    
    def __repr__(self):
        return f'<Pareja {self.codigo_vinculacion}>'
