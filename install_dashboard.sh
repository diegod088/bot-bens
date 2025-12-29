#!/bin/bash
# Script de instalación y configuración del Dashboard

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║  📦 Instalación y Configuración del Dashboard         ║"
echo "║     Bot Telegram + Sistema de Pagos                  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar si estamos en el directorio correcto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Debe ejecutarse desde la raíz del proyecto"
    exit 1
fi

# Activar entorno virtual o crear si no existe
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv .venv
else
    echo -e "${YELLOW}📦 Entorno virtual ya existe${NC}"
fi

source .venv/bin/activate

# Instalar dependencias
echo -e "${YELLOW}📥 Instalando dependencias...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q Flask==3.0.0 Werkzeug==3.0.1

echo -e "${GREEN}✅ Dependencias instaladas${NC}"

# Crear/actualizar base de datos
echo -e "${YELLOW}🗄️  Inicializando base de datos...${NC}"
python3 -c "from database import init_database; init_database()"
echo -e "${GREEN}✅ Base de datos lista${NC}"

# Configurar token de administrador
echo ""
echo -e "${BLUE}🔐 Configuración de Administrador${NC}"
python3 configure_admin.py

# Hacer scripts ejecutables
chmod +x run_dashboard.sh 2>/dev/null || true
chmod +x run_both.sh 2>/dev/null || true

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗"
echo "║          ✅ Instalación Completada                       ║"
echo "╠════════════════════════════════════════════════════════╣"
echo -e "║ ${GREEN}📊 Para iniciar el Dashboard:${BLUE}${NC}"
echo "║    ./run_dashboard.sh"
echo "║    o"
echo "║    python dashboard.py"
echo -e "║                                                        ║"
echo -e "║ ${GREEN}🚀 Para iniciar Bot + Dashboard:${BLUE}${NC}"
echo "║    ./run_both.sh"
echo -e "║                                                        ║"
echo -e "║ ${GREEN}📍 Acceso:${BLUE}${NC}"
echo "║    URL: http://127.0.0.1:5000"
echo "║    (Token configurado anteriormente)"
echo "║"
echo "║ 📚 Documentación:"
echo "║    - DASHBOARD_README.md (Características y API)"
echo "║    - GUIA_DASHBOARD.md (Guía de uso completa)"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
