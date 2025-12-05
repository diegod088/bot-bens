#!/usr/bin/env python3
"""
Telegram Bot with Telegram Stars Payment System

A bot that forwards media from Telegram links with a free limit for videos.
Users can pay with Telegram Stars to unlock Premium (videos unlimited for 30 days).
Photos are always free.
"""

import os
import re
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice

# Load environment variables from .env file
load_dotenv()
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters, PreCheckoutQueryHandler, CallbackQueryHandler
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaPhoto
from telethon.errors import (
    ChannelPrivateError, ChatForbiddenError, InviteHashExpiredError,
    InviteHashInvalidError, FloodWaitError, UserAlreadyParticipantError
)
from telethon.tl.functions.messages import ImportChatInviteRequest
import tempfile
from io import BytesIO

from database import (
    init_database,
    get_user,
    create_user,
    increment_download,
    set_premium,
    get_user_stats
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TELEGRAM_SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')

# Validate required variables
if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_SESSION_STRING]):
    raise ValueError("Missing required environment variables")

# Initialize Telethon client (for downloading from channels)
telethon_client = TelegramClient(
    StringSession(TELEGRAM_SESSION_STRING),
    int(TELEGRAM_API_ID),
    TELEGRAM_API_HASH
)

# Constants
FREE_DOWNLOAD_LIMIT = 3  # Free users: 3 videos total before needing Premium
FREE_PHOTO_DAILY_LIMIT = 10  # Free users: 10 photos daily
PREMIUM_PRICE_STARS = 500  # Price in Telegram Stars (⭐)

# Premium daily limits (unlimited photos, 50 daily for others)
PREMIUM_VIDEO_DAILY_LIMIT = 50
PREMIUM_MUSIC_DAILY_LIMIT = 50
PREMIUM_APK_DAILY_LIMIT = 50


def parse_telegram_link(url: str) -> tuple[str, int | None] | None:
    """Extrae identificador del canal y message_id (puede ser None)"""
    url = url.strip()
    
    # Enlaces con hash de invitación: t.me/+HASH o t.me/+HASH/123
    match = re.search(r't\.me/\+([^/]+)(?:/(\d+))?', url)
    if match:
        return f"+{match.group(1)}", int(match.group(2)) if match.group(2) else None
    
    # Enlaces privados numéricos: t.me/c/123456789 o t.me/c/123456789/123
    match = re.search(r't\.me/c/(\d+)(?:/(\d+))?', url)
    if match:
        return match.group(1), int(match.group(2)) if match.group(2) else None
    
    # Canales públicos: t.me/username o t.me/username/123
    match = re.search(r't\.me/([^/\s]+)(?:/(\d+))?', url)
    if match and match.group(1) not in ['joinchat', 'c', '+']:
        return match.group(1), int(match.group(2)) if match.group(2) else None
    
    return None


async def get_entity_from_identifier(identifier: str):
    """Resolve channel identifier to Telegram entity"""
    if identifier.startswith('+'):
        return await telethon_client.get_entity(identifier)
    elif identifier.isdigit():
        # For numeric channel IDs (from t.me/c/ID/MSG format)
        # Need to convert to proper channel ID: -100{channel_id}
        channel_id = int(identifier)
        return await telethon_client.get_entity(f"-100{channel_id}")
    else:
        return identifier


def extract_message_caption(message) -> str:
    """Extract caption or text from a Telegram message"""
    caption = ""
    if hasattr(message, 'caption') and message.caption:
        caption = message.caption
    elif hasattr(message, 'text') and message.text:
        caption = message.text
    
    return caption.strip() if caption else ""


async def is_photo_message(message):
    """Check if message contains a photo"""
    from telethon.tl.types import MessageMediaPhoto
    return isinstance(message.media, MessageMediaPhoto)


def detect_content_type(message) -> str:
    """
    Detect content type from message
    Returns: 'photo', 'video', 'music', 'apk', or 'other'
    """
    from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
    
    if isinstance(message.media, MessageMediaPhoto):
        return 'photo'
    
    if isinstance(message.media, MessageMediaDocument):
        doc = message.media.document
        mime_type = doc.mime_type if hasattr(doc, 'mime_type') else ''
        
        # Check file extension from attributes
        file_name = ''
        if hasattr(doc, 'attributes'):
            for attr in doc.attributes:
                if hasattr(attr, 'file_name'):
                    file_name = attr.file_name.lower()
                    break
        
        # APK detection
        if file_name.endswith('.apk') or mime_type == 'application/vnd.android.package-archive':
            return 'apk'
        
        # Music detection
        if mime_type.startswith('audio/') or file_name.endswith(('.mp3', '.m4a', '.flac', '.wav', '.ogg')):
            return 'music'
        
        # Video detection
        if mime_type.startswith('video/') or file_name.endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
            return 'video'
    
    return 'other'


def get_file_size(message) -> int:
    """Get file size in bytes"""
    from telethon.tl.types import MessageMediaDocument
    
    if isinstance(message.media, MessageMediaDocument):
        return message.media.document.size
    return 0


async def download_and_send_media(message, chat_id: int, bot):
    """Download media from protected channel and send to user"""
    path = None
    try:
        # Extract caption
        caption = extract_message_caption(message)
        
        # Truncate caption if too long (Telegram limit is 1024 characters)
        if caption and len(caption) > 1024:
            caption = caption[:1020] + "..."
        
        # Detect content type
        content_type = detect_content_type(message)
        
        # Check file size
        file_size = 0
        if hasattr(message.media, 'document') and hasattr(message.media.document, 'size'):
            file_size = message.media.document.size
        elif hasattr(message.media, 'photo') and hasattr(message.media.photo, 'sizes'):
            # For photos, get the largest size
            if message.media.photo.sizes:
                file_size = max(getattr(size, 'size', 0) for size in message.media.photo.sizes if hasattr(size, 'size'))
        
        # Warn if file is large (> 50 MB)
        MAX_SIZE = 50 * 1024 * 1024  # 50 MB in bytes
        if file_size > MAX_SIZE:
            size_mb = file_size / (1024 * 1024)
            await bot.send_message(
                chat_id=chat_id,
                text=f"⚠️ *Archivo Grande Detectado*\n\n"
                     f"📦 Tamaño: {size_mb:.1f} MB\n"
                     f"🚨 Límite de Telegram: 50 MB\n\n"
                     f"❌ Este archivo es demasiado grande para enviarlo por bot.\n\n"
                     f"💡 *Soluciones:*\n"
                     f"• Busca una versión más comprimida\n"
                     f"• Descarga directamente desde el canal original",
                parse_mode='Markdown'
            )
            return
        elif file_size > 30 * 1024 * 1024:  # Warn if > 30 MB
            size_mb = file_size / (1024 * 1024)
            await bot.send_message(
                chat_id=chat_id,
                text=f"⏳ *Archivo Grande*\n\n"
                     f"📦 Tamaño: {size_mb:.1f} MB\n\n"
                     f"Esto puede tardar varios minutos en descargar y enviar...",
                parse_mode='Markdown'
            )
        
        # Check if it's a photo
        is_photo = isinstance(message.media, MessageMediaPhoto)
        
        if is_photo:
            # For photos, download to memory
            photo_bytes = BytesIO()
            await telethon_client.download_media(message, file=photo_bytes)
            photo_bytes.seek(0)
            
            # Send as photo
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo_bytes,
                caption=caption if caption else None
            )
        else:
            # For videos/documents, download to temp file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4' if content_type == 'video' else '')
            path = temp_file.name
            temp_file.close()
            
            path = await telethon_client.download_media(message, file=path)
            
            # Send based on content type
            with open(path, 'rb') as f:
                if content_type == 'video':
                    # Send as video with video metadata
                    await bot.send_video(
                        chat_id=chat_id,
                        video=f,
                        caption=caption if caption else None,
                        supports_streaming=True
                    )
                elif content_type == 'music':
                    # Send as audio
                    await bot.send_audio(
                        chat_id=chat_id,
                        audio=f,
                        caption=caption if caption else None
                    )
                else:
                    # Send as document for APK and other files
                    await bot.send_document(
                        chat_id=chat_id,
                        document=f,
                        caption=caption if caption else None
                    )
            
            # Cleanup
            os.remove(path)
        
    except Exception as e:
        # Cleanup on error
        if path and os.path.exists(path):
            os.remove(path)
        raise e


