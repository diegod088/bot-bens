# 🚂 RAILWAY DEPLOYMENT GUIDE - PRODUCTION 24/7

## 📋 ÍNDICE
1. [Prerequisites](#prerequisites)
2. [Servicio 1: Telegram Bot](#servicio-1-telegram-bot)
3. [Servicio 2: PayPal Backend](#servicio-2-paypal-backend)
4. [Persistent Volumes](#persistent-volumes)
5. [Environment Variables](#environment-variables)
6. [Health Checks](#health-checks)
7. [Monitoring & Logs](#monitoring--logs)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Railway Account
- Crea una cuenta en [Railway.app](https://railway.app)
- Conecta tu cuenta de GitHub
- (Opcional) Agrega método de pago para plan Pro

### 2. GitHub Repository
- Push tu código a GitHub (ver `PRODUCTION_IMPROVEMENTS.md`)
- Asegúrate de que `.env`, `users.db`, `*.session` NO estén en el repo

### 3. Telegram Bot Token
- Obten de @BotFather
- Generar SESSION_STRING con `generate_session.py`

### 4. PayPal Credentials
- Developer Dashboard: https://developer.paypal.com
- Create App → Get Client ID & Secret
- Sandbox para testing, Live para producción

---

## Servicio 1: Telegram Bot

### Paso 1: Create New Project en Railway

```bash
# CLI (opcional)
railway login
railway init
```

O desde Dashboard: **New Project** → **Deploy from GitHub repo**

### Paso 2: Select Dockerfile

- Railway detectará `Dockerfile.bot` automáticamente
- Si no, en Settings → Build: set `Dockerfile Path` = `Dockerfile.bot`

### Paso 3: Configure Environment Variables

En **Variables** tab, agregar:

```env
TELEGRAM_BOT_TOKEN=8548142676:AAHDA16IY6RcSg_69tVbYOg5y-73paK7FdM
TELEGRAM_API_ID=34824079
TELEGRAM_API_HASH=d1fafc33c7acfea5979c21635732c96b
TELEGRAM_SESSION_STRING=1AZWarzoBu5oSY9B9-KDgS-vFthy8EFSPZNmvE0kFCBewdNEJWIrSKZa0UNvQPRZj79HNtf-tB8XXA65siNVaYDDeQmPC1bBPa9HSWP9L3EJeVOy6gtUW98xuBp96mg_GEPOEqkUbn8l0kBR5mgFA1wNB1ZM8qKicOXgUD-4jXdpxN9bLF0SiL6Ou_bif3B1MD8PDjj9NqBu9aDfjrtp23xsjs7CauPngHT-Vo36fRFVbhL-MjXd9kL_YxpRTeZ32Gn6NkYr7wzSWH17PvY5C7eUqSTGdeKLCvaXAk2zvwFqn7wFVCMndbv22Ux8Xu977u4Q7Z8cJk7mhx-bQGCRwxwxwiGKWzKw=
DB_PATH=/data
PYTHONUNBUFFERED=1
```

⚠️ **IMPORTANTE**: Usa TUS propios valores, NO los del ejemplo.

### Paso 4: Add Persistent Volume

Para que la base de datos persista entre deployments:

1. Go to **Volumes** tab
2. Click **+ New Volume**
3. Mount Path: `/data`
4. Size: `1GB` (ajustar según necesidad)

### Paso 5: Deploy

- Railway desplegará automáticamente
- Verifica logs en **Deployments** tab
- Busca: `"Bot started successfully. Polling for updates..."`

### Paso 6: Test Bot

- Abre Telegram
- Envía `/start` a tu bot
- Debe responder con el menú

---

## Servicio 2: PayPal Backend

### Paso 1: Create New Service

En el mismo proyecto Railway:
- **+ New** → **Empty Service**
- Nombre: `paypal-backend`

### Paso 2: Connect to GitHub Repo

- Settings → Source → Connect to same GitHub repo
- Set Build: `Dockerfile.backend`

### Paso 3: Configure Environment Variables

```env
PAYPAL_CLIENT_ID=AaiRS4yAPkrheDPnfVOxhEpzC5ZRGEG1zEpoRVE_UBtrWxxU6hdaaa7jd0ARek5Q-Na-ouYNnc_7DhV4
PAYPAL_CLIENT_SECRET=ELOf2SEn_lCYnUhIyxE5erOhJ7cqYKtSiZ4q3IkRyGhF7u45bZ3yOr9vH35VD1AqsgwEOM3vL8nL1kDI
PAYPAL_MODE=sandbox
TELEGRAM_BOT_TOKEN=8548142676:AAHDA16IY6RcSg_69tVbYOg5y-73paK7FdM
BACKEND_URL=https://paypal-backend-production.up.railway.app
DB_PATH=/data
PYTHONUNBUFFERED=1
PORT=${{PORT}}
```

⚠️ **BACKEND_URL**: 
1. Primero deploy sin BACKEND_URL
2. Railway asignará dominio público
3. Copy domain from Settings → Networking
4. Set BACKEND_URL = `https://tu-dominio.up.railway.app`
5. Redeploy

### Paso 4: Enable Public Networking

- Settings → Networking → **Generate Domain**
- Esto creará: `https://xxx.up.railway.app`
- Usa este dominio en BACKEND_URL

### Paso 5: Add Persistent Volume

1. Volumes tab → + New Volume
2. Mount Path: `/data`
3. Size: `1GB`

### Paso 6: Verify Deployment

```bash
# Test health endpoint
curl https://tu-dominio.up.railway.app/health

# Should return:
{
  "status": "healthy",
  "timestamp": "2025-12-05T...",
  "service": "paypal-backend",
  "paypal_mode": "sandbox"
}
```

---

## Persistent Volumes

### ¿Por qué son necesarios?

Railway es **ephemeral** por defecto: cada deploy borra archivos.

**Persistent Volumes** mantienen datos entre deployments:
- `users.db` (base de datos)
- `backups/` (respaldos automáticos)
- Logs importantes

### Configuración:

```yaml
# En railway.toml (opcional, también desde dashboard)
volumes:
  bot-data:
    mountPath: /data
    size: 1Gi
```

### Verificar Volume:

```bash
# En los logs del bot, buscar:
"Database initialized successfully"
"Database backup created: /data/backups/users_backup_..."
```

---

## Environment Variables

### Variables Compartidas Entre Servicios:

| Variable | Bot | Backend | Descripción |
|----------|-----|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | ✅ | Token del bot |
| `DB_PATH` | ✅ | ✅ | Path de la DB (siempre `/data`) |

### Variables Específicas del Bot:

| Variable | Requerido | Ejemplo |
|----------|-----------|---------|
| `TELEGRAM_API_ID` | ✅ | `34824079` |
| `TELEGRAM_API_HASH` | ✅ | `d1fafc33...` |
| `TELEGRAM_SESSION_STRING` | ✅ | `1AZWar...` |

### Variables Específicas del Backend:

| Variable | Requerido | Ejemplo |
|----------|-----------|---------|
| `PAYPAL_CLIENT_ID` | ✅ | `AaiRS4...` |
| `PAYPAL_CLIENT_SECRET` | ✅ | `ELOf2S...` |
| `PAYPAL_MODE` | ✅ | `sandbox` o `live` |
| `BACKEND_URL` | ✅ | `https://xxx.up.railway.app` |
| `PORT` | Auto | Railway lo asigna automáticamente |

---

## Health Checks

### Bot Health Check

El bot NO tiene endpoint HTTP, así que Railway verifica el proceso:

```dockerfile
HEALTHCHECK CMD pgrep -f bot_with_paywall.py || exit 1
```

Si el proceso muere, Railway lo reinicia automáticamente.

### Backend Health Check

HTTP endpoint en `/health`:

```bash
curl https://tu-backend.up.railway.app/health
```

Railway ping cada 30s. Si falla 3 veces consecutivas, reinicia el servicio.

### Verificar Health Status:

En Railway Dashboard → Service → **Metrics** tab:
- Green = Healthy
- Yellow = Warning
- Red = Unhealthy (reiniciando)

---

## Monitoring & Logs

### Ver Logs en Tiempo Real:

**Opción 1: Dashboard**
- Service → Deployments → Click deployment → Logs tab

**Opción 2: CLI**
```bash
railway login
railway link  # Select project
railway logs --service telegram-bot
railway logs --service paypal-backend --follow
```

### Logs Importantes:

**Bot iniciando correctamente:**
```
Bot started successfully. Polling for updates...
Telethon client connected successfully as: Yadiel
```

**Bot reconectándose:**
```
Telethon disconnected. Reconnecting...
Attempting to connect Telethon (attempt 1/10)...
Telethon client connected successfully
```

**Graceful shutdown:**
```
Received signal 15. Starting graceful shutdown...
Shutdown signal received. Stopping bot...
Bot stopped gracefully
```

**Backend healthy:**
```
Starting PayPal backend on port 8000...
PayPal Mode: sandbox
Application startup complete.
```

### Métricas:

Railway Dashboard → **Metrics** tab:
- **CPU Usage**: Debe estar < 50% promedio
- **Memory Usage**: Debe estar < 400MB (de 512MB)
- **Network**: Spikes al descargar archivos grandes
- **Restart Count**: Debe ser 0 (si aumenta, hay problema)

### Alertas Recomendadas:

1. **Memory > 80%**: Possible memory leak
2. **Restart count > 5 en 1 hora**: Bot crasheando
3. **Health check failures**: Revisar logs

---

## Troubleshooting

### ❌ Bot no se inicia

**Síntoma**: Logs muestran error al iniciar

**Posibles causas:**

1. **SESSION_STRING inválido**
```
AuthKeyUnregisteredError: Session invalid! Need to regenerate SESSION_STRING
```
**Solución**: Regenerar con `generate_session.py`

2. **Variables faltantes**
```
ValueError: Missing required environment variables: BOT_TOKEN, API_ID, ...
```
**Solución**: Verificar todas las variables en Railway dashboard

3. **Database locked**
```
sqlite3.OperationalError: database is locked
```
**Solución**: 
- Verificar que persistent volume esté montado en `/data`
- Revisar que `DB_PATH=/data` esté configurado

### ❌ Backend devuelve 503

**Síntoma**: `/health` endpoint falla

**Diagnóstico**:
```bash
curl -v https://tu-backend.up.railway.app/health
```

**Posibles causas:**

1. **PayPal credentials inválidas**
```
Failed to get PayPal access token
```
**Solución**: Verificar CLIENT_ID y CLIENT_SECRET

2. **BACKEND_URL incorrecto**
**Solución**: Debe ser `https://` y terminar sin `/`

3. **PORT no asignado**
**Solución**: Verificar que `PORT=${{PORT}}` esté en variables

### ❌ Bot se desconecta frecuentemente

**Síntoma**: Logs muestran reconexiones constantes

```
Telethon disconnected. Reconnecting...
Connection failed: [Errno 110] Connection timed out. Retrying in 2s...
```

**Solución**:
- Verificar SESSION_STRING válido
- Revisar firewall/network de Railway
- Si persiste > 1 hora, abrir ticket en Railway

### ❌ Database no persiste

**Síntoma**: Usuarios pierden datos después de redeploy

**Diagnóstico**:
```bash
# En logs, buscar:
"Database initialized successfully"
```

Si cada deploy muestra tabla creada = NO hay persistent volume

**Solución**:
1. Ir a Volumes tab
2. Verificar volume montado en `/data`
3. Verificar `DB_PATH=/data` en variables
4. Redeploy

### ❌ FloodWaitError frecuentes

**Síntoma**: Logs muestran muchos FloodWaitError

```
FloodWaitError: waiting 120s before retry
```

**Causa**: Bot haciendo demasiadas requests a Telegram

**Solución**:
- El código ya maneja con retries exponenciales
- Si persiste: limitar usuarios concurrentes
- Considerar usar webhooks en lugar de polling

### ❌ Memory leak

**Síntoma**: Memory usage incrementa hasta 100% y crash

**Diagnóstico**: Railway Metrics → Memory usage aumentando constantemente

**Solución**:
1. Verificar que archivos temporales se eliminan (código mejorado ya lo hace)
2. Revisar logs de archivos descargados:
```
Temporary file removed: /tmp/...
```
3. Si persiste, aumentar memoria a 1GB (Railway settings)

---

## 🎯 Checklist Final

### Antes de Deploy:

- [ ] Código pushed a GitHub sin archivos sensibles
- [ ] `.env` NO está en GitHub
- [ ] `users.db` NO está en GitHub
- [ ] `*.session` NO están en GitHub
- [ ] `.gitignore` actualizado
- [ ] `Dockerfile.bot` y `Dockerfile.backend` creados
- [ ] `railway.toml` configurado

### Después de Deploy Bot:

- [ ] Variables de entorno configuradas
- [ ] Persistent volume montado en `/data`
- [ ] Logs muestran: "Bot started successfully"
- [ ] `/start` funciona en Telegram
- [ ] Reconnect automático funciona

### Después de Deploy Backend:

- [ ] Variables de entorno configuradas
- [ ] BACKEND_URL apunta a dominio de Railway
- [ ] Persistent volume montado en `/data`
- [ ] `/health` endpoint devuelve 200 OK
- [ ] Dominio público generado

### Testing:

- [ ] Bot responde a comandos
- [ ] Descarga de archivos funciona
- [ ] Premium upgrade funciona (con PayPal sandbox)
- [ ] Database persiste entre reinicios
- [ ] Graceful shutdown funciona (forzar redeploy)
- [ ] Logs sin errores críticos

---

## 🚀 Next Steps

### Pasar a Producción:

1. **PayPal Live Mode**:
```env
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=<live_client_id>
PAYPAL_CLIENT_SECRET=<live_secret>
```

2. **Custom Domain** (opcional):
- Railway Settings → Networking → Custom Domains
- Agregar CNAME en tu DNS provider

3. **Monitoring Externo**:
- [UptimeRobot](https://uptimerobot.com): Ping health endpoint cada 5 min
- [BetterStack](https://betterstack.com): Logs centralizados

4. **Backups**:
- Database ya hace backup automático en `/data/backups/`
- Descargar backups periódicamente con Railway CLI:
```bash
railway run cat /data/users.db > backup_local.db
```

5. **Scaling** (si crece):
- Aumentar recursos en Railway
- Considerar PostgreSQL en lugar de SQLite
- Separar bot de workers (descarga en background)

---

## 📞 Support

**Railway Issues**:
- [Railway Discord](https://discord.gg/railway)
- [Railway Docs](https://docs.railway.app)
- [Railway Status](https://status.railway.app)

**Bot Issues**:
- Check logs primero
- Review `TROUBLESHOOTING` section
- Contact @observer_bots en Telegram

---

## 🎉 Resultado Final

Con esta configuración, tu bot:

✅ Corre 24/7 en Railway
✅ Se reconecta automáticamente si falla
✅ Maneja FloodWait con retries
✅ Database persiste entre deployments
✅ Graceful shutdown en reinicios
✅ Health checks automáticos
✅ Logs rotados y limpios
✅ Backups automáticos
✅ Listo para producción

**Costo estimado**:
- **Free tier**: $5/month de crédito (suficiente para testing)
- **Hobby plan**: $5/month (recomendado para producción)
- **Pro plan**: $20/month (para alta demanda)

---

**Última actualización**: 5 de Diciembre 2025
**Versión**: 1.0.0 Production Ready
