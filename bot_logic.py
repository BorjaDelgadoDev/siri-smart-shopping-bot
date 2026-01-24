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
    """Update the existing master message or send a new one with robust sync."""
    text, reply_markup = render_list()
    
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        print("Error: CHAT_ID not set in .env")
        return

    # 1. Intentar obtener ID de la base de datos
    master_message_id = database.get_state("master_message_id")

    # 2. Sincronización proactiva: Si no hay ID o cada N veces, verificamos el anclado de Telegram
    # Para máxima estabilidad, si no tenemos ID local, preguntamos a Telegram SIEMPRE.
    if not master_message_id:
        try:
            chat = await bot.get_chat(chat_id)
            if chat.pinned_message and chat.pinned_message.from_user.id == bot.id:
                master_message_id = str(chat.pinned_message.message_id)
                database.set_state("master_message_id", master_message_id)
                print(f"Sync: Recovered master_id {master_message_id} from pinned message.")
        except Exception as e:
            print(f"Sync Error: Could not fetch pinned message: {e}")

    # 3. Si tenemos un ID (recuperado o local), intentamos editar
    if master_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=int(master_message_id),
                text=text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            return # Éxito total: mensaje actualizado.
        except Exception as e:
            err_str = str(e).lower()
            if "message is not modified" in err_str:
                return # Nada que cambiar, salimos felices.
            
            # Si el mensaje ha desaparecido o no es editable, procedemos a crear uno nuevo
            if "message to edit not found" in err_str or "message can't be edited" in err_str:
                print(f"Master msg {master_message_id} lost/un-editable. Creating new.")
            else:
                print(f"Critical Edit Error for {master_message_id}: {e}")
                # En caso de error de red o similar, NO duplicamos, reintentamos después
                return 

    # 4. Solo llegamos aquí si NO hay mensaje o el anterior es inservible
    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        new_id = msg.message_id
        database.set_state("master_message_id", new_id)
        
        # Limpieza y Anclado
        try:
            # Borramos el rastro del "fantasma" anterior si existía para evitar duplicados visuales
            if master_message_id and int(master_message_id) != new_id:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=int(master_message_id))
                except Exception: pass
            
            # Fijamos el nuevo para la próxima vez
            await bot.pin_chat_message(chat_id=chat_id, message_id=new_id, disable_notification=True)
        except Exception: 
            pass
            
    except Exception as e:
        print(f"Fatal error sending message: {e}")
