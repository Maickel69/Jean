from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.usuario_model import Usuario
from app.models.estudiante_model import Estudiante
from app.models.docente_model import Docente
from app.models.curso_model import Curso
from app.models.materia_model import Materia
from app.models.grado_model import Grado
from app.models.nota_model import Nota
from app.models.asistencia_model import Asistencia

from app.repositories.usuario_repository import UsuarioRepository
from app import db
from datetime import datetime
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'administrador':
            flash('Acceso denegado. Solo los administradores pueden acceder.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.before_request
@login_required
@admin_required
def verificar_admin():
    # TODO: Implementar verificación de admin cuando se agregue el rol
    pass

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Estadísticas generales
    total_padres = Usuario.query.filter_by(tipo_usuario='padre').count()
    total_docentes = Usuario.query.filter_by(tipo_usuario='docente').count()
    total_estudiantes = Estudiante.query.count()
    total_cursos = Curso.query.count()
    total_materias = Materia.query.filter_by(activo=True).count()
    total_grados = Grado.query.filter_by(activo=True).count()
    
    # Estadísticas de matrícula
    from sqlalchemy import func
    total_matriculas = db.session.query(func.count()).select_from(
        db.table('estudiante_curso')
    ).scalar() or 0
    estudiantes_sin_cursos = Estudiante.query.filter(~Estudiante.cursos.any()).count()
    cursos_sin_estudiantes = Curso.query.filter(~Curso.estudiantes.any()).count()
    
    return render_template('admin/dashboard.html',
                         total_padres=total_padres,
                         total_docentes=total_docentes,
                         total_estudiantes=total_estudiantes,
                         total_cursos=total_cursos,
                         total_materias=total_materias,
                         total_grados=total_grados,
                         total_matriculas=total_matriculas,
                         estudiantes_sin_cursos=estudiantes_sin_cursos,
                         cursos_sin_estudiantes=cursos_sin_estudiantes)

@admin_bp.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.filter_by(activo=True).all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        try:
            nombre_usuario = request.form.get('nombre_usuario')
            email = request.form.get('email')
            password = request.form.get('password')
            nombre_completo = request.form.get('nombre_completo')
            telefono = request.form.get('telefono')
            tipo_usuario = request.form.get('tipo_usuario')
            
            # Verificar si el usuario ya existe
            if UsuarioRepository.obtener_por_nombre_usuario(nombre_usuario):
                flash('El nombre de usuario ya existe.', 'error')
                return render_template('admin/crear_usuario.html')
            
            if UsuarioRepository.obtener_por_email(email):
                flash('El email ya está registrado.', 'error')
                return render_template('admin/crear_usuario.html')
            
            # Crear usuario
            usuario = UsuarioRepository.crear_usuario(
                nombre_usuario=nombre_usuario,
                email=email,
                password=password,
                nombre_completo=nombre_completo,
                telefono=telefono,
                tipo_usuario=tipo_usuario
            )
            
            # Si es docente, crear perfil de docente
            if tipo_usuario == 'docente':
                especialidad = request.form.get('especialidad', 'General')
                titulo = request.form.get('titulo', '')
                
                docente = Docente(
                    usuario_id=usuario.id,
                    especialidad=especialidad,
                    titulo=titulo
                )
                db.session.add(docente)
                db.session.commit()
            
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('admin.usuarios'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el usuario.', 'error')
    
    return render_template('admin/crear_usuario.html')

# Gestión de Padres
@admin_bp.route('/padres')
@login_required
@admin_required
def gestionar_padres():
    padres = Usuario.query.filter_by(tipo_usuario='padre').all()
    return render_template('admin/padres.html', padres=padres)

@admin_bp.route('/padres/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_padre():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        email = request.form['email']
        password = request.form['password']
        nombre_completo = request.form['nombre_completo']
        telefono = request.form.get('telefono', '')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash('El nombre de usuario ya existe', 'error')
            return render_template('admin/padre_form.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya existe', 'error')
            return render_template('admin/padre_form.html')
        
        nuevo_padre = Usuario(
            nombre_usuario=nombre_usuario,
            email=email,
            nombre_completo=nombre_completo,
            telefono=telefono,
            tipo_usuario='padre'
        )
        nuevo_padre.set_password(password)
        
        db.session.add(nuevo_padre)
        db.session.commit()
        
        flash('Padre creado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_padres'))
    
    return render_template('admin/padre_form.html')

@admin_bp.route('/padres/<int:padre_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_padre(padre_id):
    padre = Usuario.query.get_or_404(padre_id)
    
    if request.method == 'POST':
        padre.email = request.form['email']
        padre.nombre_completo = request.form['nombre_completo']
        padre.telefono = request.form.get('telefono', '')
        
        if request.form.get('password'):
            padre.set_password(request.form['password'])
        
        db.session.commit()
        flash('Padre actualizado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_padres'))
    
    return render_template('admin/padre_form.html', padre=padre)

@admin_bp.route('/padres/<int:padre_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_padre(padre_id):
    padre = Usuario.query.get_or_404(padre_id)
    
    # Verificar si tiene estudiantes asociados
    if padre.estudiantes:
        flash('No se puede eliminar un padre que tiene estudiantes asociados', 'error')
        return redirect(url_for('admin.gestionar_padres'))
    
    db.session.delete(padre)
    db.session.commit()
    flash('Padre eliminado exitosamente', 'success')
    return redirect(url_for('admin.gestionar_padres'))

# Gestión de Docentes
@admin_bp.route('/docentes')
@login_required
@admin_required
def gestionar_docentes():
    docentes = db.session.query(Usuario, Docente).join(Docente, Usuario.id == Docente.usuario_id).all()
    return render_template('admin/docentes.html', docentes=docentes)

@admin_bp.route('/docentes/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_docente():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        nombre_completo = request.form['nombre_completo'].strip()
        telefono = request.form.get('telefono', '').strip()
        especialidad = request.form['especialidad'].strip()
        titulo = request.form['titulo'].strip()
        
        # Validaciones mejoradas
        errors = []
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            errors.append('El nombre de usuario ya existe')
        
        if Usuario.query.filter_by(email=email).first():
            errors.append('El email ya está registrado en el sistema')
        
        # Validar formato de email
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            errors.append('El formato del email no es válido')
        
        # Validar longitud de contraseña
        if len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        # Validar campos requeridos
        if not nombre_completo:
            errors.append('El nombre completo es requerido')
        
        if not especialidad:
            errors.append('La especialidad es requerida')
        
        if not titulo:
            errors.append('El título académico es requerido')
        
        # Si hay errores, mostrarlos y volver al formulario
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin/docente_form.html')
        
        try:
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario,
                email=email,
                nombre_completo=nombre_completo,
                telefono=telefono,
                tipo_usuario='docente'
            )
            nuevo_usuario.set_password(password)
            
            db.session.add(nuevo_usuario)
            db.session.flush()  # Para obtener el ID
            
            nuevo_docente = Docente(
                usuario_id=nuevo_usuario.id,
                especialidad=especialidad,
                titulo=titulo
            )
            
            # Generar código automáticamente
            nuevo_docente.generate_code_if_needed()
            
            db.session.add(nuevo_docente)
            db.session.commit()
            
            flash('Docente creado exitosamente', 'success')
            return redirect(url_for('admin.gestionar_docentes'))
            
        except Exception as e:
            db.session.rollback()
            if 'UNIQUE constraint failed: usuarios.email' in str(e):
                flash('El email ya está registrado en el sistema', 'error')
            elif 'UNIQUE constraint failed: usuarios.nombre_usuario' in str(e):
                flash('El nombre de usuario ya existe', 'error')
            else:
                flash('Error al crear el docente. Por favor, intenta nuevamente.', 'error')
            return render_template('admin/docente_form.html')
    
    return render_template('admin/docente_form.html')

@admin_bp.route('/docentes/<int:docente_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_docente(docente_id):
    usuario = Usuario.query.get_or_404(docente_id)
    docente = Docente.query.filter_by(usuario_id=docente_id).first()
    
    if request.method == 'POST':
        usuario.email = request.form['email']
        usuario.nombre_completo = request.form['nombre_completo']
        usuario.telefono = request.form.get('telefono', '')
        
        if request.form.get('password'):
            usuario.set_password(request.form['password'])
        
        if docente:
            docente.especialidad = request.form['especialidad']
            docente.titulo = request.form['titulo']
        
        db.session.commit()
        flash('Docente actualizado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_docentes'))
    
    return render_template('admin/docente_form.html', usuario=usuario, docente=docente)

@admin_bp.route('/docentes/<int:docente_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_docente(docente_id):
    usuario = Usuario.query.get_or_404(docente_id)
    docente = Docente.query.filter_by(usuario_id=docente_id).first()
    
    # Verificar si tiene cursos asociados
    if docente and docente.cursos:
        flash('No se puede eliminar un docente que tiene cursos asociados', 'error')
        return redirect(url_for('admin.gestionar_docentes'))
    
    if docente:
        db.session.delete(docente)
    db.session.delete(usuario)
    db.session.commit()
    flash('Docente eliminado exitosamente', 'success')
    return redirect(url_for('admin.gestionar_docentes'))

# Gestión de Estudiantes
@admin_bp.route('/estudiantes')
@login_required
@admin_required
def gestionar_estudiantes():
    estudiantes = db.session.query(Estudiante, Usuario).join(
        Usuario, Estudiante.padre_id == Usuario.id
    ).all()
    return render_template('admin/estudiantes.html', estudiantes=estudiantes)

@admin_bp.route('/estudiantes/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_estudiante():
    if request.method == 'POST':
        nombre_completo = request.form['nombre_completo']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        padre_id = request.form['padre_id']
        grado = request.form['grado']
        seccion = request.form['seccion']
        codigo_estudiante = request.form.get('codigo_estudiante', '').strip()
        
        # Convertir la fecha de string a objeto date
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            padres = Usuario.query.filter_by(tipo_usuario='padre').all()
            return render_template('admin/estudiante_form.html', padres=padres)
        
        nuevo_estudiante = Estudiante(
            nombre_completo=nombre_completo,
            fecha_nacimiento=fecha_nacimiento,
            padre_id=padre_id,
            grado=grado,
            seccion=seccion,
            codigo_estudiante=codigo_estudiante if codigo_estudiante else None
        )
        
        # Generar código automáticamente si no se proporcionó
        nuevo_estudiante.generate_code_if_needed()
        
        db.session.add(nuevo_estudiante)
        db.session.commit()
        
        flash('Estudiante creado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_estudiantes'))
    
    padres = Usuario.query.filter_by(tipo_usuario='padre').all()
    return render_template('admin/estudiante_form.html', padres=padres)

@admin_bp.route('/estudiantes/<int:estudiante_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_estudiante(estudiante_id):
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    
    if request.method == 'POST':
        estudiante.nombre_completo = request.form['nombre_completo']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        estudiante.padre_id = request.form['padre_id']
        estudiante.grado = request.form['grado']
        estudiante.seccion = request.form['seccion']
        estudiante.codigo_estudiante = request.form['codigo_estudiante']
        
        # Convertir la fecha de string a objeto date
        try:
            estudiante.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            padres = Usuario.query.filter_by(tipo_usuario='padre').all()
            return render_template('admin/estudiante_form.html', estudiante=estudiante, padres=padres)
        
        db.session.commit()
        flash('Estudiante actualizado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_estudiantes'))
    
    padres = Usuario.query.filter_by(tipo_usuario='padre').all()
    return render_template('admin/estudiante_form.html', estudiante=estudiante, padres=padres)

@admin_bp.route('/estudiantes/<int:estudiante_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_estudiante(estudiante_id):
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    db.session.delete(estudiante)
    db.session.commit()
    flash('Estudiante eliminado exitosamente', 'success')
    return redirect(url_for('admin.gestionar_estudiantes'))

# Gestión de Cursos
@admin_bp.route('/cursos')
@login_required
@admin_required
def gestionar_cursos():
    cursos = db.session.query(Curso, Docente, Usuario).join(
        Docente, Curso.docente_id == Docente.id
    ).join(
        Usuario, Docente.usuario_id == Usuario.id
    ).all()
    return render_template('admin/cursos.html', cursos=cursos)

@admin_bp.route('/cursos/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_curso():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form.get('codigo', '').strip()
        descripcion = request.form.get('descripcion', '')
        grado = request.form['grado']
        seccion = request.form['seccion']
        docente_id = request.form['docente_id']
        creditos = request.form.get('creditos', 1)
        
        nuevo_curso = Curso(
            nombre=nombre,
            codigo=codigo if codigo else None,
            descripcion=descripcion,
            grado=grado,
            seccion=seccion,
            docente_id=docente_id,
            creditos=creditos
        )
        
        # Generar código automáticamente si no se proporcionó
        nuevo_curso.generate_code_if_needed()
        
        # Establecer fechas del año académico
        nuevo_curso.set_academic_year_dates()
        
        db.session.add(nuevo_curso)
        db.session.commit()
        
        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_cursos'))
    
    docentes = db.session.query(Docente, Usuario).join(Usuario, Docente.usuario_id == Usuario.id).all()
    return render_template('admin/curso_form.html', docentes=docentes)

@admin_bp.route('/cursos/<int:curso_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    
    if request.method == 'POST':
        curso.nombre = request.form['nombre']
        curso.codigo = request.form['codigo']
        curso.descripcion = request.form.get('descripcion', '')
        curso.grado = request.form['grado']
        curso.seccion = request.form['seccion']
        curso.docente_id = request.form['docente_id']
        curso.creditos = request.form.get('creditos', 1)
        
        db.session.commit()
        flash('Curso actualizado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_cursos'))
    
    docentes = db.session.query(Docente, Usuario).join(Usuario, Docente.usuario_id == Usuario.id).all()
    return render_template('admin/curso_form.html', curso=curso, docentes=docentes)

@admin_bp.route('/cursos/<int:curso_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    
    # Verificar si tiene estudiantes asociados (por implementar relación many-to-many)
    # if curso.estudiantes:
    #     flash('No se puede eliminar un curso que tiene estudiantes asociados', 'error')
    #     return redirect(url_for('admin.gestionar_cursos'))
    
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado exitosamente', 'success')
    return redirect(url_for('admin.gestionar_cursos'))

# API para obtener cursos por grado
@admin_bp.route('/api/cursos/<int:grado_id>')
@login_required
@admin_required
def api_cursos_por_grado(grado_id):
    cursos = Curso.query.filter_by(grado_id=grado_id).all()
    return jsonify([{'id': c.id, 'nombre': f'{c.nombre} - {c.seccion}'} for c in cursos])

# Gestión de Materias
@admin_bp.route('/materias')
@login_required
@admin_required
def gestionar_materias():
    materias = Materia.query.filter_by(activo=True).all()
    return render_template('admin/materias.html', materias=materias)

@admin_bp.route('/materias/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_materia():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form.get('codigo', '').strip()
        descripcion = request.form.get('descripcion', '')
        area_curricular = request.form['area_curricular']
        horas_semanales = int(request.form.get('horas_semanales', 2))
        
        # Verificar si la materia ya existe
        if Materia.query.filter_by(nombre=nombre).first():
            flash('Ya existe una materia con ese nombre', 'error')
            return render_template('admin/materia_form.html')
        
        nueva_materia = Materia(
            nombre=nombre,
            codigo=codigo if codigo else None,
            descripcion=descripcion,
            area_curricular=area_curricular,
            horas_semanales=horas_semanales
        )
        
        db.session.add(nueva_materia)
        db.session.commit()
        
        flash('Materia creada exitosamente', 'success')
        return redirect(url_for('admin.gestionar_materias'))
    
    return render_template('admin/materia_form.html')

@admin_bp.route('/materias/<int:materia_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    
    if request.method == 'POST':
        materia.nombre = request.form['nombre']
        materia.codigo = request.form.get('codigo', '').strip()
        materia.descripcion = request.form.get('descripcion', '')
        materia.area_curricular = request.form['area_curricular']
        materia.horas_semanales = int(request.form.get('horas_semanales', 2))
        
        db.session.commit()
        flash('Materia actualizada exitosamente', 'success')
        return redirect(url_for('admin.gestionar_materias'))
    
    return render_template('admin/materia_form.html', materia=materia)

@admin_bp.route('/materias/<int:materia_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_materia(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    materia.activo = False  # Soft delete
    db.session.commit()
    flash('Materia eliminada exitosamente', 'success')
    return redirect(url_for('admin.gestionar_materias'))

# Gestión de Grados
@admin_bp.route('/grados')
@login_required
@admin_required
def gestionar_grados():
    grados = Grado.query.filter_by(activo=True).order_by(Grado.nivel, Grado.numero).all()
    return render_template('admin/grados.html', grados=grados)

@admin_bp.route('/grados/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_grado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nivel = request.form['nivel']
        numero = int(request.form['numero'])
        secciones = request.form.getlist('secciones')
        edad_minima = int(request.form.get('edad_minima', 0)) or None
        edad_maxima = int(request.form.get('edad_maxima', 0)) or None
        
        # Verificar si el grado ya existe
        if Grado.query.filter_by(nombre=nombre).first():
            flash('Ya existe un grado con ese nombre', 'error')
            return render_template('admin/grado_form.html')
        
        nuevo_grado = Grado(
            nombre=nombre,
            nivel=nivel,
            numero=numero,
            edad_minima=edad_minima,
            edad_maxima=edad_maxima
        )
        nuevo_grado.set_secciones_list(secciones)
        
        db.session.add(nuevo_grado)
        db.session.commit()
        
        flash('Grado creado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_grados'))
    
    return render_template('admin/grado_form.html')

@admin_bp.route('/grados/<int:grado_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_grado(grado_id):
    grado = Grado.query.get_or_404(grado_id)
    
    if request.method == 'POST':
        grado.nombre = request.form['nombre']
        grado.nivel = request.form['nivel']
        grado.numero = int(request.form['numero'])
        secciones = request.form.getlist('secciones')
        grado.edad_minima = int(request.form.get('edad_minima', 0)) or None
        grado.edad_maxima = int(request.form.get('edad_maxima', 0)) or None
        
        grado.set_secciones_list(secciones)
        
        db.session.commit()
        flash('Grado actualizado exitosamente', 'success')
        return redirect(url_for('admin.gestionar_grados'))
    
    return render_template('admin/grado_form.html', grado=grado)

@admin_bp.route('/grados/<int:grado_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_grado(grado_id):
    grado = Grado.query.get_or_404(grado_id)
    grado.activo = False  # Soft delete
    db.session.commit()
    flash('Grado eliminado exitosamente', 'success')
    return redirect(url_for('admin.gestionar_grados'))

# Reportes y Estadísticas
@admin_bp.route('/reportes/rendimiento')
@login_required
@admin_required
def reporte_rendimiento():
    # Estadísticas de rendimiento académico
    from sqlalchemy import func, case
    
    # Promedio general por curso (usando porcentaje)
    promedios_curso = db.session.query(
        Curso.nombre,
        Curso.grado,
        Curso.seccion,
        func.avg((Nota.calificacion / Nota.calificacion_maxima) * 100).label('promedio')
    ).join(Nota).group_by(Curso.id).all()
    
    # Estudiantes con mejor rendimiento
    mejores_estudiantes = db.session.query(
        Estudiante.nombre_completo,
        Estudiante.grado,
        Estudiante.seccion,
        func.avg((Nota.calificacion / Nota.calificacion_maxima) * 100).label('promedio')
    ).join(Nota).group_by(Estudiante.id).order_by(func.avg((Nota.calificacion / Nota.calificacion_maxima) * 100).desc()).limit(10).all()
    
    # Distribución de notas por estado (calculado manualmente)
    distribucion_notas = db.session.query(
        case(
            ((Nota.calificacion / Nota.calificacion_maxima) * 100 >= 70, 'Aprobado'),
            ((Nota.calificacion / Nota.calificacion_maxima) * 100 >= 60, 'Recuperación'),
            else_='Desaprobado'
        ).label('estado'),
        func.count(Nota.id).label('cantidad')
    ).group_by(
        case(
            ((Nota.calificacion / Nota.calificacion_maxima) * 100 >= 70, 'Aprobado'),
            ((Nota.calificacion / Nota.calificacion_maxima) * 100 >= 60, 'Recuperación'),
            else_='Desaprobado'
        )
    ).all()
    
    # Estadísticas adicionales
    total_notas = Nota.query.count()
    promedio_general = db.session.query(
        func.avg((Nota.calificacion / Nota.calificacion_maxima) * 100)
    ).scalar() or 0
    
    return render_template('admin/reporte_rendimiento.html',
                         promedios_curso=promedios_curso,
                         mejores_estudiantes=mejores_estudiantes,
                         distribucion_notas=distribucion_notas,
                         total_notas=total_notas,
                         promedio_general=promedio_general)

@admin_bp.route('/reportes/asistencias')
@login_required
@admin_required
def reporte_asistencias():
    # Estadísticas de asistencia
    from sqlalchemy import func, case
    
    # Porcentaje de asistencia por curso
    asistencia_curso = db.session.query(
        Curso.nombre,
        Curso.grado,
        Curso.seccion,
        func.count(Asistencia.id).label('total_registros'),
        func.sum(case((Asistencia.estado == 'presente', 1), else_=0)).label('presentes')
    ).join(Asistencia).group_by(Curso.id).all()
    
    # Estudiantes con menor asistencia
    menor_asistencia = db.session.query(
        Estudiante.nombre_completo,
        Estudiante.grado,
        Estudiante.seccion,
        func.count(Asistencia.id).label('total_clases'),
        func.sum(case((Asistencia.estado == 'presente', 1), else_=0)).label('asistencias')
    ).join(Asistencia).group_by(Estudiante.id).having(
        func.count(Asistencia.id) > 0
    ).order_by(
        (func.sum(case((Asistencia.estado == 'presente', 1), else_=0)) * 100.0 / func.count(Asistencia.id))
    ).limit(10).all()
    
    return render_template('admin/reporte_asistencias.html',
                         asistencia_curso=asistencia_curso,
                         menor_asistencia=menor_asistencia)

# ==============================================================================
# GESTIÓN DE MATRÍCULAS
# ==============================================================================

@admin_bp.route('/matriculas')
@login_required
@admin_required
def gestionar_matriculas():
    """Vista principal de gestión de matrículas"""
    # Obtener filtros
    grado_filtro = request.args.get('grado', '')
    curso_filtro = request.args.get('curso', '')
    estado_filtro = request.args.get('estado', '')
    
    # Query base con JOIN para obtener información completa
    query = db.session.query(
        Estudiante,
        Curso,
        db.func.count(Nota.id).label('total_notas'),
        db.func.count(Asistencia.id).label('total_asistencias')
    ).join(
        Curso, Estudiante.cursos
    ).outerjoin(
        Nota, db.and_(Nota.estudiante_id == Estudiante.id, Nota.curso_id == Curso.id)
    ).outerjoin(
        Asistencia, db.and_(Asistencia.estudiante_id == Estudiante.id, Asistencia.curso_id == Curso.id)
    )
    
    # Aplicar filtros
    if grado_filtro:
        query = query.filter(Curso.grado.ilike(f'%{grado_filtro}%'))
    if curso_filtro:
        query = query.filter(Curso.nombre.ilike(f'%{curso_filtro}%'))
    
    matriculas = query.group_by(Estudiante.id, Curso.id).all()
    
    # Estadísticas rápidas
    total_matriculas = len(matriculas)
    estudiantes_sin_cursos = Estudiante.query.filter(~Estudiante.cursos.any()).count()
    cursos_sin_estudiantes = Curso.query.filter(~Curso.estudiantes.any()).count()
    
    return render_template('admin/matriculas.html',
                         matriculas=matriculas,
                         total_matriculas=total_matriculas,
                         estudiantes_sin_cursos=estudiantes_sin_cursos,
                         cursos_sin_estudiantes=cursos_sin_estudiantes,
                         grado_filtro=grado_filtro,
                         curso_filtro=curso_filtro)

@admin_bp.route('/matriculas/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def matricular_estudiante():
    """Matricular un estudiante en un curso"""
    if request.method == 'POST':
        estudiante_id = request.form.get('estudiante_id')
        curso_id = request.form.get('curso_id')
        
        if not estudiante_id or not curso_id:
            flash('Debe seleccionar un estudiante y un curso', 'error')
            return redirect(url_for('admin.matricular_estudiante'))
        
        estudiante = Estudiante.query.get_or_404(estudiante_id)
        curso = Curso.query.get_or_404(curso_id)
        
        # Validar que no esté ya matriculado
        if curso in estudiante.cursos:
            flash(f'{estudiante.nombre_completo} ya está matriculado en {curso.nombre}', 'error')
            return redirect(url_for('admin.matricular_estudiante'))
        
        # Validar compatibilidad de grado (opcional, se puede flexibilizar)
        if estudiante.grado != curso.grado:
            flash(f'Advertencia: El grado del estudiante ({estudiante.grado}) no coincide con el del curso ({curso.grado})', 'warning')
        
        # Realizar matrícula
        try:
            estudiante.cursos.append(curso)
            db.session.commit()
            flash(f'{estudiante.nombre_completo} ha sido matriculado exitosamente en {curso.nombre}', 'success')
            return redirect(url_for('admin.gestionar_matriculas'))
        except Exception as e:
            db.session.rollback()
            flash('Error al realizar la matrícula', 'error')
    
    # Obtener estudiantes y cursos para el formulario
    estudiantes = Estudiante.query.order_by(Estudiante.nombre_completo).all()
    cursos = Curso.query.filter_by(activo=True).order_by(Curso.grado, Curso.seccion, Curso.nombre).all()
    
    return render_template('admin/matricular_estudiante.html',
                         estudiantes=estudiantes,
                         cursos=cursos)

@admin_bp.route('/matriculas/masiva', methods=['GET', 'POST'])
@login_required
@admin_required
def matricula_masiva():
    """Matricular múltiples estudiantes en un curso"""
    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        estudiantes_ids = request.form.getlist('estudiantes_ids')
        
        if not curso_id or not estudiantes_ids:
            flash('Debe seleccionar un curso y al menos un estudiante', 'error')
            return redirect(url_for('admin.matricula_masiva'))
        
        curso = Curso.query.get_or_404(curso_id)
        matriculados = 0
        ya_matriculados = []
        errores = []
        
        for estudiante_id in estudiantes_ids:
            try:
                estudiante = Estudiante.query.get(estudiante_id)
                if not estudiante:
                    continue
                
                if curso in estudiante.cursos:
                    ya_matriculados.append(estudiante.nombre_completo)
                    continue
                
                estudiante.cursos.append(curso)
                matriculados += 1
                
            except Exception as e:
                errores.append(f'{estudiante.nombre_completo}: {str(e)}')
        
        try:
            db.session.commit()
            if matriculados > 0:
                flash(f'{matriculados} estudiantes matriculados exitosamente en {curso.nombre}', 'success')
            if ya_matriculados:
                flash(f'Ya matriculados: {", ".join(ya_matriculados)}', 'info')
            if errores:
                flash(f'Errores: {"; ".join(errores)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error al realizar las matrículas masivas', 'error')
        
        return redirect(url_for('admin.gestionar_matriculas'))
    
    cursos = Curso.query.filter_by(activo=True).order_by(Curso.grado, Curso.seccion, Curso.nombre).all()
    estudiantes = Estudiante.query.order_by(Estudiante.grado, Estudiante.seccion, Estudiante.nombre_completo).all()
    
    return render_template('admin/matricula_masiva.html',
                         cursos=cursos,
                         estudiantes=estudiantes)

@admin_bp.route('/matriculas/<int:estudiante_id>/<int:curso_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def desmatricular_estudiante(estudiante_id, curso_id):
    """Desmatricular un estudiante de un curso"""
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    curso = Curso.query.get_or_404(curso_id)
    
    if curso not in estudiante.cursos:
        flash(f'{estudiante.nombre_completo} no está matriculado en {curso.nombre}', 'error')
        return redirect(url_for('admin.gestionar_matriculas'))
    
    # Verificar si tiene notas o asistencias (opcional - se puede permitir)
    tiene_notas = Nota.query.filter_by(estudiante_id=estudiante_id, curso_id=curso_id).count() > 0
    tiene_asistencias = Asistencia.query.filter_by(estudiante_id=estudiante_id, curso_id=curso_id).count() > 0
    
    if tiene_notas or tiene_asistencias:
        confirmar = request.form.get('confirmar_desmatricula')
        if not confirmar:
            flash(f'{estudiante.nombre_completo} tiene registros académicos en {curso.nombre}. Use la confirmación para proceder.', 'warning')
            return redirect(url_for('admin.gestionar_matriculas'))
    
    try:
        estudiante.cursos.remove(curso)
        db.session.commit()
        flash(f'{estudiante.nombre_completo} ha sido desmatriculado de {curso.nombre}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al desmatricular al estudiante', 'error')
    
    return redirect(url_for('admin.gestionar_matriculas'))

@admin_bp.route('/cursos/<int:curso_id>/estudiantes')
@login_required
@admin_required
def curso_estudiantes(curso_id):
    """Ver y gestionar estudiantes de un curso específico"""
    curso = Curso.query.get_or_404(curso_id)
    
    # Estudiantes matriculados con estadísticas
    estudiantes_data = []
    for estudiante in curso.estudiantes:
        notas_count = Nota.query.filter_by(estudiante_id=estudiante.id, curso_id=curso.id).count()
        asistencias_count = Asistencia.query.filter_by(estudiante_id=estudiante.id, curso_id=curso.id).count()
        presentes_count = Asistencia.query.filter_by(
            estudiante_id=estudiante.id, 
            curso_id=curso.id, 
            estado='presente'
        ).count()
        
        porcentaje_asistencia = (presentes_count * 100 / asistencias_count) if asistencias_count > 0 else 0
        
        estudiantes_data.append({
            'estudiante': estudiante,
            'notas_count': notas_count,
            'asistencias_count': asistencias_count,
            'porcentaje_asistencia': round(porcentaje_asistencia, 1)
        })
    
    # Estudiantes no matriculados del mismo grado
    estudiantes_disponibles = Estudiante.query.filter(
        Estudiante.grado == curso.grado,
        ~Estudiante.cursos.contains(curso)
    ).order_by(Estudiante.nombre_completo).all()
    
    return render_template('admin/curso_estudiantes.html',
                         curso=curso,
                         estudiantes_data=estudiantes_data,
                         estudiantes_disponibles=estudiantes_disponibles)

@admin_bp.route('/estudiantes/<int:estudiante_id>/cursos')
@login_required
@admin_required
def estudiante_cursos(estudiante_id):
    """Ver y gestionar cursos de un estudiante específico"""
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    
    # Cursos matriculados con estadísticas
    cursos_data = []
    for curso in estudiante.cursos:
        notas_count = Nota.query.filter_by(estudiante_id=estudiante.id, curso_id=curso.id).count()
        promedio = db.session.query(
            db.func.avg((Nota.calificacion / Nota.calificacion_maxima) * 100)
        ).filter_by(estudiante_id=estudiante.id, curso_id=curso.id).scalar() or 0
        
        asistencias_count = Asistencia.query.filter_by(estudiante_id=estudiante.id, curso_id=curso.id).count()
        presentes_count = Asistencia.query.filter_by(
            estudiante_id=estudiante.id, 
            curso_id=curso.id, 
            estado='presente'
        ).count()
        
        porcentaje_asistencia = (presentes_count * 100 / asistencias_count) if asistencias_count > 0 else 0
        
        cursos_data.append({
            'curso': curso,
            'notas_count': notas_count,
            'promedio': round(promedio, 1),
            'porcentaje_asistencia': round(porcentaje_asistencia, 1)
        })
    
    # Cursos disponibles del mismo grado
    cursos_disponibles = Curso.query.filter(
        Curso.grado == estudiante.grado,
        Curso.activo == True,
        ~Curso.estudiantes.contains(estudiante)
    ).order_by(Curso.nombre).all()
    
    return render_template('admin/estudiante_cursos.html',
                         estudiante=estudiante,
                         cursos_data=cursos_data,
                         cursos_disponibles=cursos_disponibles)

@admin_bp.route('/matriculas/reportes')
@login_required
@admin_required
def reportes_matriculas():
    """Reportes y estadísticas de matrículas"""
    from sqlalchemy import func
    
    # Estadísticas por grado
    matriculas_por_grado = db.session.query(
        Estudiante.grado,
        func.count(db.distinct(Estudiante.id)).label('estudiantes'),
        func.count(Curso.id).label('matriculas_totales')
    ).join(Curso, Estudiante.cursos).group_by(Estudiante.grado).all()
    
    # Cursos con más estudiantes
    cursos_populares = db.session.query(
        Curso.nombre,
        Curso.grado,
        Curso.seccion,
        func.count(Estudiante.id).label('estudiantes_count')
    ).join(Estudiante, Curso.estudiantes).group_by(Curso.id).order_by(
        func.count(Estudiante.id).desc()
    ).limit(10).all()
    
    # Estudiantes con más cursos
    estudiantes_activos = db.session.query(
        Estudiante.nombre_completo,
        Estudiante.grado,
        Estudiante.seccion,
        func.count(Curso.id).label('cursos_count')
    ).join(Curso, Estudiante.cursos).group_by(Estudiante.id).order_by(
        func.count(Curso.id).desc()
    ).limit(10).all()
    
    # Estadísticas generales
    total_estudiantes = Estudiante.query.count()
    total_cursos = Curso.query.filter_by(activo=True).count()
    total_matriculas = db.session.query(func.count()).select_from(
        db.table('estudiante_curso')
    ).scalar()
    estudiantes_sin_cursos = Estudiante.query.filter(~Estudiante.cursos.any()).count()
    cursos_sin_estudiantes = Curso.query.filter(~Curso.estudiantes.any()).count()
    
    return render_template('admin/reportes_matriculas.html',
                         matriculas_por_grado=matriculas_por_grado,
                         cursos_populares=cursos_populares,
                         estudiantes_activos=estudiantes_activos,
                         total_estudiantes=total_estudiantes,
                         total_cursos=total_cursos,
                         total_matriculas=total_matriculas,
                         estudiantes_sin_cursos=estudiantes_sin_cursos,
                         cursos_sin_estudiantes=cursos_sin_estudiantes)

# APIs para formularios dinámicos
@admin_bp.route('/api/estudiantes/<int:estudiante_id>/cursos-disponibles')
@login_required
@admin_required
def api_cursos_disponibles(estudiante_id):
    """API: Cursos disponibles para un estudiante"""
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    cursos_disponibles = Curso.query.filter(
        Curso.activo == True,
        ~Curso.estudiantes.contains(estudiante)
    ).order_by(Curso.nombre).all()
    
    return jsonify([{
        'id': curso.id,
        'nombre': curso.nombre,
        'grado': curso.grado,
        'seccion': curso.seccion,
        'codigo': curso.codigo
    } for curso in cursos_disponibles])

@admin_bp.route('/api/cursos/<int:curso_id>/estudiantes-disponibles')
@login_required
@admin_required
def api_estudiantes_disponibles(curso_id):
    """API: Estudiantes disponibles para un curso"""
    curso = Curso.query.get_or_404(curso_id)
    estudiantes_disponibles = Estudiante.query.filter(
        ~Estudiante.cursos.contains(curso)
    ).order_by(Estudiante.nombre_completo).all()
    
    return jsonify([{
        'id': estudiante.id,
        'nombre_completo': estudiante.nombre_completo,
        'grado': estudiante.grado,
        'seccion': estudiante.seccion,
        'codigo': estudiante.codigo_estudiante
    } for estudiante in estudiantes_disponibles]) 