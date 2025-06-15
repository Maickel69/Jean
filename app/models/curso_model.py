from datetime import datetime, date
from app import db

# Tabla de asociación para la relación muchos a muchos entre estudiantes y cursos
estudiante_curso = db.Table('estudiante_curso',
    db.Column('estudiante_id', db.Integer, db.ForeignKey('estudiantes.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
    db.Column('fecha_inscripcion', db.DateTime, default=datetime.utcnow)
)

class Curso(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    grado = db.Column(db.String(50), nullable=False)
    seccion = db.Column(db.String(10), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey('docentes.id'), nullable=False)
    creditos = db.Column(db.Integer, default=1)
    activo = db.Column(db.Boolean, default=True)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    
    # Relaciones
    estudiantes = db.relationship('Estudiante', secondary=estudiante_curso, lazy='subquery',
                                backref=db.backref('cursos', lazy=True))
    notas = db.relationship('Nota', backref='curso', lazy=True, cascade='all, delete-orphan')
    asistencias = db.relationship('Asistencia', backref='curso', lazy=True, cascade='all, delete-orphan')
    reuniones = db.relationship('Reunion', backref='curso', lazy=True, cascade='all, delete-orphan')
    
    def generate_code_if_needed(self):
        """Genera código si no lo tiene"""
        if not self.codigo:
            from app.utils.code_generator import CodeGenerator
            self.codigo = CodeGenerator.generate_course_code(
                materia=self.nombre or '',
                grado=self.grado or '',
                seccion=self.seccion or ''
            )
    
    def set_academic_year_dates(self):
        """Establece fechas del año académico actual si no están definidas"""
        if not self.fecha_inicio or not self.fecha_fin:
            current_year = datetime.now().year
            current_month = datetime.now().month
            
            # Si estamos en enero-julio, el año académico comenzó en marzo del año actual
            # Si estamos en agosto-diciembre, el año académico comenzará en marzo del próximo año
            if current_month >= 3 and current_month <= 12:
                # Año académico actual (marzo a diciembre)
                self.fecha_inicio = date(current_year, 3, 1)
                self.fecha_fin = date(current_year, 12, 15)
            else:
                # Próximo año académico (marzo del año siguiente)
                self.fecha_inicio = date(current_year, 3, 1)
                self.fecha_fin = date(current_year, 12, 15)
    
    def __init__(self, **kwargs):
        """Constructor que genera código y fechas automáticamente si no se proporcionan"""
        super().__init__(**kwargs)
        
        # Generar código si no se proporciona
        if not self.codigo:
            from app.utils.code_generator import CodeGenerator
            self.codigo = CodeGenerator.generate_course_code(
                materia=self.nombre or '',
                grado=self.grado or '',
                seccion=self.seccion or ''
            )
        
        # Establecer fechas del año académico si no se proporcionan
        self.set_academic_year_dates()
    
    def __repr__(self):
        return f'<Curso {self.codigo} - {self.nombre}>' 