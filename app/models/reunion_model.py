from datetime import datetime
from app import db

class Reunion(db.Model):
    __tablename__ = 'reuniones'
    
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_reunion = db.Column(db.DateTime, nullable=False)
    duracion_minutos = db.Column(db.Integer, default=60)
    modalidad = db.Column(db.String(20), default='presencial')  # 'presencial', 'virtual'
    lugar = db.Column(db.String(200))
    enlace_virtual = db.Column(db.String(500))
    estado = db.Column(db.String(20), default='programada')  # 'programada', 'realizada', 'cancelada'
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    recordatorio_enviado = db.Column(db.Boolean, default=False)
    
    def estado_display(self):
        estados = {
            'programada': 'Programada',
            'realizada': 'Realizada',
            'cancelada': 'Cancelada'
        }
        return estados.get(self.estado, self.estado)
    
    def color_estado(self):
        colores = {
            'programada': 'primary',
            'realizada': 'success',
            'cancelada': 'danger'
        }
        return colores.get(self.estado, 'secondary')
    
    def __repr__(self):
        return f'<Reunion {self.titulo} - {self.fecha_reunion}>' 