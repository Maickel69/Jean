from datetime import datetime
from app import db

class Asistencia(db.Model):
    __tablename__ = 'asistencias'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False)  # 'presente', 'ausente', 'tardanza', 'justificado'
    hora_llegada = db.Column(db.Time)
    observaciones = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def estado_display(self):
        estados = {
            'presente': 'Presente',
            'ausente': 'Ausente',
            'tardanza': 'Tardanza',
            'justificado': 'Justificado'
        }
        return estados.get(self.estado, self.estado)
    
    def color_estado(self):
        colores = {
            'presente': 'success',
            'ausente': 'danger',
            'tardanza': 'warning',
            'justificado': 'info'
        }
        return colores.get(self.estado, 'secondary')
    
    def __repr__(self):
        return f'<Asistencia {self.estudiante.nombre_completo if self.estudiante else "Sin estudiante"} - {self.fecha} - {self.estado}>' 