#!/bin/bash

# Script para iniciar el Bot y el Dashboard simultáneamente
# Uso: ./run_both.sh

set -e

# Colores para el output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║      🤖 Bot Telegram + Dashboard Admin                ║"
echo "║      Iniciando ambos servicios...                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activar entorno virtual
echo -e "${YELLOW}📦 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Verificar que los archivos necesarios existan
if [ ! -f "bot_with_paywall.py" ]; then
    echo -e "${RED}❌ Error: bot_with_paywall.py no encontrado${NC}"
    exit 1
fi

if [ ! -f "dashboard.py" ]; then
    echo -e "${RED}❌ Error: dashboard.py no encontrado${NC}"
    exit 1
fi

# Crear función para limpiar procesos al salir
cleanup() {
    echo -e "${YELLOW}\n🛑 Deteniendo servicios...${NC}"
    kill $BOT_PID $DASHBOARD_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Servicios detenidos${NC}"
    exit 0
}

# Configurar trap para Ctrl+C
trap cleanup SIGINT

# Iniciar el Bot en background
echo -e "${BLUE}🤖 Iniciando Bot Telegram...${NC}"
python bot_with_paywall.py &
BOT_PID=$!
echo -e "${GREEN}✅ Bot iniciado (PID: $BOT_PID)${NC}"

# Esperar un poco para que el bot se estabilice
sleep 2

# Iniciar el Dashboard en background
echo -e "${BLUE}📊 Iniciando Dashboard Admin...${NC}"
python dashboard.py &
DASHBOARD_PID=$!
echo -e "${GREEN}✅ Dashboard iniciado (PID: $DASHBOARD_PID)${NC}"

# Mostrar información de acceso
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║           ✅ Servicios Iniciados Correctamente         ║"
echo "╠════════════════════════════════════════════════════════╣"
echo -e "║ ${GREEN}🤖 Bot Telegram${BLUE}${NC}"
echo -e "║    Estado: Escuchando mensajes"
echo "║    PID: $BOT_PID"
echo -e "║                                                        ║"
echo -e "║ ${GREEN}📊 Dashboard Admin${BLUE}${NC}"
echo -e "║    URL: http://127.0.0.1:5000"
echo -e "║    Token: admin123"
echo "║    PID: $DASHBOARD_PID"
echo "╠════════════════════════════════════════════════════════╣"
echo -e "║ ${YELLOW}⌨️  Presiona Ctrl+C para detener todos los servicios${BLUE}${NC}"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Esperar a que ambos procesos terminen
wait $BOT_PID $DASHBOARD_PID
