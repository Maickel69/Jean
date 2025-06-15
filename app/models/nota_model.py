from datetime import datetime
from app import db

class Nota(db.Model):
    __tablename__ = 'notas'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    tipo_evaluacion = db.Column(db.String(50), nullable=False)  # 'examen', 'tarea', 'proyecto', etc.
    descripcion = db.Column(db.String(200), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)
    calificacion_maxima = db.Column(db.Float, default=20.0)
    periodo = db.Column(db.String(20), nullable=False)  # 'I Bimestre', 'II Bimestre', etc.
    fecha_evaluacion = db.Column(db.Date, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    
    def porcentaje(self):
        return (self.calificacion / self.calificacion_maxima) * 100 if self.calificacion_maxima > 0 else 0
    
    def estado(self):
        porcentaje = self.porcentaje()
        if porcentaje >= 70:
            return 'Aprobado'
        elif porcentaje >= 60:
            return 'Recuperación'
        else:
            return 'Desaprobado'
    
    def __repr__(self):
        return f'<Nota {self.descripcion} - {self.calificacion}/{self.calificacion_maxima}>' 