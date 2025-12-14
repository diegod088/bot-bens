# 🤖 Telegram Media Downloader Bot

Bot de Telegram profesional para descargar contenido multimedia de canales privados con sistema de paywall integrado usando **Telegram Stars** y **PayPal**.

## 📋 Características

### 🆓 Plan Gratis
- ✅ 10 fotos diarias
- ✅ 3 videos totales
- ❌ Música bloqueada
- ❌ APK bloqueados

### 💎 Plan Premium (500 ⭐ Telegram Stars o $5 USD PayPal)
- ✅ Fotos ilimitadas
- ✅ 50 videos diarios
- ✅ 50 canciones diarias
- ✅ 50 APK diarios
- ⏰ Duración: 30 días

### 🎯 Funcionalidades
- Descarga de fotos, videos, música y APK de canales privados
- Sistema de límites diarios con reseteo automático cada 24h
- Pagos integrados con Telegram Stars (nativo)
- Pagos alternativos con PayPal (Premium y VIP)
- Detección automática de tipo de contenido
- Interfaz profesional con diseño simétrico
- Estadísticas de uso personal y global
- Guía de uso integrada

---

## 🏗️ Arquitectura del Proyecto

```
.
├── bot_with_paywall.py    # Bot principal de Telegram
├── backend_paypal.py      # API FastAPI para pagos PayPal
├── database.py            # Gestión de base de datos SQLite
├── run_backend.py         # Launcher para el backend
├── requirements.txt       # Dependencias Python
├── .gitignore            # Archivos ignorados por Git
├── .env.example          # Plantilla de variables de entorno
└── README.md             # Este archivo
```

---

## 🚀 Instalación Local

### 1. Requisitos Previos
- Python 3.8 o superior
- Cuenta de Telegram
- API credentials de Telegram (Bot Token, API ID, API Hash)
- Cuenta PayPal Developer (opcional, para pagos PayPal)

### 2. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/telegram-bot-downloader.git
cd telegram-bot-downloader
```

### 3. Crear Entorno Virtual
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# ==========================================
# TELEGRAM BOT CREDENTIALS
# ==========================================
TELEGRAM_BOT_TOKEN=tu_bot_token_de_@BotFather
TELEGRAM_API_ID=tu_api_id_de_my.telegram.org
TELEGRAM_API_HASH=tu_api_hash_de_my.telegram.org
TELEGRAM_SESSION_STRING=tu_session_string_de_telethon

# ==========================================
# PAYPAL CREDENTIALS (Opcional)
# ==========================================
PAYPAL_CLIENT_ID=tu_paypal_client_id
PAYPAL_CLIENT_SECRET=tu_paypal_client_secret
PAYPAL_MODE=sandbox
# PAYPAL_MODE=live  # Para producción
PAYPAL_WEBHOOK_ID=tu_webhook_id_opcional

# ==========================================
# BACKEND URL
# ==========================================
# Para desarrollo local:
BACKEND_URL=http://localhost:8000

# Para producción (Railway):
# BACKEND_URL=https://tu-backend.up.railway.app
```

### 6. Obtener Credenciales

