import os
import re
from pathlib import Path

def apply_corporate_theme():
    """
    Aplica el tema corporativo a todos los templates de forma sistemática
    """
    base_dir = Path("app/templates")
    
    # Patrones de reemplazo para hacer la conversión automática
    patterns = [
        # Headers generales
        (r'class="card-modern card-glass animate-fade-in"', 
         'class="dashboard-header corporate-theme"'),
        
        # Cards modernas a corporativas
        (r'class="card-modern(?:\s+[\w-]+)*"', 
         'class="card corporate-theme"'),
        
        # Headers de cards
        (r'class="card-modern-header"', 
         'class="section-header corporate-theme"'),
        
        # Cuerpos de cards
        (r'class="card-modern-body"', 
         'class="card-body"'),
        
        # Botones modernos a corporativos
        (r'class="btn-modern btn-primary-modern(?:\s+[\w-]+)*"', 
         'class="btn btn-primary corporate-theme"'),
        
        (r'class="btn-modern btn-secondary-modern(?:\s+[\w-]+)*"', 
         'class="btn btn-secondary corporate-theme"'),
        
        # Forms
        (r'class="form-control"', 
         'class="form-control corporate-theme"'),
        
        (r'class="form-select"', 
         'class="form-select corporate-theme"'),
        
        (r'class="form-group"', 
         'class="form-group corporate-theme"'),
        
        # Badges y notifications
        (r'class="badge-modern badge-(\w+)"', 
         r'class="badge badge-\1 corporate-theme"'),
        
        # List groups
        (r'class="list-group"', 
         'class="list-group corporate-theme"'),
        
        (r'class="list-group-item"', 
         'class="list-group-item corporate-theme"'),
        
        # Modals
        (r'class="modal"', 
         'class="modal corporate-theme"'),
    ]
    
    # Archivos a procesar
    template_files = []
    
    # Recorrer todas las carpetas de templates
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                template_files.append(Path(root) / file)
    
    print(f"🎨 Aplicando tema corporativo a {len(template_files)} templates...")
    
    for template_file in template_files:
        try:
            # Leer el archivo
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Aplicar los patrones de reemplazo
            original_content = content
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            
            # Solo escribir si hubo cambios
            if content != original_content:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Actualizado: {template_file}")
            else:
                print(f"ℹ️  Sin cambios: {template_file}")
                
        except Exception as e:
            print(f"❌ Error procesando {template_file}: {e}")
    
    print(f"\n🎉 ¡Tema corporativo aplicado exitosamente!")

def add_aos_animations():
    """
    Agregar animaciones AOS a los templates
    """
    aos_patterns = [
        # Headers
        (r'(<div class="dashboard-header[^>]*>)', 
         r'\1 data-aos="fade-down"'),
        
        # Cards principales
        (r'(<div class="card corporate-theme[^>]*>)', 
         r'\1 data-aos="fade-up"'),
        
        # Stats cards
        (r'(<div class="stat-card[^>]*>)', 
         r'\1 data-aos="zoom-in"'),
    ]
    
    base_dir = Path("app/templates")
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                template_file = Path(root) / file
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for pattern, replacement in aos_patterns:
                        content = re.sub(pattern, replacement, content)
                    
                    with open(template_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
                except Exception as e:
                    print(f"Error adding AOS to {template_file}: {e}")

if __name__ == "__main__":
    apply_corporate_theme()
    add_aos_animations()
    print("\n🚀 ¡Proceso completado! Todos los templates ahora usan el tema corporativo profesional.") 