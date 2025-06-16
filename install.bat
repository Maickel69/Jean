@echo off
echo ========================================
echo   INSTALADOR SISTEMA GESTION EDUCATIVA
echo ========================================
echo.

echo [1/5] Verificando Python...

REM Intentar con python primero
python --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo ✓ Python encontrado: python
    goto python_found
)

REM Si falla, buscar python.exe en ubicaciones comunes
for %%p in (
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
) do (
    if exist %%p (
        set PYTHON_CMD=%%p
        echo ✓ Python encontrado en: %%p
        goto python_found
    )
)

echo ERROR: No se pudo encontrar Python
echo.
echo Soluciones posibles:
echo 1. Instala Python desde https://python.org ^(marca "Add to PATH"^)
echo 2. O desactiva el alias de Microsoft Store:
echo    Configuracion ^> Aplicaciones ^> Alias de ejecucion ^> Desactivar python.exe
pause
exit /b 1

:python_found

echo.
echo [2/5] Creando entorno virtual...
%PYTHON_CMD% -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)
echo ✓ Entorno virtual creado

echo.
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ⚠️  No se pudo activar el entorno virtual
    echo Usando instalacion directa...
    set USE_DIRECT_INSTALL=1
) else (
    echo ✓ Entorno virtual activado
    set USE_DIRECT_INSTALL=0
)

echo.
echo [4/5] Instalando dependencias...
if %USE_DIRECT_INSTALL%==1 (
    echo Instalando con ruta completa de Python...
    %PYTHON_CMD% -m pip install -r requirements.txt
) else (
    pip install -r requirements.txt
)
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

echo.
echo [5/5] Inicializando base de datos...
if %USE_DIRECT_INSTALL%==1 (
    %PYTHON_CMD% init_db.py
) else (
    python init_db.py
)
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