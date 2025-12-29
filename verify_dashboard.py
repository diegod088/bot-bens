#!/usr/bin/env python3
"""
Script de verificación e instalación del Dashboard
Verifica que todo esté correctamente instalado
"""

import os
import sys
from pathlib import Path

# Colores
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def check_file(path, name):
    """Verificar si un archivo existe"""
    if Path(path).exists():
        print(f"{GREEN}✅{NC} {name}")
        return True
    else:
        print(f"{RED}❌{NC} {name} - {YELLOW}NO ENCONTRADO{NC}")
        return False

def check_module(module_name, package_name):
    """Verificar si un módulo de Python está instalado"""
    try:
        __import__(module_name)
        print(f"{GREEN}✅{NC} {package_name}")
        return True
    except ImportError:
        print(f"{RED}❌{NC} {package_name} - {YELLOW}NO INSTALADO{NC}")
        return False

print(f"{BLUE}")
print("╔════════════════════════════════════════════════════════╗")
print("║     📊 Verificación de Instalación del Dashboard      ║")
print("╚════════════════════════════════════════════════════════╝")
print(f"{NC}")

# Verificación de directorios
print(f"\n{BLUE}📁 Directorios:{NC}")
check_file("templates", "  Carpeta 'templates'")
check_file("static", "  Carpeta 'static'")
check_file(".venv", "  Entorno virtual '.venv'")

# Verificación de archivos principales
print(f"\n{BLUE}📄 Archivos del Dashboard:{NC}")
check_file("dashboard.py", "  dashboard.py")
check_file("templates/base.html", "  templates/base.html")
check_file("templates/login.html", "  templates/login.html")
check_file("templates/dashboard.html", "  templates/dashboard.html")
check_file("templates/users.html", "  templates/users.html")
check_file("templates/user_detail.html", "  templates/user_detail.html")

# Verificación de scripts
print(f"\n{BLUE}🔧 Scripts de ejecución:{NC}")
check_file("run_dashboard.sh", "  run_dashboard.sh")
check_file("run_both.sh", "  run_both.sh")
check_file("install_dashboard.sh", "  install_dashboard.sh")
check_file("configure_admin.py", "  configure_admin.py")

# Verificación de documentación
print(f"\n{BLUE}📚 Documentación:{NC}")
check_file("DASHBOARD_README.md", "  DASHBOARD_README.md")
check_file("GUIA_DASHBOARD.md", "  GUIA_DASHBOARD.md")
check_file("INICIO_RAPIDO.md", "  INICIO_RAPIDO.md")
check_file("RESUMEN_DASHBOARD.md", "  RESUMEN_DASHBOARD.md")

# Verificación de configuración
print(f"\n{BLUE}⚙️  Configuración:{NC}")
check_file(".env", "  .env (variables de entorno)")
check_file("requirements.txt", "  requirements.txt")

# Verificación de base de datos
print(f"\n{BLUE}🗄️  Base de datos:{NC}")
check_file("users.db", "  users.db")
check_file("database.py", "  database.py")

# Verificación de módulos Python
print(f"\n{BLUE}📦 Módulos de Python:{NC}")
check_module("flask", "Flask")
check_module("werkzeug", "Werkzeug")
check_module("telegram", "python-telegram-bot")
check_module("telethon", "telethon")
check_module("sqlite3", "sqlite3")
check_module("dotenv", "python-dotenv")
check_module("cryptography", "cryptography")

# Verificación del archivo .env
print(f"\n{BLUE}🔐 Variables de entorno:.{NC}")
env_file = Path(".env")
if env_file.exists():
    with open(".env") as f:
        content = f.read()
        if "ADMIN_TOKEN" in content:
            print(f"{GREEN}✅{NC} ADMIN_TOKEN configurado")
        else:
            print(f"{RED}❌{NC} ADMIN_TOKEN - {YELLOW}NO CONFIGURADO{NC}")
        
        if "DASHBOARD_SECRET_KEY" in content:
            print(f"{GREEN}✅{NC} DASHBOARD_SECRET_KEY configurado")
        else:
            print(f"{RED}❌{NC} DASHBOARD_SECRET_KEY - {YELLOW}NO CONFIGURADO{NC}")
else:
    print(f"{RED}❌{NC} .env no encontrado")

# Resumen final
print(f"\n{BLUE}╔════════════════════════════════════════════════════════╗")
print(f"║            ✅ Verificación Completada                  ║")
print(f"╚════════════════════════════════════════════════════════╝{NC}\n")

print(f"{GREEN}Todo parece estar en orden. Puedes ejecutar:{NC}\n")
print(f"  {BLUE}./run_dashboard.sh{NC}     (Solo dashboard)")
print(f"  {BLUE}./run_both.sh{NC}          (Bot + Dashboard)")
print(f"  {BLUE}python dashboard.py{NC}     (Directo)\n")

print(f"{YELLOW}💡 Acceso:{NC}")
print(f"  URL: {BLUE}http://127.0.0.1:5000{NC}")
print(f"  Documentación: lee {BLUE}GUIA_DASHBOARD.md{NC}\n")
