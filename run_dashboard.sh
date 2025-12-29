#!/usr/bin/env bash
# Script para iniciar el dashboard del bot

cd "$(dirname "$0")"

echo "🚀 Iniciando Dashboard del Bot..."
echo "📍 Accede a: http://127.0.0.1:5000"
echo "🔑 Token por defecto: admin123"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

source .venv/bin/activate
python dashboard.py
