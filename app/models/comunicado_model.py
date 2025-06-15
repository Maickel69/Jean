from datetime import datetime
from app import db

class Comunicado(db.Model):
    __tablename__ = 'comunicados'
    
    id = db.Column(db.Integer, primary_key=True)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(50), default='general')  # 'general', 'urgente', 'informativo', 'academico'
    dirigido_a = db.Column(db.String(50), default='padres')  # 'padres', 'estudiantes', 'todos'
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))  # Opcional, para comunicados específicos de curso
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)
    prioritario = db.Column(db.Boolean, default=False)
    
    # Relaciones
    curso = db.relationship('Curso', backref='comunicados')
    
    def tipo_display(self):
        tipos = {
            'general': 'General',
            'urgente': 'Urgente',
            'informativo': 'Informativo',
            'academico': 'Académico'
        }
        return tipos.get(self.tipo, self.tipo)
    
    def color_tipo(self):
        colores = {
            'general': 'primary',
            'urgente': 'danger',
            'informativo': 'info',
            'academico': 'success'
        }
        return colores.get(self.tipo, 'secondary')
    
    def esta_vigente(self):
        if not self.fecha_vencimiento:
            return True
        return datetime.utcnow() <= self.fecha_vencimiento
    
    def __repr__(self):
        return f'<Comunicado {self.titulo}>' 