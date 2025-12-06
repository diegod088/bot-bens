#!/usr/bin/env python3
"""
PayPal Payment Backend Server

Handles PayPal checkout creation and webhook validation.
Communicates with the Telegram bot to upgrade users to premium.
"""

import os
import hmac
import hashlib
import logging
import requests
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
import base64

from database import set_premium, get_user

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')  # Your backend URL

# PayPal API URLs
if PAYPAL_MODE == 'live':
    PAYPAL_API_URL = "https://api-m.paypal.com"
else:
    PAYPAL_API_URL = "https://api-m.sandbox.paypal.com"

PAYPAL_WEBHOOK_ID = os.getenv('PAYPAL_WEBHOOK_ID')  # Get from PayPal dashboard

# Validate required variables
if not all([PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, TELEGRAM_BOT_TOKEN, BACKEND_URL]):
    raise ValueError("Missing required environment variables")

app = FastAPI(title="PayPal Payment Backend")

# Constants
PREMIUM_PRICE_USD = 5
VIP_PRICE_USD = 10


def get_paypal_access_token() -> str:
    """Get PayPal OAuth access token"""
    url = f"{PAYPAL_API_URL}/v1/oauth2/token"
    
    auth = base64.b64encode(
        f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()
    ).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    
    return response.json()["access_token"]


