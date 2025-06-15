from datetime import datetime
from app import db

class Chat(db.Model):
    __tablename__ = 'chats'
    
    id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))  # Opcional, para contexto del curso
    asunto = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)
    fecha_lectura = db.Column(db.DateTime)
    importante = db.Column(db.Boolean, default=False)
    archivo_adjunto = db.Column(db.String(500))  # Ruta del archivo adjunto si existe
    
    # Relaciones
    curso = db.relationship('Curso', backref='chats')
    
    def marcar_como_leido(self):
        if not self.leido:
            self.leido = True
            self.fecha_lectura = datetime.utcnow()
    
    def tiempo_transcurrido(self):
        delta = datetime.utcnow() - self.fecha_envio
        
        if delta.days > 0:
            return f"hace {delta.days} día{'s' if delta.days > 1 else ''}"
        elif delta.seconds > 3600:
            horas = delta.seconds // 3600
            return f"hace {horas} hora{'s' if horas > 1 else ''}"
        elif delta.seconds > 60:
            minutos = delta.seconds // 60
            return f"hace {minutos} minuto{'s' if minutos > 1 else ''}"
        else:
            return "hace unos segundos"
    
    def __repr__(self):
        return f'<Chat {self.asunto} - {self.emisor.nombre_completo if self.emisor else "Sin emisor"}>' 