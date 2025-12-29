#!/usr/bin/env python3
"""
Dashboard Web para administradores del bot
Accesible solo con token de administrador
VERSIÓN MEJORADA con más funcionalidades
"""

import os
import csv
import io
import shutil
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, send_file
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime, timedelta
import sqlite3
from database import get_user_stats
import logging

load_dotenv()

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv("DASHBOARD_SECRET_KEY", "cambiar-esta-clave-en-produccion")

# Token de administrador desde variables de entorno
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin123")

DB_FILE = "users.db"


def get_db_connection():
    """Conectar a la base de datos"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    """Decorador para verificar si el usuario está autenticado como admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================
# Health Check Endpoint (for Railway/Docker)
# ============================================================

@app.route('/health')
def health_check():
    """Health check endpoint for Railway and Docker"""
    try:
        # Check database connection
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'service': 'dashboard',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login para administradores"""
    if request.method == 'POST':
        # Support both 'token' (old) and 'password' (new) fields
        token = request.form.get('password') or request.form.get('token', '')
        if token == ADMIN_TOKEN:
            session['admin'] = True
            logger.info("Admin login successful")
            return redirect(url_for('dashboard'))
        else:
            logger.warning(f"Failed admin login attempt with token: {token[:5]}...")
            return render_template('login.html', error="Contraseña incorrecta")
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Cerrar sesión de admin"""
    session.clear()
    logger.info("Admin logout")
    return redirect(url_for('login'))


@app.route('/settings')
@login_required
def settings_page():
    """Página de configuración del sistema"""
    now = datetime.now().strftime('%d/%m/%Y %H:%M')
    # Get limits from env or defaults
    limits = {
        'photo': int(os.getenv('LIMIT_PHOTO', 5)),
        'video': int(os.getenv('LIMIT_VIDEO', 3)),
        'music': int(os.getenv('LIMIT_MUSIC', 5)),
        'apk': int(os.getenv('LIMIT_APK', 2))
    }
    return render_template('settings.html', now=now, limits=limits)


@app.route('/activity')
@login_required
def activity_page():
    """Página de actividad reciente"""
    return render_template('activity.html')


@app.route('/')
@login_required
def dashboard():
    """Dashboard principal con estadísticas generales"""
    stats = get_user_stats()
    # Format estimated revenue for display
    stats['estimated_revenue'] = f"{stats['revenue']['stars']:,} ⭐"
    stats['now'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render_template('dashboard.html', stats=stats, now=stats['now'])


@app.route('/api/users')
@login_required
def get_users():
    """API para obtener lista de todos los usuarios con sus datos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener búsqueda opcional
        search = request.args.get('search', '')
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        # Si hay búsqueda, filtrar por user_id
        if search:
            cursor.execute("""
                SELECT 
                    user_id,
                    first_name,
                    username,
                    downloads,
                    premium,
                    premium_until,
                    daily_photo,
                    daily_video,
                    daily_music,
                    daily_apk,
                    created_at,
                    updated_at
                FROM users
                WHERE user_id LIKE ? OR first_name LIKE ? OR username LIKE ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (f"%{search}%", f"%{search}%", f"%{search}%", per_page, offset))
        else:
            cursor.execute("""
                SELECT 
                    user_id,
                    first_name,
                    username,
                    downloads,
                    premium,
                    premium_until,
                    daily_photo,
                    daily_video,
                    daily_music,
                    daily_apk,
                    created_at,
                    updated_at
                FROM users
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (per_page, offset))
        
        users = []
        for row in cursor.fetchall():
            user_dict = dict(row)
            
            # Calcular días restantes de premium
            premium_days_left = None
            if user_dict['premium'] and user_dict['premium_until']:
                premium_until = datetime.fromisoformat(user_dict['premium_until'])
                days_left = (premium_until - datetime.now()).days
                premium_days_left = max(0, days_left)
            
            # Preparar datos para la respuesta
            users.append({
                'user_id': user_dict['user_id'],
                'first_name': user_dict['first_name'],
                'username': user_dict['username'],
                'downloads_count': user_dict['downloads'], # Renamed for frontend consistency
                'is_premium': bool(user_dict['premium']),
                'premium_expiry': user_dict['premium_until'], # Renamed for frontend consistency
                'premium_days_left': premium_days_left,
                'daily_photo': user_dict['daily_photo'],
                'daily_video': user_dict['daily_video'],
                'daily_music': user_dict['daily_music'],
                'daily_apk': user_dict['daily_apk'],
                'total_daily': (user_dict['daily_photo'] or 0) + (user_dict['daily_video'] or 0) + 
                              (user_dict['daily_music'] or 0) + (user_dict['daily_apk'] or 0),
                'created_at': user_dict['created_at'],
                'updated_at': user_dict['updated_at']
            })
        
        # Obtener total de usuarios
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'users': users,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'current_page': page
        })
    
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<int:user_id>')
@login_required
def get_user_detail(user_id):
    """API para obtener detalles detallados de un usuario específico"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        user_dict = dict(row)
        
        # Calcular información de premium
        premium_info = {
            'is_active': bool(user_dict['premium']),
            'level': user_dict.get('premium_level', 0),
            'expires_at': user_dict['premium_until']
        }
        
        if premium_info['is_active'] and user_dict['premium_until']:
            expires = datetime.fromisoformat(user_dict['premium_until'])
            days_left = (expires - datetime.now()).days
            premium_info['days_left'] = max(0, days_left)
            premium_info['expires_soon'] = days_left <= 3
        
        return jsonify({
            'user_id': user_dict['user_id'],
            'premium': premium_info,
            'downloads': user_dict['downloads'],
            'daily_usage': {
                'photos': user_dict.get('daily_photo', 0) or 0,
                'videos': user_dict.get('daily_video', 0) or 0,
                'music': user_dict.get('daily_music', 0) or 0,
                'apk': user_dict.get('daily_apk', 0) or 0
            },
            'created_at': user_dict['created_at'],
            'updated_at': user_dict['updated_at'],
            'language': user_dict.get('language', 'es')
        })
    
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
@login_required
def get_stats():
    """API para obtener estadísticas actualizadas"""
    try:
        stats = get_user_stats()
        # Format estimated revenue for display
        stats['estimated_revenue'] = f"{stats['revenue']['stars']:,} ⭐"
        
        # Add extra stats for dashboard
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Expired premium count
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE premium = 1 AND premium_until < ?
        """, (datetime.now().isoformat(),))
        stats['expired_premium'] = cursor.fetchone()[0]
        
        # Active today (users updated today)
        today = datetime.now().date().isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE date(updated_at) = ?
        """, (today,))
        stats['active_today'] = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics')
