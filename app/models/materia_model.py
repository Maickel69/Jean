from datetime import datetime
from app import db

class Materia(db.Model):
    __tablename__ = 'materias'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    area_curricular = db.Column(db.String(100), nullable=False)  # Matemática, Comunicación, Ciencias, etc.
    horas_semanales = db.Column(db.Integer, default=2)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        """Constructor que genera código automáticamente si no se proporciona"""
        super().__init__(**kwargs)
        if not self.codigo:
            self.generate_code()
    
    def generate_code(self):
        """Genera código automático basado en el nombre"""
        if self.nombre:
            # Tomar las primeras 3 letras del nombre en mayúscula
            words = self.nombre.upper().split()
            if len(words) >= 2:
                # Si hay múltiples palabras, tomar primera letra de cada una
                self.codigo = ''.join([word[0] for word in words[:3]])
            else:
                # Si es una sola palabra, tomar las primeras 3 letras
                self.codigo = words[0][:3]
            
            # Verificar unicidad y agregar número si es necesario
            counter = 1
            original_code = self.codigo
            while Materia.query.filter_by(codigo=self.codigo).first():
                self.codigo = f"{original_code}{counter}"
                counter += 1
    
    def __repr__(self):
        return f'<Materia {self.codigo} - {self.nombre}>' 