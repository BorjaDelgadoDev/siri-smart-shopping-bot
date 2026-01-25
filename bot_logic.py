from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
import database
import os
from dotenv import load_dotenv

load_dotenv()

def render_list():
    """Generate the text and the keyboard for the shopping list."""
    items = database.get_all_items()
    
    if not items:
        return "🛒 **Tu lista está vacía.**\nDicta algo a Siri para empezar.", None

    # Agrupar por categorías
    categories = {}
    for item_id, name, quantity, category in items:
        if category not in categories:
            categories[category] = []
        categories[category].append((item_id, name, quantity))

    text = "📝 **Lista de la Compra**\n\n"
    keyboard = []

    for category, category_items in categories.items():
        text += f"{category}\n"
        for item_id, name, quantity in category_items:
            quantity_str = f" ({quantity})" if quantity != "1" else ""
            text += f"• {name}{quantity_str}\n"
            keyboard.append([InlineKeyboardButton(f"✅ {name}", callback_data=f"buy_{item_id}")])
        text += "\n"

    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup

async def adopt_telegram_pin(bot: Bot):
    """On startup ONLY: Adopt Telegram's pinned message as master if it's ours."""
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        return
        
    try:
        try:
            await bot.initialize()
        except Exception:
            pass

        chat = await bot.get_chat(chat_id)
        pinned = chat.pinned_message
        if not pinned:
            print("Startup Sync: No pinned message found.")
            return

        bot_me = await bot.get_me()
        if pinned.from_user.id != bot_me.id:
            print("Startup Sync: Pinned message is not from this bot.")
            return

        # Adoptar el pin de Telegram como master
        current_master_id = database.get_state("master_message_id")
        if str(current_master_id) != str(pinned.message_id):
            print(f"Startup Sync: Adopting Telegram Pin {pinned.message_id} (was {current_master_id}).")
            database.set_state("master_message_id", str(pinned.message_id))
        else:
            print(f"Startup Sync: Master ID {current_master_id} is already in sync.")

    except Exception as e:
        print(f"Startup Sync Error: {e}")


async def update_master_message(bot: Bot):
    """Update the existing master message or send a new one. SIMPLE LOGIC."""
    text, reply_markup = render_list()
    
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        print("Error: CHAT_ID not set in .env")
        return

    master_message_id = database.get_state("master_message_id")
    if master_message_id == "None" or master_message_id is None:
        master_message_id = None

    # PASO 1: Intentar editar el mensaje existente
    if master_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=int(master_message_id),
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            print(f"Update: Edited message {master_message_id} successfully.")
            return  # ¡ÉXITO! Salimos.
        except Exception as e:
            err_str = str(e).lower()
            if "message is not modified" in err_str:
                print(f"Update: Message {master_message_id} not modified (no change).")
                return  # Nada que cambiar.
            
            # Si el mensaje ya no existe o no se puede editar, procedemos a crear uno nuevo
            if "message to edit not found" in err_str or "message can't be edited" in err_str:
                print(f"Update: Message {master_message_id} not found. Will create new.")
            else:
                print(f"Update: Unexpected edit error: {e}. Will try to create new.")

    # PASO 2: Crear mensaje nuevo (SOLO si edit falló o no había ID)
    try:
        # Limpiar estado viejo
        if master_message_id:
            try:
                await bot.delete_message(chat_id=chat_id, message_id=int(master_message_id))
            except Exception:
                pass
        
        try:
            await bot.unpin_all_chat_messages(chat_id=chat_id)
        except Exception:
            pass

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        new_id = msg.message_id
        database.set_state("master_message_id", new_id)
        print(f"Update: Sent new message {new_id}.")
        
        try:
            await bot.pin_chat_message(chat_id=chat_id, message_id=new_id, disable_notification=True)
            print(f"Update: Pinned message {new_id}.")
        except Exception as pin_err: 
            print(f"Update: Warning pinning: {pin_err}")
            
    except Exception as e:
        print(f"Update: Fatal error: {e}")