@login_required
def get_analytics():
    """API para datos de analytics y monetización"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Usuarios totales
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Usuarios premium
        cursor.execute("SELECT COUNT(*) FROM users WHERE premium = 1")
        premium_users = cursor.fetchone()[0]
        
        free_users = total_users - premium_users
        premium_percentage = round((premium_users / total_users * 100), 1) if total_users > 0 else 0
        
        # Descargas por tipo
        cursor.execute("SELECT SUM(downloads) FROM users")
        total_videos = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(daily_photo) FROM users")
        total_photos = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(daily_music) FROM users")
        total_music = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(daily_apk) FROM users")
        total_apks = cursor.fetchone()[0] or 0
        
        # Usuarios premium recientes
        cursor.execute("""
            SELECT user_id, first_name, username, downloads, premium_until, created_at
            FROM users 
            WHERE premium = 1 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        recent_premium = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Cálculos de monetización (asumiendo precio de $5 por premium)
        premium_price = 5.0  # Puedes cambiar esto
        estimated_revenue = premium_users * premium_price
        
        # Tasa de conversión (simplificada)
        conversion_rate = premium_percentage
        
        return jsonify({
            'total_users': total_users,
            'premium_users': premium_users,
            'free_users': free_users,
            'premium_percentage': premium_percentage,
            'estimated_revenue': estimated_revenue,
            'conversion_rate': conversion_rate,
            'total_videos': total_videos,
            'total_photos': total_photos,
            'total_music': total_music,
            'total_apks': total_apks,
            'recent_premium': recent_premium
        })
    
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/users')
@login_required
def users_list():
    """Página de listado de usuarios"""
    return render_template('users.html')


@app.route('/analytics')
@login_required
def analytics():
    """Página de analytics y monetización"""
    return render_template('analytics.html')


