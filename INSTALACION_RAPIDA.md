# 🚀 INSTALACIÓN RÁPIDA

## Para Windows (Recomendado)

### Opción 1: Instalación Automática
1. **Descargar** el proyecto desde GitHub
2. **Doble clic** en `install.bat`
3. **Esperar** a que termine la instalación
4. **Doble clic** en `start.bat` para ejecutar
5. **Abrir** http://localhost:5000 en tu navegador

### Opción 2: Instalación Manual
```cmd
# 1. Abrir CMD o PowerShell en la carpeta del proyecto
# 2. Ejecutar estos comandos:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python run.py
```

## Para Linux/macOS

### Opción 1: Instalación Automática
```bash
# 1. Abrir terminal en la carpeta del proyecto
# 2. Ejecutar:
chmod +x install.sh start.sh
./install.sh
./start.sh
```

### Opción 2: Instalación Manual
```bash
# 1. Abrir terminal en la carpeta del proyecto
# 2. Ejecutar estos comandos:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python run.py
```

## ✅ Verificar Instalación

Si todo salió bien, deberías ver:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

## 🔑 Usuarios de Prueba

- **Admin:** `admin` / `admin123`
- **Docente:** `docente1` / `123456`
- **Padre:** `padre_test_1` / `123456`

## ❌ Problemas Comunes

### "Python no reconocido"
- Instalar Python desde https://python.org
- Marcar "Add to PATH" durante la instalación

### "pip no reconocido"
- Python no está en PATH
- Reinstalar Python marcando "Add to PATH"

### "Error al crear entorno virtual"
- Ejecutar: `python -m pip install --upgrade pip`
- Intentar de nuevo

### "Puerto en uso"
- Cerrar otras aplicaciones que usen puerto 5000
- O cambiar puerto en `run.py`

## 📞 Soporte

Si tienes problemas:
1. Verificar que Python 3.8+ esté instalado
2. Verificar que pip funcione
3. Seguir los pasos exactamente como se indica
4. Revisar la sección de problemas comunes 