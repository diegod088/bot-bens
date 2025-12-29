#!/usr/bin/env python3
"""
Database module for user management and payment tracking
VERSIÓN OPTIMIZADA con mejores prácticas
"""

import sqlite3
import logging
from typing import Optional, Dict
from contextlib import contextmanager
from datetime import datetime, timedelta
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    logger.warning("⚠️ ENCRYPTION_KEY no encontrada en variables de entorno. Las funciones de sesión fallarán.")
else:
    logger.info("✅ ENCRYPTION_KEY cargada correctamente.")

DB_FILE = "users.db"


# ==================== CONTEXT MANAGER PARA CONEXIONES ====================

@contextmanager
def get_db_connection():
    """
    Context manager para conexiones SQLite
    Garantiza que la conexión siempre se cierra
    """
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()


# ==================== INICIALIZACIÓN ====================

def init_database():
    """Initialize the SQLite database with users table"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                language TEXT DEFAULT 'es'
            )
        """)
        
        # Add language column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'es'")
            logger.info("Added language column to users table")
        except sqlite3.OperationalError:
            # Column already exists
            pass

        # Add session_string column
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN session_string TEXT DEFAULT NULL")
            logger.info("Added session_string column to users table")
        except sqlite3.OperationalError:
            pass

        # Add phone_hash column
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN phone_hash TEXT DEFAULT NULL")
            logger.info("Added phone_hash column to users table")
        except sqlite3.OperationalError:
            pass

        # Add first_name column
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN first_name TEXT DEFAULT NULL")
            logger.info("Added first_name column to users table")
        except sqlite3.OperationalError:
            pass

        # Add username column
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN username TEXT DEFAULT NULL")
            logger.info("Added username column to users table")
        except sqlite3.OperationalError:
            pass
        
        # Índices para mejorar rendimiento
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_premium ON users(premium)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_last_reset ON users(last_reset)")
        
    logger.info("Database initialized successfully")


# ==================== OPERACIONES DE USUARIO ====================

def get_user(user_id: int, auto_reset: bool = True) -> Optional[Dict]:
    """
    Get user information from database
    
    Args:
        user_id: Telegram user ID
        auto_reset: Si True, resetea automáticamente límites expirados
        
    Returns:
        Dict with user data or None if user doesn't exist
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """SELECT user_id, first_name, username, downloads, premium, premium_level, premium_until, 
               daily_photo, daily_video, daily_music, daily_apk, last_reset, language 
               FROM users WHERE user_id = ?""",
            (user_id,)
        )
        
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Convertir Row a dict
        user_data = dict(row)
        
        # Check if premium expired
        if auto_reset and user_data['premium'] and user_data['premium_until']:
            expiry = datetime.fromisoformat(user_data['premium_until'])
            if datetime.now() > expiry:
                cursor.execute(
                    "UPDATE users SET premium = 0, premium_level = 0 WHERE user_id = ?", 
                    (user_id,)
                )
                user_data['premium'] = 0
                user_data['premium_level'] = 0
        
        # Check if daily counters need reset
        if auto_reset and user_data['last_reset']:
            last_reset_dt = datetime.fromisoformat(user_data['last_reset'])
            if datetime.now() - last_reset_dt > timedelta(hours=24):
                cursor.execute(
                    """UPDATE users SET 
                       daily_photo = 0, daily_video = 0, 
                       daily_music = 0, daily_apk = 0, 
                       last_reset = ? 
                       WHERE user_id = ?""",
                    (datetime.now().isoformat(), user_id)
                )
                user_data.update({
                    'daily_photo': 0,
                    'daily_video': 0,
                    'daily_music': 0,
                    'daily_apk': 0,
                    'last_reset': datetime.now().isoformat()
                })
        
        # Asegurar valores por defecto
        user_data['premium'] = bool(user_data['premium'])
        for key in ['daily_photo', 'daily_video', 'daily_music', 'daily_apk']:
            if user_data[key] is None:
                user_data[key] = 0
        
        return user_data


def create_user(user_id: int, first_name: str = None, username: str = None) -> bool:
    """
    Create a new user in the database or update existing info
    
    Args:
        user_id: Telegram user ID
        first_name: User's first name
        username: User's username (optional)
        
    Returns:
        True si se creó, False si ya existía (pero se actualizó info)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Intentar insertar
        try:
            cursor.execute(
                "INSERT INTO users (user_id, first_name, username, downloads, premium) VALUES (?, ?, ?, 0, 0)",
                (user_id, first_name, username)
            )
            return True
        except sqlite3.IntegrityError:
            # Si ya existe, actualizar nombre y username
            if first_name or username:
                cursor.execute(
                    "UPDATE users SET first_name = ?, username = ? WHERE user_id = ?",
                    (first_name, username, user_id)
                )
            return False
        if created:
            logger.info(f"Created new user: {user_id}")
        
        return created


