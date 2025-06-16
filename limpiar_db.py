#!/usr/bin/env python3
"""
Script para limpiar completamente la base de datos
"""
import os
import sys

def limpiar_base_datos():
    """Elimina completamente TODOS los archivos de base de datos"""
    db_paths = [
        'instance/gestion_escolar.db',
        'instance/app.db', 
        'instance/school.sqlite',
        'instance\\gestion_escolar.db',  # Windows
        'instance\\app.db',              # Windows
        'instance\\school.sqlite',       # Windows
        'gestion_escolar.db',
        'app.db',
        'school.sqlite'
    ]
    
    eliminados = 0
    
    print("🧹 LIMPIANDO BASE DE DATOS...")
    print("=" * 40)
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"✅ Eliminado: {db_path}")
                eliminados += 1
            except Exception as e:
                print(f"❌ Error eliminando {db_path}: {e}")
        else:
            print(f"ℹ️  No existe: {db_path}")
    
    print("=" * 40)
    
    if eliminados > 0:
        print(f"🎉 ¡Base de datos limpiada! ({eliminados} archivos eliminados)")
        print("✅ Ahora puedes ejecutar: python init_db.py")
    else:
        print("ℹ️  No se encontraron archivos de base de datos para eliminar")
        print("✅ Puedes ejecutar directamente: python init_db.py")
    
    return eliminados > 0

if __name__ == '__main__':
    print("🗑️  LIMPIADOR DE BASE DE DATOS")
    print("Sistema de Gestión Educativa")
    print()
    
    limpiar_base_datos()
    
    print()
    print("💡 PRÓXIMOS PASOS:")
    print("1. python init_db.py")
    print("2. python run.py")
    print()
    input("Presiona Enter para continuar...") 