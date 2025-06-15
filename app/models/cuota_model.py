from datetime import datetime
from app import db

class Cuota(db.Model):
    __tablename__ = 'cuotas'
    
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiantes.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'mensualidad', 'matricula', 'multa', 'material', 'examen'
    descripcion = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    fecha_pago = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'pagado', 'vencido', 'cancelado'
    metodo_pago = db.Column(db.String(50))  # 'efectivo', 'transferencia', 'tarjeta', 'virtual'
    referencia_pago = db.Column(db.String(100))
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def estado_display(self):
        estados = {
            'pendiente': 'Pendiente',
            'pagado': 'Pagado',
            'vencido': 'Vencido',
            'cancelado': 'Cancelado'
        }
        return estados.get(self.estado, self.estado)
    
    def color_estado(self):
        colores = {
            'pendiente': 'warning',
            'pagado': 'success',
            'vencido': 'danger',
            'cancelado': 'secondary'
        }
        return colores.get(self.estado, 'secondary')
    
    def tipo_display(self):
        tipos = {
            'mensualidad': 'Mensualidad',
            'matricula': 'Matrícula',
            'multa': 'Multa',
            'material': 'Material Educativo',
            'examen': 'Examen'
        }
        return tipos.get(self.tipo, self.tipo)
    
    def esta_vencido(self):
        if self.estado == 'pagado':
            return False
        return datetime.now().date() > self.fecha_vencimiento
    
    def dias_vencimiento(self):
        if self.estado == 'pagado':
            return 0
        delta = self.fecha_vencimiento - datetime.now().date()
        return delta.days
    
    def __repr__(self):
        return f'<Cuota {self.tipo} - {self.monto} - {self.estado}>' 