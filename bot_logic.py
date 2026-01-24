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

async def ensure_db_synced(bot: Bot):
    """Ensure the local DB is in sync with Telegram's pinned message. MUST be called first."""
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        return
        
    try:
        # 1. Asegurar inicialización
        try:
            await bot.initialize()
        except Exception:
            pass

        # 2. Consultar Telegram
        chat = await bot.get_chat(chat_id)
        pinned = chat.pinned_message
        if not pinned:
            return

        # 3. Verificar si el bot es el autor
        bot_me = await bot.get_me()
        if pinned.from_user.id != bot_me.id:
            return

        # 4. Actualizar ID del mensaje maestro localmente
        database.set_state("master_message_id", str(pinned.message_id))

        # 5. ¡SANACIÓN!: Recuperamos siempre que el pin tenga botones (nuestro backup)
        if pinned.reply_markup and pinned.text:
            print(f"Self-Healing: Checking recovery from pin {pinned.message_id}...")
            
            # Mapear botones a nombres
            item_button_names = []
            for row in pinned.reply_markup.inline_keyboard:
                for button in row:
                    if button.callback_data.startswith("buy_"):
                        item_button_names.append(button.text.replace("✅ ", "").strip())

            # Analizar el texto para encontrar categorías
            lines = pinned.text.split("\n")
            current_category = "📦 Otros"
            recovered_count = 0

            # Lista de nuestras categorías conocidas (para comparar emojis/nombres)
            # No necesitamos la lista exacta, cualquier línea que no empiece por punto ni esté vacía 
            # después del título es una categoría.
            for line in lines:
                line = line.strip()
                if not line or line.startswith("📝") or "Lista de la Compra" in line:
                    continue
                
                if line.startswith("•"):
                    # Es un producto. Formato: • Nombre (Cantidad) o • Nombre
                    name_part = line.replace("•", "").strip()
                    # Si el nombre está en nuestros botones, lo recuperamos
                    # Quitamos la cantidad del nombre para buscar en botones
                    base_name = name_part.split("(")[0].strip()
                    if base_name in item_button_names:
                        quantity = "1"
                        if "(" in name_part and ")" in name_part:
                            quantity = name_part.split("(")[1].split(")")[0]
                        
                        database.sync_item(base_name, quantity, current_category)
                        recovered_count += 1
                else:
                    # Es una categoría (ej: 🍏 Frutas y Verduras)
                    current_category = line

            print(f"Self-Healing: Reconstructed {recovered_count} items with their categories.")

    except Exception as e:
        print(f"Sync/Sanity Error: {e}")

async def update_master_message(bot: Bot):
    """Update the existing master message or send a new one with robust sync."""
    # Sincronización obligatoria antes de nada (por si Render reinició)
    await ensure_db_synced(bot)
    
    text, reply_markup = render_list()
    
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        print("Error: CHAT_ID not set in .env")
        return

    # Intentar obtener ID sincronizado
    master_message_id = database.get_state("master_message_id")

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
                except Exception:
                    pass
            
            # Fijamos el nuevo para la próxima vez
            await bot.pin_chat_message(chat_id=chat_id, message_id=new_id, disable_notification=True)
        except Exception: 
            pass
            
    except Exception as e:
        print(f"Fatal error sending message: {e}")

async def audit_and_fix(bot: Bot):
    """Real-time audit of the chat state. Returns a diagnostic report."""
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        return {"error": "CHAT_ID not configured"}

    report = {
        "timestamp": os.popen("date").read().strip(),
        "local_state": {
            "master_message_id": database.get_state("master_message_id"),
            "items_in_db": len(database.get_all_items())
        },
        "remote_state": {},
        "issues": [],
        "actions_taken": []
    }

    try:
        # Sincronización obligatoria antes de auditar
        await ensure_db_synced(bot)

        chat = await bot.get_chat(chat_id)
        pinned = chat.pinned_message
        
        if pinned:
            report["remote_state"]["pinned_message_id"] = pinned.message_id
            bot_me = await bot.get_me()
            report["remote_state"]["pinned_by_bot"] = (pinned.from_user.id == bot_me.id)
            report["remote_state"]["pinned_text_snippet"] = pinned.text[:30] + "..." if pinned.text else None
        else:
            report["remote_state"]["pinned_message_id"] = None
            report["issues"].append("No message is pinned in this chat.")

        # Diagnosis
        db_id = report["local_state"]["master_message_id"]
        pin_id = report["remote_state"].get("pinned_message_id")

        if pin_id and str(db_id) != str(pin_id):
            report["issues"].append(f"State mismatch: DB thinks {db_id}, Telegram has {pin_id} pinned.")
            # Auto-fix: Adopt the pinned one
            database.set_state("master_message_id", pin_id)
            report["actions_taken"].append(f"Updated local master_message_id to {pin_id}")

    except Exception as e:
        report["error"] = str(e)

    return report
