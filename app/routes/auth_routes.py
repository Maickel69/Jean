from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.repositories.usuario_repository import UsuarioRepository

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir según su tipo
    if current_user.is_authenticated:
        if current_user.tipo_usuario == 'padre':
            return redirect(url_for('padre.dashboard'))
        elif current_user.tipo_usuario == 'docente':
            return redirect(url_for('docente.dashboard'))
        else:  # administrador
            return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre_usuario')
        password = request.form.get('password')
        recordar = bool(request.form.get('recordar'))
        
        if not nombre_usuario or not password:
            flash('Por favor, complete todos los campos.', 'error')
            return render_template('auth/login.html')
        
        # Verificar credenciales
        usuario = UsuarioRepository.verificar_credenciales(nombre_usuario, password)
        
        if usuario:
            login_user(usuario, remember=recordar)
            
            # Redirigir según el tipo de usuario
            if usuario.tipo_usuario == 'padre':
                flash(f'¡Bienvenido/a, {usuario.nombre_completo}!', 'success')
                return redirect(url_for('padre.dashboard'))
            elif usuario.tipo_usuario == 'docente':
                flash(f'¡Bienvenido/a, {usuario.nombre_completo}!', 'success')
                return redirect(url_for('docente.dashboard'))
            else:  # administrador
                flash(f'¡Bienvenido/a, {usuario.nombre_completo}!', 'success')
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login')) 