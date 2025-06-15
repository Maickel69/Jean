from app.models.usuario_model import Usuario
from app import db

class UsuarioRepository:
    
    @staticmethod
    def crear_usuario(nombre_usuario, email, password, nombre_completo, telefono, tipo_usuario):
        try:
            usuario = Usuario(
                nombre_usuario=nombre_usuario,
                email=email,
                nombre_completo=nombre_completo,
                telefono=telefono,
                tipo_usuario=tipo_usuario
            )
            usuario.set_password(password)
            
            db.session.add(usuario)
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def obtener_por_id(usuario_id):
        return Usuario.query.get(usuario_id)
    
    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario):
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
    
    @staticmethod
    def obtener_por_email(email):
        return Usuario.query.filter_by(email=email).first()
    
    @staticmethod
    def obtener_todos():
        return Usuario.query.filter_by(activo=True).all()
    
    @staticmethod
    def obtener_por_tipo(tipo_usuario):
        return Usuario.query.filter_by(tipo_usuario=tipo_usuario, activo=True).all()
    
    @staticmethod
    def actualizar_usuario(usuario_id, **kwargs):
        try:
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return None
            
            for key, value in kwargs.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def desactivar_usuario(usuario_id):
        try:
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return None
            
            usuario.activo = False
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def verificar_credenciales(nombre_usuario, password):
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario, activo=True).first()
        if usuario and usuario.check_password(password):
            return usuario
        return None 