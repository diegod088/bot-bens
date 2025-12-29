#!/usr/bin/env python3
"""
Startup script for Railway deployment
Runs both the Telegram bot and the Dashboard web server simultaneously
"""

import os
import sys
import threading
import signal
import logging
import time
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Flag for graceful shutdown
shutdown_event = threading.Event()


def run_dashboard():
    """Run the Flask dashboard in a separate thread"""
    try:
        # Import here to avoid circular imports
        from dashboard import app
        
        # Get port from environment (Railway provides PORT)
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        
        logger.info(f"🌐 Starting Dashboard on {host}:{port}")
        
        # Use waitress for production if available, otherwise use Flask's built-in server
        try:
            from waitress import serve
            serve(app, host=host, port=port, threads=4)
        except ImportError:
            # Fallback to Flask's built-in server (not recommended for production)
            app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
            
    except Exception as e:
        logger.error(f"❌ Dashboard error: {e}")
        raise


def run_bot():
    """Run the Telegram bot (blocking, runs in separate thread)"""
    try:
        logger.info("🤖 Starting Telegram Bot...")
        
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Import and run the bot's async main function
            from bot_with_paywall import async_main
            loop.run_until_complete(async_main())
            
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        raise


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("🛑 Shutdown signal received, stopping services...")
    shutdown_event.set()
    sys.exit(0)


def main():
    """Main entry point - runs both services"""
    logger.info("=" * 60)
    logger.info("🚀 RAILWAY DEPLOYMENT STARTING")
    logger.info("=" * 60)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check required environment variables
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_API_ID', 
        'TELEGRAM_API_HASH',
        'ADMIN_TOKEN'
    ]
    
    # Alternative variable names
    alt_vars = {
        'TELEGRAM_BOT_TOKEN': 'TELEGRAM_TOKEN',
        'TELEGRAM_API_ID': 'API_ID',
        'TELEGRAM_API_HASH': 'API_HASH'
    }
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            # Check alternative name
            alt = alt_vars.get(var)
            if alt and os.environ.get(alt):
                continue
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {missing_vars}")
        logger.error("Please set these in your Railway project settings")
        sys.exit(1)
    
    logger.info("✅ All required environment variables found")
    
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True, name="TelegramBot")
    bot_thread.start()
    logger.info("✅ Bot thread started")
    
    # Give the bot a moment to start
    time.sleep(2)
    
    # Run the dashboard in the main thread (blocking)
    logger.info("🌐 Starting Dashboard in main thread")
    run_dashboard()


if __name__ == '__main__':
    main()
