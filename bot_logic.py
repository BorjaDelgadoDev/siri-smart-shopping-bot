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

        # 4. Obtener estado actual
        current_master_id = database.get_state("master_message_id")
        local_items = database.get_all_items()

        # 5. FUENTE DE VERDAD: Adoptar el pin de Telegram si es nuestro
        # Esto previene duplicados si el bot se reinicia pero el pin sigue ahí.
        if str(current_master_id) != str(pinned.message_id):
            print(f"Sync: Adopting Telegram Pin {pinned.message_id} as master.")
            database.set_state("master_message_id", str(pinned.message_id))
            current_master_id = str(pinned.message_id)

        # 6. ¡SANACIÓN!: Recuperamos solo si la DB está vacía pero SABÍAMOS que debería haber items
        # (Esto indica una pérdida accidental de datos en la DB local)
        should_heal = not local_items and database.get_state("had_items_recently") == "True"
        
        if should_heal and pinned.reply_markup and pinned.text:
            print(f"Self-Healing: DB empty & No Master ID. Recovering from pin {pinned.message_id}...")
            # ... (resto de la lógica igual)
            
            # Mapear botones a nombres e IDs
            item_button_map = {}
            for row in pinned.reply_markup.inline_keyboard:
                for button in row:
                    if button.callback_data.startswith("buy_"):
                        button_name = button.text.replace("✅ ", "").strip()
                        button_id = button.callback_data.replace("buy_", "")
                        item_button_map[button_name] = button_id

            lines = pinned.text.split("\n")
            current_category = "📦 Otros"
            recovered_count = 0

            for line in lines:
                line = line.strip()
                if not line or line.startswith("📝") or "Lista de la Compra" in line:
                    continue
                
                if line.startswith("•"):
                    name_part = line.replace("•", "").strip()
                    base_name = name_part.split("(")[0].strip()
                    if base_name in item_button_map:
                        quantity = "1"
                        if "(" in name_part and ")" in name_part:
                            quantity = name_part.split("(")[1].split(")")[0]
                        database.sync_item(base_name, quantity, current_category)
                        recovered_count += 1
                else:
                    current_category = line

            if recovered_count > 0:
                print(f"Self-Healing Cache: Force new message to sync button IDs.")
                database.set_state("master_message_id", None)

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
    # Convertir "None" string a None real
    if master_message_id == "None" or master_message_id is None:
        master_message_id = None

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
                # En caso de error crítico, asumimos que el mensaje ya no sirve

    # 4. Fallback: Crear mensaje nuevo
    try:
        # Antes de enviar uno nuevo, intentamos BORRAR el viejo y DESANCLAR TODO
        # para que no queden múltiples burbujas de "mensaje fijado".
        try:
            print("Pin-Cleanup: Cleaning up old pins before sending new master.")
            await bot.unpin_all_chat_messages(chat_id=chat_id)
            if master_message_id:
                await bot.delete_message(chat_id=chat_id, message_id=int(master_message_id))
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
        
        # Anclado silencioso
        try:
            await bot.pin_chat_message(chat_id=chat_id, message_id=new_id, disable_notification=True)
            print(f"Pin-Cleanup: New master pinned: {new_id}")
        except Exception as pin_err: 
            print(f"Warning pinning message: {pin_err}")
            
    except Exception as e:
        print(f"Fatal error sending master message: {e}")

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
