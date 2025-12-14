"""
Script para generar una nueva sesión string de Telethon
"""
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID', '32170841'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '69d9f701c17b2fa6dc6648849b25affa')

print("=" * 60)
print("GENERADOR DE SESIÓN STRING PARA TELETHON")
print("=" * 60)
print("\nEste script te permitirá crear una nueva sesión string.")
print("Necesitarás:")
print("  1. El número de teléfono de tu cuenta de Telegram")
print("  2. El código de verificación que recibirás")
print("  3. Tu contraseña de verificación en 2 pasos (si la tienes)")
print("\n" + "=" * 60)

async def generate_session():
    try:
        print(f"\n[INFO] API_ID: {API_ID}")
        print(f"[INFO] API_HASH: {API_HASH}\n")
        
        # Crear cliente con sesión vacía
        client = TelegramClient(
            StringSession(),  # Sesión vacía
            API_ID,
            API_HASH,
            device_model="Bot Session Generator",
            system_version="Windows 10",
            app_version="1.0"
        )
        
        print("[1] Conectando al servidor de Telegram...")
        await client.connect()
        print("✅ Conectado\n")
        
        # Solicitar autorización
        if not await client.is_user_authorized():
            print("[2] No estás autorizado. Iniciando proceso de login...")
            
            # Solicitar número de teléfono
            phone = input("Ingresa tu número de teléfono (con código de país, ej: +34612345678): ")
            await client.send_code_request(phone)
            
            # Solicitar código de verificación
            code = input("Ingresa el código que recibiste en Telegram: ")
            
            try:
                await client.sign_in(phone, code)
            except Exception as e:
                if "Two-steps verification" in str(e) or "SessionPasswordNeededError" in str(type(e).__name__):
                    # Requiere contraseña de verificación en 2 pasos
                    password = input("Se requiere verificación en 2 pasos. Ingresa tu contraseña: ")
                    await client.sign_in(password=password)
                else:
                    raise
        
        print("\n✅ Autorización exitosa!")
        
        # Obtener información del usuario
        me = await client.get_me()
        print(f"\n[INFO] Usuario autenticado:")
        print(f"       Nombre: {me.first_name} {me.last_name or ''}")
        print(f"       ID: {me.id}")
        print(f"       Username: @{me.username if me.username else 'Sin username'}")
        print(f"       Teléfono: {me.phone}")
        
        # Obtener la sesión string
        session_string = client.session.save()
        
        print("\n" + "=" * 60)
        print("✅ SESIÓN STRING GENERADA:")
        print("=" * 60)
        print(session_string)
        print("=" * 60)
        print("\n[IMPORTANTE] Copia esta sesión string y actualiza tu archivo .env")
        print("             Reemplaza el valor de TELEGRAM_SESSION_STRING\n")
        
        # Guardar en archivo temporal
        with open("session_string_nueva.txt", "w") as f:
            f.write(f"TELEGRAM_SESSION_STRING={session_string}\n")
            f.write(f"\n# Usuario: {me.first_name} {me.last_name or ''}\n")
            f.write(f"# ID: {me.id}\n")
            f.write(f"# Username: @{me.username if me.username else 'Sin username'}\n")
            f.write(f"# Teléfono: {me.phone}\n")
        
        print("[INFO] También se guardó en: session_string_nueva.txt")
        
        await client.disconnect()
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(generate_session())
