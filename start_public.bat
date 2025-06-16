@echo off
title Sistema de Gestión Educativa - Acceso Público
color 0A

echo.
echo ==========================================
echo   Sistema de Gestión Educativa
echo   Configuración para Acceso Público
echo ==========================================
echo.

echo [INFO] Verificando si la aplicación está lista...
if not exist "app" (
    echo [ERROR] No se encontró la carpeta 'app'
    echo [ERROR] Asegúrate de ejecutar este script desde la carpeta del proyecto
    pause
    exit /b 1
)

echo [INFO] Iniciando aplicación Flask...
echo [INFO] La aplicación se ejecutará en http://localhost:5000
echo.
echo ==========================================
echo   INSTRUCCIONES PARA ACCESO PÚBLICO:
echo ==========================================
echo.
echo 1. Mantén esta ventana abierta
echo 2. Abre otra terminal/PowerShell
echo 3. Ejecuta: ngrok http 5000
echo 4. Ngrok te dará una URL pública
echo 5. Comparte esa URL con quien quieras
echo.
echo ¿Tienes ngrok instalado?
echo Si no: Ve a https://ngrok.com y descárgalo
echo.
echo ==========================================
echo   Presiona Ctrl+C para detener
echo ==========================================
echo.

python run.py 