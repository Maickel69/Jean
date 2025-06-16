#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias estén instaladas
"""

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'flask_migrate',
        'flask_wtf',
        'wtforms',
        'werkzeug',
        'jinja2',
        'markupsafe',
        'itsdangerous',
        'click',
        'blinker',
        'dotenv',
        'alembic'
    ]
    
    errores = []
    exitos = []
    
    print("🔍 Verificando dependencias...")
    print("=" * 50)
    
    for dep in dependencias:
        try:
            # Intentar importar cada dependencia
            if dep == 'dotenv':
                import dotenv
            elif dep == 'flask_sqlalchemy':
                import flask_sqlalchemy
            elif dep == 'flask_login':
                import flask_login
            elif dep == 'flask_migrate':
                import flask_migrate
            elif dep == 'flask_wtf':
                import flask_wtf
            else:
                __import__(dep)
            
            print(f"✅ {dep:<20} - Instalado correctamente")
            exitos.append(dep)
            
        except ImportError as e:
            print(f"❌ {dep:<20} - FALTA: {str(e)}")
            errores.append((dep, str(e)))
    
    print("=" * 50)
    print(f"📊 Resumen: {len(exitos)} instaladas, {len(errores)} faltantes")
    
    if errores:
        print("\n🚨 DEPENDENCIAS FALTANTES:")
        print("-" * 30)
        
        dependencias_pip = {
            'flask': 'Flask==2.3.3',
            'flask_sqlalchemy': 'Flask-SQLAlchemy==3.0.5',
            'flask_login': 'Flask-Login==0.6.3',
            'flask_migrate': 'Flask-Migrate==4.0.5',
            'flask_wtf': 'Flask-WTF==1.1.1',
            'wtforms': 'WTForms==3.0.1',
            'werkzeug': 'Werkzeug==2.3.7',
            'jinja2': 'Jinja2==3.1.2',
            'markupsafe': 'MarkupSafe==2.1.3',
            'itsdangerous': 'itsdangerous==2.1.2',
            'click': 'click==8.1.7',
            'blinker': 'blinker==1.6.3',
            'dotenv': 'python-dotenv==1.0.0',
            'alembic': 'Alembic==1.12.0'
        }
        
        for dep, error in errores:
            pip_name = dependencias_pip.get(dep, dep)
            print(f"pip install {pip_name}")
        
        print("\n💡 SOLUCION RAPIDA:")
        print("pip install -r requirements.txt --upgrade")
        
        return False
    else:
        print("\n🎉 ¡Todas las dependencias están instaladas correctamente!")
        print("✅ Puedes ejecutar: python init_db.py")
        return True

if __name__ == '__main__':
    import sys
    
    print("🔧 VERIFICADOR DE DEPENDENCIAS")
    print("Sistema de Gestión Educativa")
    print()
    
    if verificar_dependencias():
        print("\n🚀 Todo listo para ejecutar la aplicación!")
        sys.exit(0)
    else:
        print("\n⚠️  Instala las dependencias faltantes antes de continuar.")
        sys.exit(1) 