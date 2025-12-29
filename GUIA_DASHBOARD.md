# 📊 Guía de Uso - Dashboard Admin del Bot

## 🔐 Paso 1: Acceder al Dashboard

1. Abre tu navegador web
2. Ve a: `http://127.0.0.1:5000`
3. Ingresa el token de administrador: **`admin123`** (predeterminado)

```
┌─────────────────────────────────────────┐
│  🔐 Admin Dashboard                     │
│                                         │
│  Ingresa el token de administrador:     │
│  ┌─────────────────────────────────┐   │
│  │ ••••••••••                      │   │
│  └─────────────────────────────────┘   │
│  [  Acceder  ]                          │
└─────────────────────────────────────────┘
```

## 📈 Paso 2: Dashboard Principal

Una vez autenticado, verás el **dashboard principal** con:

### Estadísticas Generales
```
┌─────────────────┬─────────────────┬─────────────────┬──────────────────┐
│ Usuarios Totales│  Premium Users  │  Free Users     │ Total Downloads  │
│       47        │        12       │       35        │      1,234       │
└─────────────────┴─────────────────┴─────────────────┴──────────────────┘

┌─────────────────┬─────────────────┬──────────────────┐
│  Activos Hoy    │ Ingresos Est.   │  Estimated $$    │
│       23        │     3,600 💫    │   $36.00         │
└─────────────────┴─────────────────┴──────────────────┘
```

### Actividad Diaria
Aquí ves el desglose de descargas por tipo:
- 📸 **Fotos**: 150 descargadas hoy
- 🎬 **Videos**: 87 descargados hoy
- 🎵 **Música**: 42 canciones descargadas
- 📱 **APKs**: 15 aplicaciones descargadas
- 📊 **Total diario**: 294 descargas

## 👥 Paso 3: Gestionar Usuarios

Haz clic en **"Usuarios"** en el menú superior.

### 🔍 Buscar Usuarios

1. Ingresa el **User ID** (número de Telegram) en la caja de búsqueda
2. Presiona **Enter** o haz clic en **"Buscar"**

```
Ejemplo: Buscar usuario 1234567890
┌──────────────────────────────────────────┐
│ Buscar por User ID...                    │ [Buscar]
└──────────────────────────────────────────┘
```

### 📋 Lista de Usuarios

Verás una tabla con todos los usuarios:

```
┌──────────────┬────────────────┬──────────────┬───────────┬──────────────┐
│ User ID      │ Estado Premium │ Días Restant │ Descargas │ Uso Diario   │
├──────────────┼────────────────┼──────────────┼───────────┼──────────────┤
│ 1438860917   │ ✨ PREMIUM     │ 15 días      │ 456       │ 📸2 🎬5 🎵1 │
│ 1234567890   │ Gratis         │ —            │ 123       │ 📸0 🎬3 🎵0 │
│ 9876543210   │ ✨ PREMIUM     │ 3 días ⚠️    │ 789       │ 📸4 🎬2 🎵2 │
└──────────────┴────────────────┴──────────────┴───────────┴──────────────┘
```

### 📊 Información en la Tabla

| Columna | Significado |
|---------|-----------|
| **User ID** | Identificador único de Telegram |
| **Estado Premium** | ✨ PREMIUM (activo) o Gratis |
| **Días Restantes** | Cuántos días de premium quedan |
| **Descargas** | Total de descargas del usuario |
| **Uso Diario** | Desglose hoy: fotos, videos, música, APKs |
| **Creación** | Fecha en que se registró |
| **Última Actividad** | Última vez que usó el bot |

### ⚠️ Indicadores Visuales

- **🟢 ✨ PREMIUM**: Usuario con suscripción activa
- **🔴 PREMIUM**: Usuario con premium expirando en ≤3 días
- **⚪ Gratis**: Usuario sin suscripción

## 👤 Paso 4: Ver Detalles de un Usuario

Haz clic en el botón **"Ver"** o en el **User ID** de cualquier usuario.

