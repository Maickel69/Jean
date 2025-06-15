@echo off
echo ========================================
echo   INSTALADOR SISTEMA GESTION EDUCATIVA
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)
echo ✓ Python encontrado

echo.
echo [2/5] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

echo.
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✓ Entorno virtual activado

echo.
echo [4/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

echo.
echo [5/5] Inicializando base de datos...
python init_db.py
if errorlevel 1 (
    echo ERROR: No se pudo inicializar la base de datos
    pause
    exit /b 1
)
echo ✓ Base de datos inicializada

echo.
echo ========================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar el sistema:
echo 1. Ejecuta: start.bat
echo 2. O manualmente: venv\Scripts\activate.bat && python run.py
echo.
echo La aplicacion estara disponible en: http://localhost:5000
echo.
echo Usuarios de prueba:
echo - Admin: admin / admin123
echo - Docente: docente1 / 123456
echo - Padre: padre_test_1 / 123456
echo.
pause 