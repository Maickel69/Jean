#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de prueba
"""

from app import create_app, db
from app.models.usuario_model import Usuario
from app.models.estudiante_model import Estudiante
from app.models.docente_model import Docente
from app.models.curso_model import Curso
from app.models.nota_model import Nota
from app.models.asistencia_model import Asistencia
from app.models.reunion_model import Reunion
from app.models.comunicado_model import Comunicado
from app.models.cuota_model import Cuota
from app.models.chat_model import Chat
from datetime import datetime, date, timedelta

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes
            db.drop_all()
            # Crear todas las tablas
            db.create_all()
            
            print("🗃️  Base de datos recreada correctamente")
            
            # Verificar que las tablas estén vacías
            from app.models.docente_model import Docente
            from app.models.usuario_model import Usuario
            
            docente_count = Docente.query.count()
            usuario_count = Usuario.query.count()
            
            if docente_count > 0 or usuario_count > 0:
                print("⚠️  ADVERTENCIA: La base de datos no está completamente vacía")
                print(f"   Docentes existentes: {docente_count}")
                print(f"   Usuarios existentes: {usuario_count}")
                print("   Limpiando registros existentes...")
                
                # Limpiar manualmente si es necesario
                db.session.execute(db.text('DELETE FROM docentes'))
                db.session.execute(db.text('DELETE FROM usuarios'))
                db.session.commit()
                print("✅ Base de datos limpiada manualmente")
                
        except Exception as e:
            print(f"❌ Error al limpiar base de datos: {e}")
            print("   Intentando continuar...")
        
        # Crear usuarios padre
        padre1 = Usuario(
            nombre_usuario='padre1',
            email='padre1@email.com',
            nombre_completo='Carlos García Mendoza',
            telefono='987654321',
            tipo_usuario='padre'
        )
        padre1.set_password('123456')
        
        padre2 = Usuario(
            nombre_usuario='padre2',
            email='padre2@email.com',
            nombre_completo='María López Rodríguez',
            telefono='987654322',
            tipo_usuario='padre'
        )
        padre2.set_password('123456')
        
        # Crear usuario administrador
        admin = Usuario(
            nombre_usuario='admin',
            email='admin@email.com',
            nombre_completo='Administrador del Sistema',
            telefono='987654320',
            tipo_usuario='administrador'
        )
        admin.set_password('admin123')
        
        # Crear usuarios docente
        docente_usuario1 = Usuario(
            nombre_usuario='docente1',
            email='docente1@email.com',
            nombre_completo='Ana Martínez Silva',
            telefono='987654323',
            tipo_usuario='docente'
        )
        docente_usuario1.set_password('123456')
        
        docente_usuario2 = Usuario(
            nombre_usuario='docente2',
            email='docente2@email.com',
            nombre_completo='Luis Hernández Torres',
            telefono='987654324',
            tipo_usuario='docente'
        )
        docente_usuario2.set_password('123456')
        
        db.session.add_all([admin, padre1, padre2, docente_usuario1, docente_usuario2])
        db.session.commit()
        
        print("👥 Usuarios creados")
        
        # Crear perfiles de docentes
        docente1 = Docente(
            usuario_id=docente_usuario1.id,
            especialidad='Matemáticas',
            titulo='Licenciado en Educación Matemática',
            anos_experiencia=8,
            horario_atencion='Lunes a Viernes 2:00 PM - 4:00 PM'
        )
        
        docente2 = Docente(
            usuario_id=docente_usuario2.id,
            especialidad='Comunicación',
            titulo='Licenciado en Lengua y Literatura',
            anos_experiencia=5,
            horario_atencion='Martes y Jueves 3:00 PM - 5:00 PM'
        )
        
        db.session.add_all([docente1, docente2])
        db.session.commit()
        
        print("👨‍🏫 Docentes creados")
        
        # Crear estudiantes
        estudiante1 = Estudiante(
            nombre_completo='Juan Carlos García López',
            fecha_nacimiento=date(2012, 5, 15),
            grado='5to Primaria',
            seccion='A',
            codigo_estudiante='EST001',
            padre_id=padre1.id
        )
        
        estudiante2 = Estudiante(
            nombre_completo='Ana María García López',
            fecha_nacimiento=date(2014, 8, 22),
            grado='3ro Primaria',
            seccion='B',
            codigo_estudiante='EST002',
            padre_id=padre1.id
        )
        
        estudiante3 = Estudiante(
            nombre_completo='Sofia López Ramírez',
            fecha_nacimiento=date(2013, 3, 10),
            grado='4to Primaria',
            seccion='A',
            codigo_estudiante='EST003',
            padre_id=padre2.id
        )
        
        db.session.add_all([estudiante1, estudiante2, estudiante3])
        db.session.commit()
        
        print("👨‍🎓 Estudiantes creados")
        
        # Crear cursos
        curso1 = Curso(
            nombre='Matemáticas 5to',
            codigo='MAT5A',
            descripcion='Curso de matemáticas para quinto grado',
            grado='5to Primaria',
            seccion='A',
            docente_id=docente1.id,
            creditos=4,
            fecha_inicio=date(2024, 3, 1),
            fecha_fin=date(2024, 12, 15)
        )
        
        curso2 = Curso(
            nombre='Comunicación 5to',
            codigo='COM5A',
            descripcion='Curso de comunicación para quinto grado',
            grado='5to Primaria',
            seccion='A',
            docente_id=docente2.id,
            creditos=4,
            fecha_inicio=date(2024, 3, 1),
            fecha_fin=date(2024, 12, 15)
        )
        
        curso3 = Curso(
            nombre='Matemáticas 3ro',
            codigo='MAT3B',
            descripcion='Curso de matemáticas para tercer grado',
            grado='3ro Primaria',
            seccion='B',
            docente_id=docente1.id,
            creditos=3,
            fecha_inicio=date(2024, 3, 1),
            fecha_fin=date(2024, 12, 15)
        )
        
        db.session.add_all([curso1, curso2, curso3])
        db.session.commit()
        
        # Asociar estudiantes con cursos
        estudiante1.cursos.append(curso1)
        estudiante1.cursos.append(curso2)
        estudiante2.cursos.append(curso3)
        estudiante3.cursos.append(curso1)
        estudiante3.cursos.append(curso2)
        
        db.session.commit()
        
        print("📚 Cursos creados y asociados")
        
        # Crear notas de ejemplo
        notas = [
            Nota(estudiante_id=estudiante1.id, curso_id=curso1.id, tipo_evaluacion='examen',
                 descripcion='Examen de Álgebra', calificacion=18.5, periodo='I Bimestre',
                 fecha_evaluacion=date(2024, 4, 15)),
            Nota(estudiante_id=estudiante1.id, curso_id=curso1.id, tipo_evaluacion='tarea',
                 descripcion='Tarea de Geometría', calificacion=19.0, periodo='I Bimestre',
                 fecha_evaluacion=date(2024, 4, 10)),
            Nota(estudiante_id=estudiante1.id, curso_id=curso2.id, tipo_evaluacion='examen',
                 descripcion='Comprensión Lectora', calificacion=17.5, periodo='I Bimestre',
                 fecha_evaluacion=date(2024, 4, 12)),
        ]
        
        db.session.add_all(notas)
        db.session.commit()
        
        print("📝 Notas de ejemplo creadas")
        
        # Crear asistencias de ejemplo
        asistencias = []
        for i in range(10):
            fecha_asistencia = date.today() - timedelta(days=i)
            asistencias.extend([
                Asistencia(estudiante_id=estudiante1.id, curso_id=curso1.id,
                          fecha=fecha_asistencia, estado='presente'),
                Asistencia(estudiante_id=estudiante1.id, curso_id=curso2.id,
                          fecha=fecha_asistencia, estado='presente'),
            ])
        
        # Agregar algunas faltas
        asistencias.append(
            Asistencia(estudiante_id=estudiante1.id, curso_id=curso1.id,
                      fecha=date.today() - timedelta(days=3), estado='ausente')
        )
        
        db.session.add_all(asistencias)
        db.session.commit()
        
        print("📅 Asistencias de ejemplo creadas")
        
        # Crear comunicados
        comunicados = [
            Comunicado(
                docente_id=docente1.id,
                titulo='Reunión de Padres de Familia',
                contenido='Se convoca a todos los padres de familia a la reunión del próximo viernes 15 de marzo a las 6:00 PM.',
                tipo='general',
                dirigido_a='padres',
                prioritario=True
            ),
            Comunicado(
                docente_id=docente2.id,
                titulo='Entrega de Materiales',
                contenido='Recordamos que deben entregar los materiales solicitados antes del 20 de marzo.',
                tipo='informativo',
                dirigido_a='padres',
                curso_id=curso2.id
            ),
        ]
        
        db.session.add_all(comunicados)
        db.session.commit()
        
        print("📢 Comunicados creados")
        
        # Crear cuotas
        cuotas = [
            Cuota(
                estudiante_id=estudiante1.id,
                tipo='mensualidad',
                descripcion='Mensualidad de Marzo 2024',
                monto=250.00,
                fecha_vencimiento=date(2024, 3, 15),
                estado='pagado',
                fecha_pago=datetime(2024, 3, 10, 14, 30)
            ),
            Cuota(
                estudiante_id=estudiante1.id,
                tipo='mensualidad',
                descripcion='Mensualidad de Abril 2024',
                monto=250.00,
                fecha_vencimiento=date(2024, 4, 15),
                estado='pendiente'
            ),
            Cuota(
                estudiante_id=estudiante2.id,
                tipo='material',
                descripcion='Material educativo 2024',
                monto=75.00,
                fecha_vencimiento=date(2024, 3, 30),
                estado='vencido'
            ),
        ]
        
        db.session.add_all(cuotas)
        db.session.commit()
        
        print("💰 Cuotas creadas")
        
        # Crear reuniones
        reuniones = [
            Reunion(
                curso_id=curso1.id,
                titulo='Reunión de evaluación académica',
                descripcion='Revisión del rendimiento académico del primer bimestre',
                fecha_reunion=datetime(2024, 4, 20, 18, 0),
                modalidad='presencial',
                lugar='Aula 5A'
            ),
            Reunion(
                curso_id=curso2.id,
                titulo='Taller de lectura para padres',
                descripcion='Cómo apoyar a sus hijos en la lectura en casa',
                fecha_reunion=datetime(2024, 4, 25, 19, 0),
                modalidad='virtual',
                enlace_virtual='https://meet.google.com/abc-def-ghi'
            ),
        ]
        
        db.session.add_all(reuniones)
        db.session.commit()
        
        print("🤝 Reuniones creadas")
        
        print("\n✅ Base de datos inicializada correctamente!")
        print("\n👤 Usuarios de prueba:")
        print("   Padre 1: usuario='padre1', password='123456'")
        print("   Padre 2: usuario='padre2', password='123456'")
        print("   Docente 1: usuario='docente1', password='123456'")
        print("   Docente 2: usuario='docente2', password='123456'")
        print("\n🚀 Ejecuta 'python run.py' para iniciar el servidor")

if __name__ == '__main__':
    init_database() 