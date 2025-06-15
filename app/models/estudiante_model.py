from datetime import datetime
from app import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(200), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    grado = db.Column(db.String(50), nullable=False)
    seccion = db.Column(db.String(10), nullable=False)
    codigo_estudiante = db.Column(db.String(20), unique=True, nullable=False)
    padre_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    notas = db.relationship('Nota', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    asistencias = db.relationship('Asistencia', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    cuotas = db.relationship('Cuota', backref='estudiante', lazy=True, cascade='all, delete-orphan')
    
    def generate_code_if_needed(self):
        """Genera código si no lo tiene"""
        if not self.codigo_estudiante:
            from app.utils.code_generator import CodeGenerator
            self.codigo_estudiante = CodeGenerator.generate_student_code()
    
    def __init__(self, **kwargs):
        """Constructor que genera código automáticamente si no se proporciona"""
        super().__init__(**kwargs)
        if not self.codigo_estudiante:
            from app.utils.code_generator import CodeGenerator
            self.codigo_estudiante = CodeGenerator.generate_student_code()
    
    def __repr__(self):
        return f'<Estudiante {self.codigo_estudiante} - {self.nombre_completo}>' 