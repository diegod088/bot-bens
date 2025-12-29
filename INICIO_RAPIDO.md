# 🚀 INICIO RÁPIDO - Dashboard del Bot

## ⚡ En 3 pasos

### 1️⃣ Instalar Dashboard (primera vez)
```bash
chmod +x install_dashboard.sh
./install_dashboard.sh
```

### 2️⃣ Iniciar el Dashboard
```bash
./run_dashboard.sh
```
O directamente:
```bash
python dashboard.py
```

### 3️⃣ Acceder
- **URL**: http://127.0.0.1:5000
- **Token**: (el que configuraste en el paso 1)

---

## 🤖 Iniciar Bot + Dashboard juntos

```bash
chmod +x run_both.sh
./run_both.sh
```

Esto inicia:
- ✅ Bot Telegram (escuchando mensajes)
- ✅ Dashboard Admin (en http://127.0.0.1:5000)

Presiona `Ctrl+C` para detener ambos.

---

## 📚 Documentación Completa

| Archivo | Descripción |
|---------|-----------|
| **DASHBOARD_README.md** | Características, API, instalación |
| **GUIA_DASHBOARD.md** | Guía paso a paso con ejemplos |
| **bot_with_paywall.py** | Bot principal |
| **dashboard.py** | Servidor del dashboard |

---

## 🔐 Cambiar Token de Admin

```bash
python configure_admin.py
```

Opciones:
1. Token personalizado
2. Token aleatorio seguro
3. Mantener actual

---

## 🔧 Estructura de Carpetas

```
bot descargar contenido/
├── bot_with_paywall.py         # Bot principal
├── dashboard.py                 # Servidor dashboard
├── database.py                  # Base de datos
├── templates/                   # Plantillas HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── users.html
│   └── user_detail.html
├── users.db                     # Base de datos SQLite
├── .env                         # Configuración
├── run_dashboard.sh             # Script iniciar dashboard
├── run_both.sh                  # Script bot + dashboard
├── install_dashboard.sh         # Script instalación
├── configure_admin.py           # Configurar admin
├── DASHBOARD_README.md          # Documentación completa
└── GUIA_DASHBOARD.md           # Guía de uso
```

---

## 🆘 Solución Rápida de Problemas

### Puerto 5000 ocupado
```bash
python -c "from dashboard import app; app.run(port=5001)"
```

### Base de datos no encontrada
```bash
python -c "from database import init_database; init_database()"
```

### Reiniciar todo
```bash
# Detener procesos
pkill -f "python dashboard.py"
pkill -f "python bot_with_paywall.py"

# Iniciar de nuevo
./run_both.sh
```

---

## 🎯 Ejemplos de Uso

### Ver estadísticas del bot
1. Entra a http://127.0.0.1:5000
2. Dashboard muestra todo en tiempo real

### Buscar un usuario
1. Ir a pestaña "Usuarios"
2. Escribir User ID (Telegram)
3. Presionar Buscar

### Monitorear premium expirando
1. Ver lista de usuarios
2. Buscar badges naranjas/rojos
3. Esos usuarios expiran en ≤3 días

---

## 🌐 Acceso Remoto

Para acceder desde otra máquina:

1. Encuentra tu IP:
   ```bash
   hostname -I    # Linux
   ipconfig        # Windows
   ```

2. Usa en otra PC:
   ```
   http://tu_ip:5000
   ```

---

## 📊 Lo que verás en el Dashboard

✅ **Dashboard Principal**
- 📈 Usuarios totales, premium, gratis
- 💾 Total de descargas
- 📊 Actividad hoy (fotos, videos, música, APKs)
- 💰 Ingresos estimados

✅ **Usuarios**
- 🔍 Buscar por ID
- 📋 Lista con paginación
- ⚠️ Alertas de premium expirando
- 🖇️ Link a detalles

✅ **Detalles de Usuario**
- 👤 Avatar y ID
- ✨ Estado premium y días restantes
- 📱 Uso diario desglosado
- 📅 Fechas de creación y actividad

---

## ✨ Features Principales

- 🔐 **Seguro**: Autenticación con token
- ⚡ **Rápido**: Actualización cada 30 segundos
- 📱 **Responsive**: Funciona en desktop, tablet y móvil
- 🎨 **Bonito**: Interfaz moderna con gradientes
- 📊 **Completo**: Todos los datos que necesitas

---

## 💡 Tips Útiles

- 🔄 Los datos se actualizan automáticamente
- 🎯 Usa la búsqueda para encontrar usuarios rápidamente
- ⚠️ Los badges coloridos indican estado premium
- 📝 Haz backup regular de `users.db`
- 🔑 Cambia el token de admin en producción

---

**¡Listo! Ya tienes tu dashboard funcionando.** 🎉

Para más detalles, lee:
- 📖 **GUIA_DASHBOARD.md** - Guía completa
- 📖 **DASHBOARD_README.md** - Documentación técnica
