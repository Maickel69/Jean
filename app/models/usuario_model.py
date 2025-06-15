from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_padre = db.Column(db.String(20), unique=True, nullable=True)  # Solo para padres
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    nombre_completo = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20))
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'padre', 'docente' o 'administrador'
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    estudiantes = db.relationship('Estudiante', backref='padre', lazy=True)
    chats_enviados = db.relationship('Chat', foreign_keys='Chat.emisor_id', backref='emisor', lazy=True)
    chats_recibidos = db.relationship('Chat', foreign_keys='Chat.receptor_id', backref='receptor', lazy=True)
    
    def generate_code_if_needed(self):
        """Genera código solo para padres si no lo tienen"""
        if self.tipo_usuario == 'padre' and not self.codigo_padre:
            from app.utils.code_generator import CodeGenerator
            self.codigo_padre = CodeGenerator.generate_parent_code()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        if self.tipo_usuario == 'padre' and self.codigo_padre:
            return f'<Usuario {self.codigo_padre} - {self.nombre_usuario}>'
        return f'<Usuario {self.nombre_usuario}>' 