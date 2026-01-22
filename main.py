from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import ai_handler
import database
import bot_logic
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json

load_dotenv()

# Initialize Bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN) if TOKEN else None

app = FastAPI(title="Smart Shopping List Bot API")

class SiriRequest(BaseModel):
    text: str

@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Shopping List Bot is running"}

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
    
    # Procesar CallbackQueries (Botón Comprar)
    if update.callback_query:
        query = update.callback_query
        data_recv = query.data
        
        if data_recv.startswith("buy_"):
            item_id = data_recv.split("_")[1]
            database.delete_item(item_id)
            await query.answer("¡Comprado!")
            await bot_logic.update_master_message(bot)
            
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