def ensure_user_exists(user_id: int):
    """Garantiza que el usuario exista en la DB"""
    if not get_user(user_id, auto_reset=False):
        create_user(user_id)


# ==================== CONTADORES ====================

def increment_total_downloads(user_id: int) -> int:
    """
    Incrementa el contador TOTAL de descargas (videos lifetime)
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        Nuevo contador total
    """
    ensure_user_exists(user_id)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE users 
               SET downloads = downloads + 1, 
                   updated_at = CURRENT_TIMESTAMP 
               WHERE user_id = ?""",
            (user_id,)
        )
        
        cursor.execute("SELECT downloads FROM users WHERE user_id = ?", (user_id,))
        new_count = cursor.fetchone()[0]
        
        logger.info(f"User {user_id} total downloads: {new_count}")
        return new_count


def increment_daily_counter(user_id: int, content_type: str) -> int:
    """
    Incrementa contador diario para tipo de contenido específico
    
    Args:
        user_id: Telegram user ID
        content_type: 'photo', 'video', 'music', or 'apk'
        
    Returns:
        Nuevo valor del contador
        
    Raises:
        ValueError: Si content_type no es válido
    """
    VALID_TYPES = {'photo', 'video', 'music', 'apk'}
    
    if content_type not in VALID_TYPES:
        raise ValueError(f"Invalid content_type: {content_type}. Must be one of {VALID_TYPES}")
    
    ensure_user_exists(user_id)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Usar parámetro para nombre de columna de forma segura
        column_name = f"daily_{content_type}"
        
        # Validación extra de seguridad
        cursor.execute("PRAGMA table_info(users)")
        valid_columns = [col[1] for col in cursor.fetchall()]
        if column_name not in valid_columns:
            raise ValueError(f"Column {column_name} does not exist")
        
        cursor.execute(
            f"""UPDATE users 
                SET {column_name} = {column_name} + 1, 
                    updated_at = CURRENT_TIMESTAMP 
                WHERE user_id = ?""",
            (user_id,)
        )
        
        cursor.execute(f"SELECT {column_name} FROM users WHERE user_id = ?", (user_id,))
        new_count = cursor.fetchone()[0]
        
        logger.info(f"User {user_id} {column_name}: {new_count}")
        return new_count


def increment_counters(user_id: int, total: bool = False, **daily_counters) -> Dict[str, int]:
    """
    Incrementa múltiples contadores en una sola transacción
    
    Args:
        user_id: Telegram user ID
        total: Si True, incrementa contador total de descargas
        **daily_counters: photo=1, video=1, music=1, apk=1
        
    Returns:
        Dict con los nuevos valores de los contadores
        
    Example:
        increment_counters(123, total=True, video=1)
        increment_counters(123, photo=1)
    """
    ensure_user_exists(user_id)
    
    result = {}
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Construir UPDATE dinámico
        updates = []
        if total:
            updates.append("downloads = downloads + 1")
        
        VALID_DAILY = {'photo', 'video', 'music', 'apk'}
        for content_type, increment in daily_counters.items():
            if content_type not in VALID_DAILY:
                logger.warning(f"Ignored invalid counter: {content_type}")
                continue
            
            if increment > 0:
                updates.append(f"daily_{content_type} = daily_{content_type} + {int(increment)}")
        
        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, (user_id,))
        
        # Obtener valores actualizados
        cursor.execute(
            """SELECT downloads, daily_photo, daily_video, daily_music, daily_apk 
               FROM users WHERE user_id = ?""",
            (user_id,)
        )
        
        row = cursor.fetchone()
        result = {
            'total_downloads': row[0],
            'daily_photo': row[1],
            'daily_video': row[2],
            'daily_music': row[3],
            'daily_apk': row[4]
        }
    
    logger.info(f"User {user_id} counters updated: {result}")
    return result


# ==================== PREMIUM ====================

def set_premium(user_id: int, months: int = 1, level: int = 1):
    """
    Set user as premium/vip for specified months
    
    Args:
        user_id: Telegram user ID
        months: Number of months to add (default 1)
        level: Premium level (1 = premium, 2 = vip)
    """
    ensure_user_exists(user_id)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get current premium_until
        cursor.execute("SELECT premium_until FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        current_until = row[0] if row else None
        
        # Calculate new expiry date
        if current_until:
            current_expiry = datetime.fromisoformat(current_until)
            if current_expiry > datetime.now():
                new_expiry = current_expiry + timedelta(days=30 * months)
            else:
                new_expiry = datetime.now() + timedelta(days=30 * months)
        else:
            new_expiry = datetime.now() + timedelta(days=30 * months)
        
        cursor.execute(
            """UPDATE users 
               SET premium = 1, 
                   premium_level = ?, 
                   premium_until = ?, 
                   updated_at = CURRENT_TIMESTAMP 
               WHERE user_id = ?""",
            (level, new_expiry.isoformat(), user_id)
        )
    
    level_name = "VIP" if level == 2 else "Premium"
    logger.info(f"User {user_id} upgraded to {level_name} until {new_expiry}")


def set_user_language(user_id: int, language: str = 'es'):
    """
    Set user's preferred language
    
    Args:
        user_id: Telegram user ID
        language: Language code ('es', 'en', 'pt', 'it')
    """
    ensure_user_exists(user_id)
    
    # Validate language
    if language not in ['es', 'en', 'pt', 'it']:
        language = 'es'
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE users 
               SET language = ?, 
                   updated_at = CURRENT_TIMESTAMP 
               WHERE user_id = ?""",
            (language, user_id)
        )
    
    logger.info(f"User {user_id} language set to {language}")


