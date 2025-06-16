@echo off
echo ========================================
echo   SOLUCION PARA PROBLEMA DE POWERSHELL
echo ========================================
echo.

echo PROBLEMA DETECTADO:
echo "No se puede cargar el archivo [...] porque la ejecucion de scripts esta deshabilitada"
echo.

echo SOLUCION 1: Usar Command Prompt (CMD) - MAS FACIL
echo ================================================
echo 1. Cierra PowerShell
echo 2. Abre "Simbolo del sistema" (CMD)
echo 3. Navega a la carpeta del proyecto:
echo    cd "C:\Users\Lenovo\Desktop\ADS WEB\jean"
echo 4. Ejecuta: install.bat
echo.
pause

echo SOLUCION 2: Arreglar PowerShell - MAS COMPLEJO
echo ===============================================
echo 1. Abre PowerShell como ADMINISTRADOR
echo 2. Ejecuta este comando:
echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo 3. Acepta cuando te pregunte (Y/Si)
echo 4. Cierra PowerShell de administrador
echo 5. Abre PowerShell normal y prueba de nuevo
echo.
pause

echo SOLUCION 3: Instalacion manual sin entorno virtual
echo ==================================================
echo Ejecuta estos comandos en PowerShell:
echo.
echo 1. Navegar a la carpeta:
echo    cd "C:\Users\Lenovo\Desktop\ADS WEB\jean"
echo.
echo 2. Instalar dependencias:
echo    C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
echo.
echo 3. Inicializar base de datos:
echo    C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\python.exe init_db.py
echo.
echo 4. Ejecutar aplicacion:
echo    C:\Users\Lenovo\AppData\Local\Programs\Python\Python313\python.exe run.py
echo.
pause

echo ========================================
echo   RECOMENDACION
echo ========================================
echo.
echo La SOLUCION 1 (usar CMD) es la mas facil y rapida.
echo.
echo ¿Quieres que abra CMD automaticamente?
echo Presiona cualquier tecla para continuar...
pause >nul

echo Abriendo Command Prompt...
start cmd /k "cd /d \"%~dp0\" && echo Estas en Command Prompt. Ahora ejecuta: install.bat"
echo.
echo ✓ CMD abierto. Ejecuta 'install.bat' en la nueva ventana.
pause 