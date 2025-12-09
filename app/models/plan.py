from datetime import datetime
from app import db

class PlanFuturo(db.Model):
    """Modelo de Plan Futuro"""
    __tablename__ = 'planes_futuros'
    
    id = db.Column(db.Integer, primary_key=True)
    pareja_id = db.Column(db.Integer, db.ForeignKey('parejas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # viaje, vehiculo, hogar, evento, personalizado
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_objetivo = db.Column(db.DateTime)
    
    # Relaciones
    pareja = db.relationship('Pareja', back_populates='planes')
    items = db.relationship('ItemPlan', back_populates='plan', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def monto_total(self):
        """Calcular monto total del plan"""
        return sum(item.monto_estimado for item in self.items)
    
    @property
    def progreso(self):
        """Calcular progreso en porcentaje"""
        total = self.monto_total
        if total == 0:
            return 0
        pagado = sum(item.monto_estimado for item in self.items if item.estado == 'pagado')
        return (pagado / total) * 100
    
    def to_dict(self, usuario_id=None):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'monto_total': self.monto_total,
            'progreso': round(self.progreso, 2),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_objetivo': self.fecha_objetivo.isoformat() if self.fecha_objetivo else None,
            'items': [item.to_dict(usuario_id) for item in self.items],
        }
    
    def __repr__(self):
        return f'<PlanFuturo {self.nombre}>'


class ItemPlan(db.Model):
    """Modelo de Item de Plan"""
    __tablename__ = 'items_plan'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('planes_futuros.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    monto_estimado = db.Column(db.Float, nullable=False)
    monto_real = db.Column(db.Float)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, en_progreso, pagado
    fecha_pago = db.Column(db.DateTime)
    notas = db.Column(db.Text)
    
    # Aportes calculados
    aporte_usuario1 = db.Column(db.Float)
    aporte_usuario2 = db.Column(db.Float)
    
    # Relaciones
    plan = db.relationship('PlanFuturo', back_populates='items')
    
    def to_dict(self, usuario_id=None):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'monto_estimado': self.monto_estimado,
            'monto_real': self.monto_real,
            'estado': self.estado,
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None,
            'notas': self.notas,
        }
        
        # Solo mostrar el aporte del usuario que consulta
        if usuario_id:
            pareja = self.plan.pareja
            if pareja.usuario1_id == usuario_id:
                data['mi_aporte'] = self.aporte_usuario1
            elif pareja.usuario2_id == usuario_id:
                data['mi_aporte'] = self.aporte_usuario2
        
        return data
    
    def __repr__(self):
        return f'<ItemPlan {self.nombre}>'
