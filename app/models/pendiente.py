from datetime import datetime
from app import db

class Pendiente(db.Model):
    """Modelo de Pendiente (Checklist)"""
    __tablename__ = 'pendientes'
    
    id = db.Column(db.Integer, primary_key=True)
    pareja_id = db.Column(db.Integer, db.ForeignKey('parejas.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)  # hogar, tramites, eventos, familia
    completado = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_completado = db.Column(db.DateTime)
    recordatorio = db.Column(db.DateTime)
    notas = db.Column(db.Text)
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Relaciones
    pareja = db.relationship('Pareja', back_populates='pendientes')
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'categoria': self.categoria,
            'completado': self.completado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_completado': self.fecha_completado.isoformat() if self.fecha_completado else None,
            'recordatorio': self.recordatorio.isoformat() if self.recordatorio else None,
            'notas': self.notas,
        }
    
    def __repr__(self):
        return f'<Pendiente {self.titulo}>'
