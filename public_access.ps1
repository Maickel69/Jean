# Sistema de Gestión Educativa - Acceso Público
# Configuración automática para acceso desde internet

Write-Host "===========================================" -ForegroundColor Green
Write-Host "   Sistema de Gestión Educativa" -ForegroundColor Cyan
Write-Host "   Configuración para Acceso Público" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Verificar si existe la aplicación
if (-not (Test-Path "app")) {
    Write-Host "[ERROR] No se encontró la carpeta 'app'" -ForegroundColor Red
    Write-Host "[ERROR] Ejecuta este script desde la carpeta del proyecto" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar si ngrok está instalado
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue

if (-not $ngrokPath) {
    Write-Host "[ADVERTENCIA] Ngrok no está instalado o no está en PATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPCIONES PARA INSTALAR NGROK:" -ForegroundColor Cyan
    Write-Host "1. Descarga desde: https://ngrok.com/download" -ForegroundColor White
    Write-Host "2. O instala con Chocolatey: choco install ngrok" -ForegroundColor White
    Write-Host "3. O instala con Scoop: scoop install ngrok" -ForegroundColor White
    Write-Host ""
    
    $continue = Read-Host "¿Quieres continuar sin ngrok? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 0
    }
}

Write-Host "[INFO] Verificando Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en PATH" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "   INICIANDO APLICACIÓN..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

# Función para iniciar la aplicación en segundo plano
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python run.py
}

# Esperar un poco para que la aplicación inicie
Start-Sleep -Seconds 3

# Verificar si la aplicación está ejecutándose
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "[OK] Aplicación iniciada correctamente en http://localhost:5000" -ForegroundColor Green
} catch {
    Write-Host "[ADVERTENCIA] La aplicación puede estar iniciando... Esperando..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Green
Write-Host "   CONFIGURANDO ACCESO PÚBLICO..." -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Green
Write-Host ""

if ($ngrokPath) {
    Write-Host "[INFO] Iniciando túnel ngrok..." -ForegroundColor Blue
    Write-Host ""
    
    # Iniciar ngrok en segundo plano y capturar la salida
    $ngrokJob = Start-Job -ScriptBlock {
        ngrok http 5000 --log=stdout
    }
    
    # Esperar un poco para que ngrok se inicie
    Start-Sleep -Seconds 5
    
    # Intentar obtener la URL pública de ngrok
    try {
        $ngrokApi = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -ErrorAction Stop
        $publicUrl = $ngrokApi.tunnels[0].public_url
        
        Write-Host "===========================================" -ForegroundColor Green
        Write-Host "   ¡APLICACIÓN ACCESIBLE PÚBLICAMENTE!" -ForegroundColor Cyan
        Write-Host "===========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "URL PÚBLICA: $publicUrl" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Comparte esta URL con quien quieras que acceda a tu aplicación" -ForegroundColor White
        Write-Host ""
        Write-Host "USUARIOS DE PRUEBA:" -ForegroundColor Cyan
        Write-Host "Admin: usuario=admin, contraseña=admin123" -ForegroundColor White
        Write-Host "Docente: usuario=docente1, contraseña=123456" -ForegroundColor White
        Write-Host "Padre: usuario=padre_test_1, contraseña=123456" -ForegroundColor White
        Write-Host ""
        
    } catch {
        Write-Host "[INFO] Ngrok está iniciando... Puedes verificar la URL en:" -ForegroundColor Blue
        Write-Host "http://localhost:4040" -ForegroundColor Yellow
    }
    
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host "   APLICACIÓN EJECUTÁNDOSE..." -ForegroundColor Cyan
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Presiona Ctrl+C para detener todo" -ForegroundColor Red
    Write-Host ""
    
    # Mantener el script ejecutándose
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } finally {
        # Limpiar procesos al salir
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -ErrorAction SilentlyContinue
        Stop-Job $ngrokJob -ErrorAction SilentlyContinue
        Remove-Job $ngrokJob -ErrorAction SilentlyContinue
        Write-Host ""
        Write-Host "[INFO] Aplicación detenida" -ForegroundColor Blue
    }
    
} else {
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host "   APLICACIÓN LOCAL EJECUTÁNDOSE..." -ForegroundColor Cyan
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Aplicación disponible en:" -ForegroundColor White
    Write-Host "- Local: http://localhost:5000" -ForegroundColor Yellow
    Write-Host "- Red local: http://TU_IP:5000" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para acceso público, instala ngrok y ejecuta:" -ForegroundColor Cyan
    Write-Host "ngrok http 5000" -ForegroundColor White
    Write-Host ""
    Write-Host "Presiona Ctrl+C para detener" -ForegroundColor Red
    
    # Mantener la aplicación ejecutándose
    try {
        Wait-Job $job
    } finally {
        Stop-Job $job -ErrorAction SilentlyContinue
        Remove-Job $job -ErrorAction SilentlyContinue
        Write-Host ""
        Write-Host "[INFO] Aplicación detenida" -ForegroundColor Blue
    }
} 