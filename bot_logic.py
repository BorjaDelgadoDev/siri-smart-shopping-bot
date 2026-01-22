from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
import database
import os
from dotenv import load_dotenv

load_dotenv()

def render_list():
    """Generatete the text and the keyboard for the shopping list."""
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
            # Botón para eliminar (comprado)
            keyboard.append([InlineKeyboardButton(f"✅ {name}", callback_data=f"buy_{item_id}")])
        text += "\n"

    reply_markup = InlineKeyboardMarkup(keyboard)
    return text, reply_markup

async def update_master_message(bot: Bot):
    """Update the existing master message or send a new one."""
    text, reply_markup = render_list()
    
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        print("Error: CHAT_ID not set in .env")
        return

    # 1. Intentar obtener ID de la base de datos
    master_message_id = database.get_state("master_message_id")

    # 2. Si no hay ID (Render reinició), intentar buscar el mensaje fijado del bot
    if not master_message_id:
        try:
            chat = await bot.get_chat(chat_id)
            if chat.pinned_message and chat.pinned_message.from_user.id == bot.id:
                master_message_id = chat.pinned_message.message_id
                database.set_state("master_message_id", master_message_id)
                print(f"Recovered master_message_id from pinned message: {master_message_id}")
        except Exception as e:
            print(f"Could not recover pinned message: {e}")

    if master_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=int(master_message_id),
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return # Éxito
        except Exception as e:
            if "Message is not modified" in str(e):
                return
            print(f"Failed to edit message {master_message_id}: {e}")

    # 3. Si no hay ID o el edit falló, enviar uno nuevo y fijarlo
    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        database.set_state("master_message_id", msg.message_id)
        
        # Intentar fijar el nuevo mensaje para futura recuperación
        try:
            await bot.pin_chat_message(chat_id=chat_id, message_id=msg.message_id)
            print(f"Message {msg.message_id} pinned successfully.")
            
            # Intentar borrar el anterior si existía uno diferente
            if master_message_id and int(master_message_id) != msg.message_id:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=int(master_message_id))
                except:
                    pass
        except Exception as pin_error:
            print(f"FAILED TO PIN: {pin_error}. Make sure the bot is ADMIN with 'Pin Messages' permission.")
            
    except Exception as e:
        print(f"Critical error sending message: {e}")
