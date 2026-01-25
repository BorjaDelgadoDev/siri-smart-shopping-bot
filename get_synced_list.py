import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
import database
import bot_logic

load_dotenv()

async def get_and_print_list():
    database.init_db()
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Error: No token")
        return
        
    bot = Bot(token=TOKEN)
    await bot.initialize()
    
    # Sincronizamos primero con Telegram
    await bot_logic.sync_and_recover(bot)
    
    # Obtenemos items
    items = database.get_all_items()
    
    if not items:
        print("VACÍA")
    else:
        for item in items:
            print(f"{item[0]}|{item[1]}|{item[2]}|{item[3]}")
            
    await bot.shutdown()

if __name__ == "__main__":
    asyncio.run(get_and_print_list())
