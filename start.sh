#!/bin/bash

echo "========================================"
echo "  INICIANDO SISTEMA GESTION EDUCATIVA"
echo "========================================"
echo

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Iniciando servidor Flask..."
echo
echo "✓ Servidor iniciado en: http://localhost:5000"
echo
echo "Presiona Ctrl+C para detener el servidor"
echo "========================================"
echo

python run.py 