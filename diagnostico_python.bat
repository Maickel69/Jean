@echo off
echo ========================================
echo   DIAGNOSTICO DE PYTHON EN WINDOWS
echo ========================================
echo.

echo [1] Verificando comando 'python'...
python --version 2>nul
if not errorlevel 1 (
    echo ✓ 'python' funciona
    python -c "import sys; print('Ubicacion:', sys.executable)"
) else (
    echo ❌ 'python' no funciona
)
echo.

echo [2] Verificando comando 'python3'...
python3 --version 2>nul
if not errorlevel 1 (
    echo ✓ 'python3' funciona
    python3 -c "import sys; print('Ubicacion:', sys.executable)"
) else (
    echo ❌ 'python3' no funciona
)
echo.

echo [3] Verificando comando 'py'...
py --version 2>nul
if not errorlevel 1 (
    echo ✓ 'py' funciona
    py -c "import sys; print('Ubicacion:', sys.executable)"
) else (
    echo ❌ 'py' no funciona
)
echo.

echo [4] Buscando instalaciones de Python...
echo Ubicaciones comunes de Python:
for %%p in (
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe"
) do (
    if exist %%p (
        echo ✓ Encontrado: %%p
        %%p --version 2>nul
    )
)
echo.

echo [5] Verificando PATH...
echo PATH actual:
echo %PATH%
echo.

echo [6] Verificando alias de Microsoft Store...
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
    echo ⚠️  PROBLEMA DETECTADO: Alias de Microsoft Store activo
    echo.
    echo SOLUCION:
    echo 1. Ve a: Configuracion ^> Aplicaciones
    echo 2. Busca: "Configuracion avanzada de aplicaciones"
    echo 3. Click en: "Alias de ejecucion de aplicaciones"
    echo 4. DESACTIVA: "python.exe" y "python3.exe"
    echo.
) else (
    echo ✓ No hay conflicto con Microsoft Store
)

echo ========================================
echo   DIAGNOSTICO COMPLETADO
echo ========================================
echo.
echo Si tienes Python instalado pero no funciona en la carpeta del proyecto:
echo 1. Usa la ruta completa de Python que SI funciona
echo 2. O arregla el PATH siguiendo las instrucciones de arriba
echo.
pause 