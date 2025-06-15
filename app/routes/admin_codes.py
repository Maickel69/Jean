"""
Rutas de administración para gestión de códigos automáticos.
Solo accesible para usuarios administradores.
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app.repositories.code_repository import CodeRepository
from app.utils.code_generator import CodeGenerator

admin_codes_bp = Blueprint('admin_codes', __name__)


def admin_required(f):
    """Decorador para requerir permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'administrador':
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_codes_bp.route('/admin/codes')
@login_required
@admin_required
def codes_dashboard():
    """Dashboard principal de administración de códigos"""
    try:
        # Obtener estadísticas
        stats = CodeRepository.get_code_statistics()
        
        # Validar integridad
        issues = CodeRepository.validate_all_codes()
        has_issues = any(len(v) > 0 for v in issues.values())
        
        return render_template(
            'admin/codes_dashboard.html',
            stats=stats,
            issues=issues,
            has_issues=has_issues
        )
    except Exception as e:
        flash(f'Error al cargar el dashboard: {str(e)}', 'error')
        return redirect(url_for('main.index'))


@admin_codes_bp.route('/admin/codes/regenerate', methods=['POST'])
@login_required
@admin_required
def regenerate_codes():
    """Regenera códigos para entidades que no los tengan"""
    try:
        counters = CodeRepository.regenerate_all_codes()
        
        message = f"Códigos regenerados: {counters['estudiantes']} estudiantes, "
        message += f"{counters['docentes']} docentes, {counters['cursos']} cursos, "
        message += f"{counters['padres']} padres"
        
        flash(message, 'success')
        
        return jsonify({
            'success': True,
            'message': message,
            'counters': counters
        })
    except Exception as e:
        flash(f'Error al regenerar códigos: {str(e)}', 'error')
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@admin_codes_bp.route('/admin/codes/validate', methods=['POST'])
@login_required
@admin_required
def validate_codes():
    """Valida la integridad de todos los códigos"""
    try:
        issues = CodeRepository.validate_all_codes()
        has_issues = any(len(v) > 0 for v in issues.values())
        
        if has_issues:
            message = "Se encontraron problemas en los códigos. Revisa los detalles."
            flash(message, 'warning')
        else:
            message = "Todos los códigos son válidos y únicos."
            flash(message, 'success')
        
        return jsonify({
            'success': True,
            'has_issues': has_issues,
            'issues': issues,
            'message': message
        })
    except Exception as e:
        flash(f'Error al validar códigos: {str(e)}', 'error')
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@admin_codes_bp.route('/admin/codes/search')
@login_required
@admin_required
def search_code():
    """Busca una entidad por su código"""
    code = request.args.get('code', '').strip()
    
    if not code:
        return jsonify({
            'success': False,
            'message': 'Código no proporcionado'
        }), 400
    
    try:
        result = CodeRepository.search_by_code(code)
        
        if result:
            return jsonify({
                'success': True,
                'found': True,
                'result': result
            })
        else:
            return jsonify({
                'success': True,
                'found': False,
                'message': f'No se encontró ninguna entidad con el código: {code}'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@admin_codes_bp.route('/admin/codes/generate/preview', methods=['POST'])
@login_required
@admin_required
def generate_code_preview():
    """Genera una vista previa de códigos sin guardar en la base de datos"""
    try:
        data = request.get_json()
        entity_type = data.get('type')
        
        if entity_type == 'student':
            code = CodeGenerator.generate_student_code()
        elif entity_type == 'teacher':
            code = CodeGenerator.generate_teacher_code()
        elif entity_type == 'parent':
            code = CodeGenerator.generate_parent_code()
        elif entity_type == 'course':
            materia = data.get('materia', 'Materia')
            grado = data.get('grado', '1')
            seccion = data.get('seccion', 'A')
            code = CodeGenerator.generate_course_code(materia, grado, seccion)
        else:
            return jsonify({
                'success': False,
                'message': 'Tipo de entidad no válido'
            }), 400
        
        return jsonify({
            'success': True,
            'code': code,
            'pattern': f"Patrón para {entity_type}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@admin_codes_bp.route('/admin/codes/statistics')
@login_required
@admin_required
def get_statistics():
    """Obtiene estadísticas detalladas de códigos"""
    try:
        stats = CodeRepository.get_code_statistics()
        
        # Calcular totales
        totals = {}
        for entity, years in stats.items():
            totals[entity] = sum(years.values()) if years else 0
        
        return jsonify({
            'success': True,
            'stats': stats,
            'totals': totals
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@admin_codes_bp.route('/admin/codes/patterns')
@login_required
@admin_required
def get_code_patterns():
    """Obtiene información sobre los patrones de códigos"""
    patterns = {
        'estudiante': {
            'formato': 'EST-YYYY-####',
            'ejemplo': 'EST-2024-0001',
            'descripcion': 'Código de estudiante con año y número secuencial'
        },
        'docente': {
            'formato': 'DOC-YYYY-####',
            'ejemplo': 'DOC-2024-0001',
            'descripcion': 'Código de docente con año y número secuencial'
        },
        'padre': {
            'formato': 'PAD-YYYY-####',
            'ejemplo': 'PAD-2024-0001',
            'descripcion': 'Código de padre con año y número secuencial'
        },
        'curso': {
            'formato': 'MAT-GRADO-SECCION',
            'ejemplo': 'MAT-5-A, COM-3-B, CIE-6-C',
            'descripcion': 'Código de curso basado en materia, grado y sección'
        }
    }
    
    return jsonify({
        'success': True,
        'patterns': patterns
    }) 