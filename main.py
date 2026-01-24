from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import ai_handler
import database
import bot_logic
from telegram import Bot, Update

load_dotenv()

# Initialize Bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN) if TOKEN else None

app = FastAPI(title="Smart Shopping List Bot API")

class SiriRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    database.init_db()
    
    # Automatización del Webhook si existe BASE_URL
    base_url = os.getenv("BASE_URL")
    if base_url and bot:
        webhook_url = f"{base_url.rstrip('/')}/webhook/telegram"
        try:
            await bot.set_webhook(url=webhook_url)
            print(f"Webhook set automatically to: {webhook_url}")
        except Exception as e:
            print(f"Error setting webhook: {e}")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Shopping List Bot is running", "version": "1.1"}

@app.post("/siri")
async def siri_endpoint(request: SiriRequest, x_auth_token: str = Header(None)):
    expected_token = os.getenv("SIRI_AUTH_TOKEN")
    
    # Validación de seguridad
    if not expected_token or x_auth_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Procesamiento asíncrono (conceptualmente, para que Siri no espere demasiado)
    # Por ahora procesamos y guardamos antes de responder, si Gemini es rápido
    raw_text = request.text
    print(f"Received from Siri: {raw_text}")
    
    products = ai_handler.process_text(raw_text)
    
    for item in products:
        name = item.get("product")
        quantity = item.get("quantity", "1")
        category = item.get("category", "Otros 📦")
        
        if name:
            database.add_item(name, quantity, category)
            print(f"Added item: {name} ({quantity}) in {category}")

    # Actualizar mensaje maestro en Telegram
    if bot:
        try:
            await bot_logic.update_master_message(bot)
        except Exception as e:
            print(f"Error updating Telegram: {e}")

    return {"status": "success", "added": len(products)}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Endpoint for Telegram Webhooks."""
    data = await request.json()
    update = Update.de_json(data, bot)
    chat_id_env = os.getenv("CHAT_ID")
    
    # 1. Procesar CallbackQueries (Botón Comprar)
    if update.callback_query:
        query = update.callback_query
        data_recv = query.data
        
        if data_recv.startswith("buy_"):
            item_id = data_recv.split("_")[1]
            database.delete_item(item_id)
            await query.answer("¡Comprado!")
            await bot_logic.update_master_message(bot)
        return {"ok": True}

    # 2. Lógica de "Limpieza" (Janitor): Borrar mensajes de usuarios en el grupo de la compra
    if update.message and str(update.message.chat_id) == chat_id_env:
        try:
            # Borrar cualquier mensaje (texto, audio, etc) que no sea del bot
            if not update.message.from_user.is_bot:
                await bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                print(f"Janitor: Deleted message from user {update.message.from_user.id}")
        except Exception as e:
            print(f"Janitor Error: {e}")

    return {"ok": True}

@app.get("/audit")
async def chat_audit(x_auth_token: str = Header(None)):
    """Secret endpoint for real-time chat monitoring and fixing."""
    expected_token = os.getenv("SIRI_AUTH_TOKEN")
    if not expected_token or x_auth_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    report = await bot_logic.audit_and_fix(bot)
    return report

@app.get("/debug/status")
async def debug_status(x_auth_token: str = Header(None)):
    """Remote monitoring endpoint."""
    expected_token = os.getenv("SIRI_AUTH_TOKEN")
    if not expected_token or x_auth_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    items = database.get_all_items()
    master_id = database.get_state("master_message_id")
    
    return {
        "status": "active",
        "master_message_id": master_id,
        "items_count": len(items),
        "items": items
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    # En Render/Railway necesitamos 0.0.0.0 para ser accesibles desde el exterior
    uvicorn.run(app, host="0.0.0.0", port=port)