@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    """Página de detalles de un usuario"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return "Usuario no encontrado", 404

        user_data = dict(row)
        # Format data for template
        user = {
            'user_id': user_data['user_id'],
            'first_name': user_data['first_name'],
            'username': user_data['username'],
            'is_premium': bool(user_data['premium']),
            'premium_expiry': user_data['premium_until'],
            'joined_date': user_data['created_at'],
            'downloads_count': user_data['downloads'],
            'last_active': user_data['updated_at']
        }
        return render_template('user_detail.html', user=user)
    except Exception as e:
        logger.error(f"Error loading user detail: {e}")
        return "Error interno", 500


@app.route('/api/user/<int:user_id>/premium', methods=['POST', 'DELETE'])
@login_required
def manage_premium(user_id):
    """API para gestionar estado premium"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'POST':
            data = request.get_json()
            days = data.get('days', 30)
            
            # Calculate new expiry
            new_expiry = (datetime.now() + timedelta(days=days)).isoformat()
            
            cursor.execute("""
                UPDATE users 
                SET premium = 1, premium_until = ?, premium_level = 1
                WHERE user_id = ?
            """, (new_expiry, user_id))
            conn.commit()
            return jsonify({'success': True, 'message': f'Premium añadido por {days} días'})
            
        elif request.method == 'DELETE':
            cursor.execute("""
                UPDATE users 
                SET premium = 0, premium_until = NULL, premium_level = 0
                WHERE user_id = ?
            """, (user_id,))
            conn.commit()
            return jsonify({'success': True, 'message': 'Premium removido'})
            
    except Exception as e:
        logger.error(f"Error managing premium for {user_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/user/<int:user_id>/reset-stats', methods=['POST'])
@login_required
def reset_user_stats(user_id):
    """API para resetear estadísticas de un usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET downloads = 0, daily_photo = 0, daily_video = 0, 
                daily_music = 0, daily_apk = 0, last_reset = ?
            WHERE user_id = ?
        """, (datetime.now().isoformat(), user_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        return jsonify({'success': True, 'message': 'Estadísticas reseteadas'})
        
    except Exception as e:
        logger.error(f"Error resetting stats for {user_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """API para eliminar un usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404
            
        return jsonify({'success': True, 'message': 'Usuario eliminado'})
        
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


# ==================== NUEVAS APIs DE ADMINISTRACIÓN ====================

@app.route('/api/system-info')
@login_required
def get_system_info():
    """API para obtener información del sistema"""
    try:
        # Get database size
        db_size = "N/A"
        if os.path.exists(DB_FILE):
            size_bytes = os.path.getsize(DB_FILE)
            if size_bytes < 1024:
                db_size = f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                db_size = f"{size_bytes / 1024:.1f} KB"
            else:
                db_size = f"{size_bytes / (1024 * 1024):.2f} MB"
        
        return jsonify({
            'db_size': db_size,
            'server_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'db_file': DB_FILE
        })
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/users')
@login_required
def export_users_csv():
    """API para exportar usuarios a CSV"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Obtener filtros
        search = request.args.get('search', '')
        status = request.args.get('status', 'all')
        
        # Construir query con filtros
        query = """
            SELECT user_id, first_name, username, downloads, premium, 
                   premium_until, daily_photo, daily_video, daily_music, 
                   daily_apk, language, created_at, updated_at
            FROM users
        """
        conditions = []
        params = []
        
        if search:
            conditions.append("(user_id LIKE ? OR first_name LIKE ? OR username LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
        
        if status == 'premium':
            conditions.append("premium = 1")
        elif status == 'free':
            conditions.append("premium = 0")
        elif status == 'expired':
            conditions.append("premium = 1 AND premium_until < datetime('now')")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'User ID', 'Nombre', 'Username', 'Descargas', 'Premium',
            'Premium Hasta', 'Fotos Hoy', 'Videos Hoy', 'Música Hoy',
            'APKs Hoy', 'Idioma', 'Creado', 'Actualizado'
        ])
        
        # Data
        for row in rows:
            writer.writerow([
                row['user_id'],
                row['first_name'] or '',
                row['username'] or '',
                row['downloads'],
                'Sí' if row['premium'] else 'No',
                row['premium_until'] or '',
                row['daily_photo'] or 0,
                row['daily_video'] or 0,
                row['daily_music'] or 0,
                row['daily_apk'] or 0,
                row['language'] or 'es',
                row['created_at'] or '',
                row['updated_at'] or ''
            ])
        
        output.seek(0)
        
        # Generate filename with date
        filename = f"usuarios_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
        
    except Exception as e:
        logger.error(f"Error exporting users: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/backup')
@login_required
def backup_database():
    """API para descargar backup de la base de datos"""
    try:
        if not os.path.exists(DB_FILE):
            return jsonify({'error': 'Base de datos no encontrada'}), 404
        
        # Create a backup copy
        backup_filename = f"backup_users_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
        backup_path = f"/tmp/{backup_filename}"
        
        shutil.copy2(DB_FILE, backup_path)
        
        return send_file(
            backup_path,
            as_attachment=True,
            download_name=backup_filename,
            mimetype='application/x-sqlite3'
        )
        
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/reset-all-daily', methods=['POST'])
@login_required
def reset_all_daily():
    """API para resetear contadores diarios de todos los usuarios"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET daily_photo = 0, daily_video = 0, 
                daily_music = 0, daily_apk = 0, 
                last_reset = ?
        """, (datetime.now().isoformat(),))
        
        affected = cursor.rowcount
        conn.commit()
        
        logger.info(f"Admin reset all daily counters. Affected: {affected}")
        return jsonify({'success': True, 'affected': affected})
        
    except Exception as e:
        logger.error(f"Error resetting all daily: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/admin/clean-expired-premium', methods=['POST'])
@login_required
def clean_expired_premium():
    """API para limpiar usuarios con premium expirado"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        now = datetime.now().isoformat()
        
        cursor.execute("""
            UPDATE users 
            SET premium = 0, premium_level = 0
            WHERE premium = 1 AND premium_until < ?
        """, (now,))
        
        affected = cursor.rowcount
        conn.commit()
        
        logger.info(f"Cleaned expired premium. Affected: {affected}")
        return jsonify({'success': True, 'affected': affected})
        
    except Exception as e:
        logger.error(f"Error cleaning expired premium: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/admin/remove-all-premium', methods=['POST'])
@login_required
def remove_all_premium():
    """API para quitar premium a todos los usuarios"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET premium = 0, premium_level = 0, premium_until = NULL
            WHERE premium = 1
        """)
        
        affected = cursor.rowcount
        conn.commit()
        
        logger.warning(f"Admin removed ALL premium. Affected: {affected}")
        return jsonify({'success': True, 'affected': affected})
        
    except Exception as e:
        logger.error(f"Error removing all premium: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/admin/delete-inactive', methods=['POST'])
@login_required
def delete_inactive_users():
    """API para eliminar usuarios inactivos (30+ días)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        
        # Don't delete premium users
        cursor.execute("""
            DELETE FROM users 
            WHERE updated_at < ? AND premium = 0
        """, (cutoff,))
        
        affected = cursor.rowcount
        conn.commit()
        
        logger.warning(f"Deleted inactive users. Affected: {affected}")
        return jsonify({'success': True, 'affected': affected})
        
    except Exception as e:
        logger.error(f"Error deleting inactive users: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/admin/add-premium-bulk', methods=['POST'])
@login_required
def add_premium_bulk():
    """API para añadir premium a múltiples usuarios"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        days = data.get('days', 30)
        
        if not user_ids:
            return jsonify({'error': 'No se proporcionaron IDs de usuarios'}), 400
        
        new_expiry = (datetime.now() + timedelta(days=days)).isoformat()
        
        placeholders = ','.join(['?' for _ in user_ids])
        cursor.execute(f"""
            UPDATE users 
            SET premium = 1, premium_until = ?, premium_level = 1
            WHERE user_id IN ({placeholders})
        """, [new_expiry] + user_ids)
        
        affected = cursor.rowcount
        conn.commit()
        
        logger.info(f"Bulk premium added. Days: {days}, Affected: {affected}")
        return jsonify({'success': True, 'affected': affected})
        
    except Exception as e:
        logger.error(f"Error bulk adding premium: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route('/api/activity/stats')
@login_required
def get_activity_stats():
    """API para obtener estadísticas de actividad"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        
        # Today's downloads (sum of daily counters)
        cursor.execute("""
            SELECT COALESCE(SUM(daily_photo + daily_video + daily_music + daily_apk), 0)
            FROM users
            WHERE date(last_reset) = ?
        """, (today,))
        today_downloads = cursor.fetchone()[0]
        
        # New users today
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE date(created_at) = ?
        """, (today,))
        new_users_today = cursor.fetchone()[0]
        
        # Active premium
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE premium = 1 AND premium_until > ?
        """, (datetime.now().isoformat(),))
        active_premium = cursor.fetchone()[0]
        
        # Expiring in 3 days
        three_days = (datetime.now() + timedelta(days=3)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE premium = 1 AND premium_until BETWEEN ? AND ?
        """, (datetime.now().isoformat(), three_days))
        expiring_soon = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'today_downloads': today_downloads,
            'new_users_today': new_users_today,
            'active_premium': active_premium,
            'expiring_soon': expiring_soon
        })
        
    except Exception as e:
        logger.error(f"Error getting activity stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/activity')
@login_required
def get_activity():
    """API para obtener actividad reciente (simulada desde datos de usuarios)"""
    try:
        page = request.args.get('page', 1, type=int)
        filter_type = request.args.get('filter', 'all')
        per_page = 20
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        activities = []
        
        # Get recent user activity based on updated_at
        cursor.execute("""
            SELECT user_id, first_name, username, downloads, premium, 
                   premium_until, daily_photo, daily_video, daily_music, 
                   daily_apk, created_at, updated_at
            FROM users
            ORDER BY updated_at DESC
            LIMIT ? OFFSET ?
        """, (per_page, offset))
        
        rows = cursor.fetchall()
        
        for row in rows:
            user_name = row['first_name'] or f"Usuario #{row['user_id']}"
            
            # Check what kind of activity this might be
            if filter_type in ['all', 'downloads']:
                total_daily = (row['daily_photo'] or 0) + (row['daily_video'] or 0) + \
                             (row['daily_music'] or 0) + (row['daily_apk'] or 0)
                
                if total_daily > 0:
                    activities.append({
                        'type': 'download',
                        'title': 'Descarga realizada',
                        'description': f'{user_name} realizó {total_daily} descarga(s) hoy',
                        'user_id': row['user_id'],
                        'timestamp': row['updated_at']
                    })
            
            if filter_type in ['all', 'premium']:
                if row['premium'] and row['premium_until']:
                    # Check if premium was recently added (within last day)
                    activities.append({
                        'type': 'premium',
                        'title': 'Usuario Premium',
                        'description': f'{user_name} tiene premium activo',
                        'user_id': row['user_id'],
                        'timestamp': row['updated_at']
                    })
            
            if filter_type in ['all', 'users']:
                # Check if new user (created recently)
                created = datetime.fromisoformat(row['created_at']) if row['created_at'] else None
                if created and (datetime.now() - created).days < 7:
                    activities.append({
                        'type': 'user',
                        'title': 'Nuevo usuario',
                        'description': f'{user_name} se registró',
                        'user_id': row['user_id'],
                        'timestamp': row['created_at']
                    })
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x['timestamp'] or '', reverse=True)
        activities = activities[:per_page]
        
        # Check if there's more
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        has_more = (page * per_page) < total
        
        conn.close()
        
        return jsonify({
            'activities': activities,
            'has_more': has_more,
            'page': page
        })
        
    except Exception as e:
        logger.error(f"Error getting activity: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/filter')
@login_required
def filter_users():
    """API avanzada para filtrar usuarios"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get filter parameters
        status = request.args.get('status', 'all')  # all, premium, free, expired
        sort_by = request.args.get('sort', 'created_at')  # created_at, downloads, updated_at
        order = request.args.get('order', 'desc')  # asc, desc
        min_downloads = request.args.get('min_downloads', 0, type=int)
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        # Build query
        conditions = []
        params = []
        
        if status == 'premium':
            conditions.append("premium = 1 AND premium_until > ?")
            params.append(datetime.now().isoformat())
        elif status == 'free':
            conditions.append("premium = 0")
        elif status == 'expired':
            conditions.append("premium = 1 AND premium_until < ?")
            params.append(datetime.now().isoformat())
        
        if min_downloads > 0:
            conditions.append("downloads >= ?")
            params.append(min_downloads)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        
        # Validate sort column
        valid_sorts = ['created_at', 'downloads', 'updated_at', 'user_id', 'premium']
        if sort_by not in valid_sorts:
            sort_by = 'created_at'
        
        order_dir = 'DESC' if order == 'desc' else 'ASC'
        
        query = f"""
            SELECT user_id, first_name, username, downloads, premium, 
                   premium_until, created_at, updated_at
            FROM users
            {where_clause}
            ORDER BY {sort_by} {order_dir}
            LIMIT ? OFFSET ?
        """
        
        params.extend([per_page, offset])
        cursor.execute(query, params)
        
        users = []
        for row in cursor.fetchall():
            user_dict = dict(row)
            premium_days_left = None
            if user_dict['premium'] and user_dict['premium_until']:
                premium_until = datetime.fromisoformat(user_dict['premium_until'])
                days_left = (premium_until - datetime.now()).days
                premium_days_left = max(0, days_left)
            
            users.append({
                'user_id': user_dict['user_id'],
                'first_name': user_dict['first_name'],
                'username': user_dict['username'],
                'downloads_count': user_dict['downloads'],
                'is_premium': bool(user_dict['premium']),
                'premium_expiry': user_dict['premium_until'],
                'premium_days_left': premium_days_left,
                'created_at': user_dict['created_at'],
                'updated_at': user_dict['updated_at']
            })
        
        # Get total with same filters
        count_query = f"SELECT COUNT(*) FROM users {where_clause}"
        cursor.execute(count_query, params[:-2] if params else [])  # Exclude LIMIT/OFFSET params
        total = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'users': users,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'current_page': page
        })
        
    except Exception as e:
        logger.error(f"Error filtering users: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment (Railway provides PORT)
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    logger.info(f"Dashboard iniciando en {host}:{port}...")
    app.run(debug=False, host=host, port=port)
