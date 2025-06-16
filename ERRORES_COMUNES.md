# 🚨 ERRORES COMUNES Y SOLUCIONES

## ❌ Error #1: "No module named 'flask_migrate'" o "No module named '[dependencia]'"

### ¿Qué hiciste mal?
- El archivo `requirements.txt` no tenía todas las dependencias necesarias
- Se instalaron dependencias de un archivo incompleto

### ¿Qué error ves?
```
ModuleNotFoundError: No module named 'flask_migrate'
ModuleNotFoundError: No module named 'alembic'
```

### ✅ Solución:
```cmd
# 1. Asegúrate de estar en el entorno virtual activado
# Si ves (venv) al inicio de la línea, está activado

# 2. Instalar las dependencias que faltan:
pip install Flask-Migrate==4.0.5
pip install Alembic==1.12.0

# 3. O reinstalar todo:
pip install -r requirements.txt --upgrade

# 4. Continuar con la inicialización:
python init_db.py
python run.py
```

### ✅ Solución Alternativa - Reinstalación Completa:
```cmd
# 1. Desactivar entorno virtual
deactivate

# 2. Eliminar carpeta venv
rmdir /s venv

# 3. Ejecutar instalación desde cero:
.\install.bat
```

---

## ❌ Error #2: "No module named 'flask'" (sin entorno virtual)

### ¿Qué hiciste mal?
```cmd
# Ejecutaste esto directamente:
python run.py
```

### ¿Por qué falla?
- Flask no está instalado en tu sistema
- No creaste un entorno virtual
- No instalaste las dependencias del proyecto

### ✅ Solución Correcta:
```cmd
# PASO 1: Instalar dependencias
.\install.bat

# PASO 2: Ejecutar aplicación
.\start.bat
```

**O manualmente:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python run.py
```

---

## ❌ Error #2: "Python no reconocido" o "No se encontró Python"

### ¿Qué hiciste mal?
- Python funciona en algunos directorios pero no en otros
- Conflicto con Microsoft Store
- Python no está en PATH correctamente

### ✅ Solución Rápida:
```cmd
# 1. Ejecutar diagnóstico
.\diagnostico_python.bat

# 2. Usar ruta completa (ejemplo):
"C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python313\python.exe" -m venv venv
```

### ✅ Solución Permanente:
1. **Desactivar alias de Microsoft Store:**
   - Ir a: `Configuración > Aplicaciones`
   - Buscar: "Configuración avanzada de aplicaciones"
   - Click: "Alias de ejecución de aplicaciones"
   - **DESACTIVAR:** `python.exe` y `python3.exe`

2. **O reinstalar Python:**
   - Descargar desde https://python.org
   - **MARCAR:** "Add Python to PATH"
   - Reiniciar terminal

---

## ❌ Error #4: "La ejecución de scripts está deshabilitada" (PowerShell)

### ¿Qué hiciste mal?
- Usaste PowerShell en lugar de Command Prompt (CMD)
- PowerShell tiene políticas de seguridad que bloquean scripts

### ¿Qué error ves?
```
No se puede cargar el archivo [...] porque la ejecución de scripts está deshabilitada en este sistema
```

### ✅ Solución Más Fácil - Usar CMD:
```cmd
# 1. Cerrar PowerShell
# 2. Abrir "Símbolo del sistema" (CMD)
# 3. Navegar a la carpeta:
cd "C:\Users\TU_USUARIO\Desktop\ADS WEB\jean"

# 4. Ejecutar instalación:
.\install.bat
```

### ✅ Solución Alternativa - Arreglar PowerShell:
```powershell
# 1. Abrir PowerShell como ADMINISTRADOR
# 2. Ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Aceptar con "Y" o "S"
# 4. Cerrar PowerShell de administrador
# 5. Probar de nuevo
```

### ✅ Solución de Emergencia - Script Automático:
```cmd
# Ejecutar este archivo:
.\solucion_powershell.bat
```

---

## ❌ Error #5: "El sistema no puede encontrar la ruta especificada"

### ¿Qué hiciste mal?
- No estás en la carpeta correcta del proyecto
- El archivo no existe en esa ubicación

### ✅ Solución:
```cmd
# Navegar a la carpeta del proyecto
cd "ruta\completa\del\proyecto"

# Verificar que existan los archivos
dir
# Deberías ver: run.py, requirements.txt, install.bat, etc.
```

---

## ❌ Error #6: "UNIQUE constraint failed" (Base de datos duplicada)

### ¿Qué hiciste mal?
- Ejecutaste `python init_db.py` múltiples veces
- La base de datos no se limpió completamente
- Ya existían datos previos

### ¿Qué error ves?
```
sqlite3.IntegrityError: UNIQUE constraint failed: docentes.codigo_docente
sqlalchemy.exc.IntegrityError: UNIQUE constraint failed
```

### ✅ Solución Rápida:
```cmd
# Verificar configuración primero:
python verificar_configuracion.py

# Limpiar TODAS las bases de datos y reiniciar:
python limpiar_db.py
python init_db.py
```

### ✅ Solución Manual:
```cmd
# Eliminar archivo de base de datos:
del instance\gestion_escolar.db

# Reinicializar:
python init_db.py
```

### ✅ Solución de Emergencia:
```cmd
# Usar el script mejorado que limpia automáticamente:
python init_db.py
# (Ahora detecta y limpia duplicados automáticamente)
```

---

## ❌ Error #7: "Port 5000 is already in use"

### ¿Qué hiciste mal?
- Ya tienes otra aplicación corriendo en puerto 5000
- Ejecutaste `run.py` múltiples veces

### ✅ Solución:
```cmd
# Opción 1: Cerrar aplicaciones que usen puerto 5000
# Opción 2: Cambiar puerto en run.py
# Opción 3: Terminar procesos Python
taskkill /f /im python.exe
```

---

## 📋 CHECKLIST ANTES DE EJECUTAR

Antes de ejecutar el proyecto, verifica:

- [ ] ✅ Python está instalado (`python --version`)
- [ ] ✅ Estás en la carpeta correcta del proyecto
- [ ] ✅ Existen los archivos: `run.py`, `requirements.txt`, `install.bat`
- [ ] ✅ **NO ejecutes `python run.py` directamente**
- [ ] ✅ Usa `install.bat` primero, luego `start.bat`

---

## 🎯 PROCESO CORRECTO (PASO A PASO)

```cmd
# 1. Descargar proyecto
git clone [repo-url]

# 2. Navegar a carpeta
cd [carpeta-proyecto]

# 3. Verificar archivos
dir

# 4. Instalación automática
.\install.bat

# 5. Ejecutar aplicación
.\start.bat

# 6. Abrir navegador
# http://localhost:5000
```

---

## 📞 ¿Sigues con problemas?

1. Lee INSTALACION_RAPIDA.md
2. Lee README.md sección "Solución de Problemas"
3. Verifica que seguiste TODOS los pasos en orden
4. NO saltes pasos
5. NO ejecutes `run.py` directamente nunca 