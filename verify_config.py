#!/usr/bin/env python3
"""
Script de verificación de configuración
Valida que todas las variables de entorno estén configuradas correctamente
"""
import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_env_var(var_name, required=True):
    """Verifica si una variable de entorno está configurada"""
    value = os.getenv(var_name)
    if value:
        # Mostrar solo primeros caracteres por seguridad
        display_value = value[:10] + "..." if len(value) > 10 else value
        print(f"  {GREEN}✓{RESET} {var_name}: {display_value}")
        return True
    else:
        status = f"{RED}✗{RESET}" if required else f"{YELLOW}⚠{RESET}"
        req_text = "REQUERIDA" if required else "Opcional"
        print(f"  {status} {var_name}: NO CONFIGURADA ({req_text})")
        return not required

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN")
    print("=" * 60)
    
    # Cargar .env si existe
    env_file = Path('.env')
    if env_file.exists():
        print(f"\n{GREEN}✓{RESET} Archivo .env encontrado\n")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key not in os.environ:
                        os.environ[key] = value
    else:
        print(f"\n{YELLOW}⚠{RESET} Archivo .env no encontrado (OK si estás en Railway)\n")
    
    all_ok = True
    
    # Variables para el BOT
    print("📱 TELEGRAM BOT:")
    all_ok &= check_env_var("TELEGRAM_BOT_TOKEN", required=True)
    all_ok &= check_env_var("TELEGRAM_API_ID", required=True)
    all_ok &= check_env_var("TELEGRAM_API_HASH", required=True)
    all_ok &= check_env_var("TELEGRAM_SESSION_STRING", required=True)
    all_ok &= check_env_var("BACKEND_URL", required=True)
    
    # Variables para el BACKEND
    print("\n💳 PAYPAL BACKEND:")
    all_ok &= check_env_var("PAYPAL_CLIENT_ID", required=True)
    all_ok &= check_env_var("PAYPAL_CLIENT_SECRET", required=True)
    all_ok &= check_env_var("PAYPAL_MODE", required=True)
    all_ok &= check_env_var("PAYPAL_WEBHOOK_ID", required=False)
    
    # Puerto (Railway lo asigna automáticamente)
    print("\n🌐 SERVIDOR:")
    check_env_var("PORT", required=False)
    
    print("\n" + "=" * 60)
    if all_ok:
        print(f"{GREEN}✓ CONFIGURACIÓN COMPLETA{RESET}")
        print("Puedes iniciar el bot y el backend.")
        return 0
    else:
        print(f"{RED}✗ CONFIGURACIÓN INCOMPLETA{RESET}")
        print("Configura las variables faltantes en .env o Railway.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