```
┌──────────────────────────────────────────────────────────┐
│ ← Volver a Usuarios                                      │
│                                                          │
│ 👤                       Usuario #1438860917             │
│                          ✨ PREMIUM  Creado: 01/12/2024  │
├──────────────────────────────────────────────────────────┤
│ ✨ Premium Activo                                        │
│ Vence: 10/01/2025 (15 días)                              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 📊 Estadísticas de Descargas                             │
│                                                          │
│ Descargas Totales: 456                                   │
│ Idioma: 🇪🇸 Español                                     │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 📅 Uso Diario (Hoy)                                      │
│                                                          │
│ 📸 Fotos: 2        🎬 Videos: 5                          │
│ 🎵 Música: 1       📱 APKs: 0                            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 📋 Información de Cuenta                                 │
│                                                          │
│ Creación: 01/12/2024 15:30:45                            │
│ Última Actividad: 27/12/2024 20:15:30                    │
└──────────────────────────────────────────────────────────┘
```

## 🎯 Casos de Uso

### Caso 1: Encontrar usuarios con premium expirando
1. Ve a **Usuarios**
2. Busca usuarios con el badge **"PREMIUM"** en color naranja/rojo
3. Estos usuarios tienen ≤3 días de premium

### Caso 2: Ver usuario más activo
1. Ve a **Usuarios**
2. Ordena por **"Descargas"** (columna numérica)
3. El usuario con el número más alto es el más activo

### Caso 3: Monitorear ingresos
1. En el **Dashboard Principal**
2. Ver la caja **"Ingresos Estimados"**
3. Cada usuario premium = 300⭐ (USD ~30)

### Caso 4: Analizar uso diario
1. Ve a **Dashboard Principal**
2. Ver sección **"Actividad Diaria"**
3. Comparar números cada día para ver tendencias

## 🔄 Actualizaciones Automáticas

- Los datos se actualizan automáticamente cada **30 segundos**
- No necesitas recargar la página manualmente
- Las estadísticas en el dashboard cambian en tiempo real

## 🔐 Cambiar Token de Administrador

Para cambiar el token predeterminado:

1. Abre el archivo `.env`
2. Busca la línea: `ADMIN_TOKEN=admin123`
3. Reemplaza `admin123` con tu nuevo token
4. Reinicia el dashboard

```env
# Antes
ADMIN_TOKEN=admin123

# Después
ADMIN_TOKEN=tu_token_super_seguro_123456
```

## 📱 Acceso desde otros dispositivos

Si necesitas acceder desde otra computadora en la red:

1. Encuentra la IP de tu máquina:
   ```bash
   ip addr show  # Linux
   ipconfig      # Windows
   ```

2. Reemplaza `127.0.0.1` en la URL:
   ```
   http://tu_ip:5000
   Ej: http://192.168.1.100:5000
   ```

## ⚙️ Mantenimiento

### Limpiar sesiones expiradas
Las sesiones se limpian automáticamente después de cerrar el navegador.

### Hacer backup de datos
El archivo `users.db` contiene toda la información. Haz backup regularmente:
```bash
cp users.db users_backup_$(date +%Y%m%d).db
```

### Ver logs del dashboard
Los logs se muestran en la terminal donde ejecutas el dashboard.

## 🆘 Preguntas Frecuentes

**P: ¿Qué es "Ingresos Estimados"?**
R: Se calcula como: Usuarios Premium × 300⭐ (el costo de una suscripción).

**P: ¿Por qué algunas descargas aparecen con 0?**
R: Significa que ningún usuario descargó ese tipo de contenido hoy.

**P: ¿Puedo editar datos directamente en el dashboard?**
R: En esta versión, el dashboard es solo para lectura. Las ediciones se hacen directamente en el bot.

**P: ¿Cómo exporto los datos?**
R: Puedes exportar `users.db` directamente. Es un archivo SQLite estándar.

**P: ¿El dashboard es seguro?**
R: Está protegido con contraseña y solo accesible localmente. Para producción, usa HTTPS y cámbialo a un puerto seguro.

---

**Última actualización**: 27/12/2024  
**Dashboard v1.0** 🚀
