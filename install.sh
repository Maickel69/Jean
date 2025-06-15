#!/bin/bash

echo "========================================"
echo "  INSTALADOR SISTEMA GESTION EDUCATIVA"
echo "========================================"
echo

echo "[1/5] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi
echo "✓ Python encontrado"

echo
echo "[2/5] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi
echo "✓ Entorno virtual creado"

echo
echo "[3/5] Activando entorno virtual..."
source venv/bin/activate
echo "✓ Entorno virtual activado"

echo
echo "[4/5] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi
echo "✓ Dependencias instaladas"

echo
echo "[5/5] Inicializando base de datos..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo inicializar la base de datos"
    exit 1
fi
echo "✓ Base de datos inicializada"

echo
echo "========================================"
echo "  INSTALACION COMPLETADA EXITOSAMENTE"
echo "========================================"
echo
echo "Para ejecutar el sistema:"
echo "1. Ejecuta: ./start.sh"
echo "2. O manualmente: source venv/bin/activate && python run.py"
echo
echo "La aplicación estará disponible en: http://localhost:5000"
echo
echo "Usuarios de prueba:"
echo "- Admin: admin / admin123"
echo "- Docente: docente1 / 123456"
echo "- Padre: padre_test_1 / 123456"
echo 