# ==================== RESET DE LÍMITES ====================

def check_and_reset_daily_limits(user_id: int) -> bool:
    """
    Check if 24 hours have passed and reset daily counters if needed
    ONLY FOR PREMIUM USERS - Free users have permanent limits
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True si se resetearon los límites, False si no era necesario
    """
    user = get_user(user_id, auto_reset=False)
    if not user or not user['last_reset']:
        return False
    
    # SOLO usuarios PREMIUM tienen reset de límites diarios
    # Usuarios FREE tienen límites PERMANENTES (no se reinician)
    if not user['premium']:
        return False
    
    last_reset_dt = datetime.fromisoformat(user['last_reset'])
    
    if datetime.now() - last_reset_dt < timedelta(hours=24):
        return False
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE users 
               SET daily_photo = 0, 
                   daily_video = 0, 
                   daily_music = 0, 
                   daily_apk = 0, 
                   last_reset = CURRENT_TIMESTAMP 
               WHERE user_id = ?""",
            (user_id,)
        )
    
    logger.info(f"Daily limits reset for PREMIUM user {user_id}")
    return True


# ==================== ESTADÍSTICAS ====================

def get_user_usage_stats(user_id: int, free_video_limit: int = 3, free_photo_limit: int = 10) -> Optional[Dict]:
    """
    Obtiene estadísticas de uso del usuario con límites
    
    Args:
        user_id: ID del usuario
        free_video_limit: Límite de videos totales para usuarios gratuitos
        free_photo_limit: Límite de fotos diarias para usuarios gratuitos
        
    Returns:
        Dict con información de uso y límites restantes o None
    """
    user = get_user(user_id)
    if not user:
        return None
    
    is_premium = user['premium']
    
    stats = {
        'is_premium': is_premium,
        'videos': {
            'used': user['downloads'],
            'limit': None if is_premium else free_video_limit,
            'remaining': None if is_premium else max(0, free_video_limit - user['downloads']),
            'unlimited': is_premium
        },
        'photos': {
            'used': user['daily_photo'],
            'limit': None if is_premium else free_photo_limit,
            'remaining': None if is_premium else max(0, free_photo_limit - user['daily_photo']),
            'unlimited': is_premium
        },
        'music': {
            'available': is_premium,
            'used': user['daily_music'] if is_premium else 0,
            'limit': 50 if is_premium else 0,
            'remaining': max(0, 50 - user['daily_music']) if is_premium else 0
        },
        'apk': {
            'available': is_premium,
            'used': user['daily_apk'] if is_premium else 0,
            'limit': 50 if is_premium else 0,
            'remaining': max(0, 50 - user['daily_apk']) if is_premium else 0
        }
    }
    
    return stats


def check_low_usage_warning(user_id: int, free_video_limit: int = 3, free_photo_limit: int = 10) -> Dict:
    """
    Verifica si el usuario está cerca de alcanzar sus límites
    
    Args:
        user_id: ID del usuario
        free_video_limit: Límite de videos totales
        free_photo_limit: Límite de fotos diarias
        
    Returns:
        Dict con warnings
    """
    stats = get_user_usage_stats(user_id, free_video_limit, free_photo_limit)
    
    if not stats or stats['is_premium']:
        return {'show_warning': False, 'type': None}
    
    # Advertir cuando queda 1 uso de videos
    videos_remaining = stats['videos']['remaining']
    if videos_remaining <= 1 and videos_remaining > 0:
        return {
            'show_warning': True,
            'type': 'video',
            'remaining': videos_remaining,
            'limit': free_video_limit,
            'percentage': (stats['videos']['used'] / free_video_limit) * 100
        }
    
    # Advertir cuando quedan 2 fotos o menos
    photos_remaining = stats['photos']['remaining']
    if photos_remaining <= 2 and photos_remaining > 0:
        return {
            'show_warning': True,
            'type': 'photo',
            'remaining': photos_remaining,
            'limit': free_photo_limit,
            'percentage': (stats['photos']['used'] / free_photo_limit) * 100
        }
    
    return {'show_warning': False, 'type': None}


def get_user_stats() -> Dict:
    """
    Get comprehensive database statistics
    
    Returns:
        Dict with detailed bot statistics
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Usuarios totales
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Usuarios premium
        cursor.execute("SELECT COUNT(*) FROM users WHERE premium = 1")
        premium_users = cursor.fetchone()[0]
        
        # Descargas totales (videos)
        cursor.execute("SELECT SUM(downloads) FROM users")
        total_downloads = cursor.fetchone()[0] or 0
        
        # Usuarios activos hoy (con descargas en las últimas 24h)
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE updated_at >= datetime('now', '-1 day')
        """)
        active_today = cursor.fetchone()[0]
        
        # Total de fotos descargadas hoy
        cursor.execute("SELECT SUM(daily_photo) FROM users")
        total_photos_today = cursor.fetchone()[0] or 0
        
        # Total de videos descargados hoy
        cursor.execute("SELECT SUM(daily_video) FROM users")
        total_videos_today = cursor.fetchone()[0] or 0
        
        # Total de música descargada hoy
        cursor.execute("SELECT SUM(daily_music) FROM users")
        total_music_today = cursor.fetchone()[0] or 0
        
        # Total de APKs descargados hoy
        cursor.execute("SELECT SUM(daily_apk) FROM users")
        total_apk_today = cursor.fetchone()[0] or 0
        
        # Ingresos estimados (300 stars por premium)
        # Asumimos que cada usuario premium pagó 300 stars
        estimated_revenue = premium_users * 300
        
        return {
            "total_users": total_users,
            "premium_users": premium_users,
            "free_users": total_users - premium_users,
            "total_downloads": total_downloads,
            "active_today": active_today,
            "daily_stats": {
                "photos": total_photos_today,
                "videos": total_videos_today,
                "music": total_music_today,
                "apk": total_apk_today,
                "total": total_photos_today + total_videos_today + total_music_today + total_apk_today
            },
            "revenue": {
                "stars": estimated_revenue,
                "premium_subs": premium_users
            }
        }


# ==================== GESTIÓN DE SESIONES (USERBOT) ====================

def _get_cipher_suite():
    """Obtiene la instancia de Fernet para encriptación"""
    if not ENCRYPTION_KEY:
        raise ValueError("CRITICAL: La variable de entorno 'ENCRYPTION_KEY' no está configurada. Configúrala en Railway/Replit o en el archivo .env")
    try:
        return Fernet(ENCRYPTION_KEY.encode())
    except Exception as e:
        raise ValueError(f"CRITICAL: La 'ENCRYPTION_KEY' es inválida. Asegúrate de que sea una clave Fernet válida. Error: {e}")

def encrypt_session(session_string: str) -> Optional[str]:
    """Encripta la cadena de sesión"""
    if not session_string:
        return None
    cipher_suite = _get_cipher_suite()
    return cipher_suite.encrypt(session_string.encode()).decode()

def decrypt_session(encrypted_session: str) -> Optional[str]:
    """Desencripta la cadena de sesión"""
    if not encrypted_session:
        return None
    cipher_suite = _get_cipher_suite()
    return cipher_suite.decrypt(encrypted_session.encode()).decode()

def hash_phone(phone_number: str) -> str:
    """Hashea el número de teléfono para privacidad"""
    return hashlib.sha256(phone_number.encode()).hexdigest()

def set_user_session(user_id: int, session_string: str, phone_number: str) -> bool:
    """
    Guarda la sesión encriptada del usuario
    """
    ensure_user_exists(user_id)
    encrypted_session = encrypt_session(session_string)
    phone_hash_val = hash_phone(phone_number)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET session_string = ?, phone_hash = ? WHERE user_id = ?",
            (encrypted_session, phone_hash_val, user_id)
        )
        return cursor.rowcount > 0

def get_user_session(user_id: int) -> Optional[str]:
    """
    Obtiene y desencripta la sesión del usuario
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT session_string FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row and row['session_string']:
            try:
                return decrypt_session(row['session_string'])
            except Exception as e:
                logger.error(f"Error decrypting session for user {user_id}: {e}")
                return None
    return None

def delete_user_session(user_id: int) -> bool:
    """Elimina la sesión del usuario"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET session_string = NULL, phone_hash = NULL WHERE user_id = ?",
            (user_id,)
        )
        return cursor.rowcount > 0

def has_active_session(user_id: int) -> bool:
    """Verifica si el usuario tiene una sesión activa"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT session_string FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return bool(row and row['session_string'])

