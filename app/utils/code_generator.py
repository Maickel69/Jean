"""
Generador automático de códigos para las entidades del sistema.
Genera códigos únicos y secuenciales para estudiantes, docentes, cursos y padres.
"""

from datetime import datetime
from app import db
from sqlalchemy import text
import re


class CodeGenerator:
    """Generador de códigos automáticos para entidades del sistema"""
    
    @staticmethod
    def generate_student_code() -> str:
        """
        Genera código automático para estudiante: EST-YYYY-####
        Ejemplo: EST-2024-0001
        """
        current_year = datetime.now().year
        prefix = f"EST-{current_year}-"
        
        # Buscar el último número usado este año
        query = text("""
            SELECT codigo_estudiante 
            FROM estudiantes 
            WHERE codigo_estudiante LIKE :pattern 
            ORDER BY CAST(SUBSTR(codigo_estudiante, -4) as INTEGER) DESC 
            LIMIT 1
        """)
        
        result = db.session.execute(query, {"pattern": f"{prefix}%"}).fetchone()
        
        if result:
            # Extraer el número del último código
            last_code = result[0]
            match = re.search(r'EST-\d{4}-(\d{4})', last_code)
            if match:
                last_number = int(match.group(1))
                new_number = last_number + 1
            else:
                new_number = 1
        else:
            new_number = 1
        
        # Verificar que el código sea único
        code = f"{prefix}{new_number:04d}"
        while True:
            check_query = text("SELECT id FROM estudiantes WHERE codigo_estudiante = :code")
            exists = db.session.execute(check_query, {"code": code}).fetchone()
            if not exists:
                break
            new_number += 1
            code = f"{prefix}{new_number:04d}"
        
        return code
    
    @staticmethod
    def generate_teacher_code() -> str:
        """
        Genera código automático para docente: DOC-YYYY-####
        Ejemplo: DOC-2024-0001
        """
        current_year = datetime.now().year
        prefix = f"DOC-{current_year}-"
        
        # Buscar el último número usado este año
        query = text("""
            SELECT codigo_docente 
            FROM docentes 
            WHERE codigo_docente LIKE :pattern 
            ORDER BY CAST(SUBSTR(codigo_docente, -4) as INTEGER) DESC 
            LIMIT 1
        """)
        
        result = db.session.execute(query, {"pattern": f"{prefix}%"}).fetchone()
        
        if result:
            # Extraer el número del último código
            last_code = result[0]
            match = re.search(r'DOC-\d{4}-(\d{4})', last_code)
            if match:
                last_number = int(match.group(1))
                new_number = last_number + 1
            else:
                new_number = 1
        else:
            new_number = 1
        
        # Verificar que el código sea único
        code = f"{prefix}{new_number:04d}"
        while True:
            check_query = text("SELECT id FROM docentes WHERE codigo_docente = :code")
            exists = db.session.execute(check_query, {"code": code}).fetchone()
            if not exists:
                break
            new_number += 1
            code = f"{prefix}{new_number:04d}"
        
        return code
    
    @staticmethod
    def generate_parent_code() -> str:
        """
        Genera código automático para padre: PAD-YYYY-####
        Ejemplo: PAD-2024-0001
        """
        current_year = datetime.now().year
        prefix = f"PAD-{current_year}-"
        
        # Buscar el último número usado este año
        query = text("""
            SELECT codigo_padre 
            FROM usuarios 
            WHERE tipo_usuario = 'padre' 
            AND codigo_padre LIKE :pattern 
            ORDER BY CAST(SUBSTR(codigo_padre, -4) as INTEGER) DESC 
            LIMIT 1
        """)
        
        result = db.session.execute(query, {"pattern": f"{prefix}%"}).fetchone()
        
        if result:
            # Extraer el número del último código
            last_code = result[0]
            match = re.search(r'PAD-\d{4}-(\d{4})', last_code)
            if match:
                last_number = int(match.group(1))
                new_number = last_number + 1
            else:
                new_number = 1
        else:
            new_number = 1
        
        # Verificar que el código sea único
        code = f"{prefix}{new_number:04d}"
        while True:
            check_query = text("SELECT id FROM usuarios WHERE codigo_padre = :code")
            exists = db.session.execute(check_query, {"code": code}).fetchone()
            if not exists:
                break
            new_number += 1
            code = f"{prefix}{new_number:04d}"
        
        return code
    
    @staticmethod
    def generate_course_code(materia: str, grado: str, seccion: str) -> str:
        """
        Genera código automático para curso: MAT-GRADO-SECCION
        Ejemplo: MAT-5-A, COM-3-B, CIE-6-C
        
        Args:
            materia: Nombre de la materia
            grado: Grado del curso
            seccion: Sección del curso
        """
        # Mapeo de materias a códigos
        materia_codes = {
            'matematicas': 'MAT',
            'matemáticas': 'MAT',
            'comunicacion': 'COM',
            'comunicación': 'COM',
            'ciencias': 'CIE',
            'ciencia': 'CIE',
            'historia': 'HIS',
            'geografia': 'GEO',
            'geografía': 'GEO',
            'educacion fisica': 'EDF',
            'educación física': 'EDF',
            'arte': 'ART',
            'musica': 'MUS',
            'música': 'MUS',
            'ingles': 'ING',
            'inglés': 'ING',
            'religion': 'REL',
            'religión': 'REL',
            'personal social': 'PSO',
            'ciencia y tecnologia': 'CYT',
            'ciencia y tecnología': 'CYT'
        }
        
        # Limpiar y normalizar el nombre de la materia
        materia_clean = materia.lower().strip()
        
        # Buscar código de materia
        materia_code = None
        for key, value in materia_codes.items():
            if key in materia_clean:
                materia_code = value
                break
        
        # Si no encuentra coincidencia, usar las primeras 3 letras en mayúscula
        if not materia_code:
            materia_code = materia_clean.replace(' ', '')[:3].upper()
        
        # Extraer número del grado
        grado_num = re.search(r'(\d+)', grado)
        grado_code = grado_num.group(1) if grado_num else grado[:2].upper()
        
        # Generar código base
        base_code = f"{materia_code}-{grado_code}-{seccion.upper()}"
        
        # Verificar si el código ya existe y generar uno único
        counter = 1
        final_code = base_code
        
        while True:
            query = text("SELECT id FROM cursos WHERE codigo = :codigo")
            result = db.session.execute(query, {"codigo": final_code}).fetchone()
            
            if not result:
                break
            
            final_code = f"{base_code}-{counter:02d}"
            counter += 1
        
        return final_code
    
    @staticmethod
    def validate_code_uniqueness(table: str, column: str, code: str) -> bool:
        """
        Valida que un código sea único en la tabla especificada
        
        Args:
            table: Nombre de la tabla
            column: Nombre de la columna
            code: Código a validar
            
        Returns:
            True si el código es único, False si ya existe
        """
        query = text(f"SELECT id FROM {table} WHERE {column} = :code")
        result = db.session.execute(query, {"code": code}).fetchone()
        return result is None 