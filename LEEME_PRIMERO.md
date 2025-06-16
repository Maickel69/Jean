# 🔥 LÉEME PRIMERO - INSTALACIÓN EN 30 SEGUNDOS

## ⚠️ ANTES DE HACER CUALQUIER COSA

**NO hagas esto:** ❌
```cmd
python run.py  # ¡ESTO DARÁ ERROR!
```

**Haz esto:** ✅
```cmd
.\install.bat
.\start.bat
```

## 🚀 INSTALACIÓN SÚPER RÁPIDA

### Windows (30 segundos):
1. **Doble clic** en `install.bat` 
2. **Esperar** a que termine (aparecerá "INSTALACION COMPLETADA")
3. **Doble clic** en `start.bat`
4. **Abrir** http://localhost:5000 en tu navegador

### ¿No tienes Windows?
Lee `INSTALACION_RAPIDA.md`

## 🔑 Usuarios de Prueba
- **Admin:** `admin` / `admin123`
- **Docente:** `docente1` / `123456` 
- **Padre:** `padre_test_1` / `123456`

## 🚨 ¿Errores Comunes?

### "No module named 'flask_migrate'"
**Dependencias incompletas**. Ejecuta: `pip install Flask-Migrate==4.0.5`

### "No module named 'flask'"
**NO seguiste los pasos**. Ve a `ERRORES_COMUNES.md`

### "No se encontró Python" 
**Conflicto de Windows**. Ejecuta `.\diagnostico_python.bat`

### "Ejecución de scripts deshabilitada"
**Problema de PowerShell**. Ejecuta `.\solucion_powershell.bat`

### "UNIQUE constraint failed"
**Base de datos duplicada**. Ejecuta `python limpiar_db.py`

---
**¿Dudas?** Lee `README.md` para instrucciones completas. 