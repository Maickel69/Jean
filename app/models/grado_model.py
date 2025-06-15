from datetime import datetime
from app import db

class Grado(db.Model):
    __tablename__ = 'grados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)  # 1ro Primaria, 2do Secundaria, etc.
    nivel = db.Column(db.String(20), nullable=False)  # Primaria, Secundaria
    numero = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4, 5, 6
    secciones = db.Column(db.String(50), default='A,B,C')  # Secciones disponibles
    edad_minima = db.Column(db.Integer)
    edad_maxima = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_secciones_list(self):
        """Retorna las secciones como lista"""
        return self.secciones.split(',') if self.secciones else []
    
    def set_secciones_list(self, secciones_list):
        """Establece las secciones desde una lista"""
        self.secciones = ','.join(secciones_list) if secciones_list else ''
    
    @staticmethod
    def get_niveles():
        """Retorna los niveles educativos disponibles"""
        return ['Primaria', 'Secundaria']
    
    @staticmethod
    def get_secciones_disponibles():
        """Retorna las secciones disponibles"""
        return ['A', 'B', 'C', 'D', 'E']
    
    def __repr__(self):
        return f'<Grado {self.nombre} - {self.nivel}>' 