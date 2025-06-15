# 🏫 Sistema de Gestión Educativa

Sistema completo de gestión educativa desarrollado en Flask con funcionalidades para administradores, docentes y padres de familia.

## 📋 Requisitos Previos

- **Python 3.8 o superior** (verificar con `python --version`)
- **pip** (gestor de paquetes de Python, viene incluido con Python)

## 🚀 Instalación y Configuración

### 1. Descargar el Proyecto
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_PROYECTO]
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```bash
# Ejecutar script de inicialización
python init_db.py
```

### 5. Ejecutar la Aplicación
```bash
python run.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 👥 Usuarios de Prueba

### Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`

### Docentes
- **Usuario:** `docente1` | **Contraseña:** `123456`
- **Usuario:** `docente2` | **Contraseña:** `123456`
- **Usuario:** `docente_nuevo1` | **Contraseña:** `123456`
- **Usuario:** `docente_nuevo2` | **Contraseña:** `123456`

### Padres de Familia
- **Usuario:** `padre_test_1` | **Contraseña:** `123456`
- **Usuario:** `padre_test_2` | **Contraseña:** `123456`
- **Usuario:** `Razoky` | **Contraseña:** `123456`

## 🏗️ Estructura del Proyecto

```
proyecto/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Rutas y controladores
│   ├── templates/       # Plantillas HTML
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   └── utils/           # Utilidades y helpers
├── instance/            # Base de datos SQLite
├── requirements.txt     # Dependencias del proyecto
├── run.py              # Archivo principal para ejecutar
├── init_db.py          # Inicialización de base de datos
└── README.md           # Este archivo
```

## 🔧 Funcionalidades

### Para Administradores
- ✅ Gestión completa de usuarios
- ✅ Administración de estudiantes y docentes
- ✅ Sistema de matrículas (individual y masiva)
- ✅ Reportes y estadísticas
- ✅ Gestión de cursos y materias
- ✅ Control de cuotas y pagos

### Para Docentes
- ✅ Dashboard personalizado
- ✅ Gestión de asistencia
- ✅ Registro de calificaciones
- ✅ Comunicados y anuncios
- ✅ Chat con padres de familia
- ✅ Programación de reuniones

### Para Padres de Familia
- ✅ Portal de seguimiento académico
- ✅ Consulta de notas y asistencia
- ✅ Comunicación con docentes
- ✅ Estado de cuotas y pagos
- ✅ Calendario de actividades

## 🛠️ Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install flask
```

### Error: "Database not found"
```bash
python init_db.py
```

### Error: "Port already in use"
- Cambiar el puerto en `run.py` o cerrar otras aplicaciones que usen el puerto 5000

### La aplicación no carga
- Verificar que todas las dependencias estén instaladas
- Asegurarse de que el entorno virtual esté activado
- Revisar que Python 3.8+ esté instalado

## 📞 Soporte

Si encuentras algún problema durante la instalación o ejecución:

1. Verifica que Python esté correctamente instalado
2. Asegúrate de que todas las dependencias se instalaron sin errores
3. Revisa que la base de datos se haya inicializado correctamente
4. Consulta la sección de solución de problemas

## 🔄 Actualización del Sistema

Para actualizar el sistema:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python init_db.py
```

---

**Desarrollado con ❤️ usando Flask y Python** 