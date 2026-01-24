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

    # 2. Sincronización proactiva y "Self-Healing"
    try:
        chat = await bot.get_chat(chat_id)
        pinned = chat.pinned_message
        
        # Si hay un mensaje fijado del bot, lo usamos como fuente de verdad
        if pinned and pinned.from_user.id == bot.id:
            master_message_id = str(pinned.message_id)
            database.set_state("master_message_id", master_message_id)
            
            # ¡MAGIA DE RECUPERACIÓN!: Si mi base de datos está vacía pero el mensaje tiene botones, recuperamos
            current_items = database.get_all_items()
            if not current_items and pinned.reply_markup:
                print("Self-Healing: Database empty but pinned message found. Recovering items...")
                # Recorremos los botones para sacar los nombres de los productos
                for row in pinned.reply_markup.inline_keyboard:
                    for button in row:
                        if button.callback_data.startswith("buy_"):
                            # El texto del botón suele ser "✅ Producto", le quitamos el emoji
                            btn_text = button.text.replace("✅ ", "").strip()
                            # Intentamos deducir la categoría del texto del mensaje
                            # (Buscamos la categoría que está justo encima del producto)
                            # Por ahora, para ser seguros, los metemos en la categoría detectada en el texto si es posible
                            # o simplemente en la categoría que ponga la lista renderizada.
                            # Para simplificar la recuperación inicial, los marcamos como recuperados.
                            database.sync_item(btn_text, "1", "📦 Recuperados (Sincronizando...)")
                
                # Refrescamos la lista con lo recuperado antes de seguir
                text, reply_markup = render_list()
                print("Self-Healing: Recovery complete.")

    except Exception as e:
        print(f"Sync/Recovery Error: {e}")

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
