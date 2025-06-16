#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE GESTIÓN EDUCATIVA
============================

⚠️  ADVERTENCIA: NO ejecutes este archivo directamente
⚠️  Si lo haces, obtendrás el error: "No module named 'flask'"

✅  FORMA CORRECTA:
    1. Ejecuta: install.bat
    2. Ejecuta: start.bat
    
✅  O manualmente:
    1. python -m venv venv
    2. venv\Scripts\activate
    3. pip install -r requirements.txt
    4. python init_db.py
    5. python run.py

📚 Para más información: lee LEEME_PRIMERO.md
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 