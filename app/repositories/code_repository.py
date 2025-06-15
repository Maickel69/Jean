"""
Repository para manejar operaciones relacionadas con códigos automáticos.
Contiene funciones utilitarias para generar y validar códigos únicos.
"""

from app import db
from app.utils.code_generator import CodeGenerator
from app.models.estudiante_model import Estudiante
from app.models.docente_model import Docente
from app.models.curso_model import Curso
from app.models.usuario_model import Usuario
from sqlalchemy import text
from typing import Dict, List, Optional


class CodeRepository:
    """Repository para operaciones con códigos automáticos"""
    
    @staticmethod
    def regenerate_all_codes() -> Dict[str, int]:
        """
        Regenera todos los códigos del sistema para entidades que no los tengan.
        Útil para migrar datos existentes.
        
        Returns:
            Dict con contadores de códigos generados por entidad
        """
        counters = {
            'estudiantes': 0,
            'docentes': 0,
            'cursos': 0,
            'padres': 0
        }
        
        try:
            # Regenerar códigos de estudiantes
            estudiantes_sin_codigo = Estudiante.query.filter(
                (Estudiante.codigo_estudiante == None) | 
                (Estudiante.codigo_estudiante == '')
            ).all()
            
            for estudiante in estudiantes_sin_codigo:
                estudiante.codigo_estudiante = CodeGenerator.generate_student_code()
                counters['estudiantes'] += 1
            
            # Regenerar códigos de docentes
            docentes_sin_codigo = Docente.query.filter(
                (Docente.codigo_docente == None) | 
                (Docente.codigo_docente == '')
            ).all()
            
            for docente in docentes_sin_codigo:
                docente.codigo_docente = CodeGenerator.generate_teacher_code()
                counters['docentes'] += 1
            
            # Regenerar códigos de cursos
            cursos_sin_codigo = Curso.query.filter(
                (Curso.codigo == None) | 
                (Curso.codigo == '')
            ).all()
            
            for curso in cursos_sin_codigo:
                curso.codigo = CodeGenerator.generate_course_code(
                    materia=curso.nombre,
                    grado=curso.grado,
                    seccion=curso.seccion
                )
                counters['cursos'] += 1
            
            # Regenerar códigos de padres
            padres_sin_codigo = Usuario.query.filter(
                Usuario.tipo_usuario == 'padre',
                (Usuario.codigo_padre == None) | 
                (Usuario.codigo_padre == '')
            ).all()
            
            for padre in padres_sin_codigo:
                padre.codigo_padre = CodeGenerator.generate_parent_code()
                counters['padres'] += 1
            
            db.session.commit()
            return counters
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_code_statistics() -> Dict[str, Dict[str, int]]:
        """
        Obtiene estadísticas de códigos generados por año.
        
        Returns:
            Dict con estadísticas por entidad y año
        """
        stats = {
            'estudiantes': {},
            'docentes': {},
            'padres': {}
        }
        
        # Estadísticas de estudiantes
        result = db.session.execute(text("""
            SELECT 
                SUBSTR(codigo_estudiante, 5, 4) as year,
                COUNT(*) as count
            FROM estudiantes 
            WHERE codigo_estudiante LIKE 'EST-%'
            GROUP BY SUBSTR(codigo_estudiante, 5, 4)
            ORDER BY year DESC
        """))
        
        for row in result:
            stats['estudiantes'][row[0]] = row[1]
        
        # Estadísticas de docentes
        result = db.session.execute(text("""
            SELECT 
                SUBSTR(codigo_docente, 5, 4) as year,
                COUNT(*) as count
            FROM docentes 
            WHERE codigo_docente LIKE 'DOC-%'
            GROUP BY SUBSTR(codigo_docente, 5, 4)
            ORDER BY year DESC
        """))
        
        for row in result:
            stats['docentes'][row[0]] = row[1]
        
        # Estadísticas de padres
        result = db.session.execute(text("""
            SELECT 
                SUBSTR(codigo_padre, 5, 4) as year,
                COUNT(*) as count
            FROM usuarios 
            WHERE tipo_usuario = 'padre' 
            AND codigo_padre LIKE 'PAD-%'
            GROUP BY SUBSTR(codigo_padre, 5, 4)
            ORDER BY year DESC
        """))
        
        for row in result:
            stats['padres'][row[0]] = row[1]
        
        return stats
    
    @staticmethod
    def validate_all_codes() -> Dict[str, List[str]]:
        """
        Valida la integridad de todos los códigos del sistema.
        
        Returns:
            Dict con listas de códigos duplicados o inválidos por entidad
        """
        issues = {
            'estudiantes_duplicados': [],
            'docentes_duplicados': [],
            'cursos_duplicados': [],
            'padres_duplicados': [],
            'codigos_invalidos': []
        }
        
        # Buscar códigos duplicados de estudiantes
        result = db.session.execute(text("""
            SELECT codigo_estudiante, COUNT(*) 
            FROM estudiantes 
            GROUP BY codigo_estudiante 
            HAVING COUNT(*) > 1
        """))
        
        for row in result:
            issues['estudiantes_duplicados'].append(row[0])
        
        # Buscar códigos duplicados de docentes
        result = db.session.execute(text("""
            SELECT codigo_docente, COUNT(*) 
            FROM docentes 
            GROUP BY codigo_docente 
            HAVING COUNT(*) > 1
        """))
        
        for row in result:
            issues['docentes_duplicados'].append(row[0])
        
        # Buscar códigos duplicados de cursos
        result = db.session.execute(text("""
            SELECT codigo, COUNT(*) 
            FROM cursos 
            GROUP BY codigo 
            HAVING COUNT(*) > 1
        """))
        
        for row in result:
            issues['cursos_duplicados'].append(row[0])
        
        # Buscar códigos duplicados de padres
        result = db.session.execute(text("""
            SELECT codigo_padre, COUNT(*) 
            FROM usuarios 
            WHERE tipo_usuario = 'padre' 
            AND codigo_padre IS NOT NULL
            GROUP BY codigo_padre 
            HAVING COUNT(*) > 1
        """))
        
        for row in result:
            issues['padres_duplicados'].append(row[0])
        
        return issues
    
    @staticmethod
    def search_by_code(code: str) -> Optional[Dict]:
        """
        Busca una entidad por su código en todas las tablas.
        
        Args:
            code: Código a buscar
            
        Returns:
            Dict con información de la entidad encontrada o None
        """
        # Buscar en estudiantes
        estudiante = Estudiante.query.filter_by(codigo_estudiante=code).first()
        if estudiante:
            return {
                'tipo': 'estudiante',
                'id': estudiante.id,
                'codigo': estudiante.codigo_estudiante,
                'nombre': estudiante.nombre_completo,
                'detalles': f"Grado: {estudiante.grado}, Sección: {estudiante.seccion}"
            }
        
        # Buscar en docentes
        docente = Docente.query.filter_by(codigo_docente=code).first()
        if docente:
            return {
                'tipo': 'docente',
                'id': docente.id,
                'codigo': docente.codigo_docente,
                'nombre': docente.usuario.nombre_completo if docente.usuario else 'Sin usuario',
                'detalles': f"Especialidad: {docente.especialidad}"
            }
        
        # Buscar en cursos
        curso = Curso.query.filter_by(codigo=code).first()
        if curso:
            return {
                'tipo': 'curso',
                'id': curso.id,
                'codigo': curso.codigo,
                'nombre': curso.nombre,
                'detalles': f"Grado: {curso.grado}, Sección: {curso.seccion}"
            }
        
        # Buscar en padres
        padre = Usuario.query.filter(
            Usuario.tipo_usuario == 'padre',
            Usuario.codigo_padre == code
        ).first()
        if padre:
            return {
                'tipo': 'padre',
                'id': padre.id,
                'codigo': padre.codigo_padre,
                'nombre': padre.nombre_completo,
                'detalles': f"Usuario: {padre.nombre_usuario}"
            }
        
        return None 