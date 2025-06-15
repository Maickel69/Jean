from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.docente_model import Docente
from app.models.curso_model import Curso
from app.models.estudiante_model import Estudiante
from app.models.nota_model import Nota
from app.models.asistencia_model import Asistencia
from app.models.comunicado_model import Comunicado
from app.models.chat_model import Chat
from app import db
from datetime import datetime, date

docente_bp = Blueprint('docente', __name__)

@docente_bp.before_request
@login_required
def verificar_docente():
    if current_user.tipo_usuario != 'docente':
        flash('No tienes permisos para acceder a esta sección.', 'error')
        return redirect(url_for('auth.login'))

@docente_bp.route('/dashboard')
def dashboard():
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    if not docente:
        flash('Perfil de docente no encontrado.', 'error')
        return redirect(url_for('auth.logout'))
    
    cursos = Curso.query.filter_by(docente_id=docente.id, activo=True).all()
    return render_template('docente/dashboard.html', docente=docente, cursos=cursos)

@docente_bp.route('/curso/<int:curso_id>')
def curso_detalle(curso_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    curso = Curso.query.filter_by(id=curso_id, docente_id=docente.id).first()
    
    if not curso:
        flash('Curso no encontrado o no tienes permisos para acceder.', 'error')
        return redirect(url_for('docente.dashboard'))
    
    estudiantes = curso.estudiantes
    return render_template('docente/curso_detalle.html', curso=curso, estudiantes=estudiantes)

@docente_bp.route('/asistencias/<int:curso_id>')
def asistencias(curso_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    curso = Curso.query.filter_by(id=curso_id, docente_id=docente.id).first()
    
    if not curso:
        flash('Curso no encontrado.', 'error')
        return redirect(url_for('docente.dashboard'))
    
    fecha_seleccionada = request.args.get('fecha', date.today().isoformat())
    asistencias = Asistencia.query.filter_by(curso_id=curso_id, fecha=fecha_seleccionada).all()
    
    return render_template('docente/asistencias.html', curso=curso, asistencias=asistencias, fecha_seleccionada=fecha_seleccionada)

@docente_bp.route('/registrar_asistencia', methods=['POST'])
def registrar_asistencia():
    curso_id = request.form.get('curso_id')
    fecha = request.form.get('fecha')
    asistencias_data = request.form.getlist('asistencias')
    
    try:
        # Eliminar asistencias existentes para esa fecha y curso
        Asistencia.query.filter_by(curso_id=curso_id, fecha=fecha).delete()
        
        # Registrar nuevas asistencias
        for asistencia_str in asistencias_data:
            estudiante_id, estado = asistencia_str.split('|')
            
            # Obtener observaciones para este estudiante
            observacion_key = f'observacion_{estudiante_id}'
            observaciones = request.form.get(observacion_key, '')
            
            asistencia = Asistencia(
                estudiante_id=int(estudiante_id),
                curso_id=int(curso_id),
                fecha=datetime.strptime(fecha, '%Y-%m-%d').date(),
                estado=estado,
                observaciones=observaciones
            )
            db.session.add(asistencia)
        
        db.session.commit()
        flash('Asistencia registrada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al registrar la asistencia.', 'error')
    
    return redirect(url_for('docente.asistencias', curso_id=curso_id))

@docente_bp.route('/notas/<int:curso_id>')
def notas(curso_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    curso = Curso.query.filter_by(id=curso_id, docente_id=docente.id).first()
    
    if not curso:
        flash('Curso no encontrado.', 'error')
        return redirect(url_for('docente.dashboard'))
    
    notas = Nota.query.filter_by(curso_id=curso_id).order_by(Nota.fecha_evaluacion.desc()).all()
    return render_template('docente/notas.html', curso=curso, notas=notas)

@docente_bp.route('/registrar_nota', methods=['GET', 'POST'])
def registrar_nota():
    curso_id = request.args.get('curso_id') or request.form.get('curso_id')
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    curso = Curso.query.filter_by(id=curso_id, docente_id=docente.id).first()
    
    if not curso:
        flash('Curso no encontrado.', 'error')
        return redirect(url_for('docente.dashboard'))
    
    if request.method == 'POST':
        try:
            estudiante_id = request.form.get('estudiante_id')
            tipo_evaluacion = request.form.get('tipo_evaluacion')
            descripcion = request.form.get('descripcion')
            calificacion = float(request.form.get('calificacion'))
            calificacion_maxima = float(request.form.get('calificacion_maxima', 20))
            periodo = request.form.get('periodo')
            fecha_evaluacion = datetime.strptime(request.form.get('fecha_evaluacion'), '%Y-%m-%d').date()
            observaciones = request.form.get('observaciones', '')
            
            nota = Nota(
                estudiante_id=int(estudiante_id),
                curso_id=int(curso_id),
                tipo_evaluacion=tipo_evaluacion,
                descripcion=descripcion,
                calificacion=calificacion,
                calificacion_maxima=calificacion_maxima,
                periodo=periodo,
                fecha_evaluacion=fecha_evaluacion,
                observaciones=observaciones
            )
            
            db.session.add(nota)
            db.session.commit()
            
            flash('Nota registrada correctamente.', 'success')
            return redirect(url_for('docente.notas', curso_id=curso_id))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar la nota.', 'error')
    
    return render_template('docente/registrar_nota.html', curso=curso)

@docente_bp.route('/comunicados')
def comunicados():
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    comunicados = Comunicado.query.filter_by(docente_id=docente.id).order_by(Comunicado.fecha_publicacion.desc()).all()
    return render_template('docente/comunicados.html', comunicados=comunicados)

@docente_bp.route('/crear_comunicado', methods=['GET', 'POST'])
def crear_comunicado():
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    cursos = Curso.query.filter_by(docente_id=docente.id, activo=True).all()
    
    if request.method == 'POST':
        try:
            titulo = request.form.get('titulo')
            contenido = request.form.get('contenido')
            tipo = request.form.get('tipo', 'general')
            dirigido_a = request.form.get('dirigido_a', 'padres')
            curso_id = request.form.get('curso_id')
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            prioritario = bool(request.form.get('prioritario'))
            
            comunicado = Comunicado(
                docente_id=docente.id,
                titulo=titulo,
                contenido=contenido,
                tipo=tipo,
                dirigido_a=dirigido_a,
                curso_id=int(curso_id) if curso_id else None,
                fecha_vencimiento=datetime.strptime(fecha_vencimiento, '%Y-%m-%d') if fecha_vencimiento else None,
                prioritario=prioritario
            )
            
            db.session.add(comunicado)
            db.session.commit()
            
            flash('Comunicado creado correctamente.', 'success')
            return redirect(url_for('docente.comunicados'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el comunicado.', 'error')
    
    return render_template('docente/crear_comunicado.html', cursos=cursos)

@docente_bp.route('/editar_comunicado/<int:comunicado_id>', methods=['GET', 'POST'])
def editar_comunicado(comunicado_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    comunicado = Comunicado.query.filter_by(id=comunicado_id, docente_id=docente.id).first()
    
    if not comunicado:
        flash('Comunicado no encontrado.', 'error')
        return redirect(url_for('docente.comunicados'))
    
    cursos = Curso.query.filter_by(docente_id=docente.id, activo=True).all()
    
    if request.method == 'POST':
        try:
            comunicado.titulo = request.form.get('titulo')
            comunicado.contenido = request.form.get('contenido')
            comunicado.tipo = request.form.get('tipo', 'general')
            comunicado.dirigido_a = request.form.get('dirigido_a', 'padres')
            
            curso_id = request.form.get('curso_id')
            comunicado.curso_id = int(curso_id) if curso_id else None
            
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            comunicado.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d') if fecha_vencimiento else None
            
            comunicado.prioritario = bool(request.form.get('prioritario'))
            
            db.session.commit()
            
            flash('Comunicado actualizado correctamente.', 'success')
            return redirect(url_for('docente.comunicados'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar el comunicado.', 'error')
    
    return render_template('docente/editar_comunicado.html', comunicado=comunicado, cursos=cursos)

@docente_bp.route('/eliminar_comunicado/<int:comunicado_id>', methods=['POST'])
def eliminar_comunicado(comunicado_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    comunicado = Comunicado.query.filter_by(id=comunicado_id, docente_id=docente.id).first()
    
    if not comunicado:
        return jsonify({'success': False, 'message': 'Comunicado no encontrado'})
    
    try:
        db.session.delete(comunicado)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Comunicado eliminado correctamente'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error al eliminar el comunicado'})

@docente_bp.route('/chat')
def chat():
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    
    # Obtener padres que tienen hijos en cursos del docente
    padres_ids = set()
    for curso in docente.cursos:
        for estudiante in curso.estudiantes:
            padres_ids.add(estudiante.padre_id)
    
    from app.models.usuario_model import Usuario
    padres = Usuario.query.filter(Usuario.id.in_(padres_ids)).all()
    
    return render_template('docente/chat.html', padres=padres)

@docente_bp.route('/chat_conversacion/<int:padre_id>')
def chat_conversacion(padre_id):
    docente = Docente.query.filter_by(usuario_id=current_user.id).first()
    
    # Obtener mensajes entre el docente actual y el padre
    mensajes = Chat.query.filter(
        db.or_(
            db.and_(Chat.emisor_id == current_user.id, Chat.receptor_id == padre_id),
            db.and_(Chat.emisor_id == padre_id, Chat.receptor_id == current_user.id)
        )
    ).order_by(Chat.fecha_envio.asc()).all()
    
    # Marcar mensajes como leídos
    for mensaje in mensajes:
        if mensaje.receptor_id == current_user.id:
            mensaje.marcar_como_leido()
    
    db.session.commit()
    
    from app.models.usuario_model import Usuario
    padre = Usuario.query.get(padre_id)
    
    return render_template('docente/chat_conversacion.html', padre=padre, mensajes=mensajes)

@docente_bp.route('/enviar_mensaje', methods=['POST'])
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