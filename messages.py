"""
Multi-language messages for Telegram Bot
Supports: Spanish (es), English (en), Portuguese (pt), Italian (it)
"""

MESSAGES = {
    "es": {
        # Start command
        "start_welcome": "� BOT DE DESCARGAS\n\n",
        "start_description": "Descarga fotos y videos de Telegram, incluidos canales privados y restringidos.\n\n",
        "start_divider": "🔐 Para acceder a contenido privado, el bot usa tu cuenta\nsolo para descargar el contenido que tú ves en Telegram.\nNo lee chats, no envía mensajes ni modifica tu cuenta.\n\n",
        "start_how_to": "🚀 *Cómo usarlo:*\n1️⃣ Copia el enlace del mensaje\n2️⃣ Pégalo aquí y envíalo\n\n",
        "start_example": "💡 *Ejemplo:*\n`https://t.me/canal/123`\n\n",
        "start_premium_active": "💎 *Estado:* Eres Premium (Sin límites)\n\n",
        "start_premium_plan": "💎 *Estado:* Eres Premium\n📅 Vence: {expiry} ({days_left} días)\n\n",
        "start_premium_usage": "",
        "start_premium_permanent": "💎 *Estado:* Premium Permanente\n\n",
        "start_usage": "",
        "start_photos_unlimited": "",
        "start_videos_count": "",
        "start_music_count": "",
        "start_apk_count": "",
        "start_renew": "",
        "start_free_plan": "👤 *Estado:* Plan Gratuito\n(Tienes un límite diario de descargas)\n\n",
        "start_photos_daily": "",
        "start_videos_total": "",
        "start_blocked": "",
        "start_upgrade": "⭐ *¿Quieres descargar sin límites?*\nUsa el botón 'Planes' abajo.",
        "start_use_buttons": "",
        "start_cta": "",
        
        # Panel
        "panel_title": "⚙️ *PANEL DE CONTROL*\n👤 *Usuario:* {user_name}\n\n",
        "panel_plan_free": "� *Plan:* Gratuito\n",
        "panel_plan_premium": "💎 *Plan:* Premium\n📅 *Vence:* {expiry} ({days_left} días)\n",
        "panel_expires": "",
        "panel_photos": "📸 Fotos: {count}/{limit}\n",
        "panel_videos": "🎬 Videos: {count}/{limit}\n",
        "panel_music": "🎵 Música: {count}/{limit}\n",
        "panel_apk": "📦 APK: {count}/{limit}\n",
        "panel_stats_title": "\n📊 *Tus Descargas de Hoy:*\n",
        "panel_stats_row": "",
        "panel_stats_unlimited": "{icon} {label}: Ilimitado ✨\n",
        "panel_connection_title": "\n🔐 *Estado de Conexión:*\n",
        "panel_connected": "✅ Conectado a Telegram",
        "panel_connection_ok": "✅ Conectado a Telegram\n_(Puedes descargar de canales privados)_\n",
        "panel_disconnected": "❌ No conectado",
        "panel_connection_fail": "❌ No conectado\n_(Conecta tu cuenta para canales privados)_\n",
        "panel_desc_connected": "_(Puedes descargar de canales privados)_\n\n",
        "panel_desc_disconnected": "_(Conecta tu cuenta para canales privados)_\n\n",
        "panel_footer": "Mejora a Premium para descargas ilimitadas\n",
        "btn_panel": "📥 Empezar a Descargar",
        "btn_connect": "🔐 Conectar Cuenta",
        "btn_disconnect": "👋 Desconectar",
        "btn_renew": "💎 Renovar Premium",
        "btn_upgrade": "💎 Mejorar a Premium",
        
        # Buttons
        "btn_panel": "📥 Empezar a Descargar",
        "btn_download_now": "📥 Empezar a Descargar",
        "btn_how_to_use": "❓ Ayuda",
        "btn_plans": "💎 Ver Planes",
        "btn_my_stats": "📊 Mis estadísticas",
        "btn_change_language": "🌐 Idioma / Language",
        "btn_support": "💬 Soporte",
        "btn_official_channel": "📢 Canal Oficial",
        "btn_pay_stars": "⭐ Pagar con Estrellas",
        "btn_join_channel": "📢 Únete al Canal Oficial",
        
        # Language selection
        "language_select": "🌐 *Selecciona tu idioma*\n\nElige el idioma que prefieres usar:",
        "language_changed": "✅ Idioma cambiado a Español",
        "btn_spanish": "🇪🇸 Español",
        "btn_english": "🇺🇸 English",
        "btn_portuguese": "🇧🇷 Português",
        "btn_italian": "🇮🇹 Italiano",
        
        # Download flow
        "download_greeting": "🎯 Vamos a descargar tu contenido\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_step_1": "📋 Paso 1 de 2\n📎 Envíame el ENLACE del mensaje que quieres descargar.\n\n¿Qué es \"el enlace\"?\n➡️ Es la dirección del mensaje, algo así como:\nhttps://t.me/canal/123\n\nCómo copiarlo (muy fácil):\n1) Abre el mensaje en Telegram\n2) Mantén el dedo encima → \"Copiar enlace\"\n3) Vuelve aquí y pégalo\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_example": "",
        "download_supported": "🔓 ¿De dónde puedo descargar?\n• Canales públicos\n• Grupos públicos\n• Canales privados\n   → Si es privado, necesito que me invites\n   (solo envíame el enlace de invitación tipo t.me/+codigo)\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_or_command": "✔ Si pegas un enlace válido, seguiré con el Paso 2 automáticamente.",
        
        # Guide
        "guide_title": "📥 BOT DE DESCARGAS — GUÍA DE USO\n\n",
        "guide_step_1": "🔐 <b>Paso 0: Conectar tu cuenta (solo una vez)</b>\nPara poder descargar contenido de canales privados o restringidos, el bot necesita usar tu cuenta únicamente para acceder al contenido que tú ves en Telegram.\n\n• No lee chats personales\n• No envía mensajes\n• No modifica tu cuenta\n\nCuando el bot lo necesite, te pedirá acceso y te guiará paso a paso.\n\n",
        "guide_step_2": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Paso 1: Copiar el enlace del mensaje</b>\n1️⃣ Abre en Telegram el mensaje que quieres descargar\n2️⃣ Mantén presionado el mensaje\n3️⃣ Toca \"Copiar enlace\"\n\n",
        "guide_formats": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Paso 2: Enviar el enlace al bot</b>\n4️⃣ Vuelve a este chat\n5️⃣ Pega el enlace\n6️⃣ Envíalo y espera la descarga\n\n",
        "guide_tips": "",
        "guide_premium": "",
        "guide_option_a": "",
        "guide_option_b": "",
        "guide_note": "",
        
        # Plans
        "plans_title": "Si solo quieres probar el bot, te sirve.\nPero si realmente quieres DESCARGAR contenido sin parar... esto NO basta.\n\n",
        "plans_free": "🚫 *PLAN GRATIS (LIMITADO)*\n\n📸 Fotos: 10 diarias\n🎬 Videos: 3 totales\n🎵 Música: ❌ Bloqueado\n📦 APK: ❌ Bloqueado\n\n",
        "plans_premium": "🔥💎 *PLAN PREMIUM — {price} ⭐*\n━━━━━━━━━━━━━━━━━━━━\n📸 Fotos: Ilimitadas\n🎬 Videos: 50 por DÍA\n🎵 Música: 50 por DÍA\n📦 APK: 50 por DÍA\n♻️ Renovación automática cada 24h\n⏳ Dura 30 días completos\n\n",
        "plans_benefits": "🚀 *¿POR QUÉ PREMIUM ES IMPARABLE?*\n✔ Descargas TODO: videos, música, APK, fotos\n✔ 50 descargas diarias por categoría\n✔ Acceso sin restricciones\n✔ Velocidad mejorada\n✔ Ideal para canales privados, contenido frecuente o descargas grandes\n✔ El bot trabaja AL MÁXIMO para ti\n\n",
        "plans_warning": "⚠️ *No te quedes limitado*\nCada día que sigues en Free → Pierdes descargas, tiempo y contenido que podrías guardar.\n\n",
        "plans_payment": "⭐ *Sube a Premium con Telegram Stars*\nToca el botón de abajo y libera TODA la potencia del bot.",
        "plans_imparable": "💎 *¡SÉ IMPARABLE CON PREMIUM!*",
        "btn_get_premium": "💎 Obtener Premium",
        "btn_back_start": "🏠 Volver al inicio",
        
        # Premium purchase
        "premium_payment_title": "💎 Premium - 30 días",
        "premium_payment_description": "Acceso completo por 30 días",
        "premium_activated": "🎉 *Premium Activado*\n\n━━━━━━━━━━━━━━━━━━━━\n\n✅ Pago recibido exitosamente\n💎 Suscripción Premium activada\n\n📅 Válido hasta: {expiry}\n⏰ Duración: 30 días\n\n━━━━━━━━━━━━━━━━━━━━\n\n🚀 Usa /start para comenzar",
        "invoice_sent": "✅ *Factura enviada*\n\nRevisa el mensaje de pago que apareció arriba.\n💳 Completa el pago para activar Premium.",
        "payment_not_configured": "⚠️ *Sistema de Pagos en Configuración*\n\nEl bot aún no tiene habilitado Telegram Stars.\n\n━━━━━━━━━━━━━━━━━━━━\n\n📋 *Para el administrador:*\n1. Abre @BotFather\n2. Usa /mybots\n3. Selecciona este bot\n4. Toca 'Payments'\n5. Habilita 'Telegram Stars'\n\n━━━━━━━━━━━━━━━━━━━━\n\n💡 Mientras tanto, disfruta:\n• 3 videos gratis\n• Fotos ilimitadas\n\n📢 Síguenos: @observer_bots",
        "payment_error": "❌ *Error Temporal*\n\nNo se pudo procesar el pago.\nIntenta nuevamente en unos momentos.\n\n📢 Soporte: @observer_bots\n\n🔧 Error: `{error}`",
        
        # Errors
        "error_invalid_link": "❌ *Enlace inválido*\n\n",
        "error_invalid_format": "El enlace debe ser de Telegram:\n• Canales públicos: t.me/canal/123\n• Canales privados: t.me/c/123456/789\n\n💡 Toca el mensaje específico → Copiar enlace",
        "error_message_not_found": "❌ *Mensaje No Encontrado*\n\n",
        "error_message_reasons": "No pude encontrar este mensaje en el canal.\n\n🔍 *Posibles razones:*\n• El mensaje fue eliminado\n• El enlace está incorrecto\n• El canal no existe\n\n💡 Verifica el enlace y envíamelo otra vez.",
        "error_no_media": "❌ *Sin Contenido*\n\n",
        "error_no_media_desc": "Este mensaje no tiene archivos para descargar.\n\n💡 Asegúrate de copiar el enlace de un mensaje con:\n📸 Fotos\n🎬 Videos\n🎵 Música\n📦 Archivos",
        "error_private_channel": "🔒 *Canal Privado - Acceso Necesario*\n\n",
        "error_private_need_access": "Para descargar de este canal privado necesito que me agregues.\n\n*🌟 2 Opciones:*\n\nOpción 1 → Envíame un enlace de invitación (empieza con t.me/+)\nOpción 2 → Agrégame manualmente al canal con mi cuenta {username}",
        
        # Limits
        "limit_free_videos": "🚫 *Límite Alcanzado*\n\n",
        "limit_free_videos_desc": "Has usado tus {count}/{limit} descargas de video.\n\n💎 *Soluciones:*\n\n1️⃣ Descarga fotos (ilimitadas)\n2️⃣ Mejora a Premium para 50 videos diarios\n\n¡Toca el botón para ver planes!",
        "limit_free_photos": "⚠️ *Límite Diario de Fotos*\n\n",
        "limit_free_photos_desc": "Has descargado {count}/{limit} fotos hoy.\n\n♻️ Tu límite se renueva en 24 horas.\n\n💎 *¿Quieres más?*\nCon Premium tienes fotos ilimitadas + 50 videos diarios",
        "limit_premium_videos": "⚠️ *Límite Diario Alcanzado*\n\n",
        "limit_premium_videos_desc": "Has descargado {count}/{limit} videos hoy.\n\n♻️ Tu límite se renueva en 24 horas.\n\n💡 Mientras esperas puedes descargar:\n✨ Fotos: Ilimitadas\n🎵 Música: {music}/{music_limit}\n📦 APK: {apk}/{apk_limit}",
        "limit_music_blocked": "🚫 *Música Bloqueada*\n\n",
        "limit_music_blocked_desc": "La descarga de música requiere Premium.\n\n💎 *Con Premium obtienes:*\n\n🎵 50 descargas de música diarias\n🎬 50 videos diarios\n✨ Fotos ilimitadas\n📦 50 APK diarios",
        "limit_apk_blocked": "🚫 *APK Bloqueado*\n\n",
        "limit_apk_blocked_desc": "La descarga de APK requiere Premium.\n\n💎 *Con Premium obtienes:*\n\n📦 50 descargas de APK diarias\n🎬 50 videos diarios\n✨ Fotos ilimitadas\n🎵 50 música diarias",
        
        # Download status
        "status_processing": "🔄 Procesando...",
        "status_detecting_album": "🔍 Detectando álbum...",
        "status_album_detected": "📸 Álbum detectado: {count} archivos\n⏳ Preparando descarga...",
        "status_sending": "📤 Enviando...",
        "status_sending_progress": "📤 Enviando {current}/{total}...",
        "status_downloading": "📥 Descargando...",
        "status_downloading_progress": "📥 Descargando {current}/{total}...",
        
        # Success messages
        "success_download": "✅ *Descarga Completada*\n\n",
        "success_album": "📸 Álbum de {count} archivos descargado\n\n",
        "success_photos_unlimited": "📸 Fotos ilimitadas con Premium ✨",
        "success_photos_daily": "📸 Fotos hoy: {count}/{limit}\n♻️ Se resetea en 24h\n\n💎 /premium para fotos ilimitadas",
        "success_videos_premium": "📊 Videos hoy: {count}/{limit}\n♻️ Se resetea en 24h",
        "success_videos_free": "📊 Videos usados: {count}/{limit}\n🎁 Te quedan: *{remaining}* descargas\n\n💎 /premium para 50 videos diarios",
        "success_music": "🎵 Música hoy: {count}/{limit}\n♻️ Se resetea en 24h",
        "success_apk": "📦 APK hoy: {count}/{limit}\n♻️ Se resetea en 24h",
        "success_auto_joined": "\n\n🔗 Canal unido automáticamente",
        
        # Stats
        "stats_title": "📊 *Tus Estadísticas*\n\n",
        "stats_plan": "💎 *Plan:* {plan}\n",
        "stats_expires": "📅 *Expira:* {expiry}\n",
        "stats_downloads": "📥 *Descargas totales:* {count}\n",
        "stats_daily": "📊 *Uso diario:*\n",
        "stats_photos": "• Fotos: {count}/{limit}\n",
        "stats_videos": "• Videos: {count}/{limit}\n",
        "stats_music": "• Música: {count}/{limit}\n",
        "stats_apk": "• APK: {count}/{limit}\n",
        "stats_reset": "\n♻️ *Se resetea:* En 24 horas",
        "btn_refresh_stats": "🔄 Actualizar Stats",
        
        # Admin stats
        "admin_stats_title": "👑 *Panel de Administración*\n\n",
        "admin_global_stats": "🌍 *Estadísticas Globales*\n\n",
        "admin_total_users": "👥 *Total Usuarios:* `{count}`\n",
        "admin_premium_users": "💎 *Usuarios Premium:* `{count}`\n",
        "admin_free_users": "🆓 *Usuarios Gratis:* `{count}`\n",
        "admin_total_downloads": "📊 *Total Histórico:* `{count:,}`\n\n",
        "admin_activity": "📈 *Actividad:*\n",
        "admin_active_today": "• Hoy: `{count}` usuarios\n",
        "admin_active_week": "• Esta semana: `{count}` usuarios\n",
        "admin_avg_downloads": "📥 *Promedio Descargas/Usuario:* `{avg:.1f}`\n",
        "admin_revenue": "💰 *Ingresos (Stars):* `{stars:,}` ⭐\n\n",
        "admin_top_users": "🏆 *Top Usuarios:*\n",
        
        # Login/Account Setup
        "login_already_active": "✅ *Ya tienes una sesión activa*\n\nSi quieres cambiar de cuenta, usa /logout primero.",
        "login_setup_title": "🔐 *Configuración de Cuenta*\n\nPara descargar contenido sin restricciones y evitar baneos, necesitas iniciar sesión con tu propia cuenta de Telegram.\n\n📱 *Paso 1:* Envíame tu número de teléfono en formato internacional.\nEjemplo: `+51999999999`",
        "login_invalid_phone": "❌ *Formato incorrecto*\n\nEl número debe incluir el código de país y empezar con +.\nEjemplo: `+51999999999`\n\nInténtalo de nuevo:",
        "login_connecting": "🔄 Conectando con Telegram...",
        "login_code_sent": "📩 *Código enviado*\n\nRevisa tus mensajes de Telegram (no SMS).\n\n⚠️ *IMPORTANTE:*\nTelegram bloquea el código si lo envías tal cual.\nPor favor, envíalo separando los números con un espacio o guión.\n\nEjemplo: Si el código es `12345`, envía `1 2 3 4 5` o `12-345`.",
        "login_error_connect": "❌ *Error al conectar*\n\n`{error}`\n\nIntenta de nuevo con /configurar",
        "login_session_expired": "❌ Sesión expirada. Usa /configurar de nuevo.",
        "login_verifying_code": "🔄 Verificando código...",
        "login_2fa_required": "🔐 *Verificación en 2 Pasos*\n\nTu cuenta tiene contraseña de doble factor (2FA).\nPor favor, envíame tu contraseña para continuar.",
        "login_success": "✅ *¡Configuración Exitosa!*\n\nTu cuenta ha sido vinculada correctamente.\nAhora el bot usará tu propia cuenta para las descargas, lo que reduce el riesgo de baneo y mejora la velocidad.\n\n🚀 ¡Ya puedes descargar contenido!",
        "login_wrong_code": "❌ *Código Incorrecto*\n\nEl código no es válido. Intenta de nuevo.\n\n💡 Recuerda: envía el código separado con espacios o guiones.\nEjemplo: `1 2 3 4 5` o `12-345`",
        "login_wrong_password": "❌ *Contraseña Incorrecta*\n\nLa contraseña 2FA no es correcta.\nIntenta de nuevo:",
        "login_cancelled": "❌ Proceso cancelado.\nUsa /configurar cuando quieras intentarlo de nuevo.",
        "logout_success": "✅ *Sesión Cerrada*\n\nTu cuenta ha sido desvinculada.\nUsa /configurar para vincular una cuenta nuevamente.",
        "logout_no_session": "ℹ️ No hay ninguna sesión activa.",
        "btn_cancel_login": "❌ Cancelar",
        "btn_back_menu": "◀️ Volver al menú",
    },
    "en": {
        # Start command
        "start_welcome": "👋 Hello! Welcome to the Downloader Bot.\n\n",
        "start_description": "📥 Download photos, videos, music, and files from Telegram messages.\nJust send me the *message link* you want to download.\n\n",
        "start_divider": "━━━━━━━━━━━━━━━━━━━━━\n",
        "start_how_to": "📌 *How to use?*\n1️⃣ Open the message in Telegram\n2️⃣ Copy the message link\n3️⃣ Paste it here and done ✅\n\n",
        "start_example": "Example: `https://t.me/channel/123`\nFor private channels: `t.me/+invitationCode`\n\n",
        "start_premium_active": "💎 *Premium Plan*\n📅 Expires: {expiry} ({days_left} days)\n\n",
        "start_premium_plan": "💎 *Premium Plan*\n📅 Expires: {expiry} ({days_left} days)\n\n",
        "start_premium_usage": "📈 *Daily Usage*\n• Photos: Unlimited ✨\n• Videos: {daily_video}/{video_limit}\n• Music: {daily_music}/{music_limit}\n• APK: {daily_apk}/{apk_limit}\n\nRenew with /premium",
        "start_premium_permanent": "💎 *Premium Active* ✨",
        "start_usage": "📈 *Daily Usage*\n",
        "start_photos_unlimited": "• Photos: Unlimited ✨\n",
        "start_videos_count": "• Videos: {daily_video}/{limit}\n",
        "start_music_count": "• Music: {daily_music}/{limit}\n",
        "start_apk_count": "• APK: {daily_apk}/{limit}\n\n",
        "start_renew": "Renew with /premium",
        "start_free_plan": "💎 *Free Plan*\n• Photos: {daily_photo}/{photo_limit}/day\n• Videos: {downloads}/{download_limit} total\n• Music & APK: ❌ Blocked\n\nUpgrade with /premium",
        "start_photos_daily": "• Photos: {daily_photo}/{limit}/day\n",
        "start_videos_total": "• Videos: {downloads}/{limit} total\n",
        "start_blocked": "• Music & APK: ❌ Blocked\n\n",
        "start_upgrade": "Upgrade your plan with /premium",
        "start_use_buttons": "\n\n👇 Use the buttons to start",
        "start_cta": "\n\n👇 Use the buttons to start",
        
        # Buttons
        "btn_panel": "📥 Start Downloading",
        "btn_download_now": "🎯 Download Now",
        "btn_how_to_use": "❓ How to use",
        "btn_plans": "💎 Plans",
        "btn_my_stats": "📊 My statistics",
        "btn_change_language": "🌐 Change language",
        "btn_support": "💬 Support",
        "btn_official_channel": "📢 Official Channel",
        "btn_pay_stars": "⭐ Pay with Stars",
        "btn_join_channel": "📢 Join Official Channel",
        "btn_connect": "🔐 Connect Account",
        "btn_disconnect": "👋 Disconnect",
        "btn_renew": "💎 Renew Premium",
        "btn_upgrade": "💎 Upgrade to Premium",
        
        # Language selection
        "language_select": "🌐 *Select your language*\n\nChoose your preferred language:",
        "language_changed": "✅ Language changed to English",
        "btn_spanish": "🇪🇸 Español",
        "btn_english": "🇺🇸 English",
        "btn_portuguese": "🇧🇷 Português",
        "btn_italian": "🇮🇹 Italiano",
        
        # Download flow
        "download_greeting": "🎯 Let's download your content\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_step_1": "📋 Step 1 of 2\n📎 Send me the LINK of the message you want to download.\n\nWhat is \"the link\"?\n➡️ It's the message address, something like:\nhttps://t.me/channel/123\n\nHow to copy it (very easy):\n1) Open the message in Telegram\n2) Press and hold → \"Copy link\"\n3) Come back here and paste it\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_example": "",
        "download_supported": "🔓 Where can I download from?\n• Public channels\n• Public groups\n• Private channels\n   → If it's private, I need an invitation\n   (just send me the invitation link like t.me/+code)\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_or_command": "✔ If you paste a valid link, I'll continue with Step 2 automatically.",
        
        # Guide
        "guide_title": "📖 <b>Usage Guide</b>\n\n",
        "guide_step_1": "🎯 <b>Step 1: Copy link</b>\n1️⃣ Open the message in Telegram\n2️⃣ Press and hold\n3️⃣ Tap Copy link\n\n",
        "guide_step_2": "🎯 <b>Step 2: Send here</b>\n4️⃣ Return to bot\n5️⃣ Paste the link\n6️⃣ Wait for your download\n\n",
        "guide_formats": "📋 <b>Valid formats:</b>\nPublic: t.me/channel/123\nPrivate: t.me/c/123456/789\n\n",
        "guide_tips": "💡 <b>Important:</b>\nThe link must include the message number\n\n",
        "guide_premium": "🔒 <b>Private Channels</b>\n\n",
        "guide_option_a": "1️⃣ Send invitation link\n",
        "guide_option_b": "2️⃣ Add the bot to channel\n\n",
        "guide_note": "📌 The bot needs access",
        
        # Plans
        "plans_title": "If you just want to test the bot, it works.\nBut if you really want to DOWNLOAD content non-stop... this is NOT enough.\n\n",
        "plans_free": "🚫 *FREE PLAN (LIMITED)*\n\n📸 Photos: 10 daily\n🎬 Videos: 3 total\n🎵 Music: ❌ Blocked\n📦 APK: ❌ Blocked\n\n",
        "plans_premium": "🔥💎 *PREMIUM PLAN — {price} ⭐*\n━━━━━━━━━━━━━━━━━━━━\n📸 Photos: Unlimited\n🎬 Videos: 50 per DAY\n🎵 Music: 50 per DAY\n📦 APK: 50 per DAY\n♻️ Auto-renewal every 24h\n⏳ Lasts 30 full days\n\n",
        "plans_benefits": "🚀 *WHY PREMIUM IS UNSTOPPABLE?*\n✔ Download EVERYTHING: videos, music, APK, photos\n✔ 50 daily downloads per category\n✔ Unrestricted access\n✔ Improved speed\n✔ Ideal for private channels, frequent content or large downloads\n✔ The bot works at MAXIMUM for you\n\n",
        "plans_warning": "⚠️ *Don't stay limited*\nEvery day you stay on Free → You lose downloads, time and content you could save.\n\n",
        "plans_payment": "⭐ *Upgrade to Premium with Telegram Stars*\nTap the button below and unleash ALL the bot's power.",
        "plans_imparable": "💎 *BE UNSTOPPABLE WITH PREMIUM!*",
        "btn_get_premium": "💎 Get Premium",
        "btn_back_start": "🏠 Back to start",
        
        # Premium purchase
        "premium_payment_title": "💎 Premium - 30 days",
        "premium_payment_description": "Full access for 30 days",
        "premium_activated": "🎉 *Premium Activated*\n\n━━━━━━━━━━━━━━━━━━━━\n\n✅ Payment received successfully\n💎 Premium subscription activated\n\n📅 Valid until: {expiry}\n⏰ Duration: 30 days\n\n━━━━━━━━━━━━━━━━━━━━\n\n🚀 Use /start to begin",
        "invoice_sent": "✅ *Invoice sent*\n\nCheck the payment message that appeared above.\n💳 Complete the payment to activate Premium.",
        "payment_not_configured": "⚠️ *Payment System in Configuration*\n\nThe bot doesn't have Telegram Stars enabled yet.\n\n━━━━━━━━━━━━━━━━━━━━\n\n📋 *For the administrator:*\n1. Open @BotFather\n2. Use /mybots\n3. Select this bot\n4. Tap 'Payments'\n5. Enable 'Telegram Stars'\n\n━━━━━━━━━━━━━━━━━━━━\n\n💡 Meanwhile, enjoy:\n• 3 free videos\n• Unlimited photos\n\n📢 Follow us: @observer_bots",
        "payment_error": "❌ *Temporary Error*\n\nCouldn't process the payment.\nTry again in a few moments.\n\n📢 Support: @observer_bots\n\n🔧 Error: `{error}`",
        
        # Errors
        "error_invalid_link": "❌ *Invalid link*\n\n",
        "error_invalid_format": "The link must be from Telegram:\n• Public channels: t.me/channel/123\n• Private channels: t.me/c/123456/789\n\n💡 Tap the specific message → Copy link",
        "error_message_not_found": "❌ *Message Not Found*\n\n",
        "error_message_reasons": "I couldn't find this message in the channel.\n\n🔍 *Possible reasons:*\n• The message was deleted\n• The link is incorrect\n• The channel doesn't exist\n\n💡 Check the link and send it again.",
        "error_no_media": "❌ *No Content*\n\n",
        "error_no_media_desc": "This message has no files to download.\n\n💡 Make sure to copy the link from a message with:\n📸 Photos\n🎬 Videos\n🎵 Music\n📦 Files",
        "error_private_channel": "🔒 *Private Channel - Access Required*\n\n",
        "error_private_need_access": "To download from this private channel I need you to add me.\n\n*🌟 2 Options:*\n\nOption 1 → Send me an invitation link (starts with t.me/+)\nOption 2 → Add me manually to the channel with my account {username}",
        
        # Limits
        "limit_free_videos": "🚫 *Limit Reached*\n\n",
        "limit_free_videos_desc": "You've used your {count}/{limit} video downloads.\n\n💎 *Solutions:*\n\n1️⃣ Download photos (unlimited)\n2️⃣ Upgrade to Premium for 50 daily videos\n\n✅ Tap the button to see plans!",
        "limit_free_photos": "⚠️ *Daily Photo Limit*\n\n",
        "limit_free_photos_desc": "You've downloaded {count}/{limit} photos today.\n\n♻️ Your limit resets in 24 hours.\n\n💎 *Want more?*\nWith Premium you get unlimited photos + 50 daily videos",
        "limit_premium_videos": "⚠️ *Daily Limit Reached*\n\n",
        "limit_premium_videos_desc": "You've downloaded {count}/{limit} videos today.\n\n♻️ Your limit resets in 24 hours.\n\n💡 While you wait you can download:\n✨ Photos: Unlimited\n🎵 Music: {music}/{music_limit}\n📦 APK: {apk}/{apk_limit}",
        "limit_music_blocked": "🚫 *Music Blocked*\n\n",
        "limit_music_blocked_desc": "Music download requires Premium.\n\n💎 *With Premium you get:*\n\n🎵 50 daily music downloads\n🎬 50 daily videos\n✨ Unlimited photos\n📦 50 daily APK",
        "limit_apk_blocked": "🚫 *APK Blocked*\n\n",
        "limit_apk_blocked_desc": "APK download requires Premium.\n\n💎 *With Premium you get:*\n\n📦 50 daily APK downloads\n🎬 50 daily videos\n✨ Unlimited photos\n🎵 50 daily music",
        
        # Download status
        "status_processing": "🔄 Processing...",
        "status_detecting_album": "🔍 Detecting album...",
        "status_album_detected": "📸 Album detected: {count} files\n⏳ Preparing download...",
        "status_sending": "📤 Sending...",
        "status_sending_progress": "📤 Sending {current}/{total}...",
        "status_downloading": "📥 Downloading...",
        "status_downloading_progress": "📥 Downloading {current}/{total}...",
        
        # Success messages
        "success_download": "✅ *Download Completed*\n\n",
        "success_album": "📸 Album of {count} files downloaded\n\n",
        "success_photos_unlimited": "📸 Unlimited photos with Premium ✨",
        "success_photos_daily": "📸 Photos today: {count}/{limit}\n♻️ Resets in 24h\n\n💎 /premium for unlimited photos",
        "success_videos_premium": "📊 Videos today: {count}/{limit}\n♻️ Resets in 24h",
        "success_videos_free": "📊 Videos used: {count}/{limit}\n🎁 Remaining: *{remaining}* downloads\n\n💎 /premium for 50 daily videos",
        "success_music": "🎵 Music today: {count}/{limit}\n♻️ Resets in 24h",
        "success_apk": "📦 APK today: {count}/{limit}\n♻️ Resets in 24h",
        "success_auto_joined": "\n\n🔗 Channel joined automatically",
        
        # Panel
        "panel_title": "⚙️ *Control Panel*\n\n",
        "panel_plan_free": "👤 *Plan:* Free\n",
        "panel_plan_premium": "💎 *Plan:* Premium\n",
        "panel_expires": "📅 *Expires:* {expiry} ({days_left} days)\n",
        "panel_stats_row": "📊 *Your Stats:*\n",
        "panel_photos": "• Photos: {count}/{limit}\n",
        "panel_videos": "• Videos: {count}/{limit}\n",
        "panel_music": "• Music: {count}/{limit}\n",
        "panel_apk": "• APK: {count}/{limit}\n",
        "panel_connection_title": "\n🔌 *Connection Status:*\n",
        "panel_connection_ok": "✅ *Bot:* Online & Connected\n",
        "panel_connection_fail": "⚠️ *Bot:* Connection Issues\n",
        "panel_footer": "\n💡 *Tip:* Upgrade to Premium for higher limits!",
        
        # Stats
        "stats_title": "📊 *Your Statistics*\n\n",
        "stats_plan": "💎 *Plan:* {plan}\n",
        "stats_expires": "📅 *Expires:* {expiry}\n",
        "stats_downloads": "📥 *Total downloads:* {count}\n",
        "stats_daily": "📊 *Daily usage:*\n",
        "stats_photos": "• Photos: {count}/{limit}\n",
        "stats_videos": "• Videos: {count}/{limit}\n",
        "stats_music": "• Music: {count}/{limit}\n",
        "stats_apk": "• APK: {count}/{limit}\n",
        "stats_reset": "\n♻️ *Resets:* In 24 hours",
        "btn_refresh_stats": "🔄 Refresh Stats",
        
        # Admin stats
        "admin_stats_title": "👑 *Administration Panel*\n\n",
        "admin_global_stats": "🌍 *Global Statistics*\n\n",
        "admin_total_users": "👥 *Total Users:* `{count}`\n",
        "admin_premium_users": "💎 *Premium Users:* `{count}`\n",
        "admin_free_users": "🆓 *Free Users:* `{count}`\n",
        "admin_total_downloads": "📊 *Total Historic:* `{count:,}`\n\n",
        "admin_activity": "📈 *Activity:*\n",
        "admin_active_today": "• Today: `{count}` users\n",
        "admin_active_week": "• This week: `{count}` users\n",
        "admin_avg_downloads": "📥 *Average Downloads/User:* `{avg:.1f}`\n",
        "admin_revenue": "💰 *Revenue (Stars):* `{stars:,}` ⭐\n\n",
        "admin_top_users": "🏆 *Top Users:*\n",
        
        # Login/Account Setup
        "login_already_active": "✅ *You already have an active session*\n\nIf you want to change accounts, use /logout first.",
        "login_setup_title": "🔐 *Account Setup*\n\nTo download content without restrictions and avoid bans, you need to log in with your own Telegram account.\n\n📱 *Step 1:* Send me your phone number in international format.\nExample: `+1234567890`",
        "login_invalid_phone": "❌ *Invalid format*\n\nThe number must include the country code and start with +.\nExample: `+1234567890`\n\nTry again:",
        "login_connecting": "🔄 Connecting to Telegram...",
        "login_code_sent": "📩 *Code sent*\n\nCheck your Telegram messages (not SMS).\n\n⚠️ *IMPORTANT:*\nTelegram blocks the code if you send it as is.\nPlease send it with spaces or dashes between numbers.\n\nExample: If the code is `12345`, send `1 2 3 4 5` or `12-345`.",
        "login_error_connect": "❌ *Connection error*\n\n`{error}`\n\nTry again with /configurar",
        "login_session_expired": "❌ Session expired. Use /configurar again.",
        "login_verifying_code": "🔄 Verifying code...",
        "login_2fa_required": "🔐 *Two-Step Verification*\n\nYour account has two-factor authentication (2FA).\nPlease send me your password to continue.",
        "login_success": "✅ *Setup Successful!*\n\nYour account has been linked successfully.\nNow the bot will use your own account for downloads, reducing ban risk and improving speed.\n\n🚀 You can now download content!",
        "login_wrong_code": "❌ *Wrong Code*\n\nThe code is invalid. Try again.\n\n💡 Remember: send the code with spaces or dashes.\nExample: `1 2 3 4 5` or `12-345`",
        "login_wrong_password": "❌ *Wrong Password*\n\nThe 2FA password is incorrect.\nTry again:",
        "login_cancelled": "❌ Process cancelled.\nUse /configurar when you want to try again.",
        "logout_success": "✅ *Session Closed*\n\nYour account has been unlinked.\nUse /configurar to link an account again.",
        "logout_no_session": "ℹ️ There is no active session.",
        "btn_cancel_login": "❌ Cancel",
        "btn_back_menu": "◀️ Back to menu",
    },
    "pt": {
        # Start command
        "start_welcome": "📥 BOT DE DOWNLOADS\n\n",
        "start_description": "Baixe fotos e vídeos do Telegram, incluindo canais privados e restritos.\n\n",
        "start_divider": "🔐 Para acessar conteúdo privado, o bot usa sua conta\napenas para baixar o conteúdo que você vê no Telegram.\nNão lê chats, não envia mensagens nem modifica sua conta.\n\n",
        "start_how_to": "🚀 *Como usar:*\n1️⃣ Copie o link da mensagem\n2️⃣ Cole aqui e envie\n\n",
        "start_example": "💡 *Exemplo:*\n`https://t.me/canal/123`\n\n",
        "start_premium_active": "💎 *Status:* Você é Premium (Sem limites)\n\n",
        "start_premium_plan": "💎 *Status:* Você é Premium\n📅 Expira: {expiry} ({days_left} dias)\n\n",
        "start_premium_usage": "",
        "start_premium_permanent": "💎 *Status:* Premium Permanente\n\n",
        "start_usage": "",
        "start_photos_unlimited": "",
        "start_videos_count": "",
        "start_music_count": "",
        "start_apk_count": "",
        "start_renew": "",
        "start_free_plan": "👤 *Status:* Plano Gratuito\n(Você tem um limite diário de downloads)\n\n",
        "start_photos_daily": "",
        "start_videos_total": "",
        "start_blocked": "",
        "start_upgrade": "⭐ *Quer baixar sem limites?*\nUse o botão 'Planos' abaixo.",
        "start_use_buttons": "",
        "start_cta": "",
        
        # Panel
        "panel_title": "⚙️ *PAINEL DE CONTROLE*\n👤 *Usuário:* {user_name}\n\n",
        "panel_plan_free": "👤 *Plano:* Gratuito\n",
        "panel_plan_premium": "💎 *Plano:* Premium\n📅 *Expira:* {expiry} ({days_left} dias)\n",
        "panel_expires": "",
        "panel_photos": "📸 Fotos: {count}/{limit}\n",
        "panel_videos": "🎬 Vídeos: {count}/{limit}\n",
        "panel_music": "🎵 Música: {count}/{limit}\n",
        "panel_apk": "📦 APK: {count}/{limit}\n",
        "panel_stats_title": "\n📊 *Seus Downloads de Hoje:*\n",
        "panel_stats_row": "",
        "panel_stats_unlimited": "{icon} {label}: Ilimitado ✨\n",
        "panel_connection_title": "\n🔐 *Status de Conexão:*\n",
        "panel_connected": "✅ Conectado ao Telegram",
        "panel_connection_ok": "✅ Conectado ao Telegram\n_(Você pode baixar de canais privados)_\n",
        "panel_disconnected": "❌ Não conectado",
        "panel_connection_fail": "❌ Não conectado\n_(Conecte sua conta para canais privados)_\n",
        "panel_desc_connected": "_(Você pode baixar de canais privados)_\n\n",
        "panel_desc_disconnected": "_(Conecte sua conta para canais privados)_\n\n",
        "panel_footer": "Melhore para Premium para downloads ilimitados\n",
        "btn_panel": "📥 Começar a Baixar",
        "btn_connect": "🔐 Conectar Conta",
        "btn_disconnect": "👋 Desconectar",
        "btn_renew": "💎 Renovar Premium",
        "btn_upgrade": "💎 Melhorar para Premium",
        
        # Buttons
        "btn_download_now": "📥 Começar a Baixar",
        "btn_how_to_use": "❓ Ajuda",
        "btn_plans": "💎 Ver Planos",
        "btn_my_stats": "📊 Minhas estatísticas",
        "btn_change_language": "🌐 Idioma / Language",
        "btn_support": "💬 Suporte",
        "btn_official_channel": "📢 Canal Oficial",
        "btn_pay_stars": "⭐ Pagar com Estrelas",
        "btn_join_channel": "📢 Entre no Canal Oficial",
        
        # Language selection
        "language_select": "🌐 *Selecione seu idioma*\n\nEscolha o idioma que você prefere usar:",
        "language_changed": "✅ Idioma alterado para Português",
        "btn_spanish": "🇪🇸 Español",
        "btn_english": "🇺🇸 English",
        "btn_portuguese": "🇧🇷 Português",
        "btn_italian": "🇮🇹 Italiano",
        
        # Download flow
        "download_greeting": "🎯 Vamos baixar seu conteúdo\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_step_1": "📋 Passo 1 de 2\n📎 Envie-me o LINK da mensagem que você quer baixar.\n\nO que é \"o link\"?\n➡️ É o endereço da mensagem, algo assim:\nhttps://t.me/canal/123\n\nComo copiar (muito fácil):\n1) Abra a mensagem no Telegram\n2) Pressione e segure → \"Copiar link\"\n3) Volte aqui e cole\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_example": "",
        "download_supported": "🔓 De onde posso baixar?\n• Canais públicos\n• Grupos públicos\n• Canais privados\n   → Se for privado, preciso que me convide\n   (apenas envie o link de convite tipo t.me/+codigo)\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_or_command": "✔ Se você colar um link válido, continuarei com o Passo 2 automaticamente.",
        
        # Guide
        "guide_title": "📥 BOT DE DOWNLOADS — GUIA DE USO\n\n",
        "guide_step_1": "🔐 <b>Passo 0: Conectar sua conta (apenas uma vez)</b>\nPara poder baixar conteúdo de canais privados ou restritos, o bot precisa usar sua conta apenas para acessar o conteúdo que você vê no Telegram.\n\n• Não lê chats pessoais\n• Não envia mensagens\n• Não modifica sua conta\n\nQuando o bot precisar, pedirá acesso e guiará você passo a passo.\n\n",
        "guide_step_2": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Passo 1: Copiar o link da mensagem</b>\n1️⃣ Abra no Telegram a mensagem que você quer baixar\n2️⃣ Pressione e segure a mensagem\n3️⃣ Toque em \"Copiar link\"\n\n",
        "guide_formats": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Passo 2: Enviar o link ao bot</b>\n4️⃣ Volte a este chat\n5️⃣ Cole o link\n6️⃣ Envie e espere o download\n\n",
        "guide_tips": "",
        "guide_premium": "",
        "guide_option_a": "",
        "guide_option_b": "",
        "guide_note": "",
        
        # Plans
        "plans_title": "Se você só quer testar o bot, funciona.\nMas se você realmente quer BAIXAR conteúdo sem parar... isso NÃO é suficiente.\n\n",
        "plans_free": "🚫 *PLANO GRÁTIS (LIMITADO)*\n\n📸 Fotos: 10 diárias\n🎬 Vídeos: 3 totais\n🎵 Música: ❌ Bloqueado\n📦 APK: ❌ Bloqueado\n\n",
        "plans_premium": "🔥💎 *PLANO PREMIUM — {price} ⭐*\n━━━━━━━━━━━━━━━━━━━━\n📸 Fotos: Ilimitadas\n🎬 Vídeos: 50 por DIA\n🎵 Música: 50 por DIA\n📦 APK: 50 por DIA\n♻️ Renovação automática a cada 24h\n⏳ Dura 30 dias completos\n\n",
        "plans_benefits": "🚀 *POR QUE O PREMIUM É IMPARÁVEL?*\n✔ Baixe TUDO: vídeos, música, APK, fotos\n✔ 50 downloads diários por categoria\n✔ Acesso sem restrições\n✔ Velocidade melhorada\n✔ Ideal para canais privados, conteúdo frequente ou downloads grandes\n✔ O bot trabalha NO MÁXIMO para você\n\n",
        "plans_warning": "⚠️ *Não fique limitado*\nCada dia que você fica no Grátis → Você perde downloads, tempo e conteúdo que poderia salvar.\n\n",
        "plans_payment": "⭐ *Suba para Premium com Telegram Stars*\nToque no botão abaixo e libere TODO o poder do bot.",
        "plans_imparable": "💎 *SEJA IMPARÁVEL COM PREMIUM!*",
        "btn_get_premium": "💎 Obter Premium",
        "btn_back_start": "🏠 Voltar ao início",
        
        # Premium purchase
        "premium_payment_title": "💎 Premium - 30 dias",
        "premium_payment_description": "Acesso completo por 30 dias",
        "premium_activated": "🎉 *Premium Ativado*\n\n━━━━━━━━━━━━━━━━━━━━\n\n✅ Pagamento recebido com sucesso\n💎 Assinatura Premium ativada\n\n📅 Válido até: {expiry}\n⏰ Duração: 30 dias\n\n━━━━━━━━━━━━━━━━━━━━\n\n🚀 Use /start para começar",
        "invoice_sent": "✅ *Fatura enviada*\n\nVerifique a mensagem de pagamento que apareceu acima.\n💳 Complete o pagamento para ativar o Premium.",
        "payment_not_configured": "⚠️ *Sistema de Pagamentos em Configuração*\n\nO bot ainda não tem Telegram Stars habilitado.\n\n━━━━━━━━━━━━━━━━━━━━\n\n📋 *Para o administrador:*\n1. Abra @BotFather\n2. Use /mybots\n3. Selecione este bot\n4. Toque em 'Payments'\n5. Habilite 'Telegram Stars'\n\n━━━━━━━━━━━━━━━━━━━━\n\n💡 Enquanto isso, aproveite:\n• 3 vídeos grátis\n• Fotos ilimitadas\n\n📢 Siga-nos: @observer_bots",
        "payment_error": "❌ *Erro Temporário*\n\nNão foi possível processar o pagamento.\nTente novamente em alguns momentos.\n\n📢 Suporte: @observer_bots\n\n🔧 Erro: `{error}`",
        
        # Errors
        "error_invalid_link": "❌ *Link inválido*\n\n",
        "error_invalid_format": "O link deve ser do Telegram:\n• Canais públicos: t.me/canal/123\n• Canais privados: t.me/c/123456/789\n\n💡 Toque na mensagem específica → Copiar link",
        "error_message_not_found": "❌ *Mensagem Não Encontrada*\n\n",
        "error_message_reasons": "Não consegui encontrar esta mensagem no canal.\n\n🔍 *Possíveis razões:*\n• A mensagem foi deletada\n• O link está incorreto\n• O canal não existe\n\n💡 Verifique o link e envie-o novamente.",
        "error_no_media": "❌ *Sem Conteúdo*\n\n",
        "error_no_media_desc": "Esta mensagem não tem arquivos para baixar.\n\n💡 Certifique-se de copiar o link de uma mensagem com:\n📸 Fotos\n🎬 Vídeos\n🎵 Música\n📦 Arquivos",
        "error_private_channel": "🔒 *Canal Privado - Acesso Necessário*\n\n",
        "error_private_need_access": "Para baixar deste canal privado preciso que você me adicione.\n\n*🌟 2 Opções:*\n\nOpção 1 → Envie-me um link de convite (começa com t.me/+)\nOpção 2 → Adicione-me manualmente ao canal com minha conta {username}",
        
        # Limits
        "limit_free_videos": "🚫 *Limite Atingido*\n\n",
        "limit_free_videos_desc": "Você usou seus {count}/{limit} downloads de vídeo.\n\n💎 *Soluções:*\n\n1️⃣ Baixe fotos (ilimitadas)\n2️⃣ Melhore para Premium para 50 vídeos diários\n\nToque no botão para ver os planos!",
        "limit_free_photos": "⚠️ *Limite Diário de Fotos*\n\n",
        "limit_free_photos_desc": "Você baixou {count}/{limit} fotos hoje.\n\n♻️ Seu limite reseta em 24 horas.\n\n💎 *Quer mais?*\nCom Premium você tem fotos ilimitadas + 50 vídeos diários",
        "limit_premium_videos": "⚠️ *Limite Diário Atingido*\n\n",
        "limit_premium_videos_desc": "Você baixou {count}/{limit} vídeos hoje.\n\n♻️ Seu limite reseta em 24 horas.\n\n💡 Enquanto espera você pode baixar:\n✨ Fotos: Ilimitadas\n🎵 Música: {music}/{music_limit}\n📦 APK: {apk}/{apk_limit}",
        "limit_music_blocked": "🚫 *Música Bloqueada*\n\n",
        "limit_music_blocked_desc": "O download de música requer Premium.\n\n💎 *Com Premium você obtém:*\n\n🎵 50 downloads de música diários\n🎬 50 vídeos diários\n✨ Fotos ilimitadas\n📦 50 APK diários",
        "limit_apk_blocked": "🚫 *APK Bloqueado*\n\n",
        "limit_apk_blocked_desc": "O download de APK requer Premium.\n\n💎 *Com Premium você obtém:*\n\n📦 50 downloads de APK diários\n🎬 50 vídeos diários\n✨ Fotos ilimitadas\n🎵 50 música diários",
        
        # Download status
        "status_processing": "🔄 Processando...",
        "status_detecting_album": "🔍 Detectando álbum...",
        "status_album_detected": "📸 Álbum detectado: {count} arquivos\n⏳ Preparando download...",
        "status_sending": "📤 Enviando...",
        "status_sending_progress": "📤 Enviando {current}/{total}...",
        "status_downloading": "📥 Baixando...",
        "status_downloading_progress": "📥 Baixando {current}/{total}...",
        
        # Success messages
        "success_download": "✅ *Download Concluído*\n\n",
        "success_album": "📸 Álbum de {count} arquivos baixado\n\n",
        "success_photos_unlimited": "📸 Fotos ilimitadas com Premium ✨",
        "success_photos_daily": "📸 Fotos hoje: {count}/{limit}\n♻️ Reseta em 24h\n\n💎 /premium para fotos ilimitadas",
        "success_videos_premium": "📊 Vídeos hoje: {count}/{limit}\n♻️ Reseta em 24h",
        "success_videos_free": "📊 Vídeos usados: {count}/{limit}\n🎁 Restam: *{remaining}* downloads\n\n💎 /premium para 50 vídeos diários",
        "success_music": "🎵 Música hoje: {count}/{limit}\n♻️ Reseta em 24h",
        "success_apk": "📦 APK hoje: {count}/{limit}\n♻️ Reseta em 24h",
        "success_auto_joined": "\n\n🔗 Canal entrou automaticamente",
        
        # Stats
        "stats_title": "📊 *Suas Estatísticas*\n\n",
        "stats_plan": "💎 *Plano:* {plan}\n",
        "stats_expires": "📅 *Expira:* {expiry}\n",
        "stats_downloads": "📥 *Downloads totais:* {count}\n",
        "stats_daily": "📊 *Uso diário:*\n",
        "stats_photos": "• Fotos: {count}/{limit}\n",
        "stats_videos": "• Vídeos: {count}/{limit}\n",
        "stats_music": "• Música: {count}/{limit}\n",
        "stats_apk": "• APK: {count}/{limit}\n",
        "stats_reset": "\n♻️ *Reseta:* Em 24 horas",
        "btn_refresh_stats": "🔄 Atualizar Stats",
        
        # Admin stats
        "admin_stats_title": "👑 *Painel de Administração*\n\n",
        "admin_global_stats": "🌍 *Estatísticas Globais*\n\n",
        "admin_total_users": "👥 *Total Usuários:* `{count}`\n",
        "admin_premium_users": "💎 *Usuários Premium:* `{count}`\n",
        "admin_free_users": "🆓 *Usuários Grátis:* `{count}`\n",
        "admin_total_downloads": "📊 *Total Histórico:* `{count:,}`\n\n",
        "admin_activity": "📈 *Atividade:*\n",
        "admin_active_today": "• Hoje: `{count}` usuários\n",
        "admin_active_week": "• Esta semana: `{count}` usuários\n",
        "admin_avg_downloads": "📥 *Média Downloads/Usuário:* `{avg:.1f}`\n",
        "admin_revenue": "💰 *Receita (Stars):* `{stars:,}` ⭐\n\n",
        "admin_top_users": "🏆 *Top Usuários:*\n",
        
        # Login/Account Setup
        "login_already_active": "✅ *Você já tem uma sessão ativa*\n\nSe quiser mudar de conta, use /logout primeiro.",
        "login_setup_title": "🔐 *Configuração de Conta*\n\nPara baixar conteúdo sem restrições e evitar banimentos, você precisa fazer login com sua própria conta do Telegram.\n\n📱 *Passo 1:* Envie-me seu número de telefone em formato internacional.\nExemplo: `+5511999999999`",
        "login_invalid_phone": "❌ *Formato inválido*\n\nO número deve incluir o código do país e começar com +.\nExemplo: `+5511999999999`\n\nTente novamente:",
        "login_connecting": "🔄 Conectando ao Telegram...",
        "login_code_sent": "📩 *Código enviado*\n\nVerifique suas mensagens do Telegram (não SMS).\n\n⚠️ *IMPORTANTE:*\nO Telegram bloqueia o código se você enviá-lo como está.\nPor favor, envie-o com espaços ou hífens entre os números.\n\nExemplo: Se o código for `12345`, envie `1 2 3 4 5` ou `12-345`.",
        "login_error_connect": "❌ *Erro de conexão*\n\n`{error}`\n\nTente novamente com /configurar",
        "login_session_expired": "❌ Sessão expirada. Use /configurar novamente.",
        "login_verifying_code": "🔄 Verificando código...",
        "login_2fa_required": "🔐 *Verificação em Duas Etapas*\n\nSua conta tem autenticação de dois fatores (2FA).\nPor favor, envie-me sua senha para continuar.",
        "login_success": "✅ *Configuração Concluída!*\n\nSua conta foi vinculada com sucesso.\nAgora o bot usará sua própria conta para downloads, reduzindo o risco de banimento e melhorando a velocidade.\n\n🚀 Você já pode baixar conteúdo!",
        "login_wrong_code": "❌ *Código Errado*\n\nO código é inválido. Tente novamente.\n\n💡 Lembre-se: envie o código com espaços ou hífens.\nExemplo: `1 2 3 4 5` ou `12-345`",
        "login_wrong_password": "❌ *Senha Incorreta*\n\nA senha 2FA está incorreta.\nTente novamente:",
        "login_cancelled": "❌ Processo cancelado.\nUse /configurar quando quiser tentar novamente.",
        "logout_success": "✅ *Sessão Encerrada*\n\nSua conta foi desvinculada.\nUse /configurar para vincular uma conta novamente.",
        "logout_no_session": "ℹ️ Não há sessão ativa.",
        "btn_cancel_login": "❌ Cancelar",
        "btn_back_menu": "◀️ Voltar ao menu",
    },
    "it": {
        # Start command
        "start_welcome": "📥 BOT DI DOWNLOAD\n\n",
        "start_description": "Scarica foto e video da Telegram, inclusi canali privati e ristretti.\n\n",
        "start_divider": "🔐 Per accedere ai contenuti privati, il bot usa il tuo account\nsolo per scaricare i contenuti che vedi su Telegram.\nNon legge chat, non invia messaggi né modifica il tuo account.\n\n",
        "start_how_to": "🚀 *Come usarlo:*\n1️⃣ Copia il link del messaggio\n2️⃣ Incollalo qui e invialo\n\n",
        "start_example": "💡 *Esempio:*\n`https://t.me/canale/123`\n\n",
        "start_premium_active": "💎 *Stato:* Sei Premium (Senza limiti)\n\n",
        "start_premium_plan": "💎 *Stato:* Sei Premium\n📅 Scade: {expiry} ({days_left} giorni)\n\n",
        "start_premium_usage": "",
        "start_premium_permanent": "💎 *Stato:* Premium Permanente\n\n",
        "start_usage": "",
        "start_photos_unlimited": "",
        "start_videos_count": "",
        "start_music_count": "",
        "start_apk_count": "",
        "start_renew": "",
        "start_free_plan": "👤 *Stato:* Piano Gratuito\n(Hai un limite giornaliero di download)\n\n",
        "start_photos_daily": "",
        "start_videos_total": "",
        "start_blocked": "",
        "start_upgrade": "⭐ *Vuoi scaricare senza limiti?*\nUsa il pulsante 'Piani' qui sotto.",
        "start_use_buttons": "",
        "start_cta": "",
        
        # Panel
        "panel_title": "⚙️ *PANNELLO DI CONTROLLO*\n👤 *Utente:* {user_name}\n\n",
        "panel_plan_free": "👤 *Piano:* Gratuito\n",
        "panel_plan_premium": "💎 *Piano:* Premium\n📅 *Scade:* {expiry} ({days_left} giorni)\n",
        "panel_expires": "",
        "panel_photos": "📸 Foto: {count}/{limit}\n",
        "panel_videos": "🎬 Video: {count}/{limit}\n",
        "panel_music": "🎵 Musica: {count}/{limit}\n",
        "panel_apk": "📦 APK: {count}/{limit}\n",
        "panel_stats_title": "\n📊 *I Tuoi Download di Oggi:*\n",
        "panel_stats_row": "",
        "panel_stats_unlimited": "{icon} {label}: Illimitato ✨\n",
        "panel_connection_title": "\n🔐 *Stato Connessione:*\n",
        "panel_connected": "✅ Connesso a Telegram",
        "panel_connection_ok": "✅ Connesso a Telegram\n_(Puoi scaricare da canali privati)_\n",
        "panel_disconnected": "❌ Non connesso",
        "panel_connection_fail": "❌ Non connesso\n_(Connetti il tuo account per canali privati)_\n",
        "panel_desc_connected": "_(Puoi scaricare da canali privati)_\n\n",
        "panel_desc_disconnected": "_(Connetti il tuo account per canali privati)_\n\n",
        "panel_footer": "Passa a Premium per download illimitati\n",
        "btn_panel": "📥 Inizia a Scaricare",
        "btn_connect": "🔐 Connetti Account",
        "btn_disconnect": "👋 Disconnetti",
        "btn_renew": "💎 Rinnova Premium",
        "btn_upgrade": "💎 Passa a Premium",
        
        # Buttons
        "btn_download_now": "📥 Inizia a Scaricare",
        "btn_how_to_use": "❓ Aiuto",
        "btn_plans": "💎 Vedi Piani",
        "btn_my_stats": "📊 Le mie statistiche",
        "btn_change_language": "🌐 Lingua / Language",
        "btn_support": "💬 Supporto",
        "btn_official_channel": "📢 Canale Ufficiale",
        "btn_pay_stars": "⭐ Paga con Stelle",
        "btn_join_channel": "📢 Unisciti al Canale Ufficiale",
        
        # Language selection
        "language_select": "🌐 *Seleziona la tua lingua*\n\nScegli la lingua che preferisci usare:",
        "language_changed": "✅ Lingua cambiata in Italiano",
        "btn_spanish": "🇪🇸 Español",
        "btn_english": "🇺🇸 English",
        "btn_portuguese": "🇧🇷 Português",
        "btn_italian": "🇮🇹 Italiano",
        
        # Download flow
        "download_greeting": "🎯 Scarichiamo il tuo contenuto\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_step_1": "📋 Passo 1 di 2\n📎 Inviami il LINK del messaggio che vuoi scaricare.\n\nCos'è \"il link\"?\n➡️ È l'indirizzo del messaggio, qualcosa come:\nhttps://t.me/canale/123\n\nCome copiarlo (molto facile):\n1) Apri il messaggio su Telegram\n2) Tieni premuto → \"Copia link\"\n3) Torna qui e incollalo\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_example": "",
        "download_supported": "🔓 Da dove posso scaricare?\n• Canali pubblici\n• Gruppi pubblici\n• Canali privati\n   → Se è privato, ho bisogno che tu mi inviti\n   (inviami solo il link di invito tipo t.me/+codice)\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_or_command": "✔ Se incolli un link valido, continuerò con il Passo 2 automaticamente.",
        
        # Guide
        "guide_title": "📥 BOT DI DOWNLOAD — GUIDA ALL'USO\n\n",
        "guide_step_1": "🔐 <b>Passo 0: Connetti il tuo account (solo una volta)</b>\nPer poter scaricare contenuti da canali privati o ristretti, il bot ha bisogno di usare il tuo account solo per accedere ai contenuti che vedi su Telegram.\n\n• Non legge chat personali\n• Non invia messaggi\n• Non modifica il tuo account\n\nQuando il bot ne avrà bisogno, chiederà l'accesso e ti guiderà passo passo.\n\n",
        "guide_step_2": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Passo 1: Copia il link del messaggio</b>\n1️⃣ Apri su Telegram il messaggio che vuoi scaricare\n2️⃣ Tieni premuto il messaggio\n3️⃣ Tocca \"Copia link\"\n\n",
        "guide_formats": "━━━━━━━━━━━━━━━━━━━━━\n🎯 <b>Passo 2: Invia il link al bot</b>\n4️⃣ Torna a questa chat\n5️⃣ Incolla il link\n6️⃣ Invialo e aspetta il download\n\n",
        "guide_tips": "",
        "guide_premium": "",
        "guide_option_a": "",
        "guide_option_b": "",
        "guide_note": "",
        
        # Plans
        "plans_title": "Se vuoi solo provare il bot, funziona.\nMa se vuoi davvero SCARICARE contenuti senza sosta... questo NON basta.\n\n",
        "plans_free": "🚫 *PIANO GRATIS (LIMITATO)*\n\n📸 Foto: 10 giornaliere\n🎬 Video: 3 totali\n🎵 Musica: ❌ Bloccato\n📦 APK: ❌ Bloccato\n\n",
        "plans_premium": "🔥💎 *PIANO PREMIUM — {price} ⭐*\n━━━━━━━━━━━━━━━━━━━━\n📸 Foto: Illimitate\n🎬 Video: 50 al GIORNO\n🎵 Musica: 50 al GIORNO\n📦 APK: 50 al GIORNO\n♻️ Rinnovo automatico ogni 24h\n⏳ Dura 30 giorni completi\n\n",
        "plans_benefits": "🚀 *PERCHÉ PREMIUM È INARRESTABILE?*\n✔ Scarica TUTTO: video, musica, APK, foto\n✔ 50 download giornalieri per categoria\n✔ Accesso senza restrizioni\n✔ Velocità migliorata\n✔ Ideale per canali privati, contenuti frequenti o download grandi\n✔ Il bot lavora AL MASSIMO per te\n\n",
        "plans_warning": "⚠️ *Non restare limitato*\nOgni giorno che resti su Gratis → Perdi download, tempo e contenuti che potresti salvare.\n\n",
        "plans_payment": "⭐ *Passa a Premium con Telegram Stars*\nTocca il pulsante qui sotto e libera TUTTA la potenza del bot.",
        "plans_imparable": "💎 *SII INARRESTABILE CON PREMIUM!*",
        "btn_get_premium": "💎 Ottieni Premium",
        "btn_back_start": "🏠 Torna all'inizio",
        
        # Premium purchase
        "premium_payment_title": "💎 Premium - 30 giorni",
        "premium_payment_description": "Accesso completo per 30 giorni",
        "premium_activated": "🎉 *Premium Attivato*\n\n━━━━━━━━━━━━━━━━━━━━\n\n✅ Pagamento ricevuto con successo\n💎 Abbonamento Premium attivato\n\n📅 Valido fino: {expiry}\n⏰ Durata: 30 giorni\n\n━━━━━━━━━━━━━━━━━━━━\n\n🚀 Usa /start per iniziare",
        "invoice_sent": "✅ *Fattura inviata*\n\nControlla il messaggio di pagamento apparso sopra.\n💳 Completa il pagamento per attivare Premium.",
        "payment_not_configured": "⚠️ *Sistema di Pagamenti in Configurazione*\n\nIl bot non ha ancora Telegram Stars abilitato.\n\n━━━━━━━━━━━━━━━━━━━━\n\n📋 *Per l'amministratore:*\n1. Apri @BotFather\n2. Usa /mybots\n3. Seleziona questo bot\n4. Tocca 'Payments'\n5. Abilita 'Telegram Stars'\n\n━━━━━━━━━━━━━━━━━━━━\n\n💡 Nel frattempo, goditi:\n• 3 video gratis\n• Foto illimitate\n\n📢 Seguici: @observer_bots",
        "payment_error": "❌ *Errore Temporaneo*\n\nNon è stato possibile elaborare il pagamento.\nRiprova tra qualche momento.\n\n📢 Supporto: @observer_bots\n\n🔧 Errore: `{error}`",
        
        # Errors
        "error_invalid_link": "❌ *Link non valido*\n\n",
        "error_invalid_format": "Il link deve essere di Telegram:\n• Canali pubblici: t.me/canale/123\n• Canali privati: t.me/c/123456/789\n\n💡 Tocca il messaggio specifico → Copia link",
        "error_message_not_found": "❌ *Messaggio Non Trovato*\n\n",
        "error_message_reasons": "Non ho trovato questo messaggio nel canale.\n\n🔍 *Possibili motivi:*\n• Il messaggio è stato eliminato\n• Il link non è corretto\n• Il canale non esiste\n\n💡 Verifica il link e invialo di nuovo.",
        "error_no_media": "❌ *Nessun Contenuto*\n\n",
        "error_no_media_desc": "Questo messaggio non ha file da scaricare.\n\n💡 Assicurati di copiare il link da un messaggio con:\n📸 Foto\n🎬 Video\n🎵 Musica\n📦 File",
        "error_private_channel": "🔒 *Canale Privato - Accesso Necessario*\n\n",
        "error_private_need_access": "Per scaricare da questo canale privato ho bisogno che tu mi aggiunga.\n\n*🌟 2 Opzioni:*\n\nOpzione 1 → Inviami un link di invito (inizia con t.me/+)\nOpzione 2 → Aggiungimi manualmente al canale con il mio account {username}",
        
        # Limits
        "limit_free_videos": "🚫 *Limite Raggiunto*\n\n",
        "limit_free_videos_desc": "Hai usato i tuoi {count}/{limit} download di video.\n\n💎 *Soluzioni:*\n\n1️⃣ Scarica foto (illimitate)\n2️⃣ Passa a Premium per 50 video giornalieri\n\nTocca il pulsante per vedere i piani!",
        "limit_free_photos": "⚠️ *Limite Giornaliero Foto*\n\n",
        "limit_free_photos_desc": "Hai scaricato {count}/{limit} foto oggi.\n\n♻️ Il tuo limite si resetta in 24 ore.\n\n💎 *Vuoi di più?*\nCon Premium hai foto illimitate + 50 video giornalieri",
        "limit_premium_videos": "⚠️ *Limite Giornaliero Raggiunto*\n\n",
        "limit_premium_videos_desc": "Hai scaricato {count}/{limit} video oggi.\n\n♻️ Il tuo limite si resetta in 24 ore.\n\n💡 Mentre aspetti puoi scaricare:\n✨ Foto: Illimitate\n🎵 Musica: {music}/{music_limit}\n📦 APK: {apk}/{apk_limit}",
        "limit_music_blocked": "🚫 *Musica Bloccata*\n\n",
        "limit_music_blocked_desc": "Il download di musica richiede Premium.\n\n💎 *Con Premium ottieni:*\n\n🎵 50 download di musica giornalieri\n🎬 50 video giornalieri\n✨ Foto illimitate\n📦 50 APK giornalieri",
        "limit_apk_blocked": "🚫 *APK Bloccato*\n\n",
        "limit_apk_blocked_desc": "Il download di APK richiede Premium.\n\n💎 *Con Premium ottieni:*\n\n📦 50 download di APK giornalieri\n🎬 50 video giornalieri\n✨ Foto illimitate\n🎵 50 musica giornalieri",
        
        # Download status
        "status_processing": "🔄 Elaborazione...",
        "status_detecting_album": "🔍 Rilevamento album...",
        "status_album_detected": "📸 Album rilevato: {count} file\n⏳ Preparazione download...",
        "status_sending": "📤 Invio...",
        "status_sending_progress": "📤 Invio {current}/{total}...",
        "status_downloading": "📥 Scaricamento...",
        "status_downloading_progress": "📥 Scaricamento {current}/{total}...",
        
        # Success messages
        "success_download": "✅ *Download Completato*\n\n",
        "success_album": "📸 Album di {count} file scaricato\n\n",
        "success_photos_unlimited": "📸 Foto illimitate con Premium ✨",
        "success_photos_daily": "📸 Foto oggi: {count}/{limit}\n♻️ Si resetta in 24h\n\n💎 /premium per foto illimitate",
        "success_videos_premium": "📊 Video oggi: {count}/{limit}\n♻️ Si resetta in 24h",
        "success_videos_free": "📊 Video usati: {count}/{limit}\n🎁 Rimangono: *{remaining}* download\n\n💎 /premium per 50 video giornalieri",
        "success_music": "🎵 Musica oggi: {count}/{limit}\n♻️ Si resetta in 24h",
        "success_apk": "📦 APK oggi: {count}/{limit}\n♻️ Si resetta in 24h",
        "success_auto_joined": "\n\n🔗 Canale unito automaticamente",
        
        # Stats
        "stats_title": "📊 *Le Tue Statistiche*\n\n",
        "stats_plan": "💎 *Piano:* {plan}\n",
        "stats_expires": "📅 *Scade:* {expiry}\n",
        "stats_downloads": "📥 *Download totali:* {count}\n",
        "stats_daily": "📊 *Uso giornaliero:*\n",
        "stats_photos": "• Foto: {count}/{limit}\n",
        "stats_videos": "• Video: {count}/{limit}\n",
        "stats_music": "• Musica: {count}/{limit}\n",
        "stats_apk": "• APK: {count}/{limit}\n",
        "stats_reset": "\n♻️ *Si resetta:* Tra 24 ore",
        "btn_refresh_stats": "🔄 Aggiorna Stats",
        
        # Admin stats
        "admin_stats_title": "👑 *Pannello di Amministrazione*\n\n",
        "admin_global_stats": "🌍 *Statistiche Globali*\n\n",
        "admin_total_users": "👥 *Totale Utenti:* `{count}`\n",
        "admin_premium_users": "💎 *Utenti Premium:* `{count}`\n",
        "admin_free_users": "🆓 *Utenti Gratis:* `{count}`\n",
        "admin_total_downloads": "📊 *Totale Storico:* `{count:,}`\n\n",
        "admin_activity": "📈 *Attività:*\n",
        "admin_active_today": "• Oggi: `{count}` utenti\n",
        "admin_active_week": "• Questa settimana: `{count}` utenti\n",
        "admin_avg_downloads": "📥 *Media Download/Utente:* `{avg:.1f}`\n",
        "admin_revenue": "💰 *Entrate (Stars):* `{stars:,}` ⭐\n\n",
        "admin_top_users": "🏆 *Top Utenti:*\n",
        
        # Login/Account Setup
        "login_already_active": "✅ *Hai già una sessione attiva*\n\nSe vuoi cambiare account, usa prima /logout.",
        "login_setup_title": "🔐 *Configurazione Account*\n\nPer scaricare contenuti senza restrizioni ed evitare ban, devi accedere con il tuo account Telegram.\n\n📱 *Passo 1:* Inviami il tuo numero di telefono in formato internazionale.\nEsempio: `+39123456789`",
        "login_invalid_phone": "❌ *Formato non valido*\n\nIl numero deve includere il prefisso del paese e iniziare con +.\nEsempio: `+39123456789`\n\nRiprova:",
        "login_connecting": "🔄 Connessione a Telegram...",
        "login_code_sent": "📩 *Codice inviato*\n\nControlla i tuoi messaggi Telegram (non SMS).\n\n⚠️ *IMPORTANTE:*\nTelegram blocca il codice se lo invii così com'è.\nPer favore, invialo con spazi o trattini tra i numeri.\n\nEsempio: Se il codice è `12345`, invia `1 2 3 4 5` o `12-345`.",
        "login_error_connect": "❌ *Errore di connessione*\n\n`{error}`\n\nRiprova con /configurar",
        "login_session_expired": "❌ Sessione scaduta. Usa di nuovo /configurar.",
        "login_verifying_code": "🔄 Verifica codice...",
        "login_2fa_required": "🔐 *Verifica in Due Passaggi*\n\nIl tuo account ha l'autenticazione a due fattori (2FA).\nPer favore, inviami la tua password per continuare.",
        "login_success": "✅ *Configurazione Completata!*\n\nIl tuo account è stato collegato con successo.\nOra il bot userà il tuo account per i download, riducendo il rischio di ban e migliorando la velocità.\n\n🚀 Ora puoi scaricare contenuti!",
        "login_wrong_code": "❌ *Codice Errato*\n\nIl codice non è valido. Riprova.\n\n💡 Ricorda: invia il codice con spazi o trattini.\nEsempio: `1 2 3 4 5` o `12-345`",
        "login_wrong_password": "❌ *Password Errata*\n\nLa password 2FA non è corretta.\nRiprova:",
        "login_cancelled": "❌ Processo annullato.\nUsa /configurar quando vuoi riprovare.",
        "logout_success": "✅ *Sessione Chiusa*\n\nIl tuo account è stato scollegato.\nUsa /configurar per collegare di nuovo un account.",
        "logout_no_session": "ℹ️ Non c'è nessuna sessione attiva.",
        "btn_cancel_login": "❌ Annulla",
        "btn_back_menu": "◀️ Torna al menu",
    }
}


def get_msg(key, lang="es", **kwargs):
    """
    Get a message in the specified language
    
    Args:
        key: Message key
        lang: Language code ('es', 'en', 'pt', 'it')
        **kwargs: Format parameters for the message
    
    Returns:
        Formatted message string
    """
    try:
        # Fallback to Spanish if language not found
        if lang not in MESSAGES:
            lang = 'es'
        msg = MESSAGES[lang].get(key, MESSAGES["es"].get(key, f"[Missing: {key}]"))
        if kwargs:
            return msg.format(**kwargs)
        return msg
    except KeyError:
        return f"[Missing: {key}]"
    except Exception as e:
        return f"[Error formatting {key}: {e}]"


def get_user_language(user):
    """Get user's preferred language, defaulting to Spanish"""
    if user and isinstance(user, dict):
        lang = user.get('language', 'es')
        # Validate language code
        if lang not in ['es', 'en', 'pt', 'it']:
            return 'es'
        return lang
    return 'es'
