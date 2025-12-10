from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(UserMixin, db.Model):
    """Modelo de Usuario"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    apodo = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(10), nullable=False)  # 'esposa' o 'esposo'
    foto_perfil = db.Column(db.String(255))
    ingreso_mensual = db.Column(db.Float, default=0.0)  # PRIVADO
    pareja_id = db.Column(db.Integer, db.ForeignKey('parejas.id'))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Campos para recuperación de contraseña
    codigo_recuperacion = db.Column(db.String(10))
    codigo_recuperacion_expira = db.Column(db.DateTime)
    
    # Relaciones
    pareja = db.relationship('Pareja', back_populates='usuarios', foreign_keys=[pareja_id])
    gastos_personales = db.relationship('GastoPersonal', back_populates='usuario', lazy='dynamic')
    
    def set_password(self, password):
        """Hashear contraseña"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verificar contraseña - compatible con bcrypt y werkzeug"""
        try:
            # Intentar con bcrypt primero
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except ValueError:
            # Si falla, intentar con werkzeug (para usuarios antiguos)
            from werkzeug.security import check_password_hash
            return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_private=False):
        """Convertir a diccionario"""
        data = {
            'id': self.id,
            'email': self.email,
            'apodo': self.apodo,
            'rol': self.rol,
            'foto_perfil': self.foto_perfil,
            'pareja_id': self.pareja_id,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
        }
        if include_private:
            data['ingreso_mensual'] = self.ingreso_mensual
        return data
    
    def __repr__(self):
        return f'<Usuario {self.apodo}>'