def create_paypal_order(user_id: int, amount: float, plan: str = "premium") -> dict:
    """Create PayPal order"""
    access_token = get_paypal_access_token()
    
    url = f"{PAYPAL_API_URL}/v2/checkout/orders"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    plan_name = "VIP" if plan == "vip" else "Premium"
    
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": str(user_id),
                "amount": {
                    "currency_code": "USD",
                    "value": str(amount)
                },
                "description": f"Telegram Bot {plan_name} - Suscripción 1 mes"
            }
        ],
        "application_context": {
            "brand_name": "Telegram Media Bot",
            "return_url": f"{BACKEND_URL}/paypal/success?user_id={user_id}&plan={plan}",
            "cancel_url": f"{BACKEND_URL}/paypal/cancel?user_id={user_id}"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()


def verify_paypal_webhook(request_body: bytes, headers: dict) -> bool:
    """Verify PayPal webhook signature"""
    if not PAYPAL_WEBHOOK_ID:
        logger.warning("PAYPAL_WEBHOOK_ID not set, skipping verification")
        return True  # For testing only - remove in production
    
    # Get required headers
    transmission_id = headers.get("paypal-transmission-id")
    transmission_time = headers.get("paypal-transmission-time")
    cert_url = headers.get("paypal-cert-url")
    auth_algo = headers.get("paypal-auth-algo")
    transmission_sig = headers.get("paypal-transmission-sig")
    
    if not all([transmission_id, transmission_time, cert_url, auth_algo, transmission_sig]):
        logger.error("Missing required webhook headers")
        return False
    
    # Verify using PayPal API
    access_token = get_paypal_access_token()
    
    url = f"{PAYPAL_API_URL}/v1/notifications/verify-webhook-signature"
    
    headers_verify = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "transmission_id": transmission_id,
        "transmission_time": transmission_time,
        "cert_url": cert_url,
        "auth_algo": auth_algo,
        "transmission_sig": transmission_sig,
        "webhook_id": PAYPAL_WEBHOOK_ID,
        "webhook_event": request_body.decode()
    }
    
    response = requests.post(url, headers=headers_verify, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("verification_status") == "SUCCESS"
    
    return False


def notify_telegram_user(user_id: int, message: str):
    """Send message to Telegram user via bot"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": user_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info(f"Notification sent to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to notify user {user_id}: {e}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PayPal Payment Backend",
        "mode": PAYPAL_MODE
    }


@app.get("/pay")
async def create_payment(user_id: int = Query(...), plan: str = Query("premium")):
    """
    Create PayPal payment link for user
    
    Args:
        user_id: Telegram user ID
        plan: 'premium' or 'vip'
        
    Returns:
        Redirect to PayPal checkout
    """
    try:
        logger.info(f"Creating payment for user {user_id}, plan: {plan}")
        
        # Determine price based on plan
        if plan == "vip":
            amount = VIP_PRICE_USD
        else:
            amount = PREMIUM_PRICE_USD
        
        # Create PayPal order
        order = create_paypal_order(user_id, amount, plan)
        
        # Get approval URL
        approval_url = None
        for link in order.get("links", []):
            if link["rel"] == "approve":
                approval_url = link["href"]
                break
        
        if not approval_url:
            raise HTTPException(status_code=500, detail="Failed to create payment link")
        
        logger.info(f"Payment link created for user {user_id}: {order['id']}")
        
        # Redirect user to PayPal
        return RedirectResponse(url=approval_url)
    
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/paypal/success")
async def paypal_success(user_id: int = Query(...), token: str = Query(...), plan: str = Query("premium")):
    """Handle successful PayPal payment redirect"""
    logger.info(f"Payment success callback for user {user_id}, token: {token}, plan: {plan}")
    
    # Capture the payment
    try:
        access_token = get_paypal_access_token()
        
        url = f"{PAYPAL_API_URL}/v2/checkout/orders/{token}/capture"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if payment is completed
        if result.get("status") == "COMPLETED":
            # Determine premium level based on plan
            level = 2 if plan == "vip" else 1
            plan_name = "VIP" if plan == "vip" else "Premium"
            plan_emoji = "👑" if plan == "vip" else "💎"
            
            # Upgrade user to premium/vip
            set_premium(user_id, months=1, level=level)
            
            # Notify user
            from datetime import datetime, timedelta
            expiry = datetime.now() + timedelta(days=30)
            notify_telegram_user(
                user_id,
                f"✅ *Pago recibido exitosamente*\n\n"
                f"{plan_emoji} Suscripción {plan_name} activada por 30 días\n"
                f"Válida hasta: {expiry.strftime('%d/%m/%Y')}\n\n"
                "Envía /start para continuar usando el bot."
            )
            
            logger.info(f"User {user_id} upgraded to {plan_name}")
            
            return {
                "status": "success",
                "message": "Payment completed! Check your Telegram bot.",
                "user_id": user_id
            }
        else:
            logger.warning(f"Payment not completed for user {user_id}: {result.get('status')}")
            return {
                "status": "pending",
                "message": "Payment is being processed.",
                "user_id": user_id
            }
    
    except Exception as e:
        logger.error(f"Error capturing payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/paypal/cancel")
async def paypal_cancel(user_id: int = Query(...)):
    """Handle cancelled PayPal payment"""
    logger.info(f"Payment cancelled by user {user_id}")
    
    notify_telegram_user(
        user_id,
        "❌ Pago cancelado\n\n"
        "Si cambias de opinión, usa /premium para obtener acceso ilimitado."
    )
    
    return {
        "status": "cancelled",
        "message": "Payment was cancelled.",
        "user_id": user_id
    }


@app.post("/paypal/webhook")
async def paypal_webhook(request: Request):
    """
    Handle PayPal webhook events
    
    This endpoint receives notifications from PayPal when payments are completed.
    """
    try:
        # Get raw body and headers
        body = await request.body()
        headers = dict(request.headers)
        
        # Verify webhook signature
        if not verify_paypal_webhook(body, headers):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Parse event
        event = await request.json()
        event_type = event.get("event_type")
        
        logger.info(f"Received webhook event: {event_type}")
        
        # Handle CHECKOUT.ORDER.APPROVED
        if event_type == "CHECKOUT.ORDER.APPROVED":
            order_id = event["resource"]["id"]
            
            # Get user_id from purchase_units
            purchase_units = event["resource"].get("purchase_units", [])
            if purchase_units:
                user_id = int(purchase_units[0].get("reference_id", 0))
                
                if user_id:
                    logger.info(f"Order approved for user {user_id}, capturing payment...")
                    
                    # Payment will be captured in the success endpoint
                    # This is just a notification that order was approved
        
        # Handle PAYMENT.CAPTURE.COMPLETED
        elif event_type == "PAYMENT.CAPTURE.COMPLETED":
            # Get user_id from custom_id or reference_id
            resource = event.get("resource", {})
            purchase_units = resource.get("purchase_units", [])
            
            if purchase_units:
                user_id = int(purchase_units[0].get("reference_id", 0))
                
                if user_id:
                    # Verify payment status
                    status = resource.get("status")
                    
                    if status == "COMPLETED":
                        # Upgrade user to premium
                        set_premium(user_id)
                        
                        # Notify user
                        from datetime import datetime, timedelta
                        expiry = datetime.now() + timedelta(days=30)
                        notify_telegram_user(
                            user_id,
                            "✅ *Pago confirmado*\n\n"
                            f"🎉 Suscripción Premium activada por 30 días\n"
                            f"Válida hasta: {expiry.strftime('%d/%m/%Y')}\n\n"
                            "Ahora tienes acceso ilimitado. ¡Disfruta!"
                        )
                        
                        logger.info(f"User {user_id} upgraded to premium via webhook")
        
        return {"status": "received"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
