#!/usr/bin/env python3
"""
Script para configurar el token de administrador del dashboard
"""

import os
import sys
from dotenv import load_dotenv, set_key
import secrets

# Cargar .env actual
load_dotenv()
ENV_FILE = ".env"

print("=" * 60)
print("🔐 Configuración de Token de Administrador")
print("=" * 60)

# Mostrar token actual
current_token = os.getenv("ADMIN_TOKEN", "admin123")
print(f"\n📝 Token actual: {current_token}")

print("\n¿Qué deseas hacer?")
print("1. Cambiar a un token personalizado")
print("2. Generar un token aleatorio seguro")
print("3. Mantener el token actual")
print("4. Salir")

choice = input("\nSelecciona una opción (1-4): ").strip()

if choice == "1":
    new_token = input("\n🔑 Ingresa el nuevo token de administrador: ").strip()
    if len(new_token) < 8:
        print("❌ Error: El token debe tener al menos 8 caracteres")
        sys.exit(1)
    
    set_key(ENV_FILE, "ADMIN_TOKEN", new_token)
    print(f"✅ Token actualizado: {new_token}")
    
elif choice == "2":
    new_token = secrets.token_urlsafe(32)
    set_key(ENV_FILE, "ADMIN_TOKEN", new_token)
    print(f"\n✅ Token generado aleatoriamente:")
    print(f"   {new_token}")
    print("\n📋 Guárdalo en un lugar seguro")
    
elif choice == "3":
    print(f"✅ Manteniendo token actual: {current_token}")
    
elif choice == "4":
    print("👋 Saliendo...")
    sys.exit(0)
else:
    print("❌ Opción inválida")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 Configuración completada")
print("=" * 60)
print("\n✅ Para acceder al dashboard:")
print("   URL: http://127.0.0.1:5000")
print(f"   Token: {os.getenv('ADMIN_TOKEN')}")
