# Railway Configuration
# Este archivo es opcional pero facilita el despliegue

# ==========================================
# SERVICIO 1: TELEGRAM BOT
# ==========================================
# Name: telegram-bot
# Start Command: python bot_with_paywall.py
# 
# Variables de entorno requeridas:
# - TELEGRAM_BOT_TOKEN
# - TELEGRAM_API_ID
# - TELEGRAM_API_HASH
# - TELEGRAM_SESSION_STRING
# - BACKEND_URL

# ==========================================
# SERVICIO 2: PAYPAL BACKEND
# ==========================================
# Name: paypal-backend
# Start Command: python run_backend.py
#
# Variables de entorno requeridas:
# - PAYPAL_CLIENT_ID
# - PAYPAL_CLIENT_SECRET
# - PAYPAL_MODE (sandbox o live)
# - TELEGRAM_BOT_TOKEN
# - BACKEND_URL
# - PORT (asignado automáticamente por Railway)
#
# Networking:
# - Generar dominio público en Settings → Networking
# - Usar ese dominio como BACKEND_URL en ambos servicios

# ==========================================
# NOTAS DE DESPLIEGUE
# ==========================================
# 1. Crear proyecto nuevo en Railway
# 2. Crear 2 servicios desde el mismo repo GitHub
# 3. Configurar variables de entorno en cada servicio
# 4. El backend generará un dominio público automáticamente
# 5. Copiar ese dominio y actualizar BACKEND_URL en ambos servicios
# 6. Verificar que ambos servicios estén "Active" (verde)
# 7. Probar con /start y /testpay en el bot

# ==========================================
# HEALTHCHECKS
# ==========================================
# Bot: No requiere healthcheck (usa polling)
# Backend: Railway detectará automáticamente el puerto HTTP
