"""
Multi-language messages for Telegram Bot
Supports: Spanish (es) and English (en)
"""

MESSAGES = {
    "es": {
        # Start command
        "start_welcome": "👋 ¡Hola! Soy tu Bot de Descargas.\n\n",
        "start_description": "📥 *¿Qué puedo hacer por ti?*\nPuedo descargar fotos, videos, música y archivos de Telegram, incluso de canales restringidos.\n\n",
        "start_divider": "━━━━━━━━━━━━━━━━━━━━━\n",
        "start_how_to": "🚀 *¿Cómo empezar?*\nEs muy fácil, solo sigue estos pasos:\n\n1️⃣ Ve al mensaje que quieres descargar en Telegram.\n2️⃣ Copia el enlace del mensaje.\n3️⃣ Pégalo aquí y envíalo.\n\n",
        "start_example": "💡 *Ejemplo de enlace:*\n`https://t.me/canal/123`\n\n",
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
        "panel_title": "⚙️ *Panel de Control*\n\n👤 *Usuario:* {user_name}\n\n",
        "panel_connected": "✅ Conectado",
        "panel_disconnected": "❌ No conectado",
        "panel_desc_connected": "✅ *Tu cuenta está conectada*\n\nAhora puedes descargar contenido de canales privados y restringidos sin problemas.\n\n",
        "panel_desc_disconnected": "⚠️ *Cuenta no conectada*\n\nPara descargar de canales privados o restringidos, necesitas conectar tu cuenta.\n\n",
        "btn_panel": "⚙️ Mi Cuenta",
        "btn_connect": "🔐 Conectar Cuenta",
        "btn_disconnect": "👋 Desconectar",
        
        # Buttons
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
        
        # Download flow
        "download_greeting": "🎯 Vamos a descargar tu contenido\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_step_1": "📋 Paso 1 de 2\n📎 Envíame el ENLACE del mensaje que quieres descargar.\n\n¿Qué es \"el enlace\"?\n➡️ Es la dirección del mensaje, algo así como:\nhttps://t.me/canal/123\n\nCómo copiarlo (muy fácil):\n1) Abre el mensaje en Telegram\n2) Mantén el dedo encima → \"Copiar enlace\"\n3) Vuelve aquí y pégalo\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_example": "",
        "download_supported": "🔓 ¿De dónde puedo descargar?\n• Canales públicos\n• Grupos públicos\n• Canales privados\n   → Si es privado, necesito que me invites\n   (solo envíame el enlace de invitación tipo t.me/+codigo)\n\n━━━━━━━━━━━━━━━━━━━━\n\n",
        "download_or_command": "✔ Si pegas un enlace válido, seguiré con el Paso 2 automáticamente.",
        
        # Guide
        "guide_title": "📖 <b>Guía de Uso</b>\n\n",
        "guide_step_1": "🎯 <b>Paso 1: Copiar enlace</b>\n1️⃣ Abre el mensaje en Telegram\n2️⃣ Mantén presionado\n3️⃣ Toca Copiar enlace\n\n",
        "guide_step_2": "🎯 <b>Paso 2: Enviar aquí</b>\n4️⃣ Vuelve al bot\n5️⃣ Pega el enlace\n6️⃣ Espera tu descarga\n\n",
        "guide_formats": "📋 <b>Formatos válidos:</b>\nPúblico: t.me/canal/123\nPrivado: t.me/c/123456/789\n\n",
        "guide_tips": "💡 <b>Importante:</b>\nEl enlace debe incluir el número del mensaje\n\n",
        "guide_premium": "🔒 <b>Canales Privados</b>\n\n",
        "guide_option_a": "1️⃣ Envia enlace de invitacion\n",
        "guide_option_b": "2️⃣ Agrega el bot al canal\n\n",
        "guide_note": "📌 El bot necesita acceso",
        
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
        "btn_download_now": "🎯 Download Now",
        "btn_how_to_use": "❓ How to use",
        "btn_plans": "💎 Plans",
        "btn_my_stats": "📊 My statistics",
        "btn_change_language": "🌐 Change language",
        "btn_support": "💬 Support",
        "btn_official_channel": "📢 Official Channel",
        "btn_pay_stars": "⭐ Pay with Stars",
        "btn_join_channel": "📢 Join Official Channel",
        
        # Language selection
        "language_select": "🌐 *Select your language*\n\nChoose your preferred language:",
        "language_changed": "✅ Language changed to English",
        "btn_spanish": "🇪🇸 Español",
        "btn_english": "🇺🇸 English",
        
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
    }
}


def get_msg(key, lang="es", **kwargs):
    """
    Get a message in the specified language
    
    Args:
        key: Message key
        lang: Language code ('es' or 'en')
        **kwargs: Format parameters for the message
    
    Returns:
        Formatted message string
    """
    try:
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
        return user.get('language', 'es')
    return 'es'
