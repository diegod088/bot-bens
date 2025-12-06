#!/usr/bin/env python3
"""
Script para iniciar el backend de pagos PayPal
Compatible con Railway y ejecución local
"""
import os
from pathlib import Path

# Cargar variables de entorno desde .env solo si existe (desarrollo local)
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    print("Loading environment variables from .env file...")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # No sobrescribir variables ya existentes (Railway las inyecta)
                if key not in os.environ:
                    os.environ[key] = value

# Validar variables críticas
required_vars = [
    'PAYPAL_CLIENT_ID',
    'PAYPAL_CLIENT_SECRET',
    'TELEGRAM_BOT_TOKEN',
    'BACKEND_URL'
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(missing_vars)}\n"
        "Please set them in Railway dashboard or in .env file for local development."
    )

# Importar y ejecutar el backend
if __name__ == "__main__":
    import uvicorn
    from backend_paypal import app
    
    # Railway proporciona PORT automáticamente, default 8000 para local
    port = int(os.getenv("PORT", 8000))
    
    print(f"Starting PayPal backend on port {port}...")
    print(f"PayPal Mode: {os.getenv('PAYPAL_MODE', 'sandbox')}")
    print(f"Backend URL: {os.getenv('BACKEND_URL')}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
