#!/bin/bash

# ====================================================
# Test Railway Deployment Locally
# ====================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║      🧪 Test Railway Deployment Locally                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo "Copy .env.example to .env and fill in the values"
    exit 1
fi

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

# Check dependencies
echo -e "${YELLOW}📦 Checking dependencies...${NC}"
pip install -q -r requirements.txt

# Set test port
export PORT=5000
export HOST=0.0.0.0

echo -e "${GREEN}✅ Environment ready${NC}"
echo -e "${YELLOW}🚀 Starting services (Bot + Dashboard)...${NC}"
echo ""
echo -e "${BLUE}Dashboard will be available at: http://localhost:${PORT}${NC}"
echo -e "${BLUE}Health check: http://localhost:${PORT}/health${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Run the start script
python start.py
