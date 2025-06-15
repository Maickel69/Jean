from datetime import datetime
from app import db

class Docente(db.Model):
    __tablename__ = 'docentes'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_docente = db.Column(db.String(20), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(200))
    anos_experiencia = db.Column(db.Integer, default=0)
    horario_atencion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    fecha_contratacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='docente_perfil')
    cursos = db.relationship('Curso', backref='docente', lazy=True)
    comunicados = db.relationship('Comunicado', backref='docente', lazy=True)
    
    def generate_code_if_needed(self):
        """Genera código si no lo tiene"""
        if not self.codigo_docente:
            from app.utils.code_generator import CodeGenerator
            self.codigo_docente = CodeGenerator.generate_teacher_code()
    
    def __init__(self, **kwargs):
        """Constructor que genera código automáticamente si no se proporciona"""
        super().__init__(**kwargs)
        if not self.codigo_docente:
            from app.utils.code_generator import CodeGenerator
            self.codigo_docente = CodeGenerator.generate_teacher_code()
    
    def __repr__(self):
        return f'<Docente {self.codigo_docente} - {self.usuario.nombre_completo if self.usuario else "Sin usuario"}>' 