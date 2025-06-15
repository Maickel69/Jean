from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.estudiante_model import Estudiante
from app.models.curso_model import Curso
from app.models.nota_model import Nota
from app.models.asistencia_model import Asistencia
from app.models.reunion_model import Reunion
from app.models.comunicado_model import Comunicado
from app.models.cuota_model import Cuota
from app.models.chat_model import Chat
from app.models.docente_model import Docente
from app import db

padre_bp = Blueprint('padre', __name__)

@padre_bp.before_request
@login_required
def verificar_padre():
    if current_user.tipo_usuario != 'padre':
        flash('No tienes permisos para acceder a esta sección.', 'error')
        return redirect(url_for('auth.login'))

@padre_bp.route('/dashboard')
def dashboard():
    estudiantes = Estudiante.query.filter_by(padre_id=current_user.id, activo=True).all()
    return render_template('padre/dashboard.html', estudiantes=estudiantes)

@padre_bp.route('/seleccionar_hijo/<int:estudiante_id>')
def seleccionar_hijo(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    return render_template('padre/hijo_dashboard.html', estudiante=estudiante)

@padre_bp.route('/cursos/<int:estudiante_id>')
def cursos(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    cursos = estudiante.cursos
    return render_template('padre/cursos.html', estudiante=estudiante, cursos=cursos)

@padre_bp.route('/notas/<int:estudiante_id>')
def notas(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    notas = Nota.query.filter_by(estudiante_id=estudiante_id).order_by(Nota.fecha_evaluacion.desc()).all()
    return render_template('padre/notas.html', estudiante=estudiante, notas=notas)

@padre_bp.route('/asistencias/<int:estudiante_id>')
def asistencias(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    asistencias = Asistencia.query.filter_by(estudiante_id=estudiante_id).order_by(Asistencia.fecha.desc()).all()
    return render_template('padre/asistencias.html', estudiante=estudiante, asistencias=asistencias)

@padre_bp.route('/reuniones/<int:estudiante_id>')
def reuniones(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    # Obtener reuniones de los cursos del estudiante
    curso_ids = [curso.id for curso in estudiante.cursos]
    reuniones = Reunion.query.filter(Reunion.curso_id.in_(curso_ids)).order_by(Reunion.fecha_reunion.desc()).all()
    
    return render_template('padre/reuniones.html', estudiante=estudiante, reuniones=reuniones)

@padre_bp.route('/comunicados/<int:estudiante_id>')
def comunicados(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    # Obtener comunicados generales y específicos de los cursos del estudiante
    curso_ids = [curso.id for curso in estudiante.cursos]
    comunicados = Comunicado.query.filter(
        db.or_(
            Comunicado.curso_id.is_(None),  # Comunicados generales
            Comunicado.curso_id.in_(curso_ids)  # Comunicados específicos de curso
        )
    ).filter_by(activo=True).order_by(Comunicado.fecha_publicacion.desc()).all()
    
    return render_template('padre/comunicados.html', estudiante=estudiante, comunicados=comunicados)

@padre_bp.route('/cuotas/<int:estudiante_id>')
def cuotas(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    cuotas = Cuota.query.filter_by(estudiante_id=estudiante_id).order_by(Cuota.fecha_vencimiento.desc()).all()
    return render_template('padre/cuotas.html', estudiante=estudiante, cuotas=cuotas)

@padre_bp.route('/pagar_cuota/<int:cuota_id>')
def pagar_cuota(cuota_id):
    cuota = Cuota.query.get_or_404(cuota_id)
    
    # Verificar que la cuota pertenece a un hijo del padre actual
    if cuota.estudiante.padre_id != current_user.id:
        flash('No tienes permisos para acceder a esta cuota.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    # TODO: Integrar con pasarela de pagos real
    return render_template('padre/pagar_cuota.html', cuota=cuota)

@padre_bp.route('/chat/<int:estudiante_id>')
def chat(estudiante_id):
    estudiante = Estudiante.query.filter_by(id=estudiante_id, padre_id=current_user.id).first()
    if not estudiante:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('padre.dashboard'))
    
    # Obtener docentes de los cursos del estudiante
    docentes = []
    for curso in estudiante.cursos:
        if curso.docente not in docentes:
            docentes.append(curso.docente)
    
    return render_template('padre/chat.html', estudiante=estudiante, docentes=docentes)

@padre_bp.route('/chat_conversacion/<int:docente_id>')
def chat_conversacion(docente_id):
    docente = Docente.query.get_or_404(docente_id)
    
    # Obtener mensajes entre el padre actual y el docente
    mensajes = Chat.query.filter(
        db.or_(
            db.and_(Chat.emisor_id == current_user.id, Chat.receptor_id == docente.usuario_id),
            db.and_(Chat.emisor_id == docente.usuario_id, Chat.receptor_id == current_user.id)
        )
    ).order_by(Chat.fecha_envio.asc()).all()
    
    # Marcar mensajes como leídos
    for mensaje in mensajes:
        if mensaje.receptor_id == current_user.id:
            mensaje.marcar_como_leido()
    
    db.session.commit()
    
    return render_template('padre/chat_conversacion.html', docente=docente, mensajes=mensajes)

@padre_bp.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    receptor_id = request.form.get('receptor_id')
    asunto = request.form.get('asunto')
    mensaje = request.form.get('mensaje')
    curso_id = request.form.get('curso_id')
    
    if not receptor_id or not asunto or not mensaje:
        return jsonify({'success': False, 'message': 'Faltan datos requeridos'})
    
    try:
        nuevo_chat = Chat(
            emisor_id=current_user.id,
            receptor_id=int(receptor_id),
            curso_id=int(curso_id) if curso_id else None,
            asunto=asunto,
            mensaje=mensaje
        )
        
        db.session.add(nuevo_chat)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Mensaje enviado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error al enviar el mensaje'})

@padre_bp.route('/informacion_docente/<int:docente_id>')
def informacion_docente(docente_id):
    docente = Docente.query.get_or_404(docente_id)
    return render_template('padre/informacion_docente.html', docente=docente) 