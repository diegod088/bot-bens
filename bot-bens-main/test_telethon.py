import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('TELEGRAM_API_ID'))
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_STRING = os.getenv('TELEGRAM_SESSION_STRING')

print(f"API_ID: {API_ID}")
print(f"API_HASH: {API_HASH}")
print(f"Session String Length: {len(SESSION_STRING) if SESSION_STRING else 0}")

async def test_telethon():
    try:
        print("\n[1] Creando cliente Telethon con StringSession...")
        client = TelegramClient(
            StringSession(SESSION_STRING),
            API_ID,
            API_HASH,
            device_model="Test Script",
            system_version="Windows 10",
            app_version="1.0"
        )
        
        print("[2] Conectando al servidor de Telegram...")
        await client.connect()
        print("✅ Conectado al servidor")
        
        print("[3] Verificando autorización...")
        is_authorized = await client.is_user_authorized()
        print(f"¿Está autorizado?: {is_authorized}")
        
        if is_authorized:
            print("\n[4] Obteniendo información del usuario...")
            me = await client.get_me()
            print(f"✅ Usuario: {me.first_name} {me.last_name or ''}")
            print(f"   ID: {me.id}")
            print(f"   Username: @{me.username if me.username else 'Sin username'}")
            print(f"   Phone: {me.phone}")
            
            print("\n[5] Probando obtener un canal público...")
            try:
                # Intentar obtener información de un canal público conocido
                entity = await client.get_entity('telegram')
                print(f"✅ Canal obtenido: {entity.title}")
            except Exception as e:
                print(f"❌ Error al obtener canal: {e}")
        else:
            print("\n❌ LA SESIÓN NO ESTÁ AUTORIZADA")
            print("Necesitas generar una nueva sesión string")
        
        print("\n[6] Desconectando...")
        await client.disconnect()
        print("✅ Desconectado")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_telethon())