#### Bot Token de Telegram
1. Habla con [@BotFather](https://t.me/botfather)
2. Usa `/newbot` y sigue las instrucciones
3. Copia el token proporcionado

#### API ID y API Hash
1. Ve a https://my.telegram.org
2. Inicia sesión con tu número de teléfono
3. Crea una aplicación en "API Development Tools"
4. Copia API ID y API Hash

#### Session String de Telethon
```bash
# Ejecuta este script una vez para generar el session string
python -c "
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input('API ID: '))
api_hash = input('API Hash: ')

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print('Session String:', client.session.save())
"
```

#### PayPal Credentials (Opcional)
1. Ve a https://developer.paypal.com
2. Crea una App en Dashboard
3. Copia Client ID y Secret
4. Usa "sandbox" para pruebas, "live" para producción

### 7. Ejecutar en Local

#### Opción A: Solo Bot (sin PayPal)
```bash
python bot_with_paywall.py
```

#### Opción B: Bot + Backend PayPal (2 terminales)

**Terminal 1 - Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Bot:**
```bash
python bot_with_paywall.py
```

---

## ☁️ Despliegue en Railway

Railway permite desplegar fácilmente con 2 servicios independientes.

### 1. Crear Proyecto en Railway
1. Ve a https://railway.app
2. Crea una cuenta o inicia sesión
3. Click en "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Conecta tu repositorio

### 2. Crear Servicio para el BOT

1. En tu proyecto Railway, click en "New Service"
2. Selecciona "GitHub Repo"
3. Elige tu repositorio
4. Configura:
   - **Name:** `telegram-bot`
   - **Start Command:** `python bot_with_paywall.py`

5. Agrega variables de entorno en Settings → Variables:
   ```
   TELEGRAM_BOT_TOKEN=tu_bot_token
   TELEGRAM_API_ID=tu_api_id
   TELEGRAM_API_HASH=tu_api_hash
   TELEGRAM_SESSION_STRING=tu_session_string
   BACKEND_URL=https://tu-backend.up.railway.app
   ```

### 3. Crear Servicio para el BACKEND

1. En el mismo proyecto, click en "New Service"
2. Selecciona "GitHub Repo"
3. Elige tu repositorio
4. Configura:
   - **Name:** `paypal-backend`
   - **Start Command:** `python run_backend.py`

5. Agrega variables de entorno:
   ```
   PAYPAL_CLIENT_ID=tu_paypal_client_id
   PAYPAL_CLIENT_SECRET=tu_paypal_secret
   PAYPAL_MODE=live
   TELEGRAM_BOT_TOKEN=tu_bot_token
   BACKEND_URL=https://tu-backend.up.railway.app
   ```

6. En Settings → Networking:
   - Railway generará automáticamente un dominio público
   - Copia este dominio (ej: `https://tu-backend.up.railway.app`)
   - Actualiza la variable `BACKEND_URL` en **ambos servicios**

### 4. Configurar Webhook de PayPal (Opcional)

1. Ve a PayPal Developer Dashboard
2. Crea un Webhook apuntando a: `https://tu-backend.up.railway.app/webhook/paypal`
3. Copia el Webhook ID
4. Agrégalo como variable `PAYPAL_WEBHOOK_ID` en el servicio backend

### 5. Habilitar Telegram Stars

1. Abre [@BotFather](https://t.me/botfather)
2. Envía `/mybots`
3. Selecciona tu bot
4. Toca "Payments" → "Telegram Stars"
5. Acepta los términos

### 6. Verificar Despliegue

- Ambos servicios deben estar en estado "Active" (verde)
- Revisa los logs en Railway para detectar errores
- Prueba el bot enviando `/start`
- Prueba pagos con `/testpay`

---

## 📊 Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Menú principal con estado de cuenta |
| `/premium` | Ver planes y suscribirse |
| `/stats` | Ver estadísticas personales y del bot |
| `/help` | Guía de uso completa |
| `/testpay` | Probar sistema de pagos Telegram Stars |

---

## 🗂️ Variables de Entorno

### Para el BOT (bot_with_paywall.py)

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de @BotFather | ✅ | `123456:ABC-DEF...` |
| `TELEGRAM_API_ID` | API ID de my.telegram.org | ✅ | `12345678` |
| `TELEGRAM_API_HASH` | API Hash de my.telegram.org | ✅ | `abcdef123456...` |
| `TELEGRAM_SESSION_STRING` | Session string de Telethon | ✅ | `1BVtsOK4Bu...` |
| `BACKEND_URL` | URL del backend PayPal | ✅ | `https://backend.railway.app` |

### Para el BACKEND (backend_paypal.py)

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `PAYPAL_CLIENT_ID` | Client ID de PayPal | ✅ | `AaBbCcDd...` |
| `PAYPAL_CLIENT_SECRET` | Secret de PayPal | ✅ | `EeFfGgHh...` |
| `PAYPAL_MODE` | Modo de PayPal | ✅ | `sandbox` o `live` |
| `PAYPAL_WEBHOOK_ID` | ID del webhook de PayPal | ❌ | `WH-123...` |
| `TELEGRAM_BOT_TOKEN` | Token del bot | ✅ | `123456:ABC...` |
| `BACKEND_URL` | URL del backend | ✅ | `https://backend.railway.app` |
| `PORT` | Puerto del servidor | ❌ | `8000` (auto en Railway) |

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE

**NUNCA** subas estos archivos/datos a GitHub:
- ❌ `.env` - Contiene todas las credenciales
- ❌ `users.db` - Base de datos con información de usuarios
- ❌ `*.session` - Archivos de sesión de Telethon
- ❌ `*.log` - Archivos de logs con posibles datos sensibles

### ✅ Buenas Prácticas

1. **Usa el `.gitignore` proporcionado** - Ya está configurado correctamente
2. **Variables de entorno** - Todas las credenciales en `.env` (local) o Railway (producción)
3. **No hardcodees secrets** - Usa siempre `os.getenv()`
4. **Backup de `users.db`** - Haz backups regulares de la base de datos en producción
5. **Modo sandbox primero** - Prueba con PayPal sandbox antes de usar live
6. **HTTPS obligatorio** - Usa siempre HTTPS en producción (Railway lo proporciona)

---

## 🛠️ Base de Datos

El bot usa SQLite (`users.db`) con la siguiente estructura:

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    downloads INTEGER DEFAULT 0,
    premium INTEGER DEFAULT 0,
    premium_level INTEGER DEFAULT 0,
    premium_until TIMESTAMP DEFAULT NULL,
    daily_photo INTEGER DEFAULT 0,
    daily_video INTEGER DEFAULT 0,
    daily_music INTEGER DEFAULT 0,
    daily_apk INTEGER DEFAULT 0,
    last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Consultas Útiles

```bash
# Ver todos los usuarios
sqlite3 users.db "SELECT * FROM users;"

# Ver usuarios Premium activos
sqlite3 users.db "SELECT user_id, premium_until FROM users WHERE premium = 1;"

# Dar Premium manualmente (30 días)
sqlite3 users.db "UPDATE users SET premium = 1, premium_until = datetime('now', '+30 days') WHERE user_id = 123456789;"

# Resetear contadores de un usuario
sqlite3 users.db "UPDATE users SET daily_video = 0, daily_music = 0, daily_apk = 0, daily_photo = 0 WHERE user_id = 123456789;"
```

---

## 🐛 Solución de Problemas

### El bot no arranca

```bash
# Verificar variables de entorno
python -c "import os; print('BOT_TOKEN:', bool(os.getenv('TELEGRAM_BOT_TOKEN')))"

# Ver logs detallados
python bot_with_paywall.py
```

### Telegram Stars no funciona

1. Verifica que esté habilitado en @BotFather → Payments → Telegram Stars
2. Prueba con `/testpay` en el bot
3. Revisa los logs del bot

### PayPal no funciona

1. Verifica que `BACKEND_URL` sea correcto y accesible
2. Revisa logs del backend: `tail -f backend.log`
3. Verifica credenciales de PayPal
4. Usa `PAYPAL_MODE=sandbox` para pruebas

### Railway no arranca

1. Verifica que todas las variables estén configuradas
2. Revisa logs en Railway dashboard
3. Verifica que `requirements.txt` tenga todas las dependencias
4. Asegúrate de que los comandos de inicio sean correctos

---

## 📝 Estructura de Archivos para Subir a GitHub

```
✅ Subir a GitHub:
├── bot_with_paywall.py
├── backend_paypal.py
├── database.py
├── run_backend.py
├── requirements.txt
├── .gitignore
├── .env.example          # Plantilla SIN credenciales reales
└── README.md

❌ NO subir (ya están en .gitignore):
├── .env                  # Credenciales reales
├── users.db              # Base de datos
├── *.session             # Sesiones de Telethon
├── *.log                 # Logs
├── __pycache__/          # Python cache
└── .venv/                # Entorno virtual
```

---

## 📞 Soporte

**Canal Oficial:** [@observer_bots](https://t.me/observer_bots)

### Reportar Problemas

Incluye:
1. Descripción detallada del problema
2. Logs relevantes (sin credenciales)
3. Versión de Python: `python --version`
4. Sistema operativo
5. Comando que causó el error

---

## 📄 Licencia

Este proyecto es privado. No distribuir sin autorización.

---

## 🙏 Créditos

Desarrollado con:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Framework del bot
- [Telethon](https://github.com/LonamiWebs/Telethon) - Cliente de Telegram
- [FastAPI](https://fastapi.tiangolo.com/) - Backend web
- [PayPal REST API](https://developer.paypal.com/) - Procesamiento de pagos

---

**¿Listo para desplegar? 🚀**

1. ✅ Configura tus credenciales en `.env` (local) o Railway (producción)
2. ✅ Habilita Telegram Stars en @BotFather
3. ✅ Despliega en Railway siguiendo la guía
4. ✅ Prueba con `/testpay`
5. ✅ ¡Empieza a recibir suscripciones!
