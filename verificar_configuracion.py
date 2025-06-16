 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar la configuracion de la base de datos
"""
import os
from app import create_app

def verificar_configuracion():
    """Verifica que base de datos esta configurada para usar la aplicacion"""
    
    print("🔍 VERIFICANDO CONFIGURACION DE BASE DE DATOS")
    print("=" * 50)
    
    try:
        app = create_app()
        
        with app.app_context():
            # Obtener la URI de la base de datos configurada
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"📄 URI configurada: {db_uri}")
            
            # Extraer el nombre del archivo
            if 'sqlite:///' in db_uri:
                db_file = db_uri.replace('sqlite:///', '')
                print(f"📁 Archivo de BD: {db_file}")
                
                # Verificar si existe
                if os.path.exists(db_file):
                    size = os.path.getsize(db_file)
                    print(f"✅ Archivo existe: {size:,} bytes")
                else:
                    print("❌ Archivo NO existe")
            
            print()
            print("📂 ARCHIVOS EN CARPETA INSTANCE:")
            instance_dir = 'instance'
            if os.path.exists(instance_dir):
                for file in os.listdir(instance_dir):
                    if file.endswith(('.db', '.sqlite')):
                        file_path = os.path.join(instance_dir, file)
                        size = os.path.getsize(file_path)
                        print(f"   📄 {file}: {size:,} bytes")
            else:
                print("   ❌ Carpeta instance no existe")
            
            print()
            print("🔎 ANALISIS:")
            
            # Verificar si hay multiples archivos de BD
            db_files = []
            if os.path.exists('instance'):
                for file in os.listdir('instance'):
                    if file.endswith(('.db', '.sqlite')) and os.path.getsize(os.path.join('instance', file)) > 0:
                        db_files.append(file)
            
            if len(db_files) > 1:
                print("⚠️  PROBLEMA: Multiples bases de datos detectadas")
                for db_file in db_files:
                    print(f"   - {db_file}")
                print("   Esto puede causar conflictos de datos")
                print()
                print("💡 RECOMENDACION:")
                print("   1. Ejecutar: python limpiar_db.py")
                print("   2. Ejecutar: python init_db.py")
            elif len(db_files) == 1:
                print(f"✅ Una sola base de datos: {db_files[0]}")
            else:
                print("ℹ️  No hay bases de datos creadas")
                print("   Ejecutar: python init_db.py")
                
    except Exception as e:
        print(f"❌ Error al verificar configuracion: {e}")
        
    print("=" * 50)

if __name__ == '__main__':
    verificar_configuracion()
    print()
    input("Presiona Enter para continuar...") 