# 🤖 Bot Admin Dashboard

Panel de administración web para gestionar y monitorear el bot de Telegram con sistema de pagos premium.

## 🚀 Características

- **Autenticación de Administrador**: Acceso protegido con token
- **Dashboard Principal**: Estadísticas en tiempo real del bot
  - Total de usuarios
  - Usuarios con Premium
  - Descargas totales
  - Actividad diaria

- **Gestión de Usuarios**: Listado completo de usuarios con búsqueda
  - Estado de premium de cada usuario
  - Días restantes de suscripción
  - Uso diario (fotos, videos, música, APKs)
  - Información de creación y última actividad

- **Detalles de Usuario**: Información detallada por usuario
  - Estado premium y fecha de expiración
  - Descargas totales
  - Estadísticas de uso diario
  - Idioma preferido

- **Actualización en Tiempo Real**: Los datos se actualizan automáticamente cada 30 segundos

## 📋 Requisitos

- Python 3.8+
- Flask 3.0.0+
- Base de datos SQLite (`users.db`)

## 🔧 Instalación

1. **Instalar dependencias**:
```bash
pip install Flask==3.0.0 Werkzeug==3.0.1
```

2. **Configurar variables de entorno** en `.env`:
```
ADMIN_TOKEN=tu_token_seguro_aqui
DASHBOARD_SECRET_KEY=tu_clave_secreta_aqui
```

## ▶️ Cómo ejecutar

### Opción 1: Script bash
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Opción 2: Comando directo
```bash
source .venv/bin/activate
python dashboard.py
```

El dashboard estará disponible en: **http://127.0.0.1:5000**

## 🔐 Acceso

1. Abre en tu navegador: http://127.0.0.1:5000
2. Ingresa el token de administrador (por defecto: `admin123`)
3. ¡Listo! Tendrás acceso al dashboard

> ⚠️ **IMPORTANTE**: Cambia el token predeterminado antes de usar en producción.

## 📊 Secciones del Dashboard

### 1. Dashboard Principal (`/`)
- Estadísticas generales del bot
- Actividad diaria (fotos, videos, música, APKs)
- Información del sistema
- Actualización automática cada 30 segundos

### 2. Gestión de Usuarios (`/users`)
- Lista completa de usuarios
- Búsqueda por User ID
- Paginación (20 usuarios por página)
- Indicadores visuales:
  - 🟢 Premium activo
  - 🔴 Expirando pronto (≤3 días)
  - ⚪ Gratis

### 3. Detalles de Usuario (`/user/<id>`)
- Información completa del usuario
- Estado premium detallado
- Gráficos de uso diario
- Fechas de creación y última actividad

## 🔑 Variables de Entorno

```env
# Token de administrador para acceder al dashboard
ADMIN_TOKEN=admin123

# Clave secreta para sesiones Flask
DASHBOARD_SECRET_KEY=dashboard-secret-key-cambiar-en-produccion
```

## 📈 API Endpoints

El dashboard expone los siguientes endpoints internos:

- `GET /api/stats` - Obtener estadísticas generales
- `GET /api/users?page=1&search=` - Obtener lista de usuarios
- `GET /api/user/<user_id>` - Obtener detalles de un usuario

Todos requieren autenticación de administrador.

## 🎨 Interfaz Visual

- **Diseño Responsivo**: Compatible con desktop, tablet y móvil
- **Tema Moderno**: Gradientes y colores corporativos
- **Indicadores Visuales**: Badges, gráficos y estadísticas en tiempo real
- **Navegación Intuitiva**: Menú superior fijo con opciones principales

## 🐛 Solución de Problemas

### Puerto 5000 ya está en uso
```bash
# En otro puerto (ej: 5001)
python -c "from dashboard import app; app.run(port=5001)"
```

### Base de datos no encontrada
Asegúrate que `users.db` existe y está en el mismo directorio que `dashboard.py`.

### Error "Token incorrecto"
Verifica que el `ADMIN_TOKEN` en `.env` coincida con el que ingresaste.

## 🔒 Seguridad

- ✅ Autenticación basada en token
- ✅ Sesiones encriptadas con Flask
- ✅ Cambio de contraseña recomendado en producción
- ✅ HTTPS recomendado en producción

## 📝 Notas

- El dashboard accede a la misma base de datos SQLite que usa el bot
- Los datos se actualizan automáticamente cada 30 segundos
- El servidor escucha en `127.0.0.1:5000` (solo localhost)

## 🚀 Próximas Mejoras

- [ ] Exportar datos a CSV/Excel
- [ ] Gráficos de estadísticas históricas
- [ ] Gestión de premium manual
- [ ] Sistema de logs del bot en tiempo real
- [ ] Notificaciones de usuarios con premium expirando

---

**Versión**: 1.0  
**Última actualización**: Diciembre 2024
