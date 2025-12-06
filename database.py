#!/usr/bin/env python3
"""
Database module for user management and payment tracking
"""

import sqlite3
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

DB_FILE = "users.db"


def init_database():
    """Initialize the SQLite database with users table"""
    conn = sqlite3.connect(DB_FILE)
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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add new columns if they don't exist (for migration)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN premium_level INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN daily_photo INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN daily_video INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN daily_music INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN daily_apk INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def get_user(user_id: int) -> Optional[Dict]:
    """
    Get user information from database
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        Dict with user data or None if user doesn't exist
    """
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        """SELECT user_id, downloads, premium, premium_level, premium_until, 
           daily_photo, daily_video, daily_music, daily_apk, last_reset 
           FROM users WHERE user_id = ?""",
        (user_id,)
    )
    
    row = cursor.fetchone()
    
    if row:
        premium = bool(row[2])
        premium_level = row[3] or 0
        premium_until = row[4]
        last_reset = row[9]
        
        # Check if premium expired
        if premium and premium_until:
            expiry = datetime.fromisoformat(premium_until)
            if datetime.now() > expiry:
                cursor.execute(
                    "UPDATE users SET premium = 0, premium_level = 0 WHERE user_id = ?", 
                    (user_id,)
                )
                conn.commit()
                premium = False
                premium_level = 0
        
        # Check if daily counters need reset (24 hours)
        if last_reset:
            last_reset_dt = datetime.fromisoformat(last_reset)
            if datetime.now() - last_reset_dt > timedelta(hours=24):
                cursor.execute(
                    """UPDATE users SET daily_photo = 0, daily_video = 0, 
                       daily_music = 0, daily_apk = 0, last_reset = ? 
                       WHERE user_id = ?""",
                    (datetime.now().isoformat(), user_id)
                )
                conn.commit()
                # Reset counters in returned data
                row = (row[0], row[1], premium, premium_level, row[4], 0, 0, 0, 0, datetime.now().isoformat())
        
        conn.close()
        
        return {
            "user_id": row[0],
            "downloads": row[1],
            "premium": premium,
            "premium_level": premium_level,
            "premium_until": premium_until,
            "daily_photo": row[5] or 0,
            "daily_video": row[6] or 0,
            "daily_music": row[7] or 0,
            "daily_apk": row[8] or 0,
            "last_reset": row[9] if len(row) > 9 else None
        }
    
    conn.close()
    return None


def create_user(user_id: int):
    """
    Create a new user in the database
    
    Args:
        user_id: Telegram user ID
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, downloads, premium) VALUES (?, 0, 0)",
        (user_id,)
    )
    
    conn.commit()
    conn.close()
    logger.info(f"Created new user: {user_id}")


def increment_download(user_id: int) -> int:
    """
    Increment download count for a user
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        New download count
    """
    # Ensure user exists
    if not get_user(user_id):
        create_user(user_id)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE users SET downloads = downloads + 1, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
        (user_id,)
    )
    
    cursor.execute("SELECT downloads FROM users WHERE user_id = ?", (user_id,))
    new_count = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    logger.info(f"User {user_id} downloads: {new_count}")
    return new_count


def increment_daily_counter(user_id: int, content_type: str) -> int:
    """
    Increment daily counter for specific content type
    
    Args:
        user_id: Telegram user ID
        content_type: 'photo', 'video', 'music', or 'apk'
        
    Returns:
        New counter value for that type
    """
    if content_type not in ['photo', 'video', 'music', 'apk']:
        raise ValueError(f"Invalid content_type: {content_type}")
    
    # Ensure user exists
    if not get_user(user_id):
        create_user(user_id)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    column_name = f"daily_{content_type}"
    cursor.execute(
        f"UPDATE users SET {column_name} = {column_name} + 1, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
        (user_id,)
    )
    
    cursor.execute(f"SELECT {column_name} FROM users WHERE user_id = ?", (user_id,))
    new_count = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    logger.info(f"User {user_id} daily_{content_type}: {new_count}")
    return new_count


def set_premium(user_id: int, months: int = 1, level: int = 1):
    """
    Set user as premium/vip for specified months
    
    Args:
        user_id: Telegram user ID
        months: Number of months to add (default 1)
        level: Premium level (1 = premium, 2 = vip)
    """
    from datetime import datetime, timedelta
    
    # Ensure user exists
    if not get_user(user_id):
        create_user(user_id)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get current premium_until
    cursor.execute("SELECT premium_until FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    current_until = row[0] if row else None
    
    # Calculate new expiry date
    if current_until:
        # Extend from current expiry
        current_expiry = datetime.fromisoformat(current_until)
        if current_expiry > datetime.now():
            new_expiry = current_expiry + timedelta(days=30 * months)
        else:
            new_expiry = datetime.now() + timedelta(days=30 * months)
    else:
        # New premium user
        new_expiry = datetime.now() + timedelta(days=30 * months)
    
    cursor.execute(
        """UPDATE users SET premium = 1, premium_level = ?, premium_until = ?, 
           updated_at = CURRENT_TIMESTAMP WHERE user_id = ?""",
        (level, new_expiry.isoformat(), user_id)
    )
    
    conn.commit()
    conn.close()
    
    level_name = "VIP" if level == 2 else "Premium"
    logger.info(f"User {user_id} upgraded to {level_name} until {new_expiry}")


def check_and_reset_daily_limits(user_id: int):
    """
    Check if 24 hours have passed and reset daily counters if needed
    
    Args:
        user_id: Telegram user ID
    """
    from datetime import datetime, timedelta
    
    user = get_user(user_id)
    if not user:
        return
    
    # Check if last_reset exists and if 24 hours have passed
    if user['last_reset']:
        try:
            last_reset = datetime.fromisoformat(user['last_reset'])
            now = datetime.now()
            
            # If more than 24 hours have passed, reset counters
            if now - last_reset >= timedelta(hours=24):
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                
                cursor.execute(
                    """UPDATE users SET daily_photo = 0, daily_video = 0, daily_music = 0, 
                       daily_apk = 0, last_reset = CURRENT_TIMESTAMP WHERE user_id = ?""",
                    (user_id,)
                )
                
                conn.commit()
                conn.close()
                
                logger.info(f"Daily limits reset for user {user_id}")
        except ValueError:
            # Invalid datetime format, set current time
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET last_reset = CURRENT_TIMESTAMP WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()


def get_user_stats() -> Dict:
    """Get database statistics"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE premium = 1")
    premium_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(downloads) FROM users")
    total_downloads = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_users": total_users,
        "premium_users": premium_users,
        "free_users": total_users - premium_users,
        "total_downloads": total_downloads
    }