async def send_premium_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send invoice for Premium subscription payment with Telegram Stars"""
    chat_id = update.effective_chat.id
    title = "💎 Suscripción Premium"
    description = "Fotos Ilimitadas + 50 Videos + 50 Música + 50 APK diarios | 30 días de acceso"
    payload = "premium_30_days"
    currency = "XTR"  # Telegram Stars currency code
    
    # Price in Telegram Stars
    prices = [LabeledPrice("Premium 30 días", PREMIUM_PRICE_STARS)]
    
    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token="",  # Empty for Stars payments
        currency=currency,
        prices=prices
    )


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answer pre-checkout query (approve all by default)"""
    query = update.pre_checkout_query
    await query.answer(ok=True)


async def show_premium_plans(query, context: ContextTypes.DEFAULT_TYPE):
    """Show premium plans information"""
    message = (
        "💎 *Planes de Suscripción* 💎\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🆓 *GRATIS*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Fotos: Ilimitadas\n"
        "🎬 Videos: Solo 3 totales\n"
        "🎵 Música: ✖️ Bloqueado\n"
        "📦 APK: ✖️ Bloqueado\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💎 *PREMIUM* — {PREMIUM_PRICE_STARS} ⭐\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Fotos: Ilimitadas\n"
        "🎬 Videos: 50 cada día ✨\n"
        "🎵 Música: 50 cada día ✨\n"
        "📦 APK: 50 cada día ✨\n"
        "♻️ Contador se resetea diario\n"
        "⏰ Válido: 30 días\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ *Con Premium desbloqueas:*\n"
        "• Música y APK disponibles\n"
        "• 50 descargas diarias de cada tipo\n"
        "• Límites se renuevan cada 24h\n\n"
        "⭐ *Paga con Telegram Stars*\n"
        "Usa el botón abajo para suscribirte."
    )
    
    # Add payment and channel buttons
    keyboard = [
        [InlineKeyboardButton("⭐ Pagar con Estrellas", callback_data="pay_premium")],
        [InlineKeyboardButton("📢 Únete al Canal Oficial", url="https://t.me/observer_bots")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    
    if query.data == "view_plans":
        # Show premium plans
        await query.answer()
        await show_premium_plans(query, context)
        return
    
    if query.data == "show_guide":
        # Show detailed usage guide
        await query.answer()
        guide_message = (
            "📖 *Guía Completa de Uso*\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔐 *CANALES/GRUPOS PRIVADOS*\n\n"
            "*Paso 1: Enviar Enlace de Invitación*\n"
            "Primero, envíame el enlace de invitación del canal o grupo\\.\n\n"
            "✅ Formato correcto:\n"
            "`t.me/+AbC123XyZ`\n"
            "`t.me/joinchat/AbC123XyZ`\n\n"
            "El bot se unirá automáticamente al canal\\.\n\n"
            "*Paso 2: Enviar Enlace del Mensaje*\n"
            "Después de unirme, envía el enlace del mensaje específico\\.\n\n"
            "✅ Formato correcto:\n"
            "`t.me/+AbC123XyZ/456`\n"
            "`t.me/c/1234567890/456`\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌐 *CANALES PÚBLICOS*\n\n"
            "Para canales públicos es más simple:\n"
            "Envía directamente el enlace del mensaje\\.\n\n"
            "✅ Formato correcto:\n"
            "`t.me/nombre_canal/123`\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💡 *CONSEJOS*\n\n"
            "• Si recibes un error, verifica que el enlace sea correcto\n"
            "• Para canales privados, siempre envía primero la invitación\n"
            "• El bot soporta videos, fotos, música, APK y texto\n"
            "• Los archivos mayores a 50 MB no se pueden descargar\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "❓ ¿Necesitas ayuda? @observer\\_bots"
        )
        
        keyboard = [[InlineKeyboardButton("« Volver al Menú", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(guide_message, parse_mode='MarkdownV2', reply_markup=reply_markup)
        return
    
    if query.data == "back_to_menu":
        # Return to main menu
        await query.answer()
        user_id = update.effective_user.id
        user = get_user(user_id)
        from datetime import datetime
        
        welcome_message = "✨ *Media Downloader Bot* ✨\n\n"
        welcome_message += "Descarga contenido de Telegram de forma simple y rápida.\n\n"
        welcome_message += "━━━━━━━━━━━━━━━━━━━━\n"
        welcome_message += "📊 *Tu Plan Actual*\n\n"
        
        if user['premium']:
            from database import check_and_reset_daily_limits
            check_and_reset_daily_limits(user_id)
            user = get_user(user_id)
            
            if user.get('premium_until'):
                expiry = datetime.fromisoformat(user['premium_until'])
                days_left = (expiry - datetime.now()).days
                welcome_message += (
                    "💎 *PREMIUM ACTIVO*\n"
                    f"📅 Expira: {expiry.strftime('%d/%m/%Y')}\n"
                    f"⏳ {days_left} días restantes\n\n"
                    "📈 *Uso Diario*\n"
                    f"🎬 Videos: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                    f"🎵 Música: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
                    f"📦 APK: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}\n"
                    "📸 Fotos: Ilimitadas\n\n"
                    "♻️ Renueva con /premium"
                )
            else:
                welcome_message += "💎 *PREMIUM ACTIVO*\n✨ Acceso completo"
        else:
            from database import check_and_reset_daily_limits
            check_and_reset_daily_limits(user_id)
            user = get_user(user_id)
            
            remaining = FREE_DOWNLOAD_LIMIT - user['downloads']
            welcome_message += (
                "🆓 *GRATIS*\n"
                f"📸 Fotos: {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT} (diarias)\n"
                f"🎬 Videos: {user['downloads']}/{FREE_DOWNLOAD_LIMIT} (totales)\n"
                "🎵 Música: No disponible\n"
                "📦 APK: No disponible\n\n"
                "💎 Mejora tu plan con /premium"
            )
        
        welcome_message += "\n\n━━━━━━━━━━━━━━━━━━━━\n"
        welcome_message += "📖 *Cómo Usar el Bot*\n\n"
        welcome_message += "🔐 *Para canales/grupos privados:*\n"
        welcome_message += "1️⃣ Envía primero el enlace de invitación\n"
        welcome_message += "   _Ejemplo:_ `t.me/+AbC123XyZ`\n"
        welcome_message += "2️⃣ Luego envía el enlace del mensaje\n"
        welcome_message += "   _Ejemplo:_ `t.me/+AbC123XyZ/456`\n\n"
        welcome_message += "🌐 *Para canales públicos:*\n"
        welcome_message += "➡️ Envía directamente el enlace del mensaje\n"
        welcome_message += "   _Ejemplo:_ `t.me/canal/123`\n\n"
        welcome_message += "🔗 ¡Envía un enlace para comenzar!"
        
        keyboard = [
            [InlineKeyboardButton("💎 Ver Planes Premium", callback_data="view_plans")],
            [InlineKeyboardButton("📖 Guía de Uso", callback_data="show_guide")],
            [InlineKeyboardButton("📢 Únete al Canal Oficial", url="https://t.me/observer_bots")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)
        return
    
    await query.answer("📄 Procesando...", show_alert=False)
    
    if query.data == "pay_premium":
        # Send the invoice when button is pressed
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested payment invoice")
        
        try:
            await send_premium_invoice_callback(update, context)
            logger.info(f"Invoice sent successfully to user {user_id}")
            
            # Send confirmation message
            await query.message.reply_text(
                "✅ *Factura enviada*\n\n"
                "Revisa el mensaje de pago que apareció arriba.\n"
                "💳 Completa el pago para activar Premium.",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error sending invoice to user {user_id}: {error_msg}")
            
            # Check if it's a Telegram Stars configuration error
            if "currency" in error_msg.lower() or "stars" in error_msg.lower() or "xtr" in error_msg.lower():
                await query.message.reply_text(
                    "⚠️ *Sistema de Pagos en Configuración*\n\n"
                    "El bot aún no tiene habilitado Telegram Stars.\n\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "📋 *Para el administrador:*\n"
                    "1. Abre @BotFather\n"
                    "2. Usa /mybots\n"
                    "3. Selecciona este bot\n"
                    "4. Toca 'Payments'\n"
                    "5. Habilita 'Telegram Stars'\n\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"
                    "💡 Mientras tanto, disfruta:\n"
                    "• 3 videos gratis\n"
                    "• Fotos ilimitadas\n\n"
                    "📢 Síguenos: @observer_bots",
                    parse_mode='Markdown'
                )
            else:
                await query.message.reply_text(
                    "❌ *Error Temporal*\n\n"
                    "No se pudo procesar el pago.\n"
                    "Intenta nuevamente en unos momentos.\n\n"
                    "📢 Soporte: @observer_bots\n\n"
                    f"🔧 Error: `{error_msg[:100]}`",
                    parse_mode='Markdown'
                )


async def send_premium_invoice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send invoice for Premium subscription when callback button is pressed"""
    chat_id = update.effective_chat.id
    title = "💎 Suscripción Premium"
    description = "50 Videos + 50 Música + 50 APK diarios | Fotos Ilimitadas | 30 días de acceso"
    payload = "premium_30_days"
    currency = "XTR"  # Telegram Stars currency code
    
    # Price in Telegram Stars
    prices = [LabeledPrice("Premium 30 días", PREMIUM_PRICE_STARS)]
    
    try:
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",  # Empty for Stars payments
            currency=currency,
            prices=prices
        )
        logger.info(f"Invoice successfully sent to chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send invoice to chat {chat_id}: {e}")
        # Send informative error message
        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⚠️ *Sistema de Pagos Temporalmente No Disponible*\n\n"
                "El bot está configurándose para aceptar pagos con Telegram Stars.\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "💡 *Mientras tanto:*\n"
                "• Disfruta de las 3 descargas gratuitas de videos\n"
                "• 10 fotos diarias gratis\n\n"
                "📢 Únete al canal para actualizaciones:\n"
                "@observer_bots\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔧 Error técnico: `{str(e)[:50]}`"
            ),
            parse_mode='Markdown'
        )
        raise


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment with Telegram Stars"""
    user_id = update.effective_user.id
    payment_info = update.message.successful_payment
    
    logger.info(f"Payment received from user {user_id}: {payment_info.total_amount} {payment_info.currency}")
    
    # Activate Premium for 30 days
    set_premium(user_id, months=1)
    
    from datetime import datetime, timedelta
    expiry = datetime.now() + timedelta(days=30)
    
    await update.message.reply_text(
        "🎉 *Premium Activado*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ Pago recibido exitosamente\n"
        "💎 Suscripción Premium activada\n\n"
        f"📅 Válido hasta: {expiry.strftime('%d/%m/%Y')}\n"
        "⏰ Duración: 30 días\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 Usa /start para comenzar",
        parse_mode='Markdown'
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id
    from datetime import datetime
    
    # Ensure user exists in database
    if not get_user(user_id):
        create_user(user_id)
    
    user = get_user(user_id)
    
    welcome_message = "✨ *Media Downloader Bot* ✨\n\n"
    welcome_message += "Descarga contenido de Telegram de forma simple y rápida.\n\n"
    welcome_message += "━━━━━━━━━━━━━━━━━━━━\n"
    welcome_message += "📊 *Tu Plan Actual*\n\n"
    
    if user['premium']:
        # Check and reset daily limits if needed
        from database import check_and_reset_daily_limits
        check_and_reset_daily_limits(user_id)
        user = get_user(user_id)  # Refresh after potential reset
        
        if user.get('premium_until'):
            expiry = datetime.fromisoformat(user['premium_until'])
            days_left = (expiry - datetime.now()).days
            welcome_message += (
                "💎 *PREMIUM ACTIVO*\n"
                f"📅 Expira: {expiry.strftime('%d/%m/%Y')}\n"
                f"⏳ {days_left} días restantes\n\n"
                "📈 *Uso Diario*\n"
                f"🎬 Videos: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                f"🎵 Música: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
                f"📦 APK: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}\n"
                "📸 Fotos: Ilimitadas\n\n"
                "♻️ Renueva con /premium"
            )
        else:
            welcome_message += "💎 *PREMIUM ACTIVO*\n✨ Acceso completo"
    else:
        # Check and reset daily limits for FREE users too
        from database import check_and_reset_daily_limits
        check_and_reset_daily_limits(user_id)
        user = get_user(user_id)  # Refresh after potential reset
        
        remaining = FREE_DOWNLOAD_LIMIT - user['downloads']
        welcome_message += (
            "🆓 *GRATIS*\n"
            f"📸 Fotos: {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT} (diarias)\n"
            f"🎬 Videos: {user['downloads']}/{FREE_DOWNLOAD_LIMIT} (totales)\n"
            "🎵 Música: No disponible\n"
            "📦 APK: No disponible\n\n"
            "💎 Mejora tu plan con /premium"
        )
    
    welcome_message += "\n\n━━━━━━━━━━━━━━━━━━━━\n"
    welcome_message += "📖 *Cómo Usar*\n\n"
    welcome_message += "🔐 *Canales Privados*\n"
    welcome_message += "   1️⃣ Envía enlace de invitación\n"
    welcome_message += "      `t.me/+HASH`\n"
    welcome_message += "   2️⃣ Envía enlace del mensaje\n"
    welcome_message += "      `t.me/+HASH/123`\n\n"
    welcome_message += "🌐 *Canales Públicos*\n"
    welcome_message += "   ➡️ Envía enlace directo\n"
    welcome_message += "      `t.me/canal/123`\n\n"
    welcome_message += "💡 _Usa el botón Guía para más info_"
    
    # Add buttons: Premium plans, channel, and how-to guide
    keyboard = [
        [InlineKeyboardButton("💎 Ver Planes Premium", callback_data="view_plans")],
        [InlineKeyboardButton("📖 Guía de Uso", callback_data="show_guide")],
        [InlineKeyboardButton("📢 Únete al Canal Oficial", url="https://t.me/observer_bots")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)


async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /premium command - Show subscription info and send invoice"""
    from datetime import datetime
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    message = (
        "💎 *Planes de Suscripción* 💎\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🆓 *GRATIS*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Fotos: 10 cada día\n"
        "🎬 Videos: Solo 3 totales\n"
        "🎵 Música: ✖️ Bloqueado\n"
        "📦 APK: ✖️ Bloqueado\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💎 *PREMIUM* — {PREMIUM_PRICE_STARS} ⭐\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Fotos: Ilimitadas ✨\n"
        "🎬 Videos: 50 cada día ✨\n"
        "🎵 Música: 50 cada día ✨\n"
        "📦 APK: 50 cada día ✨\n"
        "♻️ Contador se resetea diario\n"
        "⏰ Válido: 30 días\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✅ *Con Premium desbloqueas:*\n"
        "• Fotos ilimitadas sin restricción\n"
        "• Música y APK disponibles\n"
        "• 50 descargas diarias de cada tipo\n"
        "• Límites se renuevan cada 24h\n\n"
        "⭐ *Paga con Telegram Stars*\n"
        "Usa el botón abajo para suscribirte."
    )
    
    if user and user['premium']:
        if user.get('premium_until'):
            expiry = datetime.fromisoformat(user['premium_until'])
            days_left = (expiry - datetime.now()).days
            message = (
                "✨ *Ya eres Premium* ✨\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📅 Expira: {expiry.strftime('%d/%m/%Y')}\n"
                f"⏳ {days_left} días restantes\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "💎 *Renovar Premium*\n"
                f"Precio: *{PREMIUM_PRICE_STARS} ⭐*\n\n"
                "Usa el botón abajo para renovar."
            )
    
    # Send message with payment button and channel button
    keyboard = [
        [InlineKeyboardButton("⭐ Pagar con Estrellas", callback_data="pay_premium")],
        [InlineKeyboardButton("📢 Únete al Canal Oficial", url="https://t.me/observer_bots")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)


async def testpay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test payment system - Send invoice directly"""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} testing payment system with /testpay")
    
    try:
        chat_id = update.effective_chat.id
        title = "💎 TEST - Premium"
        description = "Prueba del sistema de pagos con Telegram Stars"
        payload = "test_payment"
        currency = "XTR"
        prices = [LabeledPrice("Test Premium", PREMIUM_PRICE_STARS)]
        
        await context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",
            currency=currency,
            prices=prices
        )
        
        await update.message.reply_text(
            "✅ *Sistema de Pagos Funcionando*\n\n"
            "La factura de prueba se envió correctamente.\n"
            "Telegram Stars está habilitado. ✨",
            parse_mode='Markdown'
        )
        logger.info(f"Test invoice sent successfully to user {user_id}")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Test payment failed for user {user_id}: {error_msg}")
        
        await update.message.reply_text(
            "❌ *Sistema de Pagos NO Configurado*\n\n"
            f"Error: `{error_msg[:200]}`\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔧 *Solución:*\n"
            "1. Abre @BotFather\n"
            "2. /mybots → Selecciona tu bot\n"
            "3. Payments → Telegram Stars\n"
            "4. Habilita y acepta términos\n\n"
            "📢 @observer_bots",
            parse_mode='Markdown'
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command - Show usage guide"""
    message = (
        "📖 *Guía de Uso* 📖\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🔗 *Cómo Usar el Bot*\n\n"
        "1️⃣ Copia un enlace de Telegram\n"
        "   Ejemplo: https://t.me/canal/123\n\n"
        "2️⃣ Envía el enlace al bot\n\n"
        "3️⃣ ¡Recibe tu contenido al instante!\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📋 *Comandos Disponibles*\n\n"
        "• /start - Menú principal\n"
        "• /premium - Ver planes y suscribirse\n"
        "• /stats - Ver tus estadísticas\n"
        "• /help - Esta guía de uso\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📦 *Tipos de Contenido*\n\n"
        "✅ Fotos\n"
        "✅ Videos\n"
        "✅ Música (Premium)\n"
        "✅ APK (Premium)\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🆓 *Plan Gratis*\n"
        "• 10 fotos diarias\n"
        "• 3 videos totales\n"
        "• Música y APK bloqueados\n\n"
        "💎 *Plan Premium*\n"
        "• Fotos ilimitadas\n"
        "• 50 videos diarios\n"
        "• 50 canciones diarias\n"
        "• 50 APK diarios\n"
        f"• Solo {PREMIUM_PRICE_STARS} estrellas por 30 días\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 Usa /premium para mejorar tu plan\n"
        "📢 Únete a @observer\\_bots"
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - Show user and bot statistics"""
    user_id = update.effective_user.id
    
    # Get stats
    stats = get_user_stats()
    user = get_user(user_id)
    
    from datetime import datetime
    from database import check_and_reset_daily_limits
    
    # Reset daily limits if needed
    if user['premium']:
        check_and_reset_daily_limits(user_id)
        user = get_user(user_id)  # Refresh
    
    # Build message
    message = "📊 *Estadísticas* 📊\n\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Personal stats
    message += "👤 *Tu Cuenta*\n\n"
    
    if user['premium']:
        if user.get('premium_until'):
            expiry = datetime.fromisoformat(user['premium_until'])
            days_left = (expiry - datetime.now()).days
            message += f"💎 Plan: Premium\n"
            message += f"📅 Expira: {expiry.strftime('%d/%m/%Y')}\n"
            message += f"⏳ Días restantes: {days_left}\n\n"
            message += "📈 *Uso Diario (Hoy)*\n"
            message += f"🎬 Videos: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
            message += f"🎵 Música: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
            message += f"📦 APK: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}\n"
            message += f"📸 Fotos: Ilimitadas\n"
        else:
            message += "💎 Plan: Premium Vitalicio\n"
    else:
        # Reset daily limits for FREE users too
        check_and_reset_daily_limits(user_id)
        user = get_user(user_id)  # Refresh
        
        remaining = FREE_DOWNLOAD_LIMIT - user['downloads']
        message += "🆓 Plan: Gratis\n"
        message += f"🎬 Videos: {user['downloads']}/{FREE_DOWNLOAD_LIMIT} (totales)\n"
        message += f"🎁 Restantes: {remaining}\n"
        message += f"📸 Fotos: {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT} (diarias)\n"
    
    message += "\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # Global stats
    message += "🌍 *Estadísticas del Bot*\n\n"
    message += f"👥 Usuarios totales: {stats['total_users']}\n"
    message += f"💎 Usuarios Premium: {stats['premium_users']}\n"
    message += f"🆓 Usuarios Gratis: {stats['free_users']}\n"
    message += f"📥 Descargas totales: {stats['total_downloads']}\n\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"
    message += "💡 Usa /premium para mejorar tu plan"
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with Telegram links"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if not text:
        return
    
    # Extract Telegram links
    links = re.findall(r'https?://t\.me/[^\s]+', text)
    if not links:
        return
    
    # Ensure user exists
    if not get_user(user_id):
        create_user(user_id)
    
    user = get_user(user_id)
    
    # Parse link
    link = links[0]
    parsed = parse_telegram_link(link)
    
    if not parsed:
        await update.message.reply_text(
            "❌ *Enlace Inválido*\n\n"
            "El enlace que enviaste no es válido.\n\n"
            "📌 *Formatos aceptados:*\n"
            "• Canales públicos: t.me/canal/123\n"
            "• Canales privados: t.me/+HASH/123\n"
            "• Enlaces numéricos: t.me/c/123456/789\n\n"
            "💡 Copia el enlace completo desde Telegram y envíamelo otra vez.",
            parse_mode='Markdown'
        )
        return
    
    channel_id, message_id = parsed
    joined_automatically = False  # Track if we joined a channel
    
    # If no message_id, this is just an invitation link to join
    if message_id is None:
        if channel_id.startswith('+'):
            try:
                invite_hash = channel_id[1:]
                result = await telethon_client(ImportChatInviteRequest(invite_hash))
                await asyncio.sleep(1)
                
                # Get channel name from result
                channel_name = getattr(result.chats[0], 'title', 'canal') if result.chats else 'canal'
                
                await update.message.reply_text(
                    f"✅ *Unido Exitosamente*\n\n"
                    f"Me uní al canal: *{channel_name}*\n\n"
                    f"Ahora puedes enviarme enlaces de mensajes específicos del canal para descargar contenido.\n\n"
                    f"📝 Ejemplo: t.me/+HASH/123",
                    parse_mode='Markdown'
                )
                return
            except UserAlreadyParticipantError:
                await update.message.reply_text(
                    "ℹ️ *Ya Estoy en el Canal*\n\n"
                    "Ya soy miembro de este canal.\n\n"
                    "Puedes enviarme enlaces de mensajes específicos para descargar contenido.\n\n"
                    "📝 Ejemplo: t.me/+HASH/123",
                    parse_mode='Markdown'
                )
                return
            except InviteHashExpiredError:
                await update.message.reply_text(
                    "La invitación ha expirado\n\n"
                    "Pide al administrador del canal un enlace nuevo (debe empezar con t.me/+) y envíamelo otra vez."
                )
                return
            except InviteHashInvalidError:
                await update.message.reply_text(
                    "Enlace de invitación inválido o ya usado\n\n"
                    "Asegúrate de copiar el enlace completo que empieza con t.me/+"
                )
                return
            except FloodWaitError as flood_e:
                await update.message.reply_text(
                    f"⏳ *Límite de Velocidad*\n\n"
                    f"Demasiadas solicitudes. Espera {flood_e.seconds} segundos e inténtalo nuevamente.",
                    parse_mode='Markdown'
                )
                return
            except Exception as join_e:
                logger.error(f"Error joining channel: {join_e}")
                await update.message.reply_text(
                    "❌ *Error al Unirse al Canal*\n\n"
                    "No pude unirme al canal automáticamente.\n\n"
                    "🔍 *Qué puedes hacer:*\n"
                    "1️⃣ Verifica que el enlace sea correcto\n"
                    "2️⃣ Pide un nuevo enlace de invitación al admin\n"
                    "3️⃣ Intenta agregar el bot manualmente al canal\n\n"
                    "💡 Si el problema persiste, contacta al administrador del canal.",
                    parse_mode='Markdown'
                )
                return
        else:
            await update.message.reply_text(
                "❌ *Enlace Incompleto*\n\n"
                "Este enlace no tiene el número de mensaje.\n\n"
                "📝 *Necesito el enlace completo:*\n"
                "• Para canales públicos: t.me/canal/123\n"
                "• Para canales privados: t.me/c/123456/789\n\n"
                "💡 Toca el mensaje específico → Copiar enlace",
                parse_mode='Markdown'
            )
            return
    
    try:
        # Get the message
        message = None
        entity = None
        
        logger.info(f"Attempting to get message {message_id} from channel {channel_id}")
        
        try:
            entity = await get_entity_from_identifier(channel_id)
            logger.info(f"Entity resolved: {entity}")
            message = await telethon_client.get_messages(entity, ids=message_id)
            logger.info(f"Message retrieved: {message is not None}")
        except ValueError as ve:
            logger.warning(f"ValueError getting entity: {ve}")
            # Entity not found in cache
            # For numeric channel IDs, we need to get all dialogs to find it
            if channel_id.isdigit():
                try:
                    logger.info(f"Numeric channel ID, searching in dialogs...")
                    # Get the channel from dialogs
                    async for dialog in telethon_client.iter_dialogs():
                        if dialog.is_channel and str(dialog.entity.id) == channel_id:
                            entity = dialog.entity
                            logger.info(f"Found channel in dialogs: {dialog.entity.title}")
                            message = await telethon_client.get_messages(entity, ids=message_id)
                            logger.info(f"Message retrieved from dialog channel: {message is not None}")
                            break
                    
                    if not message:
                        # Channel not found in dialogs, need invitation
                        raise ChannelPrivateError(None)
                except Exception as ex:
                    logger.error(f"Failed to get entity from dialogs: {ex}")
                    raise ChannelPrivateError(None)
            elif channel_id.startswith('+'):
                # For invite links, try to get entity directly or join
                try:
                    logger.info(f"Trying to get entity directly for invite link")
                    entity = await telethon_client.get_entity(channel_id)
                    message = await telethon_client.get_messages(entity, ids=message_id)
                    logger.info(f"Message retrieved after direct entity fetch: {message is not None}")
                except Exception as ex:
                    logger.error(f"Failed to get entity directly: {ex}")
                    # If still fails, treat as private channel
                    raise ChannelPrivateError(None)
            else:
                raise ChannelPrivateError(None)
        except (ChannelPrivateError, ChatForbiddenError):
            # If channel is private and we have an invite hash, try to join
            if channel_id.startswith('+'):
                try:
                    # Extract hash from identifier (remove '+' prefix)
                    invite_hash = channel_id[1:]
                    await telethon_client(ImportChatInviteRequest(invite_hash))
                    
                    # Wait a moment for the join to complete
                    await asyncio.sleep(1)
                    
                    # Try to get the message again
                    entity = await get_entity_from_identifier(channel_id)
                    message = await telethon_client.get_messages(entity, ids=message_id)
                    
                    await update.message.reply_text("Unido al canal automáticamente. Descargando...")
                    joined_automatically = True
                    
                except InviteHashExpiredError:
                    await update.message.reply_text(
                        "La invitación ha expirado\n\n"
                        "Pide al administrador del canal un enlace nuevo (debe empezar con t.me/+) y envíamelo otra vez."
                    )
                    return
                except InviteHashInvalidError:
                    await update.message.reply_text(
                        "Enlace de invitación inválido o ya usado\n\n"
                        "Asegúrate de copiar el enlace completo que empieza con t.me/+"
                    )
                    return
                except FloodWaitError as flood_e:
                    await update.message.reply_text(
                        f"⏳ *Límite de Velocidad*\n\n"
                        f"Demasiadas solicitudes. Espera {flood_e.seconds} segundos e inténtalo nuevamente.",
                        parse_mode='Markdown'
                    )
                    return
                except Exception as join_e:
                    logger.error(f"Error joining channel: {join_e}")
                    await update.message.reply_text(
                        "❌ *Error al Unirse al Canal*\n\n"
                        "No pude unirme al canal automáticamente.\n\n"
                        "🔍 *Qué puedes hacer:*\n"
                        "1️⃣ Verifica que el enlace sea correcto\n"
                        "2️⃣ Pide un nuevo enlace de invitación al admin\n"
                        "3️⃣ Intenta agregar el bot manualmente al canal\n\n"
                        "💡 Si el problema persiste, contacta al administrador del canal.",
                        parse_mode='Markdown'
                    )
                    return
            else:
                # Private channel without invite hash
                me = await telethon_client.get_me()
                username = f"@{me.username}" if me.username else "el bot"
                await update.message.reply_text(
                    f"Este es un canal privado y no tengo acceso\n\n"
                    f"Para que pueda descargar:\n\n"
                    f"Opción 1 → Envíame un enlace de invitación (empieza con t.me/+)\n"
                    f"Opción 2 → Agrégame manualmente al canal con mi cuenta {username}"
                )
                return
        
        if not message:
            await update.message.reply_text(
                "❌ *Mensaje No Encontrado*\n\n"
                "No pude encontrar este mensaje en el canal.\n\n"
                "🔍 *Posibles razones:*\n"
                "• El mensaje fue eliminado\n"
                "• El enlace está incorrecto\n"
                "• El canal no existe\n\n"
                "💡 Verifica el enlace y envíamelo otra vez.",
                parse_mode='Markdown'
            )
            return
        
        # Check for nested links
        if not message.media and message.text:
            inner_links = re.findall(r'https?://t\.me/[^\s\)]+', message.text)
            if inner_links:
                inner_parsed = parse_telegram_link(inner_links[0])
                if inner_parsed:
                    inner_channel_id, inner_message_id = inner_parsed
                    
                    # Skip nested link if it has no message_id
                    if inner_message_id is None:
                        logger.info(f"Skipping nested link without message_id: {inner_links[0]}")
                    else:
                        try:
                            # Try same logic as main message retrieval
                            inner_entity = None
                            inner_msg = None
                            
                            try:
                                inner_entity = await get_entity_from_identifier(inner_channel_id)
                                inner_msg = await telethon_client.get_messages(inner_entity, ids=inner_message_id)
                            except ValueError as ve_inner:
                                # Try to find in dialogs if numeric
                                if inner_channel_id.isdigit():
                                    async for dialog in telethon_client.iter_dialogs():
                                        if dialog.is_channel and str(dialog.entity.id) == inner_channel_id:
                                            inner_entity = dialog.entity
                                            inner_msg = await telethon_client.get_messages(inner_entity, ids=inner_message_id)
                                            break
                            
                            if inner_msg and inner_msg.media:
                                message = inner_msg
                                logger.info("Using nested link message with media")
                                
                        except Exception as nested_ex:
                            logger.warning(f"Could not process nested link: {nested_ex}")
                            # Continue with original message if nested fails
        
        # Check if message has media or text content
        if not message:
            await update.message.reply_text(
                "❌ *Mensaje No Encontrado*\n\n"
                "No pude encontrar este mensaje en el canal.",
                parse_mode='Markdown'
            )
            return
        
        # If message has only text (no media), send the text
        if not message.media:
            if message.text:
                # Send the text content
                text_to_send = message.text
                
                # Add caption if available
                if hasattr(message, 'caption') and message.caption:
                    text_to_send = f"{message.caption}\n\n{text_to_send}"
                
                await update.message.reply_text(
                    f"📄 *Contenido del Mensaje:*\n\n{text_to_send}",
                    parse_mode='Markdown'
                )
                return
            else:
                await update.message.reply_text(
                    "❌ *Sin Contenido*\n\n"
                    "Este mensaje no contiene texto ni archivos para descargar.\n\n"
                    "📥 *Puedo descargar:*\n"
                    "• Texto\n"
                    "• Videos y GIFs\n"
                    "• Fotos e imágenes\n"
                    "• Música y audio\n"
                    "• Archivos APK\n\n"
                    "💡 Envíame un enlace a un mensaje que contenga alguno de estos.",
                    parse_mode='Markdown'
                )
                return
        
        # Detect content type
        content_type = detect_content_type(message)
        
        # Check photo limits
        if content_type == 'photo':
            if not user['premium']:
                # FREE users: 10 photos daily
                from database import check_and_reset_daily_limits
                check_and_reset_daily_limits(user_id)
                user = get_user(user_id)  # Refresh after potential reset
                
                if user['daily_photo'] >= FREE_PHOTO_DAILY_LIMIT:
                    await update.message.reply_text(
                        "⚠️ *Límite Diario Alcanzado*\n\n"
                        f"Has descargado {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT} fotos hoy.\n\n"
                        "━━━━━━━━━━━━━━━━━━━━\n\n"
                        "💎 *Con Premium obtienes:*\n"
                        "✅ Fotos: Ilimitadas\n"
                        "✅ Videos: 50 diarios\n"
                        "✅ Música: 50 diarias\n"
                        "✅ APK: 50 diarios\n"
                        "♻️ Videos, música y APK se renuevan diario\n\n"
                        f"💰 Solo {PREMIUM_PRICE_STARS} ⭐ por 30 días\n\n"
                        "━━━━━━━━━━━━━━━━━━━━\n\n"
                        "⭐ Usa /premium para suscribirte",
                        parse_mode='Markdown'
                    )
                    return
            # Premium users have unlimited photos, continue
        # Music and APK blocked for FREE users
        elif content_type in ['music', 'apk'] and not user['premium']:
            content_name = 'Música' if content_type == 'music' else 'APK'
            await update.message.reply_text(
                "🔒 *Contenido Bloqueado*\n\n"
                f"✖️ {content_name} solo para usuarios Premium\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "💎 *Con Premium obtienes:*\n"
                f"✅ {content_name}: 50 diarias\n"
                "✅ Videos: 50 diarios\n"
                "✅ Todo se resetea cada día\n\n"
                f"💰 Solo {PREMIUM_PRICE_STARS} ⭐ por 30 días\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "⭐ Usa /premium para suscribirte",
                parse_mode='Markdown'
            )
            return
        # Check video limits
        elif content_type == 'video':
            if user['premium']:
                # Check premium daily video limit
                from database import check_and_reset_daily_limits
                check_and_reset_daily_limits(user_id)
                user = get_user(user_id)  # Refresh after potential reset
                
                if user['daily_video'] >= PREMIUM_VIDEO_DAILY_LIMIT:
                    await update.message.reply_text(
                        "⚠️ *Límite Diario Alcanzado*\n\n"
                        f"Has descargado {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT} videos hoy.\n\n"
                        "♻️ Tu límite se renueva en 24 horas.\n\n"
                        "💡 Mientras esperas puedes descargar:\n"
                        "✨ Fotos: Ilimitadas\n"
                        f"🎵 Música: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
                        f"📦 APK: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}",
                        parse_mode='Markdown'
                    )
                    return
            else:
                # Check FREE total video limit
                if user['downloads'] >= FREE_DOWNLOAD_LIMIT:
                    await update.message.reply_text(
                        "⚠️ *Límite Alcanzado*\n\n"
                        "Has usado tus 3 videos gratuitos.\n\n"
                        "━━━━━━━━━━━━━━━━━━━━\n\n"
                        "💎 *Mejora a Premium y obtén:*\n"
                        "✅ 50 videos cada día\n"
                        "✅ 50 canciones cada día\n"
                        "✅ 50 APK cada día\n"
                        "♻️ Límites se renuevan diario\n\n"
                        f"💰 Solo {PREMIUM_PRICE_STARS} ⭐ por 30 días\n\n"
                        "━━━━━━━━━━━━━━━━━━━━\n\n"
                        "⭐ Usa /premium para suscribirte",
                        parse_mode='Markdown'
                    )
                    return
        # Check music limits for premium
        elif content_type == 'music' and user['premium']:
            from database import check_and_reset_daily_limits
            check_and_reset_daily_limits(user_id)
            user = get_user(user_id)  # Refresh
            
            if user['daily_music'] >= PREMIUM_MUSIC_DAILY_LIMIT:
                await update.message.reply_text(
                    "⚠️ *Límite Diario Alcanzado*\n\n"
                    f"Has descargado {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT} canciones hoy.\n\n"
                    "♻️ Tu límite se renueva en 24 horas.\n\n"
                    "💡 Mientras esperas puedes descargar:\n"
                    "✨ Fotos: Ilimitadas\n"
                    f"🎬 Videos: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                    f"📦 APK: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}",
                    parse_mode='Markdown'
                )
                return
        # Check APK limits for premium
        elif content_type == 'apk' and user['premium']:
            from database import check_and_reset_daily_limits
            check_and_reset_daily_limits(user_id)
            user = get_user(user_id)  # Refresh
            
            if user['daily_apk'] >= PREMIUM_APK_DAILY_LIMIT:
                await update.message.reply_text(
                    "⚠️ *Límite Diario Alcanzado*\n\n"
                    f"Has descargado {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT} APK hoy.\n\n"
                    "♻️ Tu límite se renueva en 24 horas.\n\n"
                    "💡 Mientras esperas puedes descargar:\n"
                    "✨ Fotos: Ilimitadas\n"
                    f"🎬 Videos: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                    f"🎵 Música: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}",
                    parse_mode='Markdown'
                )
                return
        
        # Now process the download
        status = await update.message.reply_text("📤 Enviando...")
        
        # Try direct forward first
        try:
            await context.bot.forward_message(
                chat_id=user_id,
                from_chat_id=message.chat_id,
                message_id=message.id
            )
            await status.delete()
            
            # Show success message and update counters
            from database import increment_daily_counter
            
            if content_type == 'photo':
                from database import increment_daily_counter
                if user['premium']:
                    success_msg = "✅ *Descarga Completada*\n\n📸 Fotos ilimitadas con Premium ✨"
                    if joined_automatically:
                        success_msg += "\n\n🔗 Canal unido automáticamente"
                    await update.message.reply_text(success_msg, parse_mode='Markdown')
                else:
                    increment_daily_counter(user_id, 'photo')
                    user = get_user(user_id)
                    success_msg = (
                        f"✅ *Descarga Completada*\n\n"
                        f"📸 Fotos hoy: {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT}\n"
                        f"♻️ Se resetea en 24h\n\n"
                        f"💎 /premium para fotos ilimitadas"
                    )
                    if joined_automatically:
                        success_msg += "\n\n🔗 Canal unido automáticamente"
                    await update.message.reply_text(success_msg, parse_mode='Markdown')
            elif content_type == 'video':
                # Increment counters
                if user['premium']:
                    increment_daily_counter(user_id, 'video')
                    user = get_user(user_id)
                    success_msg = (
                        f"✅ *Descarga Completada*\n\n"
                        f"📊 Videos hoy: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                        f"♻️ Se resetea en 24h"
                    )
                    if joined_automatically:
                        success_msg += "\n\n🔗 Canal unido automáticamente"
                    await update.message.reply_text(success_msg, parse_mode='Markdown')
                else:
                    new_count = increment_download(user_id)
                    remaining = FREE_DOWNLOAD_LIMIT - new_count
                    success_msg = (
                        f"✅ *Descarga Completada*\n\n"
                        f"📊 Videos usados: {new_count}/{FREE_DOWNLOAD_LIMIT}\n"
                        f"🎁 Te quedan: *{remaining}* descargas\n\n"
                        f"💎 /premium para 50 videos diarios"
                    )
                    if joined_automatically:
                        success_msg += "\n\n🔗 Canal unido automáticamente"
                    await update.message.reply_text(success_msg, parse_mode='Markdown')
            elif content_type == 'music':
                increment_daily_counter(user_id, 'music')
                user = get_user(user_id)
                success_msg = (
                    f"✅ *Descarga Completada*\n\n"
                    f"🎵 Música hoy: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
                    f"♻️ Se resetea en 24h"
                )
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
            elif content_type == 'apk':
                increment_daily_counter(user_id, 'apk')
                user = get_user(user_id)
                success_msg = (
                    f"✅ *Descarga Completada*\n\n"
                    f"📦 APK hoy: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}\n"
                    f"♻️ Se resetea en 24h"
                )
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
            else:
                success_msg = "✅ *Descarga Completada*"
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
            
            return
        except Exception:
            pass
        
        # Download and send (for protected channels)
        await status.edit_text("📥 Descargando...")
        await download_and_send_media(message, user_id, context.bot)
        await status.delete()
        
        # Show success message and update counters
        from database import increment_daily_counter
        
        if content_type == 'photo':
            from database import increment_daily_counter
            if user['premium']:
                success_msg = "✅ *Descarga Completada*\n\n📸 Fotos ilimitadas con Premium ✨"
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
            else:
                increment_daily_counter(user_id, 'photo')
                user = get_user(user_id)
                success_msg = (
                    f"✅ *Descarga Completada*\n\n"
                    f"📸 Fotos hoy: {user['daily_photo']}/{FREE_PHOTO_DAILY_LIMIT}\n"
                    f"♻️ Se resetea en 24h\n\n"
                    f"💎 /premium para fotos ilimitadas"
                )
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
        elif content_type == 'video':
            # Increment counters
            if user['premium']:
                increment_daily_counter(user_id, 'video')
                user = get_user(user_id)
                success_msg = (
                    f"✅ *Descarga Completada*\n\n"
                    f"📊 Videos hoy: {user['daily_video']}/{PREMIUM_VIDEO_DAILY_LIMIT}\n"
                    f"♻️ Se resetea en 24h"
                )
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
            else:
                new_count = increment_download(user_id)
                remaining = FREE_DOWNLOAD_LIMIT - new_count
                success_msg = (
                    f"✅ *Descarga Completada*\n\n"
                    f"📊 Videos usados: {new_count}/{FREE_DOWNLOAD_LIMIT}\n"
                    f"🎁 Te quedan: *{remaining}* descargas\n\n"
                    f"💎 /premium para 50 videos diarios"
                )
                if joined_automatically:
                    success_msg += "\n\n🔗 Canal unido automáticamente"
                await update.message.reply_text(success_msg, parse_mode='Markdown')
        elif content_type == 'music':
            increment_daily_counter(user_id, 'music')
            user = get_user(user_id)
            success_msg = (
                f"✅ *Descarga Completada*\n\n"
                f"🎵 Música hoy: {user['daily_music']}/{PREMIUM_MUSIC_DAILY_LIMIT}\n"
                f"♻️ Se resetea en 24h"
            )
            if joined_automatically:
                success_msg += "\n\n🔗 Canal unido automáticamente"
            await update.message.reply_text(success_msg, parse_mode='Markdown')
        elif content_type == 'apk':
            increment_daily_counter(user_id, 'apk')
            user = get_user(user_id)
            success_msg = (
                f"✅ *Descarga Completada*\n\n"
                f"📦 APK hoy: {user['daily_apk']}/{PREMIUM_APK_DAILY_LIMIT}\n"
                f"♻️ Se resetea en 24h"
            )
            if joined_automatically:
                success_msg += "\n\n🔗 Canal unido automáticamente"
            await update.message.reply_text(success_msg, parse_mode='Markdown')
        else:
            success_msg = "✅ *Descarga Completada*"
            if joined_automatically:
                success_msg += "\n\n🔗 Canal unido automáticamente"
            await update.message.reply_text(success_msg, parse_mode='Markdown')
    
    except FloodWaitError as e:
        await update.message.reply_text(
            f"⏳ *Límite de Velocidad*\n\n"
            f"Espera {e.seconds} segundos e inténtalo nuevamente.",
            parse_mode='Markdown'
        )
    except Exception as e:
        import traceback
        logger.error(f"Error processing message: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        await update.message.reply_text(
            "❌ *Error Inesperado*\n\n"
            "Ocurrió un problema al procesar tu enlace.\n\n"
            "🔄 *Qué hacer:*\n"
            "1️⃣ Verifica que el enlace sea correcto\n"
            "2️⃣ Intenta con otro enlace\n"
            "3️⃣ Si el problema continúa, contacta al soporte\n\n"
            "💡 Puedes usar /help para ver la guía de uso.",
            parse_mode='Markdown'
        )


async def post_init(application: Application):
    """Initialize database and Telethon client"""
    init_database()
    await telethon_client.start()
    me = await telethon_client.get_me()
    logger.info(f"Telethon client connected as: {me.first_name}")
    
    # Set bot commands menu
    from telegram import BotCommand
    commands = [
        BotCommand("start", "🏠 Menú principal"),
        BotCommand("premium", "💎 Información de suscripción Premium"),
        BotCommand("stats", "📊 Ver estadísticas"),
        BotCommand("help", "📖 Guía de uso")
    ]
    await application.bot.set_my_commands(commands)


async def post_shutdown(application: Application):
    """Cleanup on shutdown"""
    await telethon_client.disconnect()


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).post_shutdown(post_shutdown).build()
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("premium", premium_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("testpay", testpay_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Add callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Add payment handlers
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("Bot started. Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
