@echo off
echo ========================================
echo   INICIANDO SISTEMA GESTION EDUCATIVA
echo ========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Iniciando servidor Flask...
echo.
echo ✓ Servidor iniciado en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python run.py 