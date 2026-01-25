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

async def sync_and_recover(bot: Bot):
    """
    Synchronizes local state with Telegram's pinned message.
    If the database is empty (e.g., after a Render restart), it recovers items from the pin text.
    """
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
            return

        bot_me = await bot.get_me()
        if pinned.from_user.id != bot_me.id:
            return

        # 1. Adoptar el ID del mensaje maestro
        database.set_state("master_message_id", str(pinned.message_id))

        # 2. Si la base de datos está vacía, recuperar items del texto del mensaje
        local_items = database.get_all_items()
        if not local_items and pinned.text:
            print(f"Sync: DB empty. Attempting recovery from pin {pinned.message_id}...")
            
            lines = pinned.text.split("\n")
            current_category = "13. 📦 Otros"
            recovered_count = 0

            for line in lines:
                line = line.strip()
                if not line or "Lista de la Compra" in line:
                    continue
                
                # Detectar categorías (no empiezan por • y no son el título)
                if not line.startswith("•") and not line.startswith("📝"):
                    current_category = line
                    continue

                if line.startswith("•"):
                    name_part = line.replace("•", "").strip()
                    base_name = name_part.split("(")[0].strip()
                    
                    # Extraer cantidad si existe: "Item (2 kilos)"
                    quantity = "1"
                    if "(" in name_part and ")" in name_part:
                        quantity = name_part.split("(")[1].split(")")[0]
                    
                    # Recuperar el ID del botón si existe para que los botones sigan funcionando
                    recovered_id = item_button_map.get(base_name)
                    
                    database.add_item(base_name, quantity, current_category, item_id=recovered_id)
                    recovered_count += 1
            
            if recovered_count > 0:
                print(f"Sync: Recovered {recovered_count} items from pin text.")
                database.set_state("had_items_recently", "True")

    except Exception as e:
        print(f"Critical Sync Error: {e}")

async def update_master_message(bot: Bot):
    """Update the existing master message or send a new one. SIMPLE EDIT-FIRST LOGIC."""
    # SINCRONIZACIÓN TOTAL EN CADA UPDATE
    await sync_and_recover(bot)
    
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
            
            # RE-PIN ASEGURADO: Siempre intentamos fijarlo por si se perdió el pin
            try:
                await bot.pin_chat_message(chat_id=chat_id, message_id=int(master_message_id), disable_notification=True)
            except Exception:
                 pass
                 
            return
        except Exception as e:
            err_str = str(e).lower()
            if "message is not modified" in err_str:
                print(f"Update: Message {master_message_id} not modified.")
                return
            
            if "message to edit not found" in err_str or "message can't be edited" in err_str:
                print(f"Update: Message {master_message_id} not found. Will create new.")
            else:
                print(f"Update: Unexpected edit error: {e}")

    # PASO 2: Crear mensaje nuevo
    try:
        # Limpiar
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
        
        try:
            await bot.pin_chat_message(chat_id=chat_id, message_id=new_id, disable_notification=True)
            print(f"Update: Pinned message {new_id}.")
        except Exception as pin_err: 
            print(f"Update: Warning pinning: {pin_err}")
            
    except Exception as e:
        print(f"Update: Fatal error: {e}")
