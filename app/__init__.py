from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'clave-secreta-desarrollo-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///gestion_escolar.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario_model import Usuario
        return Usuario.query.get(int(user_id))
    
    # Agregar funciones de fecha al contexto de Jinja2
    from datetime import datetime
    import locale
    
    @app.template_global()
    def moment():
        """Función para obtener la fecha y hora actual"""
        return datetime.now()
    
    @app.template_filter('format_date')
    def format_date(date, format_string='%d/%m/%Y'):
        """Filtro para formatear fechas"""
        if date:
            return date.strftime(format_string)
        return ''
    
    @app.template_filter('format_datetime')
    def format_datetime(datetime_obj, format_string='%d/%m/%Y %H:%M'):
        """Filtro para formatear fecha y hora"""
        if datetime_obj:
            return datetime_obj.strftime(format_string)
        return ''
    
    @app.template_filter('nl2br')
    def nl2br(text):
        """Filtro para convertir saltos de línea en <br> tags"""
        if text:
            return text.replace('\n', '<br>')
        return ''
    
    @app.template_filter('to_date')
    def to_date(datetime_obj):
        """Filtro para convertir datetime a date"""
        if datetime_obj:
            return datetime_obj.date()
        return None
    
    # Registrar blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.padre_routes import padre_bp
    from app.routes.docente_routes import docente_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.admin_codes import admin_codes_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(padre_bp, url_prefix='/padre')
    app.register_blueprint(docente_bp, url_prefix='/docente')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(admin_codes_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    # Crear tablas de la base de datos
    with app.app_context():
        # Importar todos los modelos para asegurar que se creen las tablas
        from app.models import (
            Usuario, Estudiante, Docente, Curso, Nota, 
            Asistencia, Reunion, Comunicado, Cuota, Chat
        )
        db.create_all()
    
    return app